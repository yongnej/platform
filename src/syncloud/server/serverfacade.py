import uuid
from syncloud.config.config import PlatformConfig
from syncloud.server.auth import Auth
from syncloud.tools.facade import Facade
from syncloud.sam.manager import get_sam
from syncloud.insider import facade
from syncloud.app import logger


class ServerFacade:
    def __init__(self, sam, insider):
        self.sam = sam
        self.insider = insider
        self.tools = Facade()
        self.logger = logger.get_logger('ServerFacade')
        self.auth = Auth()

    def activate(self,
                 redirect_email, redirect_password, user_domain,
                 device_user, device_password,
                 api_url=None, domain=None, release=None):

        if not api_url:
            api_url = 'http://api.syncloud.it'

        if not domain:
            domain = 'syncloud.it'

        # self.reconfigure()

        self.logger.info("activate {0}, {1}, {2}, {3}, {4}, {5}".format(
            redirect_email, user_domain, device_user, release, api_url, domain))

        self.sam.update(release)
        # self.sam.upgrade_all()

        self.insider.set_redirect_info(domain, api_url)
        self.insider.acquire_domain(redirect_email, redirect_password, user_domain)

        try:
            self.insider.add_service("server", "http", "server", 80, None)
        except Exception, e:
            self.logger.info('upnp is not available ' + e.message)

        # self.logger.info("reconfiguring installed apps")
        # self.sam.reconfigure_installed_apps()

        self.logger.info("activating ldap")
        self.auth.reset(device_user, device_password)
        PlatformConfig().set_web_secret_key(unicode(uuid.uuid4().hex))

        # credentials = _get_credentials(self.remote_access.enable())
        self.logger.info("activation completed")
        return 'cred'

    # def reconfigure(self):
    #     http_conf = join(self.tools.usr_local_dir(), 'syncloud-server', 'apache', 'syncloud-server-http.conf')
    #     self.apache.add_http_site('server', http_conf)
    #     https_conf = join(self.tools.usr_local_dir(), 'syncloud-server', 'apache', 'syncloud-server-https.conf')
    #     self.apache.add_https_site('server', https_conf)
    #     self.apache.restart()

    # def get_access(self):
    #     return _get_credentials(self.remote_access.add_certificate())

    def user_domain(self):
        return self.insider.user_domain()


def get_server(insider=None):
    sam = get_sam()
    if insider is None:
        insider = facade.get_insider()
    return ServerFacade(sam, insider)