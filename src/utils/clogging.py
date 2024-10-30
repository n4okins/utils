import inspect
import logging
from typing import Optional

from .colors import JP_COLOR_CODE, Color, ColoredStr

__all__ = ["ColoredFormatter", "getColoredLogger"]


class ColoredFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        colormap: Optional[dict[str, Color]] = None,
    ):
        super().__init__(fmt, datefmt)
        self._colormap = colormap or {
            "DEBUG": JP_COLOR_CODE.AO,
            "INFO": JP_COLOR_CODE.WAKATAKEIRO,
            "WARNING": JP_COLOR_CODE.KIKUCHINASHIIRO,
            "ERROR": JP_COLOR_CODE.HIIRO,
            "CRITICAL": JP_COLOR_CODE.KURENAI,
        }

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        nest_level = (
            len(
                [
                    frame
                    for frame in inspect.getouterframes(inspect.currentframe())
                    if record.pathname == frame.filename
                ]
            )
            - 1
        )
        if levelname in self._colormap:
            if levelname == "CRITICAL":
                record.levelname = ColoredStr(
                    f"{levelname:^9}", bg=self._colormap[levelname]
                )
            else:
                record.levelname = ColoredStr(
                    f"{levelname:^9}", fg=self._colormap[levelname]
                )
            record.msg = ColoredStr(
                nest_level * "    " + record.msg, fg=self._colormap[levelname]
            )
        return super().format(record)


def getColoredLogger(
    name: Optional[str] = None,
    *,
    handlers: Optional[logging.Handler | list[logging.Handler]] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            ColoredFormatter(
                "%(asctime)s\t[%(levelname)s]\t%(message)s\t%(name)s\tL%(lineno)d\t%(funcName)s\t%(pathname)s\t",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    if handlers:
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            logger.addHandler(handler)

    logger.propagate = False
    return logger
