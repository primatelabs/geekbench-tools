#!/usr/bin/env python

#	 geekbench.py - Library for parsing .geekbench files

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

import xml.dom.minidom


def get_text(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc = rc + node.data
  return rc


class Node:
  def __init__(self):
    pass
    
  def parse(self, xml_node):
    self.parse_attributes(xml_node)
    self.parse_node(xml_node)
    
  def parse_attributes(self, xml_node):
    if xml_node.attributes == None:
      return

    for i in range(0, xml_node.attributes.length):
      attribute = xml_node.attributes.item(i)
      setattr(self, attribute.name, attribute.value)


class Document(Node):
  def __init__(self, xml_node = None):
    self.metrics = []
    self.sections = []
    self.score = None
    self.elapsed = None
    
    if xml_node != None:
      self.parse(xml_node)
    
  def parse_node(self, xml_node):
    self.score = int(get_text(xml_node.getElementsByTagName('score')[0].childNodes))
    if len(xml_node.getElementsByTagName('elapsed')) > 0:
      self.elapsed = float(get_text(xml_node.getElementsByTagName('elapsed')[0].childNodes))

    for xml_metric in xml_node.getElementsByTagName('metric'):
      self.metrics.append(Metric(xml_metric))

    for xml_section in xml_node.getElementsByTagName('section'):
      self.sections.append(Section(xml_section)) 


class Metric(Node):
  def __init__(self, xml_node = None):
    self.name = None
    self.id = None
    self.value = None
    
    if xml_node != None:
      self.parse(xml_node)
  
  def parse_node(self, xml_node):
    self.id = int(self.id)
    self.name = self.lookup_name()

  def lookup_name(self):
    names = {
      1: "Platform",
      2: "Compiler",
      3: "Operating System",
      4: "Model",
      5: "Motherboard",
      6: "CPU Brand",
      7: "CPU ID",
      8: "Threads",
      9: "Processors",
      10: "CPU Frequency",
      11: "CPU L1I",
      12: "CPU L1D",
      13: "CPU L2",
      14: "CPU L3",
      15: "FSB Frequency",
      16: "Memory",
      17: "Memory Type",
      19: "BIOS",
      20: "CPU Name",
      21: "Cores",
      32: "Model ID",
      33: "Build",
      34: "Secure"
    }
    
    if self.id in names:
      return names[self.id]
    
    return ''
    
class Section(Node):
  def __init__(self, xml_node = None):
    self.workloads = []
    self.name = None
    self.score = None
    self.id = None
    
    if xml_node != None:
      self.parse(xml_node)
      
  def parse_node(self, xml_node):
    self.id = int(self.id)
    self.score = int(get_text(xml_node.getElementsByTagName('score')[0].childNodes))
    for xml_workload in xml_node.getElementsByTagName('benchmark'):
      self.workloads.append(Workload(xml_workload))
      
    
class Workload(Node):
  def __init__(self, xml_node = None):
    self.results = []
    self.name = None
    self.id = None
    self.units = None
    self.inverse = None
    
    if xml_node != None:
      self.parse(xml_node)

  def parse_node(self, xml_node):
    self.id = int(self.id)
    for xml_result in xml_node.getElementsByTagName('result'):
      self.results.append(WorkloadResult(xml_result))


class WorkloadResult(Node):
  def __init__(self, xml_node = None):
    self.threads = None
    self.simd = None
    self.result = None
    self.rate = None
    self.score = None
    self.comment = None
    
    if xml_node != None:
      self.parse(xml_node)

  def parse_node(self, xml_node):
    self.threads = int(self.threads)
    self.simd = int(self.simd)
    self.score = int(self.score)


def parse_document(xml_string):
  xml_node = xml.dom.minidom.parseString(xml_string)
  
  return Document(xml_node)
