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
    print 'Usage: %s [filename]' % (sys.argv[0])
    exit(-1)
  
  document = geekbench.parse_document(open(sys.argv[1]).read())
  
  singlecore_scores = []
  multicore_scores = []
  
  # Iterate through the sections in this document.
  for section in document.sections:

    # Since we're calculating the processors's single-core and multi-core
    # performance, only gather scores from the integer and floating point
    # sections (and skip the memory sections).
    if section.id not in ['1', '2']:
      continue

    for workload in section.workloads:
      for result in workload.results:
        if result.threads == 1:
          singlecore_scores.append(int(result.score))
        else:
          multicore_scores.append(int(result.score))

  print 'Geekbench Score:   %7d' % (int(document.score), )
  print 'Single-Core Score: %7d' % (sum(singlecore_scores, 0) / len(singlecore_scores), )
  print 'Multi-Core Score:  %7d' % (sum(multicore_scores, 0) / len(multicore_scores), )

if __name__ == '__main__':
  main()
