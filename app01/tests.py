from django.test import TestCase

# Create your tests here.

import requests
data = requests.get("https://www.baidu.com")
print(data.text)