# -*- coding: iso-8859-1 -*-

import os
import locale
os.environ["PYTHONIOENCODING"] = "utf-8"
myLocale=locale.setlocale(category=locale.LC_ALL, locale="de_DE.UTF-8");

string_mit_scharfem_s = 'Straße'

print(string_mit_scharfem_s.encode('utf-8', errors='ignore'))