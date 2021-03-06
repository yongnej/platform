from ConfigParser import ConfigParser
from os.path import isfile, join
from syncloud_app import logger

PLATFORM_CONFIG_NAME = 'platform.cfg'
PLATFORM_APP_NAME = 'platform'
PLATFORM_CONFIG_DIR = '/opt/data/platform/config'
WEB_CERTIFICATE_PORT = 80
WEB_ACCESS_PORT = 443
WEB_PROTOCOL = 'https'


class PlatformConfig:

    def __init__(self, config_dir):
        self.parser = ConfigParser()
        self.filename = join(config_dir, PLATFORM_CONFIG_NAME)
        if (not isfile(self.filename)):
            raise Exception('platform config does not exist: {0}'.format(self.filename))
        self.parser.read(self.filename)

    def apps_root(self):
        return self.__get('apps_root')

    def data_root(self):
        return self.__get('data_root')

    def configs_root(self):
        return self.__get('configs_root')

    def config_root(self):
        return self.__get('config_root')

    def www_root_internal(self):
        return self.__get('www_root_internal')

    def www_root_public(self):
        return self.__get('www_root_public')

    def app_dir(self):
        return self.__get('app_dir')

    def data_dir(self):
        return self.__get('data_dir')

    def config_dir(self):
        return self.__get('config_dir')

    def bin_dir(self):
        return self.__get('bin_dir')

    def nginx_config_dir(self):
        return self.__get('nginx_config_dir')

    def cron_user(self):
        return self.__get('cron_user')

    def cron_cmd(self):
        return self.__get('cron_cmd')

    def openssl(self):
        return self.__get('openssl')

    def nginx(self):
        return self.__get('nginx')

    def cron_schedule(self):
        return self.__get('cron_schedule')

    def get_web_secret_key(self):
        return self.__get('web_secret_key')

    def set_web_secret_key(self, value):
        return self.__set('web_secret_key', value)

    def get_user_config(self):
        return self.__get('user_config')

    def get_log_root(self):
        return self.__get('log_root')

    def get_log_sender_pattern(self):
        return self.__get('log_sender_pattern')

    def get_internal_disk_dir(self):
        return self.__get('internal_disk_dir')

    def get_external_disk_dir(self):
        return self.__get('external_disk_dir')

    def get_disk_link(self):
        return self.__get('disk_link')

    def get_disk_root(self):
        return self.__get('disk_root')

    def get_ssh_port(self):
        return self.__get('ssh_port')

    def set_ssh_port(self, value):
        return self.__set('ssh_port', value)

    def get_rest_internal_log(self):
        return self.__get('rest_internal_log')

    def get_rest_public_log(self):
        return self.__get('rest_public_log')

    def get_ssl_certificate_file(self):
        return self.__get('ssl_certificate_file')

    def get_ssl_ca_certificate_file(self):
        return self.__get('ssl_ca_certificate_file')

    def get_ssl_ca_serial_file(self):
        return self.__get('ssl_ca_serial_file')

    def get_ssl_certificate_request_file(self):
        return self.__get('ssl_certificate_request_file')

    def get_default_ssl_certificate_file(self):
        return self.__get('default_ssl_certificate_file')

    def get_ssl_key_file(self):
        return self.__get('ssl_key_file')

    def get_ssl_ca_key_file(self):
        return self.__get('ssl_ca_key_file')

    def get_default_ssl_key_file(self):
        return self.__get('default_ssl_key_file')

    def get_openssl_config(self):
        return self.__get('openssl_config')

    def get_platform_log(self):
        return self.__get('platform_log')

    def get_installer(self):
        return self.__get('installer')

    def get_hooks_root(self):
        return self.__get('hooks_root')

    def is_certbot_test_cert(self):
        return self.parser.getboolean('platform', 'certbot_test_cert')

    def get_boot_extend_script(self):
        return self.__get('boot_extend_script')

    def __get(self, key):
        return self.parser.get('platform', key)

    def __set(self, key, value):
        self.parser.set('platform', key, value)
        with open(self.filename, 'wb') as f:
            self.parser.write(f)


class PlatformUserConfig:

    def __init__(self, config_file):
        self.log = logger.get_logger('PlatformUserConfig')
        self.parser = ConfigParser()
        self.filename = config_file

    def update_redirect(self, domain, api_url):
        self.parser.read(self.filename)
        self.log.info('setting domain={0}, api_url={1}'.format(domain, api_url))
        
        self.__set('redirect', 'domain', domain)
        self.__set('redirect', 'api_url', api_url)
        self.__save()

    def get_redirect_domain(self):
        self.parser.read(self.filename)
        if self.parser.has_section('redirect') and self.parser.has_option('redirect', 'domain'):
            return self.parser.get('redirect', 'domain')
        return 'syncloud.it'

    def get_redirect_api_url(self):
        self.parser.read(self.filename)
        if self.parser.has_section('redirect') and self.parser.has_option('redirect', 'api_url'):
            return self.parser.get('redirect', 'api_url')
        return 'http://api.syncloud.it'

    def set_user_update_token(self, user_update_token):
        self.parser.read(self.filename)
        self.__set('redirect', 'user_update_token', user_update_token)
        self.__save()

    def get_user_update_token(self):
        self.parser.read(self.filename)
        return self.parser.get('redirect', 'user_update_token')

    def set_user_email(self, user_email):
        self.parser.read(self.filename)
        self.__set('redirect', 'user_email', user_email)
        self.__save()

    def get_user_email(self):
        self.parser.read(self.filename)
        return self.parser.get('redirect', 'user_email')

    def set_custom_domain(self, custom_domain):
        self.parser.read(self.filename)
        self.__set('platform', 'custom_domain', custom_domain)
        self.__save()

    def get_custom_domain(self):
        self.parser.read(self.filename)
        if self.parser.has_option('platform', 'custom_domain'):
            return self.parser.get('platform', 'custom_domain')
        return None

    def get_user_domain(self):
        self.parser.read(self.filename)
        if self.parser.has_option('platform', 'user_domain'):
            return self.parser.get('platform', 'user_domain')
        return None

    def get_domain_update_token(self):
        self.parser.read(self.filename)
        if self.parser.has_option('platform', 'domain_update_token'):
            return self.parser.get('platform', 'domain_update_token')
        return None

    def update_domain(self, user_domain, domain_update_token):
        self.parser.read(self.filename)
        self.log.info('saving user_domain = {0}, domain_update_token = {0}'.format(user_domain, domain_update_token))
        self.__set('platform', 'user_domain', user_domain)
        self.__set('platform', 'domain_update_token', domain_update_token)
        self.__save()

    def get_external_access(self):
        self.parser.read(self.filename)
        if not self.parser.has_option('platform', 'external_access'):
            return False
        return self.parser.getboolean('platform', 'external_access')

    def is_redirect_enabled(self):
        self.parser.read(self.filename)
        if not self.parser.has_option('platform', 'redirect_enabled'):
            return True
        return self.parser.getboolean('platform', 'redirect_enabled')
    
    def set_redirect_enabled(self, enabled):
        self.parser.read(self.filename)
        self.__set('platform', 'redirect_enabled', enabled)
        self.__save()

    def update_device_access(self, upnp_enabled, external_access, public_ip, manual_certificate_port, manual_access_port):
        self.parser.read(self.filename)
        self.__set('platform', 'external_access', external_access)
        self.__set('platform', 'upnp', upnp_enabled)
        self.__set('platform', 'public_ip', public_ip)
        self.__set('platform', 'manual_certificate_port', manual_certificate_port)
        self.__set('platform', 'manual_access_port', manual_access_port)
        self.__save()

    def get_upnp(self):
        self.parser.read(self.filename)
        if not self.parser.has_option('platform', 'upnp'):
            return True
        return self.parser.getboolean('platform', 'upnp')

    def get_public_ip(self):
        self.parser.read(self.filename)
        if not self.parser.has_option('platform', 'public_ip'):
            return None
        return self.parser.get('platform', 'public_ip')

    def get_manual_certificate_port(self):
        self.parser.read(self.filename)
        if not self.parser.has_option('platform', 'manual_certificate_port'):
            return None
        return self.parser.get('platform', 'manual_certificate_port')

    def get_manual_access_port(self):
        self.parser.read(self.filename)
        if not self.parser.has_option('platform', 'manual_access_port'):
            return None
        return self.parser.get('platform', 'manual_access_port')

    def __set(self, section, key, value):
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        if value is None:
            self.parser.remove_option(section, key)
        else:
            self.parser.set(section, key, value)

    def __save(self):
        with open(self.filename, 'wb') as f:
            self.parser.write(f)

