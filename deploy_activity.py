#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import yaml
import json
import sys
import codecs

def remove_tests(data):
    
    tests = data['tests']
    tests = {'tests' : tests}

    # salva todos em tests.json
    f = codecs.open('tests.json', 'w', 'utf-8')
    json.dump(tests, f)
    f.close()

    print('see tests.json')

    # troca todos pelos públicos
    pubs = {'tests' : []}
    tests = data['tests']
    
    for test in tests:
        if 'category' in test and test['category'] == 'public':
            pubs['tests'].append(test)
    
    data['tests'] = pubs['tests']
    return pubs

def to_unicode(obj, encoding='utf-8'):
  assert isinstance(obj, basestring), type(obj)
  if isinstance(obj, unicode):
    return obj

  for encoding in ['utf-8', 'latin1']:
    try:
      obj = unicode(obj, encoding)
      return obj
    except UnicodeDecodeError:
      pass

  print("tst: unrecognized text encoding", file=sys.stderr)
  exit()


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'email'):
        return obj.email()

    return obj


if len(sys.argv) > 1:
    yaml_text = to_unicode(open(sys.argv[1], "r").read())
else:
    yaml_text = to_unicode(unicode(sys.stdin.read().decode('utf-8')))

ac_name = sys.argv[1].split('.yaml')[0]

data = yaml.load(yaml_text)
pubs = remove_tests(data)

json_text = json.dumps(
    data,
    default=date_handler,
    indent=2,
    separators=(',', ': '),
    ensure_ascii=False
)

with open(ac_name+'.json', 'w') as ac_data:
    print('see ' + ac_name + '.json')
    json.dump(json_text.encode('utf-8'), ac_data, encoding='utf-8', ensure_ascii=False)

with open('tst.json', 'w') as tst_file:
    json.dump(pubs, tst_file, encoding='utf-8', ensure_ascii=False)
    print('see tst.json')
