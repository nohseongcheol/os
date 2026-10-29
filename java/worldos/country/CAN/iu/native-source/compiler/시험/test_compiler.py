"""taannallarik_titiqqat ELF 실행 + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.tukimuagutiit_atuutilik = Path(self.임시.name)

    def sanali_pivviujuq(self, pivviujuq, 추가=None, 성공=True, turaagaq='linux', 내보냄=None):
        aqqut_Titiqpalliagaq = []
        for atiq, Ilulingit_atuutilik in dict({'시험': pivviujuq}, **(추가 or {})).items():
            aqqut = self.tukimuagutiit_atuutilik / (atiq + '.java')
            aqqut.write_text(Ilulingit_atuutilik, encoding='utf-8')
            aqqut_Titiqpalliagaq.append(str(aqqut))
        piqujijjut = [sys.executable, str(컴파일러), '--target', turaagaq, '--entry', '시험.시작', '-o', str(self.tukimuagutiit_atuutilik / 'native')]
        if 내보냄 is not None: piqujijjut += ['--export', 내보냄]
        결과 = subprocess.run(piqujijjut + aqqut_Titiqpalliagaq,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('sanali_pivviujuq tammarniq'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.tukimuagutiit_atuutilik / 'native')], timeout=5).returncode

    def 자바대조(self, pivviujuq, 추가=None):
        self.sanali_pivviujuq(pivviujuq, 추가)
        (self.tukimuagutiit_atuutilik / 'tuttarvik.java').write_text(
            'public class tuttarvik { public static void main(String[] 인수) { System.exit(시험.시작()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.tukimuagutiit_atuutilik)] +
                       [str(aqqut) for aqqut in self.tukimuagutiit_atuutilik.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.tukimuagutiit_atuutilik), 'tuttarvik'], timeout=5).returncode
        taannallarik_titiqqat = self.실행결과()
        self.assertGreaterEqual(taannallarik_titiqqat, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 nalunairli_1aacb54c)')
        self.assertEqual(taannallarik_titiqqat, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int 시작() {
                int 합 = 7;
                int atuutilik = 12345;
                for (int nalunaiqsimavik = -65; nalunaiqsimavik <= 65; nalunaiqsimavik++) {
                    atuutilik = atuutilik * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(atuutilik, nalunaiqsimavik);
                    합 += (byte)atuutilik + (short)atuutilik + (char)atuutilik;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] atuutilik = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int 시작() {
                int 합 = 13;
                for (int 가 = 0; 가 < atuutilik.length; 가++)
                    for (int 나 = 1; 나 < atuutilik.length; 나++)
                        합 = 합 * 31 + atuutilik[가] / atuutilik[나] + atuutilik[가] % atuutilik[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int anininga) { return new int[anininga]; }
            public static int 시작() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int atuutilik = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return atuutilik + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int atuutilik = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int 시작() { return 계산(1, 2, 3, 4, atuutilik) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int atuutilik = 3;
            static int 초기값() { return ++atuutilik; }
            static int 읽기() { return atuutilik; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int atuutilik = 보조.읽기() + 1;
            public static int 시작() { return atuutilik * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int atuutilik = 시험.atuutilik + 2;
            static int 읽기() { return atuutilik; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String titiqqaq = "한글\\u0000😀";
            public static int 시작() {
                if (titiqqaq != "한글\\u0000😀") return 99;
                return (titiqqaq.length() + titiqqaq.charAt(2) + titiqqaq.charAt(3) + titiqqaq.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int atuutilik) { return atuutilik <= 1 ? 1 : atuutilik * 계승(atuutilik - 1); }
            static int 연속(int atuutilik) {
                switch (atuutilik) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int atuutilik) {
                switch (atuutilik) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int 시작() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int atuutilik{} = {};'.format(nalunaiqsimavik, nalunaiqsimavik) for nalunaiqsimavik in range(270))
        덧셈 = '+'.join('atuutilik{}'.format(nalunaiqsimavik) for nalunaiqsimavik in range(270))
        self.자바대조('public class 시험 { public static int 시작() {' + 선언 +
                    'atuutilik_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] atuutilik = null; return atuutilik.length;', 102),
            ('int[] atuutilik = new int[1]; return atuutilik[1];', 103),
            ('int[] atuutilik = new int[1]; atuutilik[-1] = 3; return 0;', 103),
            ('int atuutilik = -1; return new int[atuutilik].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.sanali_pivviujuq('public class 시험 { public static int 시작() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long atuutilik; public static int 시작() { return 0; }',
            'public static int 시작() { Object atuutilik = new Object(); return 0; }',
            'public static int 시작() { System.out.println("hello"); return 0; }',
            'public static int 시작() { try { return 1; } catch (Exception tammarniq) { return 2; } }',
            'public static synchronized int 시작() { return 0; }',
            'public static int 시작() { return new byte[3].length; }',
            'static native int 외부(); public static int 시작() { return 외부(); }',
            'int atuutilik; public static int 시작() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.sanali_pivviujuq('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.tukimuagutiit_atuutilik / 'native'
        출력.write_bytes(b'original-output')
        self.sanali_pivviujuq('public class 시험 { public static int 시작() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.sanali_pivviujuq('public class 시험 { public static int 시작() { return 37; } }')
        self.assertEqual((self.tukimuagutiit_atuutilik / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.tukimuagutiit_atuutilik / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.sanali_pivviujuq('public class 시험 { public static int 시작() { return atuqtuq.실행권한(); } }',
                    {'atuqtuq': 'public class atuqtuq { public static native int 실행권한(); }'}, turaagaq='user')
        titiqqat = (self.tukimuagutiit_atuutilik / 'native').read_bytes()
        self.assertEqual(titiqqat[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', titiqqat, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.tukimuagutiit_atuutilik / 'native')]))
        # atuqtuq ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.sanali_pivviujuq('public class 시험 { public static int 시작() { return sunakkutaaq_atuutilik.포트읽기(1); } }',
                    {'sunakkutaaq_atuutilik': 'public class sunakkutaaq_atuutilik { public static native int 포트읽기(int atuutilik); }'}, 성공=False, turaagaq='user')

    def test_내보내기검증(self):
        pivviujuq = 'public class 시험 { public static int 시작() { return 0; } static int 호출(int atuutilik) { return atuutilik; } }'
        self.sanali_pivviujuq(pivviujuq, turaagaq='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.tukimuagutiit_atuutilik / 'native')]))
        self.sanali_pivviujuq(pivviujuq, 성공=False, 내보냄='bad;name=시험.호출')
        self.sanali_pivviujuq(pivviujuq, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
