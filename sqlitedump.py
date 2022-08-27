import sublime, sublime_plugin
import os
import subprocess

# adapted for functionality in windows (requires path to sqlite3.exe binary, and seems to work without issue :-]
SQLITE_BIN_PATH = 'C:\\ProgramData\\chocolatey\\bin\\sqlite3.exe'


class SqliteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region_all = sublime.Region(0, self.view.size())
    self.view.erase(edit, region_all)

    sqlite_dump = subprocess.check_output([
      SQLITE_BIN_PATH,
      self.view.file_name(),
      '.dump'
    ])
    sqlite_dump = sqlite_dump.decode('ascii', 'ignore')

    self.view.insert(edit, 0, sqlite_dump)


class EventListener(sublime_plugin.EventListener):
  def on_load(self, view):
    if not os.path.isfile(SQLITE_BIN_PATH):
      print('sqlite3 not found at {}, exiting'.format(SQLITE_BIN_PATH))
      return

    ext = os.path.splitext(view.file_name())[1]
    # checks for a few other filetypes (not great at python so probably did executed this a bit oddly)
    # open filetype: [.db]
    if ext == '.db':
      ext = '.sqlite3'
    # open filetype: [.sql]
    if ext == '.sql':
      ext = '.sqlite3'
    # open filetype: [.sqlite3]
    if ext == '':
      ext = '.sqlite3'
    if not ext == '.sqlite3':
      return

    view.run_command('sqlite')
    
