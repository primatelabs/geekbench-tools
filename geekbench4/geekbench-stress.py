#!/usr/bin/env python

#  Copyright (c) 2006-2018 Primate Labs Inc.

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

import argparse
import csv
import re
import subprocess
import time

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--runtime", type=int, default=600, help="runtime")
  parser.add_argument("--output", default='geekbench-stress.csv', help="output filename")
  parser.add_argument("--geekbench", default='/Applications/Geekbench\ 4.app/Contents/Resources/geekbench_x86_64', help="Geekbench executable path")
  args = parser.parse_args()

  start = time.time()

  cmdline = '%s --multi-core --workload-gap 0; exit 0' % (args.geekbench,)
  results = []
  while True:
    output = subprocess.check_output(cmdline, shell=True)
    match = re.search('Multi-Core Score\s+(\d+)', output)
    now = time.time() - start
    score = int(match.group(1))
    print [now, score]
    results.append([now, score])
    if now > args.runtime:
      break

  print results

  with open(args.output, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for result in results:
      writer.writerow(result)

if __name__ == "__main__":
  main()