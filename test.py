import re

text = '网游：我有超神级天赋完整版在线免费阅读_网游：我有超神级天赋小说_番茄小说官网'
a = re.search(r'_(.*?)小说_', text).group(1)
print(a)