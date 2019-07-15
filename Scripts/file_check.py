import errno, os, tempfile, sys

#Windows-specific error code indicating an invalid pathname
ERROR_INVALID_NAME = 123


def is_pathname_valid(pathname: str) -> bool:
    '''
    Return `True` if the passed pathname is a valid pathname for the current
    OS, and `False` otherwise. If the pathname provided is either not a string
    or is a string but is empty, return `False`.
    '''
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        #Strips this pathname's Windows-specific drive specifier (e.g., `C:\`)
        #if any.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True


def is_path_creatable(pathname: str) -> bool:
    '''
    Return `True` if the current user has sufficient permissions to create the
    passed pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    Return `True` if the passed pathname is a valid pathname for the current
    OS and either currently exists or is hypothetically createable; `False
    otherwise.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        return False


def is_path_sibling_creatable(pathname: str) -> bool:
    '''
    Return `True` if the current user has sifficient permissions to create
    siblings (arbitrary files in the parent directory) of the passed pathname,
    and `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()

    try:
        # Opening and immediately closing the temporary file
        with tempfile.TemporaryFile(dir=dirname): pass
        return True
    # All exceptions fall under the EnvironmentError subclass
    except EnvironmentError:
        return False


def is_path_exists_or_creatable_portable(pathname: str) -> bool:
    '''
    Return `True` if the passed pathname is a valid pathname on the current OS
    and either currently exists or is hypothetically creatable in a
    cross-platform manner optimized for POSIX-unfriendly filesystems; `False`
    otherwise.
    Never raises errors.
    '''
    try:
        # Calls is_pathname_valid() first to prevent "os" module from raising
        # undesirable exceptions on invalid pathnames
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_sibling_creatable(pathname))
    except OSError:
        pass