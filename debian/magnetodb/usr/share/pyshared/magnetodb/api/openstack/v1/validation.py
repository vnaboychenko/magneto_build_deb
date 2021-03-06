# Copyright 2014 Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import jsonschema

from magnetodb.common import exception
from magnetodb.openstack.common.log import logging


LOG = logging.getLogger(__name__)


def format_validation_msg(errors):
    # format path like object['field1'][i]['subfield2']
    messages = []
    for error in errors:
        path = list(error.path)
        f_path = ''
        if path:
            f_path = "%s%s" % (path[0],
                               ''.join(['[%r]' % i for i in path[1:]]))
        messages.append("%s %s" % (f_path, error.message))
        for suberror in sorted(error.context, key=lambda e: e.schema_path):
            messages.append(suberror.message)
    error_msg = "; ".join(messages)
    return "Validation error: %s" % error_msg


def validate_params(schema, params):
        assert isinstance(params, dict)

        validator = jsonschema.Draft4Validator(schema)
        if not validator.is_valid(params):
            errors = sorted(validator.iter_errors(params),
                            key=lambda e: e.path)
            error_msg = format_validation_msg(errors)
            LOG.info(error_msg)
            raise exception.ValidationException(error_msg)
