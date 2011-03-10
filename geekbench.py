#!/usr/bin/env python

#	 geekbench.py - Library for parsing .geekbench files

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

import xml.dom.minidom

def get_text(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc = rc + node.data
  return rc

class Document:
  def __init__(self):
    self.metrics = []
    self.sections = []
    self.score = None
    self.elapsed = None

  def get_metric(self, name):
    for metric in self.metrics:
      if metric.name.lower() == name.lower():
        return metric.value
    return None
    
  def get_benchmark(self, id):
    for section in self.sections:
      for benchmark in section.benchmarks:
        if benchmark.id == id:
          return benchmark
    return None
    
  def get_result(self, id, threads, simd):
    for section in self.sections:
      for benchmark in section.benchmarks:
        if benchmark.id == id:
          for result in benchmark.results:
            if result.threads == threads and result.simd == simd:
              return result
    return None

class Score:
  def __init__(self):
    self.value = None

class Elapsed:
  def __init__(self):
    self.value = None
    
class Metric:
  def __init__(self):
    self.name = None
    self.id = None
    self.value = None
    
class Section:
  def __init__(self):
    self.benchmarks = []
    self.name = None
    self.score = None
    self.id = None
    
class Benchmark:
  def __init__(self):
    self.results = []
    self.name = None
    self.id = None
    self.units = None
    self.inverse = None

class Result:
  def __init__(self):
    self.threads = None
    self.simd = None
    self.result = None
    self.rate = None
    self.score = None
    self.comment = None

def _parseAttributes(node, docNode):
  for i in range(0, node.attributes.length):
    attribute = node.attributes.item(i)
    setattr(docNode, attribute.name, attribute.value)
  return docNode

def _parseResult(node_result):
  result = _parseAttributes(node_result, Result())
  # TODO: Find a way for _parseAttributes to automatically determine the correct
  # type for .threads and .simd (and for other fields as well).
  result.threads = int(result.threads)
  result.simd = int(result.simd)
  return result

def _parseBenchmark(benchmark):
  docBenchmark = _parseAttributes(benchmark, Benchmark())
  for result in benchmark.getElementsByTagName('result'):
    docBenchmark.results.append(_parseResult(result)) 
  return docBenchmark

def _parseSection(section):
  docSection = _parseAttributes(section, Section())  
  docSection.score = int(get_text(section.getElementsByTagName('score')[0].childNodes))
  for benchmark in section.getElementsByTagName('benchmark'):
    docSection.benchmarks.append(_parseBenchmark(benchmark))
  return docSection
  
def _parseMetric(metric):
  return _parseAttributes(metric, Metric())
  
def _parseScore(score):
  return _parseAttributes(score, Score())
  
def _parseElapsed(elapsed):
  return _parseAttributes(elapsed, Elapsed())
    
def parse_document(xmlString):
  document = xml.dom.minidom.parseString(xmlString)

  geekbench = document.getElementsByTagName('geekbench')[0]
  docGeekbench = _parseAttributes(geekbench, Document()) 

  docGeekbench.score = int(get_text(geekbench.getElementsByTagName('score')[0].childNodes))
  if len(geekbench.getElementsByTagName('elapsed')) > 0:
    docGeekbench.elapsed = float(get_text(geekbench.getElementsByTagName('elapsed')[0].childNodes))

  metrics = geekbench.getElementsByTagName('metric')
  for metric in metrics:
    docGeekbench.metrics.append(_parseMetric(metric))
  
  sections = geekbench.getElementsByTagName('section')
  for section in sections:
    docGeekbench.sections.append(_parseSection(section)) 
  
  return docGeekbench
