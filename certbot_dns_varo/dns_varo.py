from certbot import interfaces
from certbot.plugins import dns_common
from zope.interface import implementer
import logging
import requests

logger = logging.getLogger(__name__)

@implementer(interfaces.IAuthenticator)
@implementer(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    description = 'Obtain certificates using a DNS TXT record (if you are using Varo).'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = None
        self.varo_client = None

    def _get_varo_client(self):
        if self.varo_client is None:
            api_key = self.credentials.conf('api_key')
            self.varo_client = VaroClient(api_key)
        return self.varo_client

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=10)
        add('credentials', help='Path to your Varo credentials INI file.')

    def more_info(self):
        return "This plugin configures Certbot to use Varo for DNS-01 challenge."

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Varo credentials INI file',
            {'api_key': 'API key for Varo API'}
        )

    def _perform(self, domain, validation_name, validation):
        self._get_varo_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_varo_client().del_txt_record(domain, validation_name, validation)

class VaroClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base = 'https://varo.domains/api'

    def add_txt_record(self, domain, record_name, record_value):
        zone_id = self._find_zone_id(domain)
        if not zone_id:
            raise errors.PluginError("Zone ID not found for domain: {domain}")
        payload = {
            "action": "addRecord",
            "zone": zone_id,
            "type": "TXT",
            "name": record_name,
            "content": record_value
        }
        self._api_request(payload)

    def del_txt_record(self, domain, record_name, record_value):
        zone_id = self._find_zone_id(domain)
        record_id = self._find_record_id(zone_id, record_name, record_value)
        if not record_id:
            raise errors.PluginError("Record ID not found for {record_name} with value {record_value}")
        payload = {
            "action": "deleteRecord",
            "zone": zone_id,
            "record": record_id
        }
        self._api_request(payload)

    def _find_zone_id(self, domain):
        response = self._api_request({"action": "getZones"})
        for zone in response.get('data', []):
            if domain.endswith(zone['name']):
                return zone['id']
        raise errors.PluginError("No matching zone found for domain: {domain}")

    def _find_record_id(self, zone_id, record_name, record_value):
        response = self._api_request({
            "action": "getRecords",
            "zone": zone_id,
            "name": record_name,
            "type": "TXT",
            "content": record_value
        })
        for record in response.get('data', []):
            if record['name'] == record_name and record['content'] == record_value:
                return record['uuid']
        raise errors.PluginError("No matching TXT record found for deletion.")

    def _api_request(self, payload):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        response = requests.post(self.api_base, json=payload, headers=headers)
        if response.status_code != 200:
            logger.error("API request failed: %s", response.text)
            raise errors.PluginError("API request failed with status {response.status_code}: {response.text}")
        return response.json()
