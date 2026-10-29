"""ڕاستەکی_دەیتا ELF جێبەجێکردن_فەرمان + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.ڕێبەرنامە_نرخ = Path(self.임시.name)

    def دروست_کردن_ژێدەر(self, ژێدەر, 추가=None, 성공=True, مەبەست='linux', 내보냄=None):
        گوزەر_لیست = []
        for ناو, ناوەرۆک_نرخ in dict({'시험': ژێدەر}, **(추가 or {})).items():
            گوزەر = self.ڕێبەرنامە_نرخ / (ناو + '.java')
            گوزەر.write_text(ناوەرۆک_نرخ, encoding='utf-8')
            گوزەر_لیست.append(str(گوزەر))
        فەرمان = [sys.executable, str(컴파일러), '--target', مەبەست, '--entry', '시험.ڕادان', '-o', str(self.ڕێبەرنامە_نرخ / 'native')]
        if 내보냄 is not None: فەرمان += ['--export', 내보냄]
        결과 = subprocess.run(فەرمان + گوزەر_لیست,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('دروست_کردن_ژێدەر هەڵە'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.ڕێبەرنامە_نرخ / 'native')], timeout=5).returncode

    def 자바대조(self, ژێدەر, 추가=None):
        self.دروست_کردن_ژێدەر(ژێدەر, 추가)
        (self.ڕێبەرنامە_نرخ / 'جێدەر.java').write_text(
            'public class جێدەر { public static void main(String[] 인수) { System.exit(시험.ڕادان()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ڕێبەرنامە_نرخ)] +
                       [str(گوزەر) for گوزەر in self.ڕێبەرنامە_نرخ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ڕێبەرنامە_نرخ), 'جێدەر'], timeout=5).returncode
        ڕاستەکی_دەیتا = self.실행결과()
        self.assertGreaterEqual(ڕاستەکی_دەیتا, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 سەلماندن)')
        self.assertEqual(ڕاستەکی_دەیتا, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ڕادان() {
                int 합 = 7;
                int نرخ = 12345;
                for (int پێرست = -65; پێرست <= 65; پێرست++) {
                    نرخ = نرخ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(نرخ, پێرست);
                    합 += (byte)نرخ + (short)نرخ + (char)نرخ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] نرخ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ڕادان() {
                int 합 = 13;
                for (int 가 = 0; 가 < نرخ.length; 가++)
                    for (int 나 = 1; 나 < نرخ.length; 나++)
                        합 = 합 * 31 + نرخ[가] / نرخ[나] + نرخ[가] % نرخ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] دروستکردن_تێنووسین(int گۆڕینی_ئەندازە) { return new int[گۆڕینی_ئەندازە]; }
            public static int ڕادان() {
                int[] 가 = دروستکردن_تێنووسین(8); int[] 나 = 가; int[] بەتاڵ_شت = new int[0];
                if (가 != 나 || 가 == null || بەتاڵ_شت.length != 0 || 가[7] != 0) return 99;
                int نرخ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return نرخ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int نرخ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ڕادان() { return 계산(1, 2, 3, 4, نرخ) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int نرخ = 3;
            static int 초기값() { return ++نرخ; }
            static int 읽기() { return نرخ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int نرخ = 보조.읽기() + 1;
            public static int ڕادان() { return نرخ * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int نرخ = 시험.نرخ + 2;
            static int 읽기() { return نرخ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String دەق = "한글\\u0000😀";
            public static int ڕادان() {
                if (دەق != "한글\\u0000😀") return 99;
                return (دەق.length() + دەق.charAt(2) + دەق.charAt(3) + دەق.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int کەرت(int نرخ) { return نرخ <= 1 ? 1 : نرخ * کەرت(نرخ - 1); }
            static int 연속(int نرخ) {
                switch (نرخ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int نرخ) {
                switch (نرخ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ڕادان() { return (کەرت(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int نرخ{} = {};'.format(پێرست, پێرست) for پێرست in range(270))
        덧셈 = '+'.join('نرخ{}'.format(پێرست) for پێرست in range(270))
        self.자바대조('public class 시험 { public static int ڕادان() {' + 선언 +
                    'نرخ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] نرخ = null; return نرخ.length;', 102),
            ('int[] نرخ = new int[1]; return نرخ[1];', 103),
            ('int[] نرخ = new int[1]; نرخ[-1] = 3; return 0;', 103),
            ('int نرخ = -1; return new int[نرخ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.دروست_کردن_ژێدەر('public class 시험 { public static int ڕادان() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long نرخ; public static int ڕادان() { return 0; }',
            'public static int ڕادان() { Object نرخ = new Object(); return 0; }',
            'public static int ڕادان() { System.out.println("hello"); return 0; }',
            'public static int ڕادان() { try { return 1; } catch (Exception هەڵە) { return 2; } }',
            'public static synchronized int ڕادان() { return 0; }',
            'public static int ڕادان() { return new byte[3].length; }',
            'static native int 외부(); public static int ڕادان() { return 외부(); }',
            'int نرخ; public static int ڕادان() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.دروست_کردن_ژێدەر('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ڕێبەرنامە_نرخ / 'native'
        출력.write_bytes(b'original-output')
        self.دروست_کردن_ژێدەر('public class 시험 { public static int ڕادان() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.دروست_کردن_ژێدەر('public class 시험 { public static int ڕادان() { return 37; } }')
        self.assertEqual((self.ڕێبەرنامە_نرخ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.ڕێبەرنامە_نرخ / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.دروست_کردن_ژێدەر('public class 시험 { public static int ڕادان() { return بەکارهێنەر.실행권한(); } }',
                    {'بەکارهێنەر': 'public class بەکارهێنەر { public static native int 실행권한(); }'}, مەبەست='user')
        دەیتا = (self.ڕێبەرنامە_نرخ / 'native').read_bytes()
        self.assertEqual(دەیتا[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', دەیتا, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ڕێبەرنامە_نرخ / 'native')]))
        # بەکارهێنەر ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.دروست_کردن_ژێدەر('public class 시험 { public static int ڕادان() { return ئامێر_نرخ.포트읽기(1); } }',
                    {'ئامێر_نرخ': 'public class ئامێر_نرخ { public static native int 포트읽기(int نرخ); }'}, 성공=False, مەبەست='user')

    def test_내보내기검증(self):
        ژێدەر = 'public class 시험 { public static int ڕادان() { return 0; } static int 호출(int نرخ) { return نرخ; } }'
        self.دروست_کردن_ژێدەر(ژێدەر, مەبەست='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ڕێبەرنامە_نرخ / 'native')]))
        self.دروست_کردن_ژێدەر(ژێدەر, 성공=False, 내보냄='bad;name=시험.호출')
        self.دروست_کردن_ژێدەر(ژێدەر, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
