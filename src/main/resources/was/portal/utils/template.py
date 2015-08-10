#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from freemarker.ext.beans import BeanModel
from freemarker.template import DefaultObjectWrapper, Configuration, Template
from com.xebialabs.deployit.plugin.api.udm import ConfigurationItem
from java.io import StringReader, StringWriter


class CiTemplateModel(BeanModel):
    def __init__(self, ci, wrapper):
        super(BeanModel, self).__init__(ci, wrapper)
        self._ci = ci

    def get(self, key):
        pd = self._ci.type.descriptor.getPropertyDescriptor(key)
        if pd is None:
            return BeanModel.get(self, key)
        else:
            return pd.get(key)


class CiAwareObjectWrapper(DefaultObjectWrapper):
    def wrap(self, obj):
        if obj is not None and isinstance(obj, ConfigurationItem):
            return CiTemplateModel(obj, self)
        else:
            return DefaultObjectWrapper.wrap(self, obj)


class TemplateRenderer(object):
    def __init__(self):
        conf = Configuration()
        conf.setNumberFormat("computer")
        conf.setObjectWrapper(CiAwareObjectWrapper())
        self._conf = conf

    def render(self, template, context):
        t = Template("inline", StringReader(template), self._conf)
        sw = StringWriter()
        t.process(context, sw)
        return sw.toString()
