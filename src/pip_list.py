#-------------------------------------------------------------------------------
# Name:        pip_list
# Purpose:     pip list in Python Interpreter
#-------------------------------------------------------------------------------

import pip

w = 0
for i in pip.get_installed_distributions():
    if (w < len(i.key)):
        w = len(i.key)

#for i in pip.get_installed_distributions():
#    print(i.key.ljust(w + 1) + "== " + i.version)

print("\n".join(sorted(["%s== %s" % (i.key.ljust(w+1), i.version) for i in pip.get_installed_distributions()])))
