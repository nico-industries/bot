import datetime
import enum
import logging
import os
import pathlib

__all__: tuple[str, ...] = ("Logger",)


class LogLevelColors(enum.Enum):
    """Colors for the log levels."""

    DEBUG = "\033[96m"
    INFO = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[33m"
    CRITICAL = "\033[91m"
    ENDC = "\033[0m"


class RelativePathFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter the log record."""
        record.pathname = record.pathname.replace(os.getcwd(), "~")
        return True


class Formatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            "[%(asctime)s] | %(pathname)s:%(lineno)d | %(levelname)s | %(message)s",
        )

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record."""
        return f"{LogLevelColors[record.levelname].value}{super().format(record)}{LogLevelColors.ENDC.value}"


class FileHandler(logging.FileHandler):
    _last_entry: datetime.datetime = datetime.datetime.today()

    def __init__(self, *, folder: pathlib.Path | str = "logs") -> None:
        """Create a new file handler."""
        self.folder = pathlib.Path(folder)
        self.folder.mkdir(exist_ok=True)
        super().__init__(
            self.folder / f"{datetime.datetime.today().strftime('%Y-%m-%d')}_log.log",
            encoding="utf-8",
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        if self._last_entry.date() != datetime.datetime.today().date():
            self._last_entry = datetime.datetime.today()
            self.close()
            self.baseFilename = (self.folder / f"{self._last_entry.strftime('%Y-%m-%d')}_log.log").as_posix()
            self.stream = self._open()
        super().emit(record)


class Logger(logging.Logger):
    def __init__(self, *, name: str, level: int = logging.INFO) -> None:
        super().__init__(name, level)
        self._handler = logging.StreamHandler()
        self._file_handler = FileHandler()
        self._setup()

    def _setup(self) -> None:
        """Setup the logger."""
        self._handler.addFilter(RelativePathFilter())
        self._handler.setFormatter(Formatter())
        self.addHandler(self._handler)
        self._file_handler.addFilter(RelativePathFilter())
        self._file_handler.setFormatter(Formatter())
        self.addHandler(self._file_handler)

    def set_formatter(self, formatter: logging.Formatter) -> None:
        """Set the formatter."""
        self._handler.setFormatter(formatter)
        self._file_handler.setFormatter(formatter)
