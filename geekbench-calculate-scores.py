#!/usr/bin/env python

#  Copyright (c) 2006-2015 Primate Labs Inc.

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

import json
import sys
import math

baseline_rate = {"AES" : 2297304827.712579, "Twofish" : 147104771.2752039,
"SHA1" : 284535727.5317147, "SHA2" : 113421232.21088956,
"BZip2 Compress" : 10655380.829907415,
"BZip2 Decompress" : 14207477.374253012,
"JPEG Compress" :  34828193.30901489,
"JPEG Decompress" : 61799226.229028925, "PNG Compress" : 1995970.1507709173,
"PNG Decompress" : 28823191.43475692,
"Sobel" : 90973382.70326369, "Lua" : 2355476.4774805442,
"Dijkstra" : 8971474.748035867, "BlackScholes" : 11124707.579848604,
"Mandelbrot" : 2561771045.08415, "Sharpen Filter" :  1852822632.527193,
"Blur Filter" : 2382099498.994065,  "SGEMM" : 7001462936.999326,
"DGEMM" : 3673032244.756834 , "SFFT" : 2635951419.4330635,
"DFFT" : 2276728468.11824, "N-Body" : 927967.5877615509,
"Ray Trace" : 2947755.511608884, "Stream Copy" : 10709056870.933207,
"Stream Scale" : 10717018032.487293, "Stream Add" :  12138602680.677034,
"Stream Triad" : 11796840626.258623 }

class Workload(object):
  def __init__(self, jsonf):
    self.name = jsonf['name']
    self.sc_runtime = 0
    self.sc_work = 0
    self.mc_runtime = 0
    self.mc_work = 0

    for result in jsonf['results']:
      if result['threads'] == 1:
        self.sc_runtime = result['runtime']
        self.sc_work = result['work']
      elif result['threads'] > 1:
        self.mc_runtime = result['runtime']
        self.mc_work = result['work']
      else:
        raise ValueError("Result had zero worker threads for {}".format(name))

  def sc_rate(self):
    if self.sc_runtime > 0:
      return self.sc_work / self.sc_runtime
    return 0

  def mc_rate(self):
    if self.mc_runtime > 0:
      return self.mc_work / self.mc_runtime
    return 0

  def wl_sc_score(self):
    rel = self.sc_rate() / baseline_rate[self.name]
    return int(2500 * rel)

  def wl_mc_score(self):
    rel = self.mc_rate() / baseline_rate[self.name]
    return int(2500 * rel)

def get_sections(jsondata):
  sections = {}
  ss = jsondata['sections']
  for s in ss:
    wls = s['workloads']
    section_name = s['name']
    section = []
    for wl in wls:
      section.append(Workload(wl))
    sections[section_name] = section
  return sections

def geomean(scores):
  score_total = 1
  for score in scores:
    score_total *= score
  nth_root = 1 / float(len(scores))
  return int(math.pow(score_total, nth_root))

def compute_sect_sc_score(section):
  scores = [wl.wl_sc_score() for wl in section]
  return geomean(scores)

def compute_sect_mc_score(section):
  scores = [wl.wl_mc_score() for wl in section]
  return geomean(scores)

def compute_geekbench_sc_score(sections):
  geekbench_score = 0
  try:
    geekbench_score = (0.4 * compute_sect_sc_score(sections['Integer'])) + \
    (0.4 * compute_sect_sc_score(sections['Floating Point'])) + \
    (0.2 * compute_sect_sc_score(sections['Memory']))
  except KeyError:
    pass
  return int(geekbench_score)

def compute_geekbench_mc_score(sections):
  geekbench_score = 0
  try:
    geekbench_score = (0.4 * compute_sect_mc_score(sections['Integer'])) + \
    (0.4 * compute_sect_mc_score(sections['Floating Point']))  + \
    (0.2 * compute_sect_mc_score(sections['Memory']))
  except KeyError:
    pass
  return int(geekbench_score)

def get_rate_string(wl_name, rate):

  rate_units = { "BytesSecond" : "B/sec", "Flops" : "flops",
  "AllocSecond" : "allocs/second", "PixelsSecond" : "pixels/sec",
  "NodesSecond" : "nodes/sec", "PairsSecond" : "pairs/sec"}

  wl_units = {"AES" : rate_units['BytesSecond'],
  "Twofish" : rate_units['BytesSecond'], "SHA1" : rate_units['BytesSecond'],
  "SHA2" : rate_units['BytesSecond'],
  "BZip2 Compress" : rate_units['BytesSecond'],
  "BZip2 Decompress" : rate_units['BytesSecond'],
  "JPEG Compress" :  rate_units['PixelsSecond'],
  "JPEG Decompress" : rate_units['PixelsSecond'],
  "PNG Compress" : rate_units['PixelsSecond'],
  "PNG Decompress" : rate_units['PixelsSecond'],
  "Sobel" : rate_units['PixelsSecond'],
  "Lua" : rate_units['BytesSecond'] ,
  "Dijkstra" : rate_units['PairsSecond'],
  "BlackScholes" : rate_units['NodesSecond'],
  "Mandelbrot" : rate_units['Flops'],
  "Sharpen Filter" :   rate_units['Flops'],
  "Blur Filter" :  rate_units['Flops'],
  "SGEMM" : rate_units['Flops'], "DGEMM" :  rate_units['Flops'],
  "SFFT" : rate_units['Flops'], "DFFT" :  rate_units['Flops'],
  "N-Body" : rate_units['PairsSecond'],
  "Ray Trace" : rate_units['PixelsSecond'],
  "Stream Copy" : rate_units['BytesSecond'],
  "Stream Scale" : rate_units['BytesSecond'],
  "Stream Add" :  rate_units['BytesSecond'],
  "Stream Triad" : rate_units['BytesSecond'] }

  prefixes = ["", "K", "M", "G", "T"]

  wl_unit = wl_units[wl_name]
  divisor = 1000.0

  if (wl_unit == "B/sec"):
    divisor = 1024.0

  for prefix in range(0,4):
    if rate < divisor:
      break
    rate /= divisor  

  if rate > 10.0:
    rate = round(rate, 1)
  else:
    rate = round(rate, 2)

  return "%s %s%s" % (rate, prefixes[prefix], wl_unit)

def main():
  jsonfile = open(sys.argv[1])
  jsonobj = json.load(jsonfile)

  sections = get_sections(jsonobj)
  gb_sc_score = compute_geekbench_sc_score(sections)
  gb_mc_score = compute_geekbench_mc_score(sections)


  for (section, wls) in sections.iteritems():
    print section
    for wl in wls:
      print "\t%s".expandtabs(2) % wl.name

      wl_sc_score_str = str(int(wl.wl_sc_score())).rjust(12)
      sc_rate_str = get_rate_string(wl.name, wl.sc_rate()).rjust(21)
      print "\tsingle-core%s%s".expandtabs(4) % (wl_sc_score_str, sc_rate_str)

      wl_mc_score_str = str(int(wl.wl_mc_score())).rjust(13)
      mc_rate_str = get_rate_string(wl.name, wl.mc_rate()).rjust(21)
      print "\tmulti-core%s%s".expandtabs(4) % (wl_mc_score_str , mc_rate_str)
    print ""

  print "Benchmark Summary"
  for section in sections.iterkeys():
    section_score_str = str(section + " Score").ljust(24)
    sect_sc_score_str = str(compute_sect_sc_score(sections[section])).rjust(7)
    sect_mc_score_str = str(compute_sect_mc_score(sections[section])).rjust(7)
    print "\t%s%s%s".expandtabs(2) % (section_score_str, sect_sc_score_str, 
    sect_mc_score_str)
  print ""

  gb_sc_score_just = str(gb_sc_score).rjust(7)
  gb_mc_score_just = str(gb_mc_score).rjust(7)

  print "\t%s%s%s".expandtabs(2) % ("Geekbench Score".ljust(24),
  gb_sc_score_just, gb_mc_score_just)
  jsonfile.close()

if __name__ == "__main__":
  main()



