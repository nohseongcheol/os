"""liteew_mbir ELF def_ndigel + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.dàmb_xëyma = Path(self.임시.name)

    def tabax_Cosaan(self, Cosaan, 추가=None, 성공=True, luñu_name='linux', 내보냄=None):
        Yoonu_jëmale_lim = []
        for tur_253d1510, Këmb_xëyma in dict({'시험': Cosaan}, **(추가 or {})).items():
            Yoonu_jëmale = self.dàmb_xëyma / (tur_253d1510 + '.java')
            Yoonu_jëmale.write_text(Këmb_xëyma, encoding='utf-8')
            Yoonu_jëmale_lim.append(str(Yoonu_jëmale))
        ndigel = [sys.executable, str(컴파일러), '--target', luñu_name, '--entry', '시험.daw', '-o', str(self.dàmb_xëyma / 'native')]
        if 내보냄 is not None: ndigel += ['--export', 내보냄]
        결과 = subprocess.run(ndigel + Yoonu_jëmale_lim,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('tabax_Cosaan njumte'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.dàmb_xëyma / 'native')], timeout=5).returncode

    def 자바대조(self, Cosaan, 추가=None):
        self.tabax_Cosaan(Cosaan, 추가)
        (self.dàmb_xëyma / 'dalal.java').write_text(
            'public class dalal { public static void main(String[] 인수) { System.exit(시험.daw()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.dàmb_xëyma)] +
                       [str(Yoonu_jëmale) for Yoonu_jëmale in self.dàmb_xëyma.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.dàmb_xëyma), 'dalal'], timeout=5).returncode
        liteew_mbir = self.실행결과()
        self.assertGreaterEqual(liteew_mbir, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 luñutu)')
        self.assertEqual(liteew_mbir, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int daw() {
                int 합 = 7;
                int xëyma = 12345;
                for (int àlluwa_tur = -65; àlluwa_tur <= 65; àlluwa_tur++) {
                    xëyma = xëyma * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(xëyma, àlluwa_tur);
                    합 += (byte)xëyma + (short)xëyma + (char)xëyma;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] xëyma = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int daw() {
                int 합 = 13;
                for (int 가 = 0; 가 < xëyma.length; 가++)
                    for (int 나 = 1; 나 < xëyma.length; 나++)
                        합 = 합 * 31 + xëyma[가] / xëyma[나] + xëyma[가] % xëyma[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] sos_dugal_xabaar(int tolluwaay) { return new int[tolluwaay]; }
            public static int daw() {
                int[] 가 = sos_dugal_xabaar(8); int[] 나 = 가; int[] neen_yëf = new int[0];
                if (가 != 나 || 가 == null || neen_yëf.length != 0 || 가[7] != 0) return 99;
                int xëyma = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return xëyma + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int xëyma = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int daw() { return 계산(1, 2, 3, 4, xëyma) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int xëyma = 3;
            static int 초기값() { return ++xëyma; }
            static int 읽기() { return xëyma; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int xëyma = 보조.읽기() + 1;
            public static int daw() { return xëyma * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int xëyma = 시험.xëyma + 2;
            static int 읽기() { return xëyma; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tekst = "한글\\u0000😀";
            public static int daw() {
                if (Tekst != "한글\\u0000😀") return 99;
                return (Tekst.length() + Tekst.charAt(2) + Tekst.charAt(3) + Tekst.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ci_biir_xala(int xëyma) { return xëyma <= 1 ? 1 : xëyma * ci_biir_xala(xëyma - 1); }
            static int 연속(int xëyma) {
                switch (xëyma) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int xëyma) {
                switch (xëyma) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int daw() { return (ci_biir_xala(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int xëyma{} = {};'.format(àlluwa_tur, àlluwa_tur) for àlluwa_tur in range(270))
        덧셈 = '+'.join('xëyma{}'.format(àlluwa_tur) for àlluwa_tur in range(270))
        self.자바대조('public class 시험 { public static int daw() {' + 선언 +
                    'xëyma_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] xëyma = null; return xëyma.length;', 102),
            ('int[] xëyma = new int[1]; return xëyma[1];', 103),
            ('int[] xëyma = new int[1]; xëyma[-1] = 3; return 0;', 103),
            ('int xëyma = -1; return new int[xëyma].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.tabax_Cosaan('public class 시험 { public static int daw() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long xëyma; public static int daw() { return 0; }',
            'public static int daw() { Object xëyma = new Object(); return 0; }',
            'public static int daw() { System.out.println("hello"); return 0; }',
            'public static int daw() { try { return 1; } catch (Exception njumte) { return 2; } }',
            'public static synchronized int daw() { return 0; }',
            'public static int daw() { return new byte[3].length; }',
            'static native int 외부(); public static int daw() { return 외부(); }',
            'int xëyma; public static int daw() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.tabax_Cosaan('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.dàmb_xëyma / 'native'
        출력.write_bytes(b'original-output')
        self.tabax_Cosaan('public class 시험 { public static int daw() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.tabax_Cosaan('public class 시험 { public static int daw() { return 37; } }')
        self.assertEqual((self.dàmb_xëyma / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.dàmb_xëyma / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.tabax_Cosaan('public class 시험 { public static int daw() { return kiy_jariñoo_internet.실행권한(); } }',
                    {'kiy_jariñoo_internet': 'public class kiy_jariñoo_internet { public static native int 실행권한(); }'}, luñu_name='user')
        mbir = (self.dàmb_xëyma / 'native').read_bytes()
        self.assertEqual(mbir[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', mbir, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.dàmb_xëyma / 'native')]))
        # kiy_jariñoo_internet ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.tabax_Cosaan('public class 시험 { public static int daw() { return toftal_xëyma.포트읽기(1); } }',
                    {'toftal_xëyma': 'public class toftal_xëyma { public static native int 포트읽기(int xëyma); }'}, 성공=False, luñu_name='user')

    def test_내보내기검증(self):
        Cosaan = 'public class 시험 { public static int daw() { return 0; } static int 호출(int xëyma) { return xëyma; } }'
        self.tabax_Cosaan(Cosaan, luñu_name='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.dàmb_xëyma / 'native')]))
        self.tabax_Cosaan(Cosaan, 성공=False, 내보냄='bad;name=시험.호출')
        self.tabax_Cosaan(Cosaan, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
