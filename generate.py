#!/usr/bin/env python3

import os
import shutil

from jinja2 import Environment,FileSystemLoader
from subprocess import Popen,PIPE

env = Environment(loader=FileSystemLoader("tmpl"))

snippets_dir = "snippets"
dist_dir = "dist"
gen_snippets_dir = dist_dir+"/gen_snippets"

shutil.rmtree(dist_dir, ignore_errors=True)
os.makedirs(gen_snippets_dir)

for subdir, dirs, files in os.walk(snippets_dir):
  for fname in files:
    trimmedName, ext = os.path.splitext(fname)
    full_path = subdir + "/" + fname
    if ext == '.tex':
      with open(full_path, "r") as snippet_f:
        gen_tex_name = gen_snippets_dir+"/"+fname
        gen_pdf_name = gen_snippets_dir+"/"+trimmedName+".pdf"
        with open(gen_tex_name, "w") as f:
          f.write(env.get_template("base.jinja.tex").render(
            content=snippet_f.read()
          ))

p = Popen(['make', "-f", "../../Makefile.slides", "-C", gen_snippets_dir],
  stdout=PIPE, stderr=PIPE)
out = p.communicate()
if out[1]:
  print("Warning: Make stderr non-empty.")
  print("===Stdout:")
  print(out[0].decode())
  print("===Stderr:")
  print(out[1].decode())
