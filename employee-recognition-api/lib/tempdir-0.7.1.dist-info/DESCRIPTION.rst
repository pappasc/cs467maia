Having to manually manage temporary directories is annoying.
So this class encapsulates temporary directories which just disappear after use,
including contained directories and files.
Temporary directories are created with tempfile.mkdtemp and thus save from race conditions.
Cleanup might not work on windows if files are still opened.


