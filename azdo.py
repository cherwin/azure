#!/usr/bin/env python

import os

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.work.models import TeamContext
from azure.devops.v7_0.work_item_tracking.models import WorkItemBatchGetRequest
from azure.devops.v7_0.work_item_tracking.models import JsonPatchOperation


AZDO_ORG_URL = os.environ.get('AZDO_ORG_URL')
AZDO_TOKEN = os.environ.get('AZDO_TOKEN')


class AzDo:
	def __init__(self, token=AZDO_TOKEN, org_url=AZDO_ORG_URL):
		self._token = token
		self._org_url = org_url	

		self._work_client = None
		self._work_item_tracking_client = None

	@staticmethod
	def sort_work_items_by_backlog_priority(work_items):
		return sorted(work_items, key=lambda x: x.fields["Microsoft.VSTS.Common.BacklogPriority"])

	@staticmethod
	def get_connection(org_url, token):
		creds = BasicAuthentication('', token)
		conn = Connection(base_url=org_url, creds=creds)
		return conn

	def set_clients(self):
		conn = self.get_connection(self._org_url, self._token)
		self._work_client = conn.clients.get_work_client()
		self._work_item_tracking_client = conn.clients.get_work_item_tracking_client()

	def get_backlog_features(self, project, team, sorted_by_priority=False):
		if not self._work_client or not self._work_tracking_client:
			self.set_clients()

		team_context = TeamContext(project=project, team=team)
		features = self._work_client.get_backlog_level_work_items(
			team_context,
			"Microsoft.FeatureCategory"
		)

		ids = [i.target.id for i in features.work_items]

		fields = [
				"System.Title",
				"Microsoft.VSTS.Common.BacklogPriority",
		]
		# return all fields for now
		fields = []

		req = WorkItemBatchGetRequest(fields=fields, ids=ids)
		work_items = self._work_item_tracking_client.get_work_items_batch(req)

		if sorted_by_priority:
			return self.sort_work_items_by_backlog_priority(work_items)

		return work_items

	def update_work_item_title(self, work_item_id, new_title):
		if not self._work_item_tracking_client:
			self.set_clients()

		document = [
			JsonPatchOperation(
				op="add",
				path="/fields/System.Title",
				value=new_title,
			),
		]
		work_item = self._work_item_tracking_client.update_work_item(document, work_item_id)

		return work_item


