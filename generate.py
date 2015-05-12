#!/usr/bin/env python3

import os
import shutil

from jinja2 import Environment,FileSystemLoader
from pygments import highlight
from pygments.lexers import TexLexer
from pygments.formatters import HtmlFormatter
from subprocess import Popen,PIPE

env = Environment(loader=FileSystemLoader("website-templates"),
  block_start_string='~{',block_end_string='}~',
  variable_start_string='~{{', variable_end_string='}}~')

snippets_dir = "snippets"
dist_dir = "dist"
html_index = "/index.html"
gen_snippets_dir = "/gen_snippets"
static_dir = "static"

shutil.rmtree(dist_dir, ignore_errors=True)
shutil.copytree(static_dir, dist_dir)

fnames = []
for subdir, dirs, files in os.walk(snippets_dir):
  for fname in files:
    fnames.append(fname)

snippets = []
for fname in sorted(fnames):
  trimmedName, ext = os.path.splitext(fname)
  full_path = subdir + "/" + fname
  if ext == '.tex':
    with open(full_path, "r") as snippet_f:
      gen_tex_name = gen_snippets_dir+"/"+fname
      gen_pdf_name = gen_snippets_dir+"/"+trimmedName+".pdf"
      gen_png_name = gen_snippets_dir+"/"+trimmedName+".png"
      snippet_content = snippet_f.read().strip()
      with open(dist_dir+"/"+gen_tex_name, "w") as f:
        f.write(env.get_template("base.jinja.tex").render(
          content=snippet_content
        ))
      snippets.append({
        'fname': trimmedName,
        'pdf': gen_pdf_name,
        'png': gen_png_name,
        'content': highlight(snippet_content, TexLexer(), HtmlFormatter())
      })

p = Popen(['make', "-f", "../../Makefile.slides", "-C",
  dist_dir+"/"+gen_snippets_dir, "-j", "8"], stdout=PIPE, stderr=PIPE)
out = p.communicate()
if out[1]:
  print("Warning: Make stderr non-empty.")
  print("===Stdout:")
  print(out[0].decode())
  print("===Stderr:")
  print(out[1].decode())

with open("website-templates/preamble.tex", "r") as f:
  preamble = f.read()

with open(dist_dir+"/"+html_index, "w") as idx_f:
  idx_f.write(env.get_template("index.jinja.html").render(
    snippets=snippets,
    base=highlight(
      env.get_template("base.jinja.tex").render(
        content="Start content here."
      ),
      TexLexer(),
      HtmlFormatter()
    )
  ))
