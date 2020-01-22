import json
import os.path

if os.path.exists('records.json'):
  with open('records.json', 'r') as file:
    records = json.load(file)
else:
  records = []

with open('query_ids.json', 'r') as file:
  query_ids = json.load(file)

record_urls = set([record['url'] for record in records])

new_items = []

for query_id in query_ids:
  with open('out/out-' + query_id + '.json', 'r') as file:
    query = json.load(file)
  for item in query['items']:
    if item['url'] not in record_urls:
      new_items.append(item)
      records.append(item)

# update records
with open('records.json', 'w') as file:
  json.dump(records, file)

with open('new_items.json', 'w') as file:
  json.dump(list(new_items), file)
