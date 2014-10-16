#!/usr/bin/env ruby

# Copyright (c) 2006-2014 Primate Labs Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

require 'csv'
require 'json'

if ARGV.length() != 2
  puts "Usage: #{$0} DOCUMENT CSV"
  exit
end

json = File.open(ARGV[0], 'r').read()
document = JSON.parse(json)

CSV.open(ARGV[1], 'w') do |csv|
  csv << ["timestamp",
          "battery_level",
          "iterations",
          "runtime_mean",
          "runtime_stddev"]
  for result in document['results']
    csv << [result["timestamp"],
            result["battery_level"],
            result["iterations"],
            result["runtime_mean"],
            result["runtime_stddev"]]
  end
end
