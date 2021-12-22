# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import g

from flask_resources import (
    Resource,
    response_handler,
    route,
    resource_requestctx,
)

from storm_commons.resources.parsers import (
    request_data,
    request_view_args,
    request_read_args,
    request_search_args,
)

from invenio_records_resources.resources.errors import ErrorHandlersMixin


class DepositManagementResource(ErrorHandlersMixin, Resource):
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
            route("GET", routes["list-item"], self.search),
            route("PUT", routes["update-item"], self.update),
            route("DELETE", routes["delete-item"], self.delete),
            # Deposit actions
            route("POST", routes["start-deposit-action"], self.start_deposit_job),
            # Services operations
            route("GET", routes["list-service"], self.list_plugin_services),
        ]

    @request_data
    @request_view_args
    @response_handler(many=True)
    def create(self):
        """Create a new deposit."""
        item = self.service.create(
            g.identity,
            resource_requestctx.data or {},
        )
        return item.to_dict(), 201

    @request_read_args
    @request_view_args
    @response_handler()
    def read(self):
        """Read an item."""
        item = self.service.read(
            g.identity,
            resource_requestctx.view_args["deposit_id"],
        )
        return item.to_dict(), 200

    @request_data
    @request_view_args
    @response_handler()
    def update(self):
        """Update an item."""
        item = self.service.update(
            g.identity,
            resource_requestctx.view_args["deposit_id"],
            resource_requestctx.data or {},
        )
        return item.to_dict(), 200

    @request_view_args
    def delete(self):
        """Delete an item."""
        self.service.delete(g.identity, resource_requestctx.view_args["deposit_id"])
        return "", 204

    @request_search_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over the items."""
        items = self.service.search(g.identity, resource_requestctx.args)
        return items.to_dict(), 200

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

        return item.to_dict(), 202
