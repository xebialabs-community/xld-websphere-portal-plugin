#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from com.xebialabs.deployit.plugin.api.reflect import Type

def is_file_request(deployed):
    return deployed.type.instanceOf(Type.valueOf("wp.ExecutedXmlAccessScriptPair"))

def get_step_desc(deployed, is_file, is_rollback=False):
    rollback = " "
    script = deployed.applyScript
    if is_rollback:
        rollback = " uninstall "
        script = deployed.unapplyScript
    if is_file:
        desc = "Execute user defined xmlaccess%sscript contained in %s for %s on %s" % (rollback, script, deployed.name, deployed.container.name)
    else:
        desc = "Execute user defined xmlaccess%sscript for %s on %s" % (rollback, deployed.name, deployed.container.name)
    return desc

def create_step(deployed):
    is_file = is_file_request(deployed)
    step = steps.jython(
        description=get_step_desc(deployed, is_file),
        order=74,
        script_path="was/portal/xmlscript/execute-xmlaccess.py",
        jython_context={"deployed": deployed, "req_xml": deployed.applyScript, "is_file": is_file})
    return step

def destroy_step(deployed):
    is_file = is_file_request(deployed)
    step = steps.jython(
        description=get_step_desc(deployed, is_file, is_rollback=True),
        order=26,
        script_path="was/portal/xmlscript/execute-xmlaccess.py",
        jython_context={"deployed": deployed, "req_xml": deployed.unapplyScript, "is_file": is_file})
    return step

op = str(delta.operation)
if op == "CREATE":
    context.addStep(create_step(delta.deployed))
elif op == "DESTROY":
    if delta.previous.unapplyScript:
        context.addStep(destroy_step(delta.previous))
elif op == "MODIFY":
    context.addStep(create_step(delta.deployed))
    if delta.previous.unapplyScript:
        context.addStep(destroy_step(delta.previous))




