import subprocess
import traceback
from threading import Thread


class MsBuilder:
    def __init__(self, site_id, csproj, app):
        self._site_id = site_id
        self._csproj = csproj
        self._app = app
        self._proc = None

    def start_build(self):
        self._proc = subprocess.Popen(('msbuilder.bat', self._csproj),
                                      stdin=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        self._clear_output()
        self._set_output('Build Process ID: ' + str(self._proc.pid) + '\r\n\r\n')
        Thread(target=self._read).start()

    def _set_output(self, text):
        self._app.set_console_output(self._site_id, text)

    def _clear_output(self):
        self._app.clear_console_output(self._site_id)

    def _wait_stop(self):
        if self._proc:
            code = self._proc.wait()
            self._set_output('Build Exit Code: ' + str(code))
            self._proc = None

    def _read(self):
        try:
            output = b''
            for line in self._proc.stdout:
                output += line
                if not line or line.startswith(b'-end'):
                    self._set_output(output.decode())
                    self._wait_stop()
                    break
        except:
            traceback.print_exc()
