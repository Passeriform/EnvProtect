"""Report module.

Covers report generation and its export.
"""

from __future__ import annotations
from enum import Enum
from typing import Optional, Any,  overload
from envprotect.core import Result, CrawlResult, CrawlException, DetectionResult, DetectionException, ResultType
from envprotect.exception.report import UnknownOutputStreamError


class RunType(str, Enum):
    """RunType string enum class."""

    NOOP = "noop"
    DRY_RUN = "dry-run"
    APPLY = "apply"


class Report:
    """Represents report object and exposes utility methods.

    This class defines the basic report format and allows for custom printing
    of these report objectss with varible data objects.
    """

    def __init__(self,
                 runtype: RunType = RunType.NOOP,
                 create_safe: bool = True,
                 result: Optional[ResultType] = None):
        """Define basic report object.

        Args:
            runtype: Report execution type.
            create_safe: Flag to disallow conversion of report to Apply.
            result: Result to initialize Report.
        """
        self.runtype = runtype
        self._runtype_immutable = create_safe
        self.result = result

    @overload
    @classmethod
    def generate(cls, data: CrawlResult[Any, CrawlException], runtype: RunType = RunType.NOOP) -> Report: ...

    @overload
    @classmethod
    def generate(cls, data: DetectionResult[Any, DetectionException], runtype: RunType = RunType.NOOP) -> Report: ...

    @overload
    @classmethod
    def generate(cls, data: Result, runtype: RunType = RunType.NOOP) -> Report: ...

    @classmethod
    def generate(cls, data: ResultType, runtype: RunType = RunType.NOOP) -> Report:
        """Create a default report object.

        A factory method to create a view-only (Noop) or escalatable (Dry-run)
        report instance. A dry-run instance can be raised to apply status if wanted.

        Args:
            data: Result to be loaded into the report object.
            runtype: Initial runtype for the report execution.

        Returns:
            A populated report object.
        """
        _runtype_immutable = runtype == RunType.NOOP

        report: Report = Report(runtype=runtype, create_safe=_runtype_immutable)
        report.result = data

        return report

    def dump(self, output: str = "stdout", outdir: Optional[str] = None, drill: bool = True) -> None:
        """Dump report to stdout or a file.

        Args:
            output: Set either to `stdout` for standard output or empty string for file out.
            outdir: Set to file path in case output isn't stdout.
            drill: Print nested results if enabled.
        """
        if output != "stdout":
            if outdir is None:
                raise UnknownOutputStreamError(message="""
The output file specified couldn't be written to. This issue was raised as
\033[1m outdir \033[0m parameter was not defined but \033[1m output \033[0m
was set to value other than \033[1m stdout \033[0m.
If you meant to print the report to \033[1m stdout \033[0m instead, please
specify the output as \033[1m stdout \033[1m. Else specify the \033[1m outdir
\033[1m path as well.
                """)

            try:
                with open(outdir, "w+") as outfile:
                    if drill is False:
                        outfile.write(str((type(self.result.ok), self.result.exception)))
                    else:
                        outfile.write(str(self.result))
            except OSError as os_error:
                print(f"Error occurred while writing to the output file {outdir}.")
                raise os_error
        else:
            print(str(self.result))
