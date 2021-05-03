import os
import tempfile

from ptn.logger.foldercleanup.TimedDirectoryCleanup import TimedDirectoryCleanup


def test_timed_directory_cleanup():
    with tempfile.TemporaryDirectory() as folder:
        # Go make it just in case
        if not os.path.exists(folder):
            os.mkdir(folder)

        for x in range(10):
            # Go make 10 files
            with open(os.path.join(folder, f'test_{x}.txt'), 'w') as f:
                f.write('Contents')
                f.flush()

        directory_cleanup = TimedDirectoryCleanup(directory=folder)
        assert len(os.listdir(folder)) == 10

        # Remove 5 files
        directory_cleanup.cleanup()

        # After cleaning we should have 5 folders
        assert len(os.listdir(folder)) == 5


def test_timed_directory_cleanup_custom_backup_count():
    with tempfile.TemporaryDirectory() as folder:
        # Go make it just in case
        if not os.path.exists(folder):
            os.mkdir(folder)

        for x in range(10):
            # Go make 10 files
            with open(os.path.join(folder, f'test_{x}.txt'), 'w') as f:
                f.write('Contents')
                f.flush()

        directory_cleanup = TimedDirectoryCleanup(directory=folder, backup_count=7)
        assert len(os.listdir(folder)) == 10

        # Remove 5 files
        directory_cleanup.cleanup()

        # After cleaning we should have 7 folders
        assert len(os.listdir(folder)) == 7
