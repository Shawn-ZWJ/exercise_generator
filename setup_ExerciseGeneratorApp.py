#coding:utf-8
from distutils.core import setup
import py2exe

setup(
    name=u'Exercise Generator',
    version='1.1',
    description='automatically generate exercises',
    author='Peng Shulin',
    windows = [
        {
            "script": "ExerciseGeneratorApp.py",
            #"icon_resources": [(1, "img\\wang.ico")],
        }
    ],
    options = {
        "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "dist_dir": "dist",
        }
    },
)
