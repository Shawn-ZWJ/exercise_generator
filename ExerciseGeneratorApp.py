#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
import os
import re
import sys
import math
import time
import random
from random import *
from ExerciseGeneratorDlg import *
ABOUT_INFO = u'''\
自动出题程序
将生成结果复制粘帖到Excel中排版
https://github.com/pengshulin/exercise_generator
Peng Shullin <trees_peng@163.com> 2017
'''

CONFIGS = {
u'加减法': u'''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    oper = choice( ['-', '+'] ) 
    if oper == '+':
        c = a + b
    else:
        c = a - b
    ASSERT( 0 <= c <= MAX )
    return [ a, oper, b, '=', c ]
''',

u'比较大小': u'''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    if a > b:
        oper = '>'
    elif a < b:
        oper = '<'
    else:
        oper = '='
    return [ a, oper, b ]

''',

u'排序': u'''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    b = randint(MIN, MAX)
    c = randint(MIN, MAX)
    d = randint(MIN, MAX)
    ASSERT( a < b < c < d )
    return [ a, '<', b, '<', c, '<', d ]

''',

u'生成随机数': u'''\
def generator():
    MIN, MAX = 0, 100
    a = randint(MIN, MAX)
    return [ a ]

''',



}

class AssertError(Exception):
    pass

def ASSERT(condition):
    if not condition:
        raise AssertError()


class MainDialog(MyDialog):

    def __init__(self, *args, **kwds):
        MyDialog.__init__( self, *args, **kwds )
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.button_generate.Enable(False)
        self.button_copy_result.Enable(False)
        self.combo_box_type.SetValue(u'请选择出题类型...')
        self.combo_box_type.AppendItems(CONFIGS.keys()) 
        self.spin_ctrl_number.SetValue(100)
        self.clrAllResult()

    def OnClose(self, event):
        self.Destroy()
        event.Skip()

    def OnSelectType(self, event):
        self.label_info.SetLabel('')
        tp = self.combo_box_type.GetValue()
        if CONFIGS.has_key(tp):
            self.text_ctrl_rules.SetValue( CONFIGS[tp] )
            self.button_generate.Enable(True)
        else:
            self.button_generate.Enable(False)
        event.Skip()

    def clrAllResult( self ):
        self.grid_result.ClearGrid()
        lines = self.grid_result.GetNumberRows()
        if lines:
            self.grid_result.DeleteRows(numRows=lines)

    def addResult( self, line, result ):
        if self.grid_result.AppendRows():
            #print line, result, len(result)
            for i in range(len(result)):
                self.grid_result.SetCellValue( line-1, i, unicode(result[i]) )
      
      
    def OnGenerate(self, event):
        self.label_info.SetLabel('')
        rules = self.text_ctrl_rules.GetValue()
        num = self.spin_ctrl_number.GetValue()
        counter = 0
        try:
            code = compile(rules, '', 'exec')
            exec code
            generator
        except Exception, e:
            self.label_info.SetLabel(str(e))
            return
        self.clrAllResult()
        while counter < num:
            try:
                result = generator()
                counter += 1 
                self.addResult( counter, result )
            except AssertError:
                pass
            except Exception, e:
                self.label_info.SetLabel(str(e))
                return
        self.button_copy_result.Enable(True)
        event.Skip()

    def OnCopyResult(self, event):
        self.label_info.SetLabel('')
        lines = self.grid_result.GetNumberRows()
        if lines:
            ret = []
            for l in range(lines):
                items = [self.grid_result.GetCellValue( l, c ) for c in range(26)]
                cp = '\t'.join(items).strip()
                print cp
                ret.append( cp )
            copy = '\r\n'.join(ret)
            import pyperclip
            pyperclip.copy( copy )
        event.Skip()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, ABOUT_INFO, u'关于', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
 
   



if __name__ == "__main__":
    gettext.install("app")
    #freeze_support()
    app = wx.App(0)
    app.SetAppName( 'ExerciseGeneratorApp' )
    dialog_1 = MainDialog(None, wx.ID_ANY, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
