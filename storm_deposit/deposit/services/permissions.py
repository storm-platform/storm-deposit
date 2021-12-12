# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.security import BaseRecordPermissionPolicy


class DepositPermissionPolicy(BaseRecordPermissionPolicy):
    """Permissions for the deposit records."""

    can_deposit = BaseRecordPermissionPolicy.can_use


__all__ = "DepositRecordPermissionPolicy"
