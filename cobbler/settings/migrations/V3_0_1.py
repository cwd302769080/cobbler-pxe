"""
Migration from V3.0.0 to V3.0.1
"""
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2021 Dominik Gedon <dgedon@suse.de>
# SPDX-FileCopyrightText: 2021 Enno Gotthold <egotthold@suse.de>
# SPDX-FileCopyrightText: Copyright SUSE LLC
import re

from schema import SchemaError
from cobbler.settings.migrations import V3_0_0

# schema identical to V3_0_0
schema = V3_0_0.schema


def validate(settings: dict) -> bool:
    """
    Checks that a given settings dict is valid according to the reference schema ``schema``.

    :param settings: The settings dict to validate.
    :return: True if valid settings dict otherwise False.
    """
    try:
        schema.validate(settings)
    except SchemaError:
        return False
    return True


def normalize(settings: dict) -> dict:
    """
    If data in ``settings`` is valid the validated data is returned.

    :param settings: The settings dict to validate.
    :return: The validated dict.
    """
    return schema.validate(settings)


def migrate(settings: dict) -> dict:
    """
    Migration of the settings ``settings`` to the V3.0.1 settings

    :param settings: The settings dict to migrate
    :return: The migrated dict
    """
    modules_conf_path = "/etc/cobbler/modules.conf"
    with open(modules_conf_path, "r") as modules_conf_file:
        modules_conf = modules_conf_file.readlines()

    for line in modules_conf:
        if re.match("authn_", line) is not None:
            # sed -i -e 's/authn_/authentication\./g' $path_modules_conf
            pass
        if re.match("authz_", line) is not None:
            # sed -i -e 's/authz_/authorization\./g' $path_modules_conf
            pass
        if re.match("manage_", line) is not None:
            # sed -i -e 's/manage_/managers\./g' $path_modules_conf
            pass

    with open(modules_conf_path, "w") as modules_conf_file:
        for line in modules_conf:
            modules_conf_file.write(line)

    if not validate(settings):
        raise SchemaError("V3.0.1: Schema error while validating")
    return normalize(settings)
