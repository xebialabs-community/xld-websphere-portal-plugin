#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from was.portal.utils.xmlaccess import XmlAccess
from was.portal.utils.template import TemplateRenderer
from com.xebialabs.overthere.util import OverthereUtils

xmlaccess = XmlAccess.new_instance_from_container(context, deployed.container.cell)

if is_file:
    req_file = deployed.file.getFile(req_xml)
    xml = OverthereUtils.read(req_file, "UTF-8")
else:
    xml = req_xml

rendered_xml = TemplateRenderer().render(xml, {'deployed': deployed})
xmlaccess.execute_and_log_input_output(rendered_xml)
