# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_permissions.generators import SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from storm_project.project.services.security.generators import ProjectRecordUser
from storm_deposit.deposit.services.security.generators import DepositTaskRecordOwner


class DepositTaskPermissionPolicy(RecordPermissionPolicy):
    """Permissions for the deposit records."""

    #
    # High-level permissions
    #

    # Content creators and managers
    can_manage = [DepositTaskRecordOwner(), SystemProcess()]

    # General users
    can_use = can_manage + [ProjectRecordUser()]

    #
    # Low-level permissions
    #
    can_read = can_use
    can_create = can_use
    can_search = can_use

    can_update = can_manage
    can_delete = can_manage

    can_deposit = [ProjectRecordUser(only_owners=True)]


__all__ = "DepositTaskPermissionPolicy"
