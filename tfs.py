import subprocess
import traceback
from threading import Thread


class TFS:
    def __init__(self, site_id, site_path, app):
        self._site_id = site_id
        self._site_path = site_path
        self._app = app
        self._proc = None

    def start_pull(self):
        self._proc = subprocess.Popen(('tfs.bat', self._site_path),
                                      stdin=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        self._clear_output()
        self._set_output('Pull Process ID: ' + str(self._proc.pid) + '\r\n\r\n')
        Thread(target=self._read).start()

    def _set_output(self, text):
        self._app.set_console_output(self._site_id, text)

    def _clear_output(self):
        self._app.clear_console_output(self._site_id)

    def _wait_stop(self):
        if self._proc:
            code = self._proc.wait()
            self._set_output('Pull Exit Code: ' + str(code))
            self._proc = None

    def _read(self):
        try:
            for line in self._proc.stdout:
                self._set_output(line.decode())
                if not line or line.startswith(b'-end'):
                    self._wait_stop()
                    break
        except:
            traceback.print_exc()
