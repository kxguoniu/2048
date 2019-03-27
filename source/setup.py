# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
includes = ['encoding', 'encodings.*']
options = {'py2exe':
        {'compressed': 1,
        'optimize': 2,
        'ascii': 1,
        'includes': includes,
		'dist_dir': 'dist',
        'bundle_files': 1,
        'dll_excludes': ['MSVCP90.dll'],
        }
      }
setup(
	version="1.0.0",
	options=options,
	zipfile=None,
	windows=[{"script":"2048.py",
		"icon_resources":[(1,"images\\icon.ico")]
		}],
)