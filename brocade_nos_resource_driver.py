from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails, \
    ConnectivityContext
from cloudshell.networking.generic_bootstrap import NetworkingGenericBootstrap
from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.context_utils import context_from_args
import cloudshell.networking.brocade.nos.brocade_nos_configuration as config
import inject


class BrocadeNOSDriver(ResourceDriverInterface, NetworkingResourceDriverInterface, GlobalLock):
    def __init__(self):
        super(BrocadeNOSDriver, self).__init__()
        bootstrap = NetworkingGenericBootstrap()
        bootstrap.add_config(config)
        bootstrap.initialize()

    @context_from_args
    def initialize(self, context):
        """Initialize method
        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """

        return 'Finished initializing'

    def cleanup(self):
        pass

    @context_from_args
    def ApplyConnectivityChanges(self, context, request):
        # with open("c:\\temp\json.txt", 'a') as file:
        #     file.write(str(request))
        #     file.close()
        connectivity_operations = inject.instance('connectivity_operations')
        connectivity_operations.logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
        response = connectivity_operations.apply_connectivity_changes(request)
        connectivity_operations.logger.info('Finished applying connectivity changes, responce is: {0}'.format(str(
            response)))
        connectivity_operations.logger.info('Apply Connectivity changes completed')
        return response

    @GlobalLock.lock
    @context_from_args
    def restore(self, context, path, config_type, restore_method, vrf=None):
        """Restore selected file to the provided destination

        :param path: source config file
        :param config_type: running or startup configs
        :param restore_method: append or override methods
        :param vrf: VRF management Name
        """

        configuration_operations = inject.instance('configuration_operations')
        response = configuration_operations.restore_configuration(source_file=path, restore_method=restore_method,
                                                                  config_type=config_type, vrf=vrf)
        configuration_operations.logger.info('Restore completed')
        configuration_operations.logger.info(response)

    @context_from_args
    def save(self, context, destination_host, source_filename, vrf=None):
        """Save selected file to the provided destination

        :param source_filename: source file, which will be saved
        :param destination_host: destination path where file will be saved
        :param vrf: VRF management Name
        """

        configuration_operations = inject.instance('configuration_operations')
        response = configuration_operations.save_configuration(destination_host, source_filename, vrf)
        configuration_operations.logger.info('Save completed')
        return response

    @context_from_args
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :return: response
        :rtype: string
        """

        autoload_operations = inject.instance("autoload_operations")
        response = autoload_operations.discover()
        autoload_operations.logger.info('Autoload completed')
        return response

    @GlobalLock.lock
    @context_from_args
    def update_firmware(self, context, remote_host, file_path):
        """Upload and updates firmware on the resource

        :param remote_host: path to tftp:// server where firmware file is stored
        :param file_path: firmware file name
        :return: result
        :rtype: string
        """

        firmware_operations = inject.instance("firmware_operations")
        response = firmware_operations.update_firmware(remote_host=remote_host, file_path=file_path)
        firmware_operations.logger.info(response)

    @context_from_args
    def send_custom_command(self, context, command):
        """Send custom command

        :return: result
        :rtype: string
        """

        send_command_operations = inject.instance("send_command_operations")
        response = send_command_operations.send_command(command=command)
        print response
        return response

    @context_from_args
    def send_custom_config_command(self, context, command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """
        send_command_operations = inject.instance("send_command_operations")
        result_str = send_command_operations.send_config_command(command=command)
        return result_str

    @context_from_args
    def shutdown(self, context):
        pass

    @context_from_args
    def command(self, context, command=None):
        from cloudshell.cli.service.cli_service import CliService
        from cloudshell.cli.session.session import Session
        ses = CliService()
        ss = Session

        # ses._ses
        if command is not None:
            ses.send_command(command=command)#, session=ss)


def create_context():
    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'Brocy'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = '5695cf87-a4f3-4447-a08a-1a99a936010e'
    context.reservation.owner_user = 'admin'
    context.reservation.owner_email = 'fake@qualisystems.com'
    context.reservation.environment_path ='Environment-6-7-2016 15-25'
    context.reservation.environment_name = 'Environment-6-7-2016 15-25'
    context.reservation.domain = 'Global'
    context.resource.attributes = {}
    context.resource.attributes['CLI Connection Type'] = 'SSH'
    context.resource.attributes['User'] = 'admin'
    context.resource.attributes['AdminUser'] = 'admin'

    context.resource.attributes['Password'] = 'password'
    context.resource.attributes['Enable Password'] = 'password'
    context.resource.address = '192.168.73.41'
    context.resource.attributes['SNMP Version'] = '2'
    context.resource.attributes['SNMP Read Community'] = 'public'
    context.resource.attributes['Model'] = 'Brocade NOS Switch'
    context.resource.attributes['AdminPassword'] ='password'
    context.resource.attributes['Vendor'] = 'Brocade'

    context.connectivity = ConnectivityContext()
    context.connectivity.admin_auth_token = ''
    context.connectivity.cloudshell_api_port = '8029'
    context.connectivity.quali_api_port = '9000'
    context.connectivity.server_address = 'localhost'


    # context.connectivity.server_address='localhost'
    # context.description ={}
    # context.description['family'] = 'Router'
    # context.description['fullname'] = 'Huawei37'
    # context.description['id'] = 'b476fa1f-379e-435a-b35c-65e892e1c306'
    # context.description['model'] = 'Huaewi VRP Router'
    # context.description['name'] = 'Huawei37'

    return context

request = '''
{
	"driverRequest": {
		"actions": [{
			"connectionId": "ee7a0952-db4c-44b2-9f61-8b8caafe4395",
			"connectionParams": {
				"vlanId": "2",
				"mode": "Access",
				"vlanServiceAttributes": [{
					"attributeName": "Allocation Ranges",
					"attributeValue": "2-4094",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Isolation Level",
					"attributeValue": "Exclusive",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Access Mode",
					"attributeValue": "Access",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "VLAN ID",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Pool Name",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Virtual Network",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Default VLAN",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "QnQ",
					"attributeValue": "False",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "CTag",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}],
				"type": "setVlanParameter"
			},
			"connectorAttributes": [{
				"attributeName": "Selected Network",
				"attributeValue": "2",
				"type": "connectorAttribute"
			}],
			"actionId": "ee7a0952-db4c-44b2-9f61-8b8caafe4395_43d5fc48-ddce-45fe-9147-dcd30cdecbaa",
			"actionTarget": {
				"fullName": "brocy/Chassis 0/Module 0/FortyGigabitEthernet 1-0-49",
				"fullAddress": "192.168.73.41/0/2/201728192",
				"type": "actionTarget"
			},
			"customActionAttributes": [],
			"type": "setVlan"
		}, {
			"connectionId": "ee7a0952-db4c-44b2-9f61-8b8caafe4395",
			"connectionParams": {
				"vlanId": "2",
				"mode": "Access",
				"vlanServiceAttributes": [{
					"attributeName": "Allocation Ranges",
					"attributeValue": "2-4094",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Isolation Level",
					"attributeValue": "Exclusive",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Access Mode",
					"attributeValue": "Access",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "VLAN ID",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Pool Name",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Virtual Network",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "Default VLAN",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "QnQ",
					"attributeValue": "False",
					"type": "vlanServiceAttribute"
				}, {
					"attributeName": "CTag",
					"attributeValue": "",
					"type": "vlanServiceAttribute"
				}],
				"type": "setVlanParameter"
			},
			"connectorAttributes": [{
				"attributeName": "Selected Network",
				"attributeValue": "2",
				"type": "connectorAttribute"
			}],
			"actionId": "ee7a0952-db4c-44b2-9f61-8b8caafe4395_082427a2-60da-4229-8503-f32bae05e9af",
			"actionTarget": {
				"fullName": "brocy/Chassis 0/Module 0/FortyGigabitEthernet 1-0-50",
				"fullAddress": "192.168.73.41/0/2/201736384",
				"type": "actionTarget"
			},
			"customActionAttributes": [],
			"type": "setVlan"
		}]
	}
}
'''

import cloudshell.helpers.scripts.cloudshell_scripts_helpers as qs_helper
import cloudshell.helpers.scripts.cloudshell_dev_helpers as dev_help
from cloudshell.shell.core.driver_context import *


res_id = 'f7505eb3-b637-4795-9740-19a56244a33d'
dev_help.attach_to_cloudshell_as('admin', 'admin', 'Global', res_id, 'localhost', '8029',resource_name='brocy')
resource = qs_helper.get_resource_context_details()
reservation = qs_helper.get_reservation_context_details()
connectivity = qs_helper.get_connectivity_context_details()
my_context = ResourceCommandContext(connectivity,resource,reservation,[])
my_context.reservation.reservation_id = '5695cf87-a4f3-4447-a08a-1a99a936010e'
# cont = create_context()
driv = BrocadeNOSDriver()
driv.ApplyConnectivityChanges(my_context, request)
# driv.get_inventory(cont)
# driv.command(context=cont, command='conf t')
# driv.command(context=cont, command='int fa 0/1')
# driv.command(context=cont, command='speed 100')


