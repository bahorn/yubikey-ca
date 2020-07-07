import os
from git import Repo

from .storage import Storage, DEFAULT_README

class GitStorage(Storage):
    """
    Git based storage backend.
    """

    tracked_files = []

    def __init__(self, path='.'):
        self.path = path

        # check if path is a repo, otherwise create it.
        if GitStorage._exists(path):
            self.create()
        else:
            self.repo = Repo(self.path)

    def track(self, files=[]):
        """
        Adds the file to the list of tracked files.
        """
        file_list = []

        if type(files) is not List:
            file_list.append(files)
        else:
            file_list += files

        self.tracked_files += file_list

    def create(self):
        """
        Create a respository, with all the default values.
        """
        self.repo = Repo.init(path, bare=True)
        # Now we have a bare repo, need to do initial commit.
        self.track('README.md')

        with open('README.md', 'wb') as readme:
            readme.write(DEFAULT_README)

        self.update('Initial Commit')

    def update(self, message):
        """
        Commit the changes to the repository
        """
        self.repo.add(self.tracked_files)
        self.repo.commit(message)

    def archive(self, path):
        """
        Backup the repository as a tarball.
        """
        with open(path, 'wb') as fp:
            self.repo.archive(fp)

    @staticmethod
    def _exists(path):
        """
        Helper to evaluate whenever a path exists or not.
        """
        try:
            repo = Repo(path)
        except NoSuchPathError:
            return False
        # We shouldn't catch InvalidGitRepositoryError here.
        # that should be raised up to a higher level.
        return True
