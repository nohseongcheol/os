"""hakyky_maglumat ELF ýerine_ýetir_buýruk + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.katalog_baha = Path(self.임시.name)

    def düz_gor(self, Çeşme, 추가=None, 성공=True, niýet='linux', 내보냄=None):
        ýol_Sanaw = []
        for Ad, Mazmun_baha in dict({'시험': Çeşme}, **(추가 or {})).items():
            Ýol = self.katalog_baha / (Ad + '.java')
            Ýol.write_text(Mazmun_baha, encoding='utf-8')
            ýol_Sanaw.append(str(Ýol))
        buýruk = [sys.executable, str(컴파일러), '--target', niýet, '--entry', '시험.Bitir', '-o', str(self.katalog_baha / 'native')]
        if 내보냄 is not None: buýruk += ['--export', 내보냄]
        결과 = subprocess.run(buýruk + ýol_Sanaw,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('düz_gor Hata'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.katalog_baha / 'native')], timeout=5).returncode

    def 자바대조(self, Çeşme, 추가=None):
        self.düz_gor(Çeşme, 추가)
        (self.katalog_baha / 'esasy.java').write_text(
            'public class esasy { public static void main(String[] 인수) { System.exit(시험.Bitir()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.katalog_baha)] +
                       [str(Ýol) for Ýol in self.katalog_baha.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.katalog_baha), 'esasy'], timeout=5).returncode
        hakyky_maglumat = self.실행결과()
        self.assertGreaterEqual(hakyky_maglumat, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 barla)')
        self.assertEqual(hakyky_maglumat, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Bitir() {
                int 합 = 7;
                int baha = 12345;
                for (int indeks = -65; indeks <= 65; indeks++) {
                    baha = baha * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(baha, indeks);
                    합 += (byte)baha + (short)baha + (char)baha;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] baha = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Bitir() {
                int 합 = 13;
                for (int 가 = 0; 가 < baha.length; 가++)
                    for (int 나 = 1; 나 < baha.length; 나++)
                        합 = 합 * 31 + baha[가] / baha[나] + baha[가] % baha[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] döretmek_girizmeklik(int Ululyk) { return new int[Ululyk]; }
            public static int Bitir() {
                int[] 가 = döretmek_girizmeklik(8); int[] 나 = 가; int[] boş_obýekt = new int[0];
                if (가 != 나 || 가 == null || boş_obýekt.length != 0 || 가[7] != 0) return 99;
                int baha = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return baha + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int baha = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Bitir() { return 계산(1, 2, 3, 4, baha) + 보조.Oka(); }
        }''', {'보조': '''public class 보조 {
            static int baha = 3;
            static int 초기값() { return ++baha; }
            static int Oka() { return baha; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int baha = 보조.Oka() + 1;
            public static int Bitir() { return baha * 10 + 보조.Oka(); }
        }''', {'보조': '''public class 보조 {
            static int baha = 시험.baha + 2;
            static int Oka() { return baha; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Metin = "한글\\u0000😀";
            public static int Bitir() {
                if (Metin != "한글\\u0000😀") return 99;
                return (Metin.length() + Metin.charAt(2) + Metin.charAt(3) + Metin.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktorial(int baha) { return baha <= 1 ? 1 : baha * faktorial(baha - 1); }
            static int 연속(int baha) {
                switch (baha) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int baha) {
                switch (baha) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Bitir() { return (faktorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int baha{} = {};'.format(indeks, indeks) for indeks in range(270))
        덧셈 = '+'.join('baha{}'.format(indeks) for indeks in range(270))
        self.자바대조('public class 시험 { public static int Bitir() {' + 선언 +
                    'baha_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] baha = null; return baha.length;', 102),
            ('int[] baha = new int[1]; return baha[1];', 103),
            ('int[] baha = new int[1]; baha[-1] = 3; return 0;', 103),
            ('int baha = -1; return new int[baha].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.düz_gor('public class 시험 { public static int Bitir() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long baha; public static int Bitir() { return 0; }',
            'public static int Bitir() { Object baha = new Object(); return 0; }',
            'public static int Bitir() { System.out.println("hello"); return 0; }',
            'public static int Bitir() { try { return 1; } catch (Exception Hata) { return 2; } }',
            'public static synchronized int Bitir() { return 0; }',
            'public static int Bitir() { return new byte[3].length; }',
            'static native int 외부(); public static int Bitir() { return 외부(); }',
            'int baha; public static int Bitir() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.düz_gor('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.katalog_baha / 'native'
        출력.write_bytes(b'original-output')
        self.düz_gor('public class 시험 { public static int Bitir() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.düz_gor('public class 시험 { public static int Bitir() { return 37; } }')
        self.assertEqual((self.katalog_baha / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.katalog_baha / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.düz_gor('public class 시험 { public static int Bitir() { return ulanyjy.실행권한(); } }',
                    {'ulanyjy': 'public class ulanyjy { public static native int 실행권한(); }'}, niýet='user')
        maglumat = (self.katalog_baha / 'native').read_bytes()
        self.assertEqual(maglumat[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', maglumat, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.katalog_baha / 'native')]))
        # ulanyjy ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.düz_gor('public class 시험 { public static int Bitir() { return enjam_baha.포트읽기(1); } }',
                    {'enjam_baha': 'public class enjam_baha { public static native int 포트읽기(int baha); }'}, 성공=False, niýet='user')

    def test_내보내기검증(self):
        Çeşme = 'public class 시험 { public static int Bitir() { return 0; } static int 호출(int baha) { return baha; } }'
        self.düz_gor(Çeşme, niýet='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.katalog_baha / 'native')]))
        self.düz_gor(Çeşme, 성공=False, 내보냄='bad;name=시험.호출')
        self.düz_gor(Çeşme, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
