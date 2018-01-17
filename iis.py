import subprocess
import time
import traceback
from threading import Thread

IIS_EXPRESS = r'C:\Program Files (x86)\IIS Express\iisexpress.exe'


class IIS:
    def __init__(self, id_, app):
        self._id = id_
        self._proc = None
        self._app = app
        self._start_btn = app.get_start_btn(id_)

    def toggle_service(self):
        if self._start_btn.is_started:
            self._stop_service()
        else:
            self._start_service()

    def _set_output(self, text):
        self._app.set_console_output(self._id, text)

    def _clear_output(self):
        self._app.clear_console_output(self._id)

    def _start_service(self):
        self._proc = subprocess.Popen((IIS_EXPRESS, '/siteid:' + self._id),
                                      stdin=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        self._clear_output()
        self._set_output('IIS Process ID: ' + str(self._proc.pid) + '\r\n\r\n')
        self._start_btn.set_to_stop()
        Thread(target=self._read).start()

    def _stop_service(self):
        if self._proc:
            self._proc.kill()
            self._proc.wait()
            self._proc = None
        self._start_btn.set_to_start()
        self._set_output('\r\n-------------------------- END -------------------------\r\n')

    def _delay_stop(self):
        def do_stop():
            time.sleep(3)
            self._stop_service()
        Thread(target=do_stop).start()

    def _read(self):
        try:
            for line in self._proc.stdout:
                self._set_output(line.decode())
                if (not line
                        or line.startswith(b'IIS Express stopped.')
                        or line.startswith(b'Failed to register URL')):
                    self._delay_stop()
                    break
        except:
            traceback.print_exc()
