#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from 桌面視圖 import 鍵盤


class 測試韓文字母輸入(unittest.TestCase):
    def setUp(自身值):
        自身值.文本緩衝區 = ''
        def 發送(資料):
            for 字元資料 in 資料.decode('utf-8'):
                if 字元資料 == '\x7f': 自身值.文本緩衝區 = 自身值.文本緩衝區[:-1]
                else: 自身值.文本緩衝區 += 字元資料
        自身值.鍵盤條目 = 鍵盤(發送)

    def 按下鍵(自身值, 符號值):
        自身值.鍵盤條目.已按下值(True, 符號值)
        自身值.鍵盤條目.已按下值(False, 符號值)

    def 類型分類(自身值, 已按下鍵列):
        for 已按下值 in 已按下鍵列: 自身值.按下鍵(ord(已按下值))

    def 測試單詞列(自身值):
        for 已按下鍵列,預期 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 自身值.subTest(已按下鍵列=已按下鍵列):
                自身值.setUp(); 自身值.按下鍵(0xffc6); 自身值.類型分類(已按下鍵列)
                自身值.assertEqual(自身值.文本緩衝區, 預期)

    def 測試退格(自身值):
        自身值.按下鍵(0xff31); 自身值.類型分類('dlfr')
        自身值.assertEqual(自身值.文本緩衝區,'읽')
        for 預期 in ('일','이','ㅇ',''):
            自身值.按下鍵(0xff08); 自身值.assertEqual(自身值.文本緩衝區,預期)
        自身值.類型分類('gksk'); 自身值.assertEqual(自身值.文本緩衝區,'一值')
        自身值.按下鍵(0xff08); 自身值.assertEqual(自身值.文本緩衝區,'하ㄴ')

    def 測試模式列重複與提交(自身值):
        自身值.類型分類('echo ')
        自身值.鍵盤條目.已按下值(True,0xffe1)
        自身值.鍵盤條目.已按下值(True,32); 自身值.鍵盤條目.已按下值(True,32)
        自身值.鍵盤條目.已按下值(False,32); 自身值.鍵盤條目.已按下值(False,0xffe1)
        自身值.assertTrue(自身值.鍵盤條目.韓語)
        自身值.類型分類('gksrmf'); 自身值.按下鍵(0xff31); 自身值.類型分類(' English')
        自身值.assertEqual(自身值.文本緩衝區,'echo 한글 English')
        自身值.assertFalse(自身值.鍵盤條目.韓語)
        自身值.按下鍵(0xffc6); 自身值.類型分類('rk'); 自身值.按下鍵(0xff51)
        自身值.類型分類('sk'); 自身值.assertTrue(自身值.文本緩衝區.endswith('首位操作數\x1b[D나'))

    def 測試粘貼與Unicode(自身值):
        自身值.按下鍵(0xffc6); 自身值.類型分類('rk')
        自身值.鍵盤條目.剪貼板值='粘貼值'.encode()
        自身值.鍵盤條目.已按下值(True,0xffe3); 自身值.鍵盤條目.已按下值(True,0xffe1)
        自身值.按下鍵(ord('v'))
        自身值.鍵盤條目.已按下值(False,0xffe1); 自身值.鍵盤條目.已按下值(False,0xffe3)
        自身值.按下鍵(0x0100d55c); 自身值.類型分類('sk')
        自身值.assertEqual(自身值.文本緩衝區,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
