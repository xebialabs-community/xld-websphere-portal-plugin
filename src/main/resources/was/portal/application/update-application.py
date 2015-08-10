#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

if deployed.file is None:
    printErrorAndExit("ERROR: No file found to deploy, cannot proceed")

installArgs = prepareInstallArgs()
updateArgs = ["-operation", "update", "-contents", deployed.file]
updateArgs.extend(installArgs)
print "Updating application", deployed.name, "with args: %s" % updateArgs
AdminApp.update(deployed.name, 'app', updateArgs)

# update app
deployedObject = getDeployedObject()
updateStartingWeight(deployedObject)
updateClassloader(deployedObject)
updateSessionManager(deployedObject)
updateJsfImplementation(deployedObject)
updateOtherProperties(deployedObject)
