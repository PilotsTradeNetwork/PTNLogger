import os
import re
import datetime
import logging
from itertools import islice


class TimedPatternFileHandler(logging.FileHandler):

    def __init__(self, filename_pattern, mode, backup_count):
        """File handler that uses the current time fo the log filename, by formatting the current datetime,
        according to filename_pattern, using the strftime function.

        If backup_count is non-zero, then older filenames that match the base filename are deleted to only leave the
        backup_count most recent copies, whenever opening a new log file with a different name.

        Taken from:  https://stackoverflow.com/questions/43947206/automatically-delete-old-python-log-files

        :param str filename_patter: The file name pattern to use
        :param str mode: The file mode to open the file as.
        :param int backup_count: How many files to keep
        """
        self.filename_pattern = os.path.abspath(filename_pattern)
        self.backup_count = backup_count
        self.filename = datetime.datetime.now().strftime(self.filename_pattern)

        delete = islice(self._matching_files(), self.backup_count, None)
        for entry in delete:
            os.remove(entry.path)
        super().__init__(filename=self.filename, mode=mode)

    @property
    def filename(self):
        """Generate the 'current' filename to open"""
        # use the start of *this* interval, not the next
        return datetime.datetime.now().strftime(self.filename_pattern)

    @filename.setter
    def filename(self, _):
        pass

    def _matching_files(self):
        """Generate DirEntry entries that match the filename pattern.

        The files are ordered by their last modification time, most recent
        files first.

        """
        matches = []
        basename = os.path.basename(self.filename_pattern)
        pattern = re.compile(re.sub('%[a-zA-z]', '.*', basename))

        for entry in os.scandir(os.path.dirname(self.filename_pattern)):
            if not entry.is_file():
                continue
            entry_basename = os.path.basename(entry.path)
            if re.match(pattern, entry_basename):
                matches.append(entry)
        matches.sort(key=lambda e: e.stat().st_mtime, reverse=True)
        return iter(matches)
