import sublime, sublime_plugin

class PreSaveListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		view.run_command("gocomments")

class GocommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World!")

		offset = 0
		for rgn in self.view.find_all("[/]{2}.*"):
			if rgn.size() > (75):
				print(rgn)
				start = rgn.a + offset
				end = rgn.b + offset
				self.view.replace(edit, sublime.Region(start, end), self.view.substr(sublime.Region(start, start+75)) + "\n// " + self.view.substr(sublime.Region(start+75, end)))
				offset += 4
				# self.view.insert(edit, rgn.a+75, "\n" + self.view.substr(sublime.Region(rgn.a+75, rgn.b)))
				# self.view.replace(edit, rgn, "test")

		# content = sublime.Region(0, self.view.size())
		# self.view.replace(edit, reg, "test")
