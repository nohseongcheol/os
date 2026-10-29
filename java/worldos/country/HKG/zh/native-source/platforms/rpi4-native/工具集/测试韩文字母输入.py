#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from 桌面视图 import 键盘


class 测试韩文字母输入(unittest.TestCase):
    def setUp(自身值):
        自身值.文本缓冲 = ''
        def 发送(数据):
            for 字符数据 in 数据.decode('utf-8'):
                if 字符数据 == '\x7f': 自身值.文本缓冲 = 自身值.文本缓冲[:-1]
                else: 自身值.文本缓冲 += 字符数据
        自身值.键盘条目 = 键盘(发送)

    def 按下键(自身值, 符号值):
        自身值.键盘条目.已按下值(True, 符号值)
        自身值.键盘条目.已按下值(False, 符号值)

    def 类型分类(自身值, 已按下键列):
        for 已按下值 in 已按下键列: 自身值.按下键(ord(已按下值))

    def 测试单词列(自身值):
        for 已按下键列,预期 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 自身值.subTest(已按下键列=已按下键列):
                自身值.setUp(); 自身值.按下键(0xffc6); 自身值.类型分类(已按下键列)
                自身值.assertEqual(自身值.文本缓冲, 预期)

    def 测试退格(自身值):
        自身值.按下键(0xff31); 自身值.类型分类('dlfr')
        自身值.assertEqual(自身值.文本缓冲,'읽')
        for 预期 in ('일','이','ㅇ',''):
            自身值.按下键(0xff08); 自身值.assertEqual(自身值.文本缓冲,预期)
        自身值.类型分类('gksk'); 自身值.assertEqual(自身值.文本缓冲,'一值')
        自身值.按下键(0xff08); 自身值.assertEqual(自身值.文本缓冲,'하ㄴ')

    def 测试模式列重复与提交(自身值):
        自身值.类型分类('echo ')
        自身值.键盘条目.已按下值(True,0xffe1)
        自身值.键盘条目.已按下值(True,32); 自身值.键盘条目.已按下值(True,32)
        自身值.键盘条目.已按下值(False,32); 自身值.键盘条目.已按下值(False,0xffe1)
        自身值.assertTrue(自身值.键盘条目.韩语)
        自身值.类型分类('gksrmf'); 自身值.按下键(0xff31); 自身值.类型分类(' English')
        自身值.assertEqual(自身值.文本缓冲,'echo 한글 English')
        自身值.assertFalse(自身值.键盘条目.韩语)
        自身值.按下键(0xffc6); 自身值.类型分类('rk'); 自身值.按下键(0xff51)
        自身值.类型分类('sk'); 自身值.assertTrue(自身值.文本缓冲.endswith('首位操作数\x1b[D나'))

    def 测试粘贴与Unicode(自身值):
        自身值.按下键(0xffc6); 自身值.类型分类('rk')
        自身值.键盘条目.剪贴板值='粘贴值'.encode()
        自身值.键盘条目.已按下值(True,0xffe3); 自身值.键盘条目.已按下值(True,0xffe1)
        自身值.按下键(ord('v'))
        自身值.键盘条目.已按下值(False,0xffe1); 自身值.键盘条目.已按下值(False,0xffe3)
        自身值.按下键(0x0100d55c); 自身值.类型分类('sk')
        自身值.assertEqual(自身值.文本缓冲,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
