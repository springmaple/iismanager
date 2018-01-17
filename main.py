import os
from functools import partial
from pathlib import Path
from xml.etree import ElementTree

from iis import IIS
from msbuilder import MsBuilder
from tfs import TFS
from ui import MyApp

APP_HOST_CONFIG = str(Path.home()) + r'\Documents\IISExpress\config\applicationhost.config'


class ApplicationHost:
    def __init__(self, xml_file):
        self._xml_root = ElementTree.parse(xml_file).getroot()

    def get_sites(self):
        _ = self._xml_root.find('system.applicationHost').find('sites')
        for site in _.findall('site'):
            site_path = site.find('application').find('virtualDirectory').get('physicalPath')
            yield (site.get('name'),
                   site.get('id'),
                   site_path)


class MainEntry:
    def __init__(self, app_host_config):
        self._app_host = ApplicationHost(app_host_config)
        self._iis = {}
        self._builds = {}
        self._tfs = {}
        self._my_app = None

    def start(self):
        self._my_app = my_app = MyApp(title='IIS Process Manager')
        for site_name, site_id, site_path in self._app_host.get_sites():
            csproj = None
            try:
                for file in os.listdir(site_path):
                    if file.endswith('.csproj'):
                        csproj = os.path.join(site_path, file)
            except FileNotFoundError:
                pass

            my_app.add_site(site_id,
                            site_name,
                            partial(self._btn_pull, site_id, site_path),
                            partial(self._btn_build, site_id, csproj),
                            partial(self._btn_start, site_id),
                            partial(self._show_console, site_id))
            if csproj is None:
                my_app.disable_pull_btn(site_id)
                my_app.disable_build_btn(site_id)

        my_app.run()

    def _btn_pull(self, site_id, site_path, *_):
        try:
            tfs = self._tfs[site_id]
        except KeyError:
            tfs = self._tfs[site_id] = TFS(site_id, site_path, self._my_app)

        tfs.start_pull()
        self._show_console(site_id)

    def _btn_build(self, site_id, csproj, *_):
        try:
            build = self._builds[site_id]
        except KeyError:
            build = self._builds[site_id] = MsBuilder(site_id, csproj, self._my_app)

        build.start_build()
        self._show_console(site_id)

    def _btn_start(self, site_id, *_):
        try:
            iis = self._iis[site_id]
        except KeyError:
            iis = self._iis[site_id] = IIS(site_id, self._my_app)
        iis.toggle_service()
        self._show_console(site_id)

    def _show_console(self, site_id, *_):
        self._my_app.set_console_site(site_id)


if __name__ == '__main__':
    MainEntry(APP_HOST_CONFIG).start()
