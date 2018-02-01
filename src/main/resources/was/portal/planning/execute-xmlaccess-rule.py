#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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




