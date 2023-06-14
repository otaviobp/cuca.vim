import vim  # type: ignore
import os
import cuca_utils

from cuca import Notebook, NoteFixer, Note
from cuca_gen import NoteHtmlGen

notes_backlist = {}


def CucaAddURL(url):
    vim.command('let @r="[{}]({})"'.format(cuca_utils.get_title_from_url(url), url))
    vim.command(':norm "rp')
    vim.command(":redraw!")


def CucaAddFile(path):
    notebook = Notebook(os.path.dirname(vim.current.buffer.name))
    if not notebook.is_init():
        print("Error: Notebook is not initialized")
        return

    if not os.path.exists(path):
        print("Error: File doesn't exist")
        return

    vim.command("let user_input = input('Title: ')")
    title = vim.eval("user_input")

    dest, title = notebook.add_file(path, title)
    basename = os.path.basename(dest)
    basedir = os.path.basename(os.path.dirname(dest))

    if cuca_utils.guess_filetype(path).startswith("image/"):
        link_format = "![{}]({})"
    else:
        link_format = "[{}]({})"

    cmd = 'let @r="{}"'.format(link_format)
    vim.command(cmd.format(title, os.path.join(basedir, basename)))
    vim.command(':norm "rp')
    vim.command(": redraw!")


def CucaOpen():
    def buffer_get(buffer, row, col):
        if row >= len(buffer) or col >= len(buffer[row]):
            return None

        return buffer[row][col]

    row, col = vim.current.window.cursor
    row = row - 1  # Vim indices starts at 1

    # Cursor on ! before image link
    if buffer_get(vim.current.buffer, row, col) == "!":
        col = col + 1

    # Cursor on [
    if buffer_get(vim.current.buffer, row, col) == "[":
        istart = col
    else:
        istart = vim.current.buffer[row].rfind("[", 0, col)

    if istart < 0:
        return

    # iend = vim.current.buffer[row].find("]", col)
    iend = vim.current.buffer[row].find("]", istart)
    if iend < 0:
        return

    notebook = Notebook(os.path.dirname(vim.current.buffer.name))

    # if it's a link
    link_start = vim.current.buffer[row].find("(", iend)
    if link_start - iend == 1 or link_start - iend == 2:
        link_end = vim.current.buffer[row].find(")", link_start)
        if col < istart or col > link_end:
            return

        link = vim.current.buffer[row][link_start + 1 : link_end]
        # TODO: Use a regexp here. Consolidate link parsing
        if link.startswith("http:") or link.startswith("file:") or link.startswith("https:"):
            os.system("xdg-open {}".format(link))
        else:
            os.system("xdg-open file://{}".format(notebook.cuca_data_dir(link)))
        return

    if col < istart or col > iend:
        return

    title = vim.current.buffer[row][istart + 1 : iend]
    filename = Notebook().new_file(title)

    notes_backlist[os.path.realpath(filename)] = os.path.realpath(vim.current.buffer.name)
    vim.command("edit {}".format(filename))


def CucaBack():
    rpath = os.path.realpath(vim.current.buffer.name)
    if rpath in notes_backlist:
        vim.command("edit {}".format(notes_backlist[rpath]))


def CucaFix():
    NoteFixer(Note(vim.current.buffer.name)).fix_all()
    vim.command(":e")


def CucaCreateHTML():
    path = vim.current.buffer.name
    if not os.path.exists(path):
        return

    notebook = Notebook(os.path.dirname(path))
    if not notebook.is_init():
        return

    generator = NoteHtmlGen(notebook)
    generator.save_note_html(Note(path).get_file_title())


def CucaOpenInBrowser():
    notebook = Notebook(os.path.dirname(vim.current.buffer.name))

    title = notebook.get_note(vim.current.buffer.name).get_file_title()
    html_dir = notebook.cuca_data_dir("html")
    html = os.path.join(html_dir, title + ".html")
    os.system("xdg-open file://{}".format(os.path.realpath(html)))
