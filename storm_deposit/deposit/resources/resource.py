# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import g

from storm_commons.resources.parsers import (
    request_data,
    request_view_args,
    request_read_args,
)
from flask_resources import Resource, response_handler, route, resource_requestctx


class DepositManagementResource(Resource):
    """Deposit management resource."""

    def __init__(self, config, service):
        super(DepositManagementResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the deposit resource."""
        routes = self.config.routes
        return [
            # Deposit operations
            route("GET", routes["read-item"], self.read),
            route("POST", routes["create-item"], self.create),
            # Deposit actions
            route("POST", routes["deposit-item"], self.start_deposit_job),
            # Services operations
            route("GET", routes["list-service"], self.list_plugin_services),
        ]

    def _dump(self, records):
        """Dump records to JSON."""

        is_many = type(records) == list
        return self.service.schema.dump(
            records, context={"identity": g.identity}, schema_args={"many": is_many}
        )

    @request_data
    @request_view_args
    @response_handler(many=True)
    def create(self):
        """Create a new deposit."""
        item = self.service.create(
            g.identity,
            resource_requestctx.data or {},
        )

        return self._dump(item), 201

    @request_read_args
    @request_view_args
    @response_handler()
    def read(self):
        """Read an item."""
        item = self.service.read(
            g.identity,
            resource_requestctx.view_args["deposit_id"],
        )
        return self._dump(item), 200

    @response_handler(many=True)
    def list_plugin_services(self):
        """List the available deposit plugin services."""
        return self.service.list_plugin_services(), 200

    @request_data
    @request_view_args
    @response_handler()
    def start_deposit_job(self):
        """Start a deposit job."""
        item = self.service.start_deposit_job(
            g.identity,
            resource_requestctx.view_args["deposit_id"],
            resource_requestctx.data or {},
        )

        return self._dump(item), 202
