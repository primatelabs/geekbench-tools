#!/usr/bin/env python

#	 single-core.py - Parses and displays a .geekbench file

#  Copyright (c) 2006-2012 Primate Labs Inc.

#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import re, sys, urllib
import geekbench

def main():
  if len(sys.argv) < 2:
    print 'Usage: %s [url]' % (sys.argv[0])
    exit(-1)
  
  url_match = re.match('^(.*)\/view\/(\d+)$', sys.argv[1])
  if url_match is None:
    print 'Error: Bad URL argument. Exiting.'
    exit(-1)
  
  url = '%s/show/%s.geekbench' % (url_match.group(1), url_match.group(2))  
  data = urllib.urlopen(url).read()
  document = geekbench.parse_document(data)
  
  sections = ['Integer', 'Floating Point', 'Memory', 'Stream']
  section_weights = { 'Integer' : 0.35, 'Floating Point' : 0.35, 'Memory' : 0.2, 'Stream' : 0.1 }
  section_scores = {}
  
  # Iterate through the sections in this document.
  for section in document.sections:
    scores = []
    for workload in section.workloads:
      for result in workload.results:
        if result.threads == 1:
          scores.append(int(result.score))
    section_scores[section.name] = sum(scores, 0) / len(scores)

  geekbench_score = 0
  for section in sections:
    section_title = '%s Performance:' % (section,)
    print '%-30s %5d' % (section_title, section_scores[section])
    geekbench_score += section_weights[section] * section_scores[section]
  print '\nGeekbench Score:               %5d' % (int(geekbench_score),)

if __name__ == '__main__':
  main()
