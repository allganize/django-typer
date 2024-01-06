import json

from django_typer import TyperCommand, command, callback
from django.utils.translation import gettext_lazy as _


class Command(TyperCommand):

    help = "Test minimal TyperCommand subclass - class member"

    @callback(help='Test minimal TyperCommand subclass - callback method')
    def init(self, verbosity: int = 1):
        """
        Test minimal TyperCommand subclass - callback docstring
        """
        assert self.__class__ is Command
        self.verbosity = verbosity

    @command(help="Test minimal TyperCommand subclass - command method")
    def handle(self, arg1: str, arg2: str, arg3: float = 0.5, arg4: int = 1):
        """
        Test minimal TyperCommand subclass - docstring
        """
        assert self.__class__ == Command
        opts = {"arg1": arg1, "arg2": arg2, "arg3": arg3, "arg4": arg4}
        return json.dumps(opts)
