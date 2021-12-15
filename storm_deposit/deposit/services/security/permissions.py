# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_permissions.generators import SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy
from storm_deposit.deposit.services.security.generators import ProjectDepositCreator
from storm_project.project.services.security.generators.context import UserInProject


class DepositPermissionPolicy(RecordPermissionPolicy):
    """Permissions for the deposit records."""

    #
    # High-level permissions
    #

    # Content creators and managers
    can_manage = [ProjectDepositCreator(), SystemProcess()]

    # General users
    can_use = can_manage + [UserInProject()]

    #
    # Low-level permissions
    #
    can_read = can_use

    can_create = can_manage

    can_update = can_manage

    can_delete = can_manage

    can_search = can_use

    can_deposit = can_manage


__all__ = "DepositRecordPermissionPolicy"
