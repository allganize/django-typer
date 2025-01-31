==========
Change Log
==========

v1.1.2
======

* Fixed `Overridden common Django arguments fail to pass through when passed through call_command <https://github.com/bckohan/django-typer/issues/54>`_

v1.1.1
======

* Implemented `Fix pyright type checking and add to CI <https://github.com/bckohan/django-typer/issues/51>`_
* Implemented `Convert CONTRIBUTING.rst to markdown <https://github.com/bckohan/django-typer/issues/50>`_

v1.1.0
======

* Implemented `Convert readme to markdown. <https://github.com/bckohan/django-typer/issues/48>`_
* Fixed `typer 0.12.0 breaks django_typer 1.0.9 <https://github.com/bckohan/django-typer/issues/47>`_


v1.0.9 (yanked)
===============

* Fixed `Support typer 0.12.0 <https://github.com/bckohan/django-typer/issues/46>`_

v1.0.8
======

* Fixed `Support typer 0.10 and 0.11 <https://github.com/bckohan/django-typer/issues/45>`_

v1.0.7
======

* Fixed `Helps throw an exception when invoked from an absolute path that is not relative to the getcwd() <https://github.com/bckohan/django-typer/issues/44>`_

v1.0.6
======

* Fixed `prompt options on groups still prompt when given as named parameters on call_command <https://github.com/bckohan/django-typer/issues/43>`_


v1.0.5
======

* Fixed `Options with prompt=True are prompted twice <https://github.com/bckohan/django-typer/issues/42>`_


v1.0.4
======

* Fixed `Help sometimes shows full script path in Usage: when it shouldnt. <https://github.com/bckohan/django-typer/issues/40>`_
* Fixed `METAVAR when ModelObjectParser supplied should default to model name <https://github.com/bckohan/django-typer/issues/39>`_

v1.0.3
======

* Fixed `Incomplete typing info for @command decorator <https://github.com/bckohan/django-typer/issues/33>`_

v1.0.2
======

* Fixed `name property on TyperCommand is too generic and should be private. <https://github.com/bckohan/django-typer/issues/37>`_
* Fixed `When usage errors are thrown the help output should be that of the subcommand invoked not the parent group. <https://github.com/bckohan/django-typer/issues/36>`_
* Fixed `typer installs its own system exception hook when commands are run and this may step on the installed rich hook <https://github.com/bckohan/django-typer/issues/35>`_
* Fixed `Add py.typed stub <https://github.com/bckohan/django-typer/issues/31>`_
* Fixed `Run type checking with django-stubs installed. <https://github.com/bckohan/django-typer/issues/30>`_
* Fixed `Add pyright to linting and resolve any pyright errors. <https://github.com/bckohan/django-typer/issues/29>`_
* Fixed `Missing subcommand produces stack trace without --traceback. <https://github.com/bckohan/django-typer/issues/27>`_
* Fixed `Allow handle() to be an initializer. <https://github.com/bckohan/django-typer/issues/24>`_

v1.0.1
======

* Fixed `shell_completion broken for click < 8.1 <https://github.com/bckohan/django-typer/issues/21>`_

v1.0.0
======

* Initial production/stable release.

v0.6.1b
=======

* Incremental beta release - this is also the second release candidate for version 1.
* Peg typer version to 0.9.x

v0.6.0b
=======

* Incremental beta release - this is also the first release candidate for version 1.


v0.5.0b
=======

* Incremental Beta Release

v0.4.0b
=======

* Incremental Beta Release

v0.3.0b
=======

* Incremental Beta Release

v0.2.0b
=======

* Incremental Beta Release


v0.1.0b
=======

* Initial Release (Beta)
