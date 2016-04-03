import sublime, sublime_plugin

# PREFERENCES
# Line length to break at
# Pre or Post save

class PreSaveListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		view.run_command("gocomments")

class GocommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		offset = 0
		for rgn in self.view.find_all("[/]{2}.*"):
			if rgn.size() > (75):
				print(rgn)
				start = rgn.a + offset
				end = rgn.b + offset

				adj = 75
				# if you want to search both ways, then can use an or here, and two adj's, one incrementing, one decrementing
				# just need to stop the decrementing at a certain point (50?) or smth
				while self.view.substr(sublime.Region(start+adj-1, start+adj)) != ' ':
					adj += 1
					print("adj", adj)
					if adj >= rgn.size():
						break
				if adj >= rgn.size():
					continue

				self.view.replace(edit, sublime.Region(start, end), self.view.substr(sublime.Region(start, start+adj)) + "\n// " + self.view.substr(sublime.Region(start+adj, end)))

				offset += 4

# Other ToDos
# For comments that were already multi line, may want to combine split ones with the ones below ... unless its a full sentence that's supposed to be on its own line. Will have to see what behavior makes sense here.
