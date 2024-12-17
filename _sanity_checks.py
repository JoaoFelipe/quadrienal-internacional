"""
Sanity checks for assumptions that we are taking when working with the data
"""

# 1 - Author Name uniquely identifies authors 
# DBLP uses numbers like 0001 to distinguish authors with the same name

import json
with open("output/dblp_map.json", "r") as f:
    pid_map = json.load(f)

authors = set()
for i, (pid, author) in enumerate(pid_map.items()):
    if i % 100000 == 0:
        print(i)
    current = set(author.get('author', set()))
    if current & authors:
        print("1. WARNING: author with multiple pids", current & authors)
    authors |= current

