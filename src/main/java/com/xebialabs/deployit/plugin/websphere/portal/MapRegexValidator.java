/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */
package com.xebialabs.deployit.plugin.websphere.portal;

import java.util.Collection;
import java.util.Map;
import java.util.regex.Pattern;

import com.xebialabs.deployit.plugin.api.validation.ValidationContext;

public class MapRegexValidator {

    @SuppressWarnings({ "unchecked" })
    static void validate(Object value, boolean validateKeys, String pattern, String message, ValidationContext context) {
        if (value instanceof Map) {
            Map<String, String> map = (Map<String, String>) value;
            Collection<String> values = validateKeys ? map.keySet() : map.values();
            Pattern compiledPattern = Pattern.compile(pattern);
            for (String val : values) {
                if(!compiledPattern.matcher(val).matches()) {
                    context.error(message, val, pattern);
                }
            }
        }
    }

}
