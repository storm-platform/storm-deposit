# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.services.components import (
    UserComponent,
    RecordServiceComponent,
    SoftDeleteComponent,
)
from storm_commons.services.pagination import BaseSearchOptions
from storm_commons.services.results import BaseListResult, BaseItemResult
from storm_project.project.services.links import (
    ProjectContextLink,
    project_context_pagination_links,
)

from storm_deposit.deposit.models.api import Deposit
from storm_deposit.deposit.schema import DepositObjectSchema
from storm_deposit.deposit.services.components import (
    ProjectComponent,
    PipelineComponent,
    DepositComponent,
)
from storm_deposit.deposit.services.security.permissions import (
    DepositPermissionPolicy,
)


class DepositManagementServiceConfig:
    """Deposit management service configuration."""

    result_item_cls = BaseItemResult
    result_list_cls = BaseListResult

    #
    # Common configurations
    #
    permission_policy_cls = DepositPermissionPolicy

    #
    # Record configuration
    #
    record_cls = Deposit

    schema = DepositObjectSchema

    #
    # Components
    #
    components = [
        # Contextual components
        ProjectComponent,
        UserComponent,
        PipelineComponent,
        # Deposit components
        RecordServiceComponent,
        DepositComponent,
        SoftDeleteComponent,
    ]

    links_item = {
        "self": ProjectContextLink("{+api}/projects/{project_id}/deposits/{id}")
    }
    links_search = project_context_pagination_links(
        "{+api}/projects/{project_id}/deposits{?args*}"
    )

    # Search configuration
    search = BaseSearchOptions
