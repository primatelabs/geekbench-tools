#!/usr/bin/env python

#	 geekbench-parse.py - Parses and displays a .geekbench file

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

import geekbench
import sys
import urllib2

def skip_workload(workload):
  if workload.id in [205, 206]:
    return True
  return False

def main():
  xml = urllib2.urlopen('%s.geekbench' % (sys.argv[1],)).read()
  document = geekbench.parse_document(xml)
  
  for section in document.sections:
    scores = []
    for workload in section.workloads:
      if skip_workload(workload):
        continue
      for result in workload.results:
        scores.append(result.score)
    print scores
    section.score = sum(scores) / len(scores)

  weights = {
    1: 0.35,
    2: 0.35,
    3: 0.20,
    4: 0.10
  }
  document.score = 0
  for section in document.sections:
    document.score += int(section.score * weights[section.id])

  # Display system information by iterating through the system information
  # metrics.

  for metric in document.metrics:
    print '  %-25s %s' % (metric.name, metric.value)
  print '\n'
  
  # Iterate through the sections in this document.
  for section in document.sections:
    print '%s Performance' % (section.name,)
    
    # Iterate through the workloads in this section.
    for workload in section.workloads:
      if skip_workload(workload):
        continue
      print '  ', workload.name
      
      # Iterate through the individual results in this workload.
      for result in workload.results:
        print '    ',

        # Display whether the workload was run in single-threaded or 
        # multi-threaded mode.
        if result.threads == 1:
          print 'single-threaded',
        else:
          print 'multi-threaded',

        # Display whether the workload contains scalar or vector 
        # (i.e., SIMDized) code.
        if result.simd == 0:
          print 'scalar',
        else:
          print 'vector',
          
        print result.score
    print '\n',
    
  # Display the overall score.
  print 'Geekbench 2 Score: ', document.score
        
if __name__ == '__main__':
  main()
