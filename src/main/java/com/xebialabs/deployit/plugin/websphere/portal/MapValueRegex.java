/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */
package com.xebialabs.deployit.plugin.websphere.portal;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import com.xebialabs.deployit.plugin.api.reflect.PropertyKind;
import com.xebialabs.deployit.plugin.api.validation.ApplicableTo;
import com.xebialabs.deployit.plugin.api.validation.Rule;
import com.xebialabs.deployit.plugin.api.validation.ValidationContext;

@Retention(RetentionPolicy.RUNTIME)
@Rule(clazz = MapValueRegex.Validator.class, type = "map-value-regex")
@ApplicableTo({ PropertyKind.MAP_STRING_STRING })
@Target(ElementType.FIELD)
public @interface MapValueRegex {
    String DEFAULT_MESSAGE = "Value '%s' did not conform to pattern %s";
    String pattern();
    String message() default DEFAULT_MESSAGE;

    class Validator implements com.xebialabs.deployit.plugin.api.validation.Validator<Object> {
        private String pattern;
        private String message = DEFAULT_MESSAGE;
        
        @Override
        @SuppressWarnings({ "unchecked" })
        public void validate(Object value, ValidationContext context) {
            MapRegexValidator.validate(value, false, pattern, message, context);
        }
    }
}