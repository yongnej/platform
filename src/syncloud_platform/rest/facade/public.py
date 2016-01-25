import os
from os.path import join

from syncloud_app import logger

from syncloud_platform.rest.facade.common import html_prefix
from syncloud_platform.rest.model.app import app_from_sam_app, App


class Public:

    def __init__(self, platform_config, user_platform_config, device, sam, hardware):
        self.hardware = hardware
        self.platform_config = platform_config
        self.log = logger.get_logger('rest.public')
        self.user_platform_config = user_platform_config
        self.device = device
        self.sam = sam
        self.www_dir = self.platform_config.www_root()

    def browse(self, filesystem_path):
        entries = sorted(os.listdir(filesystem_path))
        return [{'name': entry, 'is_file': os.path.isfile(join(filesystem_path, entry))} for entry in entries]

    def installed_apps(self):
        apps = [app_from_sam_app(a) for a in self.sam.installed_user_apps()]

        # TODO: Hack to add system apps, need to think about it
        apps.append(App('store', 'App Store', html_prefix + '/store.html'))
        apps.append(App('settings', 'Settings', html_prefix + '/settings.html'))
        return apps

    def get_app(self, app_id):
        return self.sam.get_app(app_id)

    def install(self, app_id):
        self.sam.install(app_id)

    def remove(self, app_id):
        return self.sam.remove(app_id)

    def upgrade(self, app_id):
        self.sam.upgrade(app_id)

    def update(self):
        return self.sam.update()

    def available_apps(self):
        return [app_from_sam_app(a) for a in self.sam.user_apps()]

    def external_access(self):
        return self.user_platform_config.get_external_access()

    def external_access_enable(self, external_access):
        self.device.set_access(self.user_platform_config.get_protocol(), external_access)

    def protocol(self):
        return self.user_platform_config.get_protocol()

    def set_protocol(self, protocol):
        self.device.set_access(protocol, self.user_platform_config.get_external_access())

    def disk_activate(self, device):
        return self.hardware.activate_disk(device)

    def system_upgrade(self):
        self.sam.upgrade('platform')

    def sam_status(self):
        return self.sam.is_running()

    def disk_deactivate(self):
        return self.hardware.deactivate_disk()

    def disks(self):
        return self.hardware.available_disks()