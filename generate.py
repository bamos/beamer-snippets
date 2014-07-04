#!/usr/bin/env python3

import os

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("tmpl"))

for subdir, dirs, files in os.walk('snippets'):
  for fname in files:
    trimmedName, ext = os.path.splitext(fname)
    full_path = subdir + "/" + fname
    if ext == '.tex':
      with open(full_path, "r") as snippet_f:
        gen_name = "dist/" + fname
        with open(gen_name, "w") as f:
          f.write(env.get_template("base.jinja.tex").render(
            content=snippet_f.read()
          ))
