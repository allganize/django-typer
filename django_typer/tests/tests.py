import inspect
import json
import os
import subprocess
import sys
from io import StringIO
from pathlib import Path

import django
import typer
from django.core.management import call_command
from django.test import TestCase

from django_typer import get_command

manage_py = Path(__file__).parent.parent.parent / "manage.py"


def get_named_arguments(function):
    sig = inspect.signature(function)
    return [
        name
        for name, param in sig.parameters.items()
        if param.default != inspect.Parameter.empty
    ]


def run_command(command, *args):
    cwd = os.getcwd()
    try:
        os.chdir(manage_py.parent)
        result = subprocess.run(
            [sys.executable, f"./{manage_py.name}", command, *args],
            capture_output=True,
            text=True,
        )

        # Check the return code to ensure the script ran successfully
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        # Parse the output
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return result.stdout
    finally:
        os.chdir(cwd)


class BasicTests(TestCase):
    def test_command_line(self):
        self.assertEqual(
            run_command("basic", "a1", "a2"),
            {"arg1": "a1", "arg2": "a2", "arg3": 0.5, "arg4": 1},
        )

        self.assertEqual(
            run_command("basic", "a1", "a2", "--arg3", "0.75", "--arg4", "2"),
            {"arg1": "a1", "arg2": "a2", "arg3": 0.75, "arg4": 2},
        )

    def test_call_command(self):
        out = StringIO()
        returned_options = json.loads(call_command("basic", ["a1", "a2"], stdout=out))
        self.assertEqual(
            returned_options, {"arg1": "a1", "arg2": "a2", "arg3": 0.5, "arg4": 1}
        )

    def test_call_command_stdout(self):
        out = StringIO()
        call_command("basic", ["a1", "a2"], stdout=out)
        printed_options = json.loads(out.getvalue())
        self.assertEqual(
            printed_options, {"arg1": "a1", "arg2": "a2", "arg3": 0.5, "arg4": 1}
        )

    def test_get_version(self):
        self.assertEqual(
            str(run_command("basic", "--version")).strip(), django.get_version()
        )

    def test_call_direct(self):
        basic = get_command("basic")
        self.assertEqual(
            json.loads(basic.handle("a1", "a2")),
            {"arg1": "a1", "arg2": "a2", "arg3": 0.5, "arg4": 1},
        )

        from django_typer.tests.test_app.management.commands.basic import (
            Command as Basic,
        )

        self.assertEqual(
            json.loads(Basic()("a1", "a2", arg3=0.75, arg4=2)),
            {"arg1": "a1", "arg2": "a2", "arg3": 0.75, "arg4": 2},
        )


class InterfaceTests(TestCase):
    """
    Make sure the django_typer decorator inerfaces match the
    typer decorator interfaces. We don't simply pass variadic arguments
    to the typer decorator because we want the IDE to offer auto complete
    suggestions.
    """

    def test_command_interface_matches(self):
        from django_typer import command

        command_params = set(get_named_arguments(command))
        typer_params = set(get_named_arguments(typer.Typer.command))

        self.assertFalse(command_params.symmetric_difference(typer_params))

    def test_callback_interface_matches(self):
        from django_typer import callback

        callback_params = set(get_named_arguments(callback))
        typer_params = set(get_named_arguments(typer.Typer.callback))

        self.assertFalse(callback_params.symmetric_difference(typer_params))


class MultiTests(TestCase):
    def test_command_line(self):
        self.assertEqual(
            run_command("multi", "cmd1", "/path/one", "/path/two"),
            {"files": ["/path/one", "/path/two"], "flag1": False},
        )

        self.assertEqual(
            run_command("multi", "cmd1", "/path/four", "/path/three", "--flag1"),
            {"files": ["/path/four", "/path/three"], "flag1": True},
        )

        self.assertEqual(
            run_command("multi", "sum", "1.2", "3.5", " -12.3"), sum([1.2, 3.5, -12.3])
        )

        self.assertEqual(run_command("multi", "cmd3"), {})

    def test_call_command(self):
        ret = json.loads(call_command("multi", ["cmd1", "/path/one", "/path/two"]))
        self.assertEqual(ret, {"files": ["/path/one", "/path/two"], "flag1": False})

        ret = json.loads(
            call_command("multi", ["cmd1", "/path/four", "/path/three", "--flag1"])
        )
        self.assertEqual(ret, {"files": ["/path/four", "/path/three"], "flag1": True})

        ret = json.loads(call_command("multi", ["sum", "1.2", "3.5", " -12.3"]))
        self.assertEqual(ret, sum([1.2, 3.5, -12.3]))

        ret = json.loads(call_command("multi", ["cmd3"]))
        self.assertEqual(ret, {})

    def test_call_command_stdout(self):
        out = StringIO()
        call_command("multi", ["cmd1", "/path/one", "/path/two"], stdout=out)
        self.assertEqual(
            json.loads(out.getvalue()),
            {"files": ["/path/one", "/path/two"], "flag1": False},
        )

        out = StringIO()
        call_command(
            "multi", ["cmd1", "/path/four", "/path/three", "--flag1"], stdout=out
        )
        self.assertEqual(
            json.loads(out.getvalue()),
            {"files": ["/path/four", "/path/three"], "flag1": True},
        )

        out = StringIO()
        call_command("multi", ["sum", "1.2", "3.5", " -12.3"], stdout=out)
        self.assertEqual(json.loads(out.getvalue()), sum([1.2, 3.5, -12.3]))

        out = StringIO()
        call_command("multi", ["cmd3"], stdout=out)
        self.assertEqual(json.loads(out.getvalue()), {})

    def test_get_version(self):
        self.assertEqual(
            str(run_command("multi", "--version")).strip(), django.get_version()
        )
        self.assertEqual(
            str(run_command("multi", "cmd1", "--version")).strip(), django.get_version()
        )
        self.assertEqual(
            str(run_command("multi", "sum", "--version")).strip(), django.get_version()
        )
        self.assertEqual(
            str(run_command("multi", "cmd3", "--version")).strip(), django.get_version()
        )

    def test_call_direct(self):
        multi = get_command("multi")

        self.assertEqual(
            json.loads(multi.cmd1(["/path/one", "/path/two"])),
            {"files": ["/path/one", "/path/two"], "flag1": False},
        )

        self.assertEqual(
            json.loads(multi.cmd1(["/path/four", "/path/three"], flag1=True)),
            {"files": ["/path/four", "/path/three"], "flag1": True},
        )

        self.assertEqual(float(multi.sum([1.2, 3.5, -12.3])), sum([1.2, 3.5, -12.3]))

        self.assertEqual(json.loads(multi.cmd3()), {})


class TestGetCommand(TestCase):
    def test_get_command(self):
        from django_typer.tests.test_app.management.commands.basic import (
            Command as Basic,
        )

        basic = get_command("basic")
        assert basic.__class__ == Basic

        from django_typer.tests.test_app.management.commands.multi import (
            Command as Multi,
        )

        multi = get_command("multi")
        assert multi.__class__ == Multi
        cmd1 = get_command("multi", "cmd1")
        assert cmd1.__func__ is multi.cmd1.__func__
        sum = get_command("multi", "sum")
        assert sum.__func__ is multi.sum.__func__
        cmd3 = get_command("multi", "cmd3")
        assert cmd3.__func__ is multi.cmd3.__func__

        from django_typer.tests.test_app.management.commands.callback1 import (
            Command as Callback1,
        )

        callback1 = get_command("callback1")
        assert callback1.__class__ == Callback1

        # callbacks are not commands
        with self.assertRaises(ValueError):
            get_command("callback1", "init")


class CallbackTests(TestCase):
    cmd_name = "callback1"

    def test_helps(self, top_level_only=False):
        buffer = StringIO()
        cmd = get_command(self.cmd_name, stdout=buffer)

        help_output_top = run_command(self.cmd_name, "--help")
        cmd.print_help("./manage.py", self.cmd_name)
        self.assertEqual(help_output_top.strip(), buffer.getvalue().strip())

        if not top_level_only:
            buffer.truncate(0)
            buffer.seek(0)
            callback_help = run_command(self.cmd_name, "5", self.cmd_name, "--help")
            cmd.print_help("./manage.py", self.cmd_name, self.cmd_name)
            self.assertEqual(callback_help.strip(), buffer.getvalue().strip())

    def test_command_line(self):
        self.assertEqual(
            run_command(self.cmd_name, "5", self.cmd_name, "a1", "a2"),
            {
                "p1": 5,
                "flag1": False,
                "flag2": True,
                "arg1": "a1",
                "arg2": "a2",
                "arg3": 0.5,
                "arg4": 1,
            },
        )

        self.assertEqual(
            run_command(
                self.cmd_name,
                "--flag1",
                "--no-flag2",
                "6",
                self.cmd_name,
                "a1",
                "a2",
                "--arg3",
                "0.75",
                "--arg4",
                "2",
            ),
            {
                "p1": 6,
                "flag1": True,
                "flag2": False,
                "arg1": "a1",
                "arg2": "a2",
                "arg3": 0.75,
                "arg4": 2,
            },
        )

    def test_call_command(self, should_raise=True):
        ret = json.loads(
            call_command(
                self.cmd_name,
                *["5", self.cmd_name, "a1", "a2"],
                **{"p1": 5, "arg1": "a1", "arg2": "a2"},
            )
        )
        self.assertEqual(
            ret,
            {
                "p1": 5,
                "flag1": False,
                "flag2": True,
                "arg1": "a1",
                "arg2": "a2",
                "arg3": 0.5,
                "arg4": 1,
            },
        )

        ret = json.loads(
            call_command(
                self.cmd_name,
                *[
                    "--flag1",
                    "--no-flag2",
                    "6",
                    self.cmd_name,
                    "a1",
                    "a2",
                    "--arg3",
                    "0.75",
                    "--arg4",
                    "2",
                ],
            )
        )
        self.assertEqual(
            ret,
            {
                "p1": 6,
                "flag1": True,
                "flag2": False,
                "arg1": "a1",
                "arg2": "a2",
                "arg3": 0.75,
                "arg4": 2,
            },
        )

        # show that order matters args vs options
        interspersed = [
            lambda: call_command(
                self.cmd_name,
                *[
                    "6",
                    "--flag1",
                    "--no-flag2",
                    self.cmd_name,
                    "n1",
                    "n2",
                    "--arg3",
                    "0.2",
                    "--arg4",
                    "9",
                ],
            ),
            lambda: call_command(
                self.cmd_name,
                *[
                    "--no-flag2",
                    "6",
                    "--flag1",
                    self.cmd_name,
                    "--arg4",
                    "9",
                    "n1",
                    "n2",
                    "--arg3",
                    "0.2",
                ],
            ),
        ]
        expected = {
            "p1": 6,
            "flag1": True,
            "flag2": False,
            "arg1": "n1",
            "arg2": "n2",
            "arg3": 0.2,
            "arg4": 9,
        }
        if should_raise:
            for call_cmd in interspersed:
                if should_raise:
                    with self.assertRaises(BaseException):
                        call_cmd()
                else:
                    self.assertEqual(json.loads(call_cmd()), expected)

    def test_call_command_stdout(self):
        out = StringIO()
        call_command(
            self.cmd_name,
            [
                "--flag1",
                "--no-flag2",
                "6",
                self.cmd_name,
                "a1",
                "a2",
                "--arg3",
                "0.75",
                "--arg4",
                "2",
            ],
            stdout=out,
        )

        self.assertEqual(
            json.loads(out.getvalue()),
            {
                "p1": 6,
                "flag1": True,
                "flag2": False,
                "arg1": "a1",
                "arg2": "a2",
                "arg3": 0.75,
                "arg4": 2,
            },
        )

    def test_get_version(self):
        self.assertEqual(
            str(run_command(self.cmd_name, "--version")).strip(), django.get_version()
        )
        self.assertEqual(
            str(run_command(self.cmd_name, "6", self.cmd_name, "--version")).strip(),
            django.get_version(),
        )

    def test_call_direct(self):
        cmd = get_command(self.cmd_name)

        self.assertEqual(
            json.loads(cmd(arg1="a1", arg2="a2", arg3=0.2)),
            {"arg1": "a1", "arg2": "a2", "arg3": 0.2, "arg4": 1},
        )


class Callback2Tests(CallbackTests):
    cmd_name = "callback2"

    def test_call_command(self):
        super().test_call_command(should_raise=False)

    def test_helps(self, top_level_only=False):
        # we only run the top level help comparison because when
        # interspersed args are allowed its impossible to get the
        # subcommand to print its help
        super().test_helps(top_level_only=True)
