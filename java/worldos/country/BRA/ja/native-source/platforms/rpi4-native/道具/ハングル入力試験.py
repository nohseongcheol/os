#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from デスクトップ表示像 import キーボード


class ハングル入力試験(unittest.TestCase):
    def setUp(自身値):
        自身値.本文緩衝域 = ''
        def 送信(データ):
            for 文字データ in データ.decode('utf-8'):
                if 文字データ == '\x7f': 自身値.本文緩衝域 = 自身値.本文緩衝域[:-1]
                else: 自身値.本文緩衝域 += 文字データ
        自身値.キーボード入口 = キーボード(送信)

    def 押下キー(自身値, 記号値):
        自身値.キーボード入口.押下済み値(True, 記号値)
        自身値.キーボード入口.押下済み値(False, 記号値)

    def 型分類(自身値, 押下済みキー一覧):
        for 押下済み値 in 押下済みキー一覧: 自身値.押下キー(ord(押下済み値))

    def 語一覧試験(自身値):
        for 押下済みキー一覧,期待 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','値'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 自身値.subTest(押下済みキー一覧=押下済みキー一覧):
                自身値.setUp(); 自身値.押下キー(0xffc6); 自身値.型分類(押下済みキー一覧)
                自身値.assertEqual(自身値.本文緩衝域, 期待)

    def 後退消去試験(自身値):
        自身値.押下キー(0xff31); 自身値.型分類('dlfr')
        自身値.assertEqual(自身値.本文緩衝域,'읽')
        for 期待 in ('일','이','ㅇ',''):
            自身値.押下キー(0xff08); 自身値.assertEqual(自身値.本文緩衝域,期待)
        自身値.型分類('gksk'); 自身値.assertEqual(自身値.本文緩衝域,'一値')
        自身値.押下キー(0xff08); 自身値.assertEqual(自身値.本文緩衝域,'하ㄴ')

    def 方式一覧反復論理積確定試験(自身値):
        自身値.型分類('echo ')
        自身値.キーボード入口.押下済み値(True,0xffe1)
        自身値.キーボード入口.押下済み値(True,32); 自身値.キーボード入口.押下済み値(True,32)
        自身値.キーボード入口.押下済み値(False,32); 自身値.キーボード入口.押下済み値(False,0xffe1)
        自身値.assertTrue(自身値.キーボード入口.韓国語)
        自身値.型分類('gksrmf'); 自身値.押下キー(0xff31); 自身値.型分類(' English')
        自身値.assertEqual(自身値.本文緩衝域,'echo 한글 English')
        自身値.assertFalse(自身値.キーボード入口.韓国語)
        自身値.押下キー(0xffc6); 自身値.型分類('rk'); 自身値.押下キー(0xff51)
        自身値.型分類('sk'); 自身値.assertTrue(自身値.本文緩衝域.endswith('先頭位置被演算子\x1b[D나'))

    def 貼付け論理積Unicode試験(自身値):
        自身値.押下キー(0xffc6); 自身値.型分類('rk')
        自身値.キーボード入口.貼付け板値='貼付け値'.encode()
        自身値.キーボード入口.押下済み値(True,0xffe3); 自身値.キーボード入口.押下済み値(True,0xffe1)
        自身値.押下キー(ord('v'))
        自身値.キーボード入口.押下済み値(False,0xffe1); 自身値.キーボード入口.押下済み値(False,0xffe3)
        自身値.押下キー(0x0100d55c); 自身値.型分類('sk')
        自身値.assertEqual(自身値.本文緩衝域,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
