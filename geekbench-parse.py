#!/usr/bin/env python

#	 geekbench-parse.py - Parses and displays a .geekbench file

#  Copyright (c) 2006-2010 Primate Labs

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

def main():
  document = geekbench.parse_document(open(sys.argv[1], 'rt').read())  
  
  # Display system information by iterating through the system information
  # metrics.
  
  for metric in document.metrics:
    print '  %-25s %s' % (metric.name, metric.value)
  print '\n'
  
  # Iterate through the sections in this document.
  for section in document.sections:
    print '%s Performance' % (section.name,)
    
    # Iterate through the benchmarks in this section.
    for benchmark in section.benchmarks:
      print '  ', benchmark.name
      
      # Iterate through the individual results in this benchmark.
      for result in benchmark.results:
        print '    ',

        # Display whether the benchmark was run in single-threaded or 
        # multi-threaded mode.
        if result.threads == 1:
          print 'single-threaded',
        else:
          print 'multi-threaded',

        # Display whether the benchmark contains scalar or vector 
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
