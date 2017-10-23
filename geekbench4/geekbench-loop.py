#!/usr/bin/env python

#  Copyright (c) 2006-2017 Primate Labs Inc.

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
import json
import subprocess
import sys
import math
import csv
import numpy

from collections import defaultdict

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--iterations", type=int, default=10, help="number of iterations to execute")
  parser.add_argument("--output", default='geekbench-loop.csv', help="output filename")
  parser.add_argument("--geekbench", default='geekbench4', help="Geekbench executable path")
  args = parser.parse_args()

  cmdline = [args.geekbench, '--no-upload']
  filenames = []
  for i in range(0, args.iterations):
    filename = '%d.gb4' % (i,)
    filenames.append(filename)

    tmp = list(cmdline)
    tmp.extend(['--save', filename])
    subprocess.call(tmp)

  iterations = []
  scores = defaultdict(list)
  names = {}
  for filename in filenames:
    with open(filename) as geekbench_file:
      result = json.load(geekbench_file)

    iteration = {}

    for section in result['sections']:
      key = '0, %d' % (section['id'],)
      name = section['name']
      names[key] = name
      iteration[key] = section['score']
      scores[key].append(section['score'])
      for workload in section['workloads']:
        key = '%d %d' % (section['id'], workload['id'])
        name = '%s (%s)' % (workload['name'], section['name'])
        names[key] = name
        iteration[key] = workload['score']
        scores[key].append(workload['score'])
    iterations.append(iteration)

  stats = {}
  for key in names.keys():
    s = scores[key]
    stats[key] = [
      numpy.amin(s),
      numpy.amax(s),
      numpy.mean(s),
      numpy.median(s),
      numpy.std(s),
      numpy.std(s) / numpy.mean(s)]

  with open(args.output, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    keys = sorted(names.keys())
    row = ['Iteration']
    for key in keys:
      row.append(names[key])

    writer.writerow(row)

    count = 1
    for iteration in iterations:
      row = [str(count)]
      count += 1
      for key in keys:
        row.append(iteration[key])
      writer.writerow(row)

    writer.writerow([])

    metastats = [[0,"Min"],[1,"Max"],[2,"Mean"],[3,"Median"],[4,"StdDev"],[5,"CoV"]]
    for metastat in metastats:
      row = [metastat[1],]
      for key in keys:
        row.append(stats[key][metastat[0]])
      writer.writerow(row)


if __name__ == "__main__":
  main()
