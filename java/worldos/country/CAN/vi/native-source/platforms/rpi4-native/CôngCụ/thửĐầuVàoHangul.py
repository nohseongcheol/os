#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from khungNhìnMànLàmViệc import BànPhím


class thửĐầuVàoHangul(unittest.TestCase):
    def setUp(giáTrịBảnThân):
        giáTrịBảnThân.bộĐệmVănBản = ''
        def gửi(DữLiệu):
            for dữLiệuKýTự in DữLiệu.decode('utf-8'):
                if dữLiệuKýTự == '\x7f': giáTrịBảnThân.bộĐệmVănBản = giáTrịBảnThân.bộĐệmVănBản[:-1]
                else: giáTrịBảnThân.bộĐệmVănBản += dữLiệuKýTự
        giáTrịBảnThân.mụcBànPhím = BànPhím(gửi)

    def phímNhấn(giáTrịBảnThân, giáTrịKýHiệu):
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(True, giáTrịKýHiệu)
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(False, giáTrịKýHiệu)

    def loạiMụcKiểu(giáTrịBảnThân, cácPhímĐãNhấn):
        for giáTrịĐãNhấn in cácPhímĐãNhấn: giáTrịBảnThân.phímNhấn(ord(giáTrịĐãNhấn))

    def thửCácTừ(giáTrịBảnThân):
        for cácPhímĐãNhấn,dựKiến in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with giáTrịBảnThân.subTest(cácPhímĐãNhấn=cácPhímĐãNhấn):
                giáTrịBảnThân.setUp(); giáTrịBảnThân.phímNhấn(0xffc6); giáTrịBảnThân.loạiMụcKiểu(cácPhímĐãNhấn)
                giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản, dựKiến)

    def thửXóaLùi(giáTrịBảnThân):
        giáTrịBảnThân.phímNhấn(0xff31); giáTrịBảnThân.loạiMụcKiểu('dlfr')
        giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản,'읽')
        for dựKiến in ('일','이','ㅇ',''):
            giáTrịBảnThân.phímNhấn(0xff08); giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản,dựKiến)
        giáTrịBảnThân.loạiMụcKiểu('gksk'); giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản,'giáTrịMột')
        giáTrịBảnThân.phímNhấn(0xff08); giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản,'하ㄴ')

    def thửChốtVàLặpLạiCácChếĐộ(giáTrịBảnThân):
        giáTrịBảnThân.loạiMụcKiểu('echo ')
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(True,0xffe1)
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(True,32); giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(True,32)
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(False,32); giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(False,0xffe1)
        giáTrịBảnThân.assertTrue(giáTrịBảnThân.mụcBànPhím.tiếngHàn)
        giáTrịBảnThân.loạiMụcKiểu('gksrmf'); giáTrịBảnThân.phímNhấn(0xff31); giáTrịBảnThân.loạiMụcKiểu(' English')
        giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản,'echo 한글 English')
        giáTrịBảnThân.assertFalse(giáTrịBảnThân.mụcBànPhím.tiếngHàn)
        giáTrịBảnThân.phímNhấn(0xffc6); giáTrịBảnThân.loạiMụcKiểu('rk'); giáTrịBảnThân.phímNhấn(0xff51)
        giáTrịBảnThân.loạiMụcKiểu('sk'); giáTrịBảnThân.assertTrue(giáTrịBảnThân.bộĐệmVănBản.endswith('toánHạngĐầuTiên\x1b[D나'))

    def thửUnicodeVàDán(giáTrịBảnThân):
        giáTrịBảnThân.phímNhấn(0xffc6); giáTrịBảnThân.loạiMụcKiểu('rk')
        giáTrịBảnThân.mụcBànPhím.giáTrịBảngTạm='giáTrịDán'.encode()
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(True,0xffe3); giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(True,0xffe1)
        giáTrịBảnThân.phímNhấn(ord('v'))
        giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(False,0xffe1); giáTrịBảnThân.mụcBànPhím.giáTrịĐãNhấn(False,0xffe3)
        giáTrịBảnThân.phímNhấn(0x0100d55c); giáTrịBảnThân.loạiMụcKiểu('sk')
        giáTrịBảnThân.assertEqual(giáTrịBảnThân.bộĐệmVănBản,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
