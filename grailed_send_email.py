import json
import boto3

client = boto3.client('ses')

with open('email.txt', 'r') as file:
  email = file.readline()

with open('new_items.json', 'r') as file:
  items = json.load(file)

html_items = ''
for item in items:
  html_items += '''
<a href="{item_url}" class="item">
  <img src="{img_url}">
  <p>{item_title}</p>
  <p>Size {item_size} &mdash; {item_price}</p>
</a>
'''.format(item_url=item['url'], img_url=item['img_url'], item_title=item['title'], item_size=item['size'], item_price=item['price'])

html_string = '''
<!DOCTYPE html>
<html>
<head>
<style>

.container {
  display: flex;
  flex-flow: row wrap;
}

.item {
  border: 1px solid black;
  margin: 20px;
  padding: 10px;
  display: flex;
  flex-flow: column nowrap;
  width: 240px;
}

img {
  height: 320px;
  width: 240px;
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
      'Data': '[Grailed Notifier] New Items Posted',
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
