#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
