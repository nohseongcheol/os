#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from Masaüstü_Görünüm import klavye


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_tampon = ''
        def göndermek(veri):
            for karakter_verileri in veri.decode('utf-8'):
                if karakter_verileri == '\x7f': 자신.SMS_tampon = 자신.SMS_tampon[:-1]
                else: 자신.SMS_tampon += karakter_verileri
        자신.klavye_girdi = klavye(göndermek)

    def bas_tuş(자신, simge_değer):
        자신.klavye_girdi.누름값(True, simge_değer)
        자신.klavye_girdi.누름값(False, simge_değer)

    def TÜR_alan(자신, 누름열):
        for 누름값 in 누름열: 자신.bas_tuş(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.bas_tuş(0xffc6); 자신.TÜR_alan(누름열)
                자신.assertEqual(자신.SMS_tampon, 예상결과)

    def test_앞글자지우기(자신):
        자신.bas_tuş(0xff31); 자신.TÜR_alan('dlfr')
        자신.assertEqual(자신.SMS_tampon,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.bas_tuş(0xff08); 자신.assertEqual(자신.SMS_tampon,예상결과)
        자신.TÜR_alan('gksk'); 자신.assertEqual(자신.SMS_tampon,'하나')
        자신.bas_tuş(0xff08); 자신.assertEqual(자신.SMS_tampon,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TÜR_alan('echo ')
        자신.klavye_girdi.누름값(True,0xffe1)
        자신.klavye_girdi.누름값(True,32); 자신.klavye_girdi.누름값(True,32)
        자신.klavye_girdi.누름값(False,32); 자신.klavye_girdi.누름값(False,0xffe1)
        자신.assertTrue(자신.klavye_girdi.한글여부)
        자신.TÜR_alan('gksrmf'); 자신.bas_tuş(0xff31); 자신.TÜR_alan(' English')
        자신.assertEqual(자신.SMS_tampon,'echo 한글 English')
        자신.assertFalse(자신.klavye_girdi.한글여부)
        자신.bas_tuş(0xffc6); 자신.TÜR_alan('rk'); 자신.bas_tuş(0xff51)
        자신.TÜR_alan('sk'); 자신.assertTrue(자신.SMS_tampon.endswith('가\x1b[D나'))

    def test_yapıştırmak_VE_UNICODE(자신):
        자신.bas_tuş(0xffc6); 자신.TÜR_alan('rk')
        자신.klavye_girdi.pano_değer='yapıştırmak_değer'.encode()
        자신.klavye_girdi.누름값(True,0xffe3); 자신.klavye_girdi.누름값(True,0xffe1)
        자신.bas_tuş(ord('v'))
        자신.klavye_girdi.누름값(False,0xffe1); 자신.klavye_girdi.누름값(False,0xffe3)
        자신.bas_tuş(0x0100d55c); 자신.TÜR_alan('sk')
        자신.assertEqual(자신.SMS_tampon,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
