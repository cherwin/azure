#!/usr/bin/env python

import argparse
import re
import time
import os 
import sys

from collections import namedtuple
from pprint import pprint
from halo import Halo

from azdo import AzDo


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('project', help='The project name')
	parser.add_argument('team', help='The team name')
	args = parser.parse_args()

	azdo = AzDo()

	work_items = azdo.get_backlog_features(
		args.project,
		args.team,
		sorted_by_priority=True,
	)

	Title = namedtuple("Title", ["id", "current", "new"])
	titles = []

	for count, w in enumerate(work_items, 1):
		title_current = w.fields["System.Title"]
		title_clean = (re.sub('^\d+\. ', '', title_current))
		title_new = str(count) + f". {title_clean}"

		titles.append(Title(w.id, title_current, title_new))

	filtered = list(filter(lambda x: x.new != x.current, titles))

	spinner = Halo(text='Press CTRL-C to cancel', spinner='dots2')
	for title in filtered:
		spinner.info(f"{title.current} -> {title.new}")

	if os.environ.get("AZDO_DESTRUCTIVE") and len(filtered) > 0:
		try:
			seconds = 8
			spinner.start()
			time.sleep(seconds)
		except KeyboardInterrupt:
			spinner.fail("Interrupted")
			sys.exit(1)

		for title in filtered:
			spinner.warn(f"{title.current} -> {title.new}")
			w = azdo.update_work_item_title(title.id, title.new)

			if os.environ.get("AZDO_VERBOSIVE"):
				pprint(w.as_dict())
		
		spinner.succeed("Updated all work items")


