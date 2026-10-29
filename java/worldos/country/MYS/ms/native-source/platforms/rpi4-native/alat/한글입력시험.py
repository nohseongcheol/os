#!/usr/bin/env python3
"""Composition/shortcut tests independent of a host input method."""
import unittest
from meja_lihat import papan_kekunci


class 한글입력시험(unittest.TestCase):
    def setUp(자신):
        자신.SMS_penimbal = ''
        def e_mel_9aee63bd(data):
            for data_aksara in data.decode('utf-8'):
                if data_aksara == '\x7f': 자신.SMS_penimbal = 자신.SMS_penimbal[:-1]
                else: 자신.SMS_penimbal += data_aksara
        자신.papan_kekunci_pemasukan = papan_kekunci(e_mel_9aee63bd)

    def tekan_Kunci(자신, simbol_VALUE):
        자신.papan_kekunci_pemasukan.누름값(True, simbol_VALUE)
        자신.papan_kekunci_pemasukan.누름값(False, simbol_VALUE)

    def TYPE_bidang(자신, 누름열):
        for 누름값 in 누름열: 자신.tekan_Kunci(ord(누름값))

    def test_낱말(자신):
        for 누름열,예상결과 in [('gksrmf','한글'),('dkssudgktpdy','안녕하세요'),
                ('rhk','과'),('rhos','괜'),('dml','의'),('rkqt','값'),
                ('rkqtk','갑사'),('dkswdk','앉아'),('qkfrk','발가'),
                ('RkRnd','까꿍'),('Wkfqdk','짧아'),('dkflfkddms','아리랑은')]:
            with 자신.subTest(누름열=누름열):
                자신.setUp(); 자신.tekan_Kunci(0xffc6); 자신.TYPE_bidang(누름열)
                자신.assertEqual(자신.SMS_penimbal, 예상결과)

    def test_앞글자지우기(자신):
        자신.tekan_Kunci(0xff31); 자신.TYPE_bidang('dlfr')
        자신.assertEqual(자신.SMS_penimbal,'읽')
        for 예상결과 in ('일','이','ㅇ',''):
            자신.tekan_Kunci(0xff08); 자신.assertEqual(자신.SMS_penimbal,예상결과)
        자신.TYPE_bidang('gksk'); 자신.assertEqual(자신.SMS_penimbal,'하나')
        자신.tekan_Kunci(0xff08); 자신.assertEqual(자신.SMS_penimbal,'하ㄴ')

    def test_전환반복확정(자신):
        자신.TYPE_bidang('echo ')
        자신.papan_kekunci_pemasukan.누름값(True,0xffe1)
        자신.papan_kekunci_pemasukan.누름값(True,32); 자신.papan_kekunci_pemasukan.누름값(True,32)
        자신.papan_kekunci_pemasukan.누름값(False,32); 자신.papan_kekunci_pemasukan.누름값(False,0xffe1)
        자신.assertTrue(자신.papan_kekunci_pemasukan.한글여부)
        자신.TYPE_bidang('gksrmf'); 자신.tekan_Kunci(0xff31); 자신.TYPE_bidang(' English')
        자신.assertEqual(자신.SMS_penimbal,'echo 한글 English')
        자신.assertFalse(자신.papan_kekunci_pemasukan.한글여부)
        자신.tekan_Kunci(0xffc6); 자신.TYPE_bidang('rk'); 자신.tekan_Kunci(0xff51)
        자신.TYPE_bidang('sk'); 자신.assertTrue(자신.SMS_penimbal.endswith('가\x1b[D나'))

    def ujian_tampal_AND_Unikod(자신):
        자신.tekan_Kunci(0xffc6); 자신.TYPE_bidang('rk')
        자신.papan_kekunci_pemasukan.papan_klip_VALUE='tampal_VALUE'.encode()
        자신.papan_kekunci_pemasukan.누름값(True,0xffe3); 자신.papan_kekunci_pemasukan.누름값(True,0xffe1)
        자신.tekan_Kunci(ord('v'))
        자신.papan_kekunci_pemasukan.누름값(False,0xffe1); 자신.papan_kekunci_pemasukan.누름값(False,0xffe3)
        자신.tekan_Kunci(0x0100d55c); 자신.TYPE_bidang('sk')
        자신.assertEqual(자신.SMS_penimbal,'가붙여넣기한나')


if __name__ == '__main__': unittest.main()
