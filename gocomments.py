import sublime, sublime_plugin, re

# PREFERENCES
# Line length to break at
# Pre or Post save
# Whether or not it should be on save or on key binding?

class PreSaveListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		view.run_command("gocomments")

# TWO BUGS FOUND:
# If you comment out an entire block (so code, not comments), and then save ...they all get chopped up. YIkes, what to do?
# In line comments are getting split , ie: var x // here we define x blah blah.
# --> those should not be split no matter the length... regex must be off

class GocommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		offset = 0
		rgns = self.view.find_all("[ \t]*[/]{2}.*")
		for i, rgn in enumerate(rgns):
			if rgn.size() > (75):
				# print(rgn)
				start = rgn.a + offset
				end = rgn.b + offset
				comment = sublime.Region(start, end)

				adj = 75
				# if you want to search both ways, then can use an or here, and two adj's, one incrementing, one decrementing
				# just need to stop the decrementing at a certain point (50?) or smth.
				# Could also make it so if it finds a punctuation mark (. ? !) then it wraps there.
				while self.view.substr(sublime.Region(start+adj-1, start+adj)) != ' ':
					adj += 1
					# If we reach the end of the string stop looking.
					if adj >= rgn.size():
						break
				# And continue without wrapping anything.
				if adj >= rgn.size():
					continue

				# If the new comment line would be less than 25 characters, don't bother.
				if end - (start+adj) < 25:
					continue

				# Determine the indentation.
				match = re.search(r'^([ \t]+)', self.view.substr(comment))
				if match:
					indent = match.group(0)
					offset += match.end()
				else:
					indent = ""

				# Determine punctuation.
				# can only do this at the very end of a wrapped and --checked against following regions-- string
				# to make sure it's not just a long multi line comment that was partially self wrapped
				# [\.\?\!;]*$

				# Check following regions...
				# * need to check if rgns[i+1] exists first
				if rgns[i+1].a == (rgn.b + 1):
					print(self.view.substr(comment))
					print("here")
					# [ \t]*[/]{2}[\s]* ... need the opposite of this

				self.view.replace(edit, comment, self.view.substr(sublime.Region(start, start+adj)) + "\n" + indent + "// " + self.view.substr(sublime.Region(start+adj, end)))

				offset += 4

# Other ToDos
# For comments that were already multi line, may want to combine split ones with the ones below ... unless its a full sentence that's supposed to be on its own line. Will have to see what behavior makes sense here.
#  ... basically if the end of the split line is a period, don't do anything, but if it's not, combine it with the line below
# so you would need to add a check when you start each region to see if there's an adjacent region above that's less than 75 chars

# will also have to handle cases where even the split line is greater than 75 chars. need to check if reg 75 to end is greater than 75 
# a recursive design here would probably make the most sense

# will also have to make it so we check if its a .go file before doing any of this