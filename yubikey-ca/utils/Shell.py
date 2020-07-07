class Shell:
    def __init__(self):
        self.out = {}
        self.pass_fds = []
        self.pipeout_fds = []

    def pipein(self, data):
        """
        Equivalent of zsh/bash <() operator
        Create a pipe, send data to it so a child process can read it as a /proc/self/fd/ file
        """
        rfd, wfd = os.pipe()
        if os.fork() == 0:
            os.close(rfd)
            while data:
                data = data[os.write(wfd, data):]
            os.close(wfd)
            sys.exit(0)
        else:
            self.pass_fds.append(rfd)
            os.close(wfd)
            return "/proc/self/fd/%s" % rfd

    def pipeout(self, name):
        """
        Provides a fd usable by the subprocess for writing
        Its result will be in sh.out[name]
        """
        rfd, wfd = os.pipe()
        self.pass_fds.append(wfd)
        self.pipeout_fds.append((name, rfd))
        return "/proc/self/fd/%s" % wfd

    def _read_pipe(self, name, rfd):
        with os.fdopen(rfd, 'rb') as f:
            self.out[name] = f.read()

    def _close_fds(self):
        for fd in self.pass_fds:
            os.close(fd)
        self.pass_fds.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close_fds()

    def run(self, *args, input=None, **kwargs):
        kwargs.setdefault('stdout', subprocess.PIPE)
        if input is not None:
            kwargs.setdefault('stdin', subprocess.PIPE)
        with subprocess.Popen(args, pass_fds=self.pass_fds, **kwargs) as process:
            self._close_fds()
            threads = []
            for pfd in self.pipeout_fds:
                thread = threading.Thread(target=self._read_pipe, args=pfd)
                thread.start()
                threads.append(thread)
            stdout, stderr = process.communicate(input)
            retcode = process.wait()
            [thread.join() for thread in threads]
            if retcode:
                raise subprocess.CalledProcessError(retcode, process.args, output=stdout, stderr=stderr)
            return stdout

def run(*args, **kwargs):
    with Shell() as sh:
        return sh.run(*args, **kwargs)
