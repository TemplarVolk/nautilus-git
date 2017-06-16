#!/usr/bin/python2
"""
Nautilus git pluging to show useful information under any
git directory

Author : Bilal Elmoussaoui (bil.elmoussaoui@gmail.com)
Website : https://github.com/bil-elmoussaoui/nautilus-git
Licence : GPL-3.0
nautilus-git is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
nautilus-git is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with nautilus-git. If not, see <http://www.gnu.org/licenses/>.
"""
import difflib
from os import path
from subprocess import PIPE, Popen
from urlparse import urlsplit
from urllib2 import unquote


def get_file_path(uri):
    """Return file path from an uri."""
    url = urlsplit(uri)
    if url.scheme.lower() == "file":
        return unquote(url.path)
    return None


def is_git(folder_path):
    """Verify if the current folder_path is a git directory."""
    folder_path = get_file_path(folder_path)
    if folder_path:
        output = execute('git rev-parse --is-inside-work-tree',
                         folder_path).lower()
        return output == "true"
    return None


def get_real_git_dir(directory):
    """Return the absolute path of the .git folder."""
    dirs = directory.split("/")
    for i in range(len(dirs) - 1, 0, -1):
        current_path = "/".join(dirs[0:i])
        git_folder = path.join(current_path, ".git")
        if path.exists(git_folder):
            return current_path
    return None


def execute(cmd, working_dir=None):
    """Execute a shell command."""
    if working_dir:
        command = Popen(cmd, shell=True, stdout=PIPE,
                        stderr=PIPE, cwd=working_dir)
    else:
        command = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output = command.communicate()[0]
    return output.decode("utf-8").strip()


def get_diff(content1, content2):
    differ = difflib.Differ()
    diff = list(differ.compare(content1, content2))
    resultat = []
    line_no1 = 0
    line_no2 = 0

    for line in diff:
        code = line[:2]
        line_code = line[2:]
        if code == "  ":
            line_no1 += 1
            line_no2 += 1
        elif code == "- ":
            if line != "\n":
                line_no1 += 1
                resultat.append([line_no1, None, code, line_code])
            else:
                line_no1 -= 1
        elif code == "+ ":
            if line != "\n":
                line_no2 += 1
                resultat.append([None, line_no2, code, line_code])
            else:
                line_no2 -= 1
    return resultat
