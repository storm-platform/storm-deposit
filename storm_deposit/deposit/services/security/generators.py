# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_project.project.records.systemfields.access import ProjectAgent
from storm_project.project.services.security.generators import ProjectRecordAgent


class DepositTaskRecordOwner(ProjectRecordAgent):
    """Generator to define a deposit owner.

    Note:
        A ``Deposit owner`` should be a valid project user.
    """

    def _select_record_agent(self, record, **kwargs):

        # special case: to define a deposit owner, we will
        # use the associated project informations:
        user_agent = ProjectAgent(dict(user=record.user.id))
        project_agent = ProjectAgent(dict(project=record.project.id))

        return [project_agent], [user_agent]
