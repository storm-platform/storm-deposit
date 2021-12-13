# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from invenio_db import db

from storm_commons.services.service import PluginService
from invenio_records_resources.services import ServiceSchemaWrapper


class DepositManagementService(PluginService):
    def _validate(self, service, obj, identity, raise_errors):
        """Validate a object based on a schema service."""
        return service.load(
            obj, context={"identity": identity}, raise_errors=raise_errors
        )

    def _create(self, record_cls, identity, data):
        """Create a deposit operation."""
        self.require_permission(identity, "create")

        # Validate the deposit record metadata
        # `metadata` is a field that allow custom fields definition.
        self._validate(self.schema, py_.omit(data, "metadata"), identity, True)

        # Reading the selected `service id`
        service_id = data.get("service")

        # Validate custom metadata fields
        metadata = data.get("metadata", {})

        if metadata:
            service = self.plugin_manager.service(service_id)
            if service.schema:
                service_schema = ServiceSchemaWrapper(self, schema=service.schema)

                self._validate(service_schema, metadata, identity, True)

        # It's the components who saves the actual data in the record.
        record = record_cls.create()

        # Run components
        for component in self.components:
            if hasattr(component, "create"):
                component.create(identity, record=record, data=data, service=service_id)

        # Saving the data
        db.session.commit()

        return record

    def start_deposit_job(self, identity, id_, data):
        """Start the deposit job task."""
        # Resolve and require permission
        record = self.record_cls.get_record(id=id_)
        self.require_permission(identity, "deposit", record=record)

        # Selecting the service
        deposit_plugin_service = self._plugin_manager.service(record.service)

        # Run components
        for component in self.components:
            if hasattr(component, "start_deposit"):
                component.start_deposit(identity, record=record, data=data)

        # Saving the data
        db.session.commit()

        # Running!
        deposit_plugin_service.service.delay(id_, data)

        return record
