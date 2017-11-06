# XLD Websphere Portal Plugin

## CI status ##

[![Build Status][xld-websphere-portal-plugin-travis-image]][xld-websphere-portal-plugin-travis-url]
[![Codacy][xld-websphere-portal-plugin-codacy-image] ][xld-websphere-portal-plugin-codacy-url]
[![Code Climate][xld-websphere-portal-plugin-code-climate-image] ][xld-websphere-portal-plugin-code-climate-url]
[![License: MIT][xld-websphere-portal-plugin-license-image]][xld-websphere-portal-plugin-license-url]
![Github All Releases][xld-websphere-portal-plugin-downloads-image]

[xld-websphere-portal-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xld-websphere-portal-plugin.svg?branch=master
[xld-websphere-portal-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xld-websphere-portal-plugin
[xld-websphere-portal-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/28340ed9e96a4d84a05965d2eef307d4
[xld-websphere-portal-plugin-codacy-url]: https://www.codacy.com/app/joris-dewinne/xld-websphere-portal-plugin
[xld-websphere-portal-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xld-websphere-portal-plugin/badges/gpa.svg
[xld-websphere-portal-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xld-websphere-portal-plugin
[xld-websphere-portal-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-websphere-portal-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-websphere-portal-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-websphere-portal-plugin/total.svg

## Preface ##

This document describes the functionality provided by the IBM WebSphere Portal (WP) plugin.


## Overview ##

The Websphere Portal plugin is an XL Deploy plugin that extends the capabilities of the XLD Websphere plugin for managing deployments and resources on an existing WebSphere Portal server. It offers out of the box support for deploying, updating and undeploying portlets developed using the IBM-API or JSR-268.  Also the capability to run user supplied xmlaccess scripts.

## Features ##

* Deploy, update and undeploys Portlets packaged in Web applications archives (WAR).
	* Manage Access Permissions
	* Manage Preferences
	* IBM-API type portlets
	* JSR-268 type portlets
* XML access script execution
	* Template support
	* Placeholder support

## Requirements ##

* **XLD Server** 5+
* **XLD Websphere Plugin** 5+
* **IBM WebSphere Portal** 6.1, 7.0 and 8.0 
		

## Installation ##

Plugin can be downloaded directly from the plugin's repository on [Github](https://github.com/xebialabs-community/xld-websphere-portal-plugin/releases).

Place the plugin XLDP file into __&lt;xld-home&gt;/plugins__ directory. Make sure you have the Websphere plugin mentioned in the requirements section also installed.

## Websphere Portal Connection Information ##

This plugin adds configuration settings under the __Portal__ tab of the __was.DeploymentMananger__ and __was.UnmanagedServer__ configuration items. All properties are required.

| Property | Description |
| -------- | ----------- |
| wpHome   | Location of WebSphere Portal on the primary node. e.g C:\IBM\WebSphere\PortalServer |
| wpAdminUsername | Username of the administrative user |
| wpAdminPassword | Password of the administrative user |
| wpConfigUrl | The URL of the WebSphere Portal configuration API. e.g http://localhost:10039/wps/config |


## Deploying a Portlet War ##

The Portlet War (__wp.War__) configuration item can be defined in a deployment package. __wp.War__ extends the default behaviour of the __was.War__ with additional settings under the __Portal__ tab to describe the Portal application.

| Property | Description | 
| -------- | ----------- |
| portalAppName | Name for the portal application | 
| portalAppUid | Unique identifier for the portal application as defined in the portal.xml |
| portalAppConcreteUid | Concrete Unique identifier for the portal application as defined in the portlet.xml. Only __required__ for __IBM-API__ type portlets |
| disableDeregisterOnUninstall | Disables deregistration of portlets on uninstall of application. |
         
### Defining portlets ###

The portlets that are contained in the War are described using the __wp.PortletSpec__ type. This type is a child of the __wp.War__

| Property | Description | 
| -------- | ----------- |
| portletName | Name of the portlet as described in the portlet.xml |
| uniqueName | Unique name for portlet. e.g. com.xebialabs.WelcomePortlet. _Optional_|
| preferences |Preferences for the portlet described as a key value map. _Optional_. |
| clones | See _Defining portlet clones_ below. _Optional_. |
| authLevel | The String representation of the associated auth level. Only used when step-up autentication is enabled. _Optional_. |
| userAclMapping | See _access permissions_ below. _Optional_. |
| groupAclMapping | See _access permissions_ below. _Optional_. |

### Access permissions ###
Portlet access permissions can be defined under the __Security__ tab. The permission can be captured for a _user_ or _user\_group_ as a key value map. The _key_ being the desired security level. The _value_ should container the desired subject ids delimited by a pipe (\|).
Valid security levels are, 

* user
* privileged user
* contributor
* editor
* manager
* delegator
* security administrator
* administrator

### Defining portlet clones ###

Portlets which need to be cloned can be specified using the __wp.PortletCloneSpec__ type. This type is a child of __wp.PortletSpec__.
A clone of a portlet is an instance of a portlet with it's own name and specifications like preferences. Therefore it needs some propterties of which some are like a normal portlet.

| Property | Description | 
| -------- | ----------- |
| cloneName | A clone name needs $cloned in the name. If you fully specify the clone name here e.g. welcomePortlet.$cloned.clone1 then it will be used. If only a simple name is used then a full name is generate with portletName and this name, e.g. portletName=welcome-portlet and cloneName = clone1 makes name welcome-portlet.$cloned.clone1. |
| uniqueName | Unique name for portlet. e.g. com.xebialabs.WelcomePortlet. _Optional_|
| preferences |Preferences for the portlet described as a key value map. _Optional_. |
| defaultLocale | A default locale which describes the portlet. Needs to be in the localedata list |
| localedata | See _Locale data_ below |
| authLevel | The String representation of the associated auth level. Only used when step-up autentication is enabled. _Optional_. |
| userAclMapping | See _access permissions_ above. _Optional_. |
| groupAclMapping | See _access permissions_ above. _Optional_. |

### Locale data ###  

A portlet Clone needs like name and description, this can be specified using the __wp.PortletCloneLocaleDataSpec__ type. This type is a child of __wp.PortletCloneSpec__.
For portlets this is normally stated in the portlet.xml, but for clones this needs to be added, as it is probably different then the original portlet.
One locale needs to be setup, and be referred as default locale for the clone. All other locales are optional.

| Property | Description | 
| -------- | ----------- |
| locale | The locale. e.g. en |
| title | Portlet title in specified locale. |
| description | Portlet descriptions in specified locale. _Optional_. |
| keywords | Portlet keywords in specified locale. _Optional_. |


### Sample _deployit-manifest.xml_ ###

```xml
<?xml version="1.0" encoding="UTF-8"?>
<udm.DeploymentPackage version="1.0" application="IBMPortletApp">
  <deployables>
    <wp.War name="WelcomePortlet.war" file="WelcomePortlet.war/WelcomePortlet.war">
      <contextRoot>/wps/PA_WPS_XLD_Welcome</contextRoot>
      <portalAppName>Welcome</portalAppName>
      <portalAppUid>com.ibm.wps.portlets.welcome</portalAppUid>
      <portalAppConcreteUid>com.ibm.wps.portlets.welcome.1</portalAppConcreteUid>
      <portlets>
        <wp.PortletSpec name="WelcomePortlet.war/WelcomePortlet">
          <portletName>Welcome Portlet</portletName>
          <uniqueName>com.xebialabs.welcomeportlet</uniqueName>
          <preferences>
            <entry key="apref">apref_value</entry>
          </preferences>
          <userAclMapping>
            <entry key="user">anonymous portal user</entry>
          </userAclMapping>
          <groupAclMapping>
            <entry key="user">all authenticated portal users</entry>
          </groupAclMapping>
          <clones>
          <wp.PortletCloneSpec name="WelcomePortlet.war/WelcomePortlet/clonespec1">
            <cloneName>clone1</cloneName>
            <preferences>
              <entry key="apref">apref_value_for_clone</entry>
            </preferences>
            <defaultlocale>en</defaultlocale>
            <localedata>
              <wp.PortletCloneLocaleDataSpec name="WelcomePortlet.war/WelcomePortlet/clonespec1/en">
                <locale>en</locale>
                <title>Welcome Portlet Clone</title>
              </wp.PortletCloneLocaleDataSpec>
            </localedata>
            <userAclMapping>
              <entry key="user">anonymous portal user</entry>
            </userAclMapping>
            <groupAclMapping>
              <entry key="user">all authenticated portal users</entry>
            </groupAclMapping>
          </wp.PortletCloneSpec>
        </clones>
        </wp.PortletSpec>
      </portlets>
    </wp.War>
  </deployables>
</udm.DeploymentPackage>
```

## Deploying user supplied XmlAccess script

The plugin offers configuration item types __wp.XmlAccessScriptPair__ and __wp.XmlAccessInlineScriptPair__ that can be defined in a deployment package. The user should provide the xmlaccess script to execute on the target portal server.  The xmlaccess script can contain [Freemarker](http://freemarker.org/docs/index.html) templating logic that will be resolved by the plugin before execution. Freemarker variable __deployed__ is available to the template to resolve properties.

The types also allow the user to supply an optional rollback xmlaccess script that would undo the main xmlaccess script. 

Both types have the same functionality except for the location of the xmlaccess script to execute. __wp.XmlAccessInlineScriptPair__ defines the script as a property on the configuration item, whereas __wp.XmlAccessScriptPair__ is an artifact folder containing the files to execute.

### wp.XmlAccessInlineScriptPair ###
A resource containing inline XmlAccess scripts that are used for deployment and rollback.

| Property | Description | 
| -------- | ----------- |
| applyScript | XmlAccess to execute on deployment |
| unapplyScript | XmlAccess to execute on rollback. Should undo what the apply script did.|
| configUri | Uri to be appended to the wpConfigUrl defined on the container. Used when applying xmlaccess to a virtual portal. Example if the wpConfigUrl is _http://localhost:10039/wps/config_ and this property is set to _sp_, then final config url will be _http://localhost:10039/wps/config/sp_|

### wp.XmlAccessScriptPair ###

A folder containing 2 XmlAccess files that are used for deployment and rollback.

| Property | Description | 
| -------- | ----------- |
| applyScript | Name of XmlAccess file in folder to execute on deployment |
| unapplyScript | Name of XmlAccess file in folder to execute on rollback. Should undo what the apply file did.|   
| configUri | Uri to be appended to the wpConfigUrl defined on the container. Used when applying xmlaccess to a virtual portal. Example if the wpConfigUrl is _http://localhost:10039/wps/config_ and this property is set to _sp_, then final config url will be _http://localhost:10039/wps/config/sp_|


### Sample deployit-manifest.xml ###

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<udm.DeploymentPackage version="3.0" application="IBMPortletApp">
  <deployables>
    <wp.XmlAccessScriptPair name="XebiaLabsPortalPage" file="XebiaLabsPortalPage/Archive.zip">
      <applyScript>createPage.xml</applyScript>
      <unapplyScript>destroyPage.xml</unapplyScript>
    </wp.XmlAccessScriptPair>
  </deployables>
</udm.DeploymentPackage>
```



## Sample Dars ##

Sample dars are available to show XLD deployment packaging.
The dars use the WelcomePortlet.war and Blurb2.war that come with Websphere Portal Server. They also contain sample xmlaccess scripts to defined pages. The dars can be executed in order of their version to demonstrate deploy, upgrade and undeploy logic as performed by the plugin.

* [IBMPortletApp-1.0.dar](./src/main/docs/samples/IBMPortletApp-1.0.dar)
* [IBMPortletApp-2.0.dar](./src/main/docs/samples/IBMPortletApp-2.0.dar)
* [IBMPortletApp-3.0.dar](./src/main/docs/samples/IBMPortletApp-3.0.dar)
* [JsrPortletApp-1.0.dar](./src/main/docs/samples/JsrPortletApp-1.0.dar)
* [JsrPortletApp-2.0.dar](./src/main/docs/samples/JsrPortletApp-2.0.dar)

