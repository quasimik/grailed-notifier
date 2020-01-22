import json
import boto3
import sys

client = boto3.client('ses')

with open('email.txt', 'r') as file:
  email = file.readline()

with open('new_items.json', 'r') as file:
  items = json.load(file)

if len(items) == 0:
  sys.exit()

html_items = ''
for item in items:
  html_items += '''
<li>[Size {item_size} &mdash; {item_price}] <a href="{item_url}" class="item">{item_title}</a></li>
'''.format(item_url=item['url'], item_title=item['title'], item_size=item['size'], item_price=item['price'])

html_string = '''
<!DOCTYPE html>
<html>
<head>
<style>

.container {
  width: 600px;
}

</style>
</head>
<body>
  <div class="container">
''' + html_items + '''
  </div>
</body>
</html>
'''

client.send_email(
  Source=email,
  Destination={
    'ToAddresses': [email]
  },
  Message={
    'Subject': {
      'Data': '[Grailed Notifier] ' + str(len(items)) + ' New Items Posted',
      'Charset': 'UTF-8'
    },
    'Body': {
      'Html': {
        'Data': html_string,
        'Charset': 'UTF-8'
      }
    }
  }
)
