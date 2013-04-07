# Copyright (c) 2013 Max Bourinov bourinov@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sublime
import sublime_plugin
import re
import os

#
# This plug-in generates ErlDoc for selected spec
class SpecDocCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				spec = (self.view.substr(region)).replace(os.linesep, '')
				if self.is_spec(spec):
					Result = ''
					Result += self.make_line()
					Result += self.make_spec_line(spec)
					Result += self.make_param_list(spec)
					Result += self.make_doc()
					Result += self.make_line()
					# insert result just above selected spec
					self.view.insert(edit, region.begin(), '\n' + Result)

	def make_spec_line(self, Str):
		R = re.match('^-spec[\w\s\d]*\((.*)\)\s*->\s*(.*)\.', Str)
		H = R.group(1)
		if not H == '':
			P = []
			for chunk in H.split(','):
				Ch1 = re.match('^\s*([\w\d]*)\s*::.*', chunk)
				P.append(Ch1.group(1))
			else:
				Params = ', '.join(P)
				Result = '%% @spec(' + Params + ') -> Result\n'
				return Result
		else:
			Result = '%% @spec() -> Result\n'
			return Result

	def make_param_list(self, Str):
		R = re.match('^-spec[\w\s\d]*\((.*)\)\s*->\s*(.*)\.', Str)
		H = R.group(1)
		if not (H == ''):
			P = []
			for chunk in H.split(','):
				Ch1 = re.match('^\s*([\w\d]*)\s*::\s*(.*)\s*', chunk)
				P.append('%%   ' + Ch1.group(1) + ' = ' + Ch1.group(2))
			else:
				return '\n'.join(P) + '\n%%   Result = ' + R.group(2)
		else:
			return '%%   Result = ' + R.group(2)

	def make_line(self):
		return '%%------------------------------------------------------------------------------\n'

	def make_doc(self):
		return '\n%% @doc\n%% @end\n'

	def is_spec(self, Str):
		if re.match('^-spec', Str):
			return True
		else:
			return False