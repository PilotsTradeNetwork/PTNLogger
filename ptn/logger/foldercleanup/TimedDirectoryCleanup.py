import os
import shutil
from itertools import islice


class TimedDirectoryCleanup:

    def __init__(self, directory, backup_count=5):
        """
        Class offers support to delete a list of files from a specified directory

        :param str directory: The directory to inspect and cleanup
        :param int backup_count: How many files to keep
        """
        self.directory = directory
        self.backup_count = backup_count

    def cleanup(self):

        delete = islice(self._matching_files(), self.backup_count, None)
        for entry in delete:
            os.remove(entry)

    def _matching_files(self):
        """
        Matches all the files in the given directory, reverse ordered.
        """
        matches = []

        for entry in os.scandir(self.directory):
            # Just loop over every file and save it to the list
            matches.append(entry)

        matches.sort(key=lambda e: e.stat().st_mtime, reverse=True)
        return iter(matches)
