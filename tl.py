import sublime
import sublime_plugin
import re

COMMENT_COL = 40

# TODO:
# - use variable for column number
# - if there is already a comment on the line, don't add one.

class tlInsertCommentCommand(sublime_plugin.TextCommand):
	def get_lang(self):
		scope = self.view.scope_name(self.view.sel()[0].end())
		res = re.search('\\bsource\\.([a-z+\-]+)', scope)
		lang = res.group(1) if res else 'c'
		return lang

	def insert_c_comment(self, edit):
		for region in self.view.sel():
			line = self.view.line(region)
			line_str = self.view.substr(line)

			if len(line_str.strip()) > 0:
				row, col = self.view.rowcol(line.end())
				if col < COMMENT_COL:
					num_spaces = COMMENT_COL - col
				else:
					num_spaces = 1

				comment = " " * num_spaces
			else:
				comment = ""

			comment = comment + "/*  */"
			self.view.insert(edit, line.end(), comment)

		# after inserting the comment at the end of each line, move the cursors
		self.view.run_command("move_to", {"extend": False, "to": "hardeol"})
		self.view.run_command("move", {"by": "characters", "forward": False})
		self.view.run_command("move", {"by": "characters", "forward": False})
		self.view.run_command("move", {"by": "characters", "forward": False})

	def insert_python_comment(self, edit):
		for region in self.view.sel():
			line = self.view.line(region)
			line_str = self.view.substr(line)

			if len(line_str.strip()) > 0:
				row, col = self.view.rowcol(line.end())
				if col < COMMENT_COL:
					num_spaces = COMMENT_COL - col
				else:
					num_spaces = 1

				comment = " " * num_spaces
			else:
				comment = ""

			comment = comment + "# "
			self.view.insert(edit, line.end(), comment)

		# after inserting the comment at the end of each line, move the cursors
		self.view.run_command("move_to", {"extend": False, "to": "hardeol"})

	def run(self, edit):
		lang = self.get_lang()

		if lang == "c" or lang == "c++":
			self.insert_c_comment(edit)
		elif lang == "python":
			self.insert_python_comment(edit)

'''
class TlSortRecentFiles(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        self.move_active_to_top()
        
    def on_selection_modified_async(self, view):
        self.move_active_to_top()

    def move_active_to_top(self):
        window, group, index, view = self.get_active_view_index()

        # If there's no group, index
        if group == -1 or index == -1:
            return

        if index != 0:
            window.set_view_index(view, group, 0)

    def get_active_view_index(self):
        window = sublime.active_window()
        group = window.active_group()
        view = window.active_view_in_group(group)

        # print(dir(view))

        # If get_view_index appears to have bugs then the following code might
        # be useful
        # index = -1
        # views = window.views_in_group(group)
        # for i, v in enumerate(views):
        #     if v.id() == view.id():
        #         index = i
        #         break

        _, index = window.get_view_index(view)

        return window, group, index, view
'''