"""اصل_کوائف ELF نفاذ_کریں_حکم + OpenJDK پیمائش 대조. 임시 시험 자료만 생성한다."""
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
        self.ڈائریکٹری_قدر = Path(self.임시.name)

    def مرتب_کریں_ماخذ(self, ماخذ_فائل, 추가=None, 성공=True, ہدف='linux', 내보냄=None):
        راہ_فہرست = []
        for نام, مشمول_قدر in dict({'시험': ماخذ_فائل}, **(추가 or {})).items():
            راستہ_2 = self.ڈائریکٹری_قدر / (نام + '.java')
            راستہ_2.write_text(مشمول_قدر, encoding='utf-8')
            راہ_فہرست.append(str(راستہ_2))
        حکم = [sys.executable, str(컴파일러), '--target', ہدف, '--entry', '시험.چلائیں', '-o', str(self.ڈائریکٹری_قدر / 'native')]
        if 내보냄 is not None: حکم += ['--export', 내보냄]
        پیمائش = subprocess.run(حکم + راہ_فہرست,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(پیمائش.returncode, 0, پیمائش.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(پیمائش.returncode, 0)
            self.assertIn('مرتب_کریں_ماخذ غلطی'.encode(), پیمائش.stderr)
        return پیمائش

    def 실행결과(self):
        return subprocess.run([str(self.ڈائریکٹری_قدر / 'native')], timeout=5).returncode

    def 자바대조(self, ماخذ_فائل, 추가=None):
        self.مرتب_کریں_ماخذ(ماخذ_فائل, 추가)
        (self.ڈائریکٹری_قدر / 'میزبان.java').write_text(
            'public class میزبان { public static void main(String[] دلائل) { System.exit(시험.چلائیں()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ڈائریکٹری_قدر)] +
                       [str(راستہ_2) for راستہ_2 in self.ڈائریکٹری_قدر.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ڈائریکٹری_قدر), 'میزبان'], timeout=5).returncode
        اصل_کوائف = self.실행결과()
        self.assertGreaterEqual(اصل_کوائف, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 تصدیق_کریں)')
        self.assertEqual(اصل_کوائف, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int چلائیں() {
                int 합 = 7;
                int قدر = 12345;
                for (int اشاریہ = -65; اشاریہ <= 65; اشاریہ++) {
                    قدر = قدر * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(قدر, اشاریہ);
                    합 += (byte)قدر + (short)قدر + (char)قدر;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] قدر = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int چلائیں() {
                int 합 = 13;
                for (int 가 = 0; 가 < قدر.length; 가++)
                    for (int 나 = 1; 나 < قدر.length; 나++)
                        합 = 합 * 31 + قدر[가] / قدر[나] + قدر[가] % قدر[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] بنائیں_اندراج(int حجم) { return new int[حجم]; }
            public static int چلائیں() {
                int[] 가 = بنائیں_اندراج(8); int[] 나 = 가; int[] خالی_آبجیکٹ = new int[0];
                if (가 != 나 || 가 == null || خالی_آبجیکٹ.length != 0 || 가[7] != 0) return 99;
                int قدر = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return قدر + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int قدر = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int چلائیں() { return 계산(1, 2, 3, 4, قدر) + 보조.پڑھیں(); }
        }''', {'보조': '''public class 보조 {
            static int قدر = 3;
            static int 초기값() { return ++قدر; }
            static int پڑھیں() { return قدر; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int قدر = 보조.پڑھیں() + 1;
            public static int چلائیں() { return قدر * 10 + 보조.پڑھیں(); }
        }''', {'보조': '''public class 보조 {
            static int قدر = 시험.قدر + 2;
            static int پڑھیں() { return قدر; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String متن = "한글\\u0000😀";
            public static int چلائیں() {
                if (متن != "한글\\u0000😀") return 99;
                return (متن.length() + متن.charAt(2) + متن.charAt(3) + متن.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int عامل_دار(int قدر) { return قدر <= 1 ? 1 : قدر * عامل_دار(قدر - 1); }
            static int 연속(int قدر) {
                switch (قدر) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int قدر) {
                switch (قدر) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int چلائیں() { return (عامل_دار(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int قدر{} = {};'.format(اشاریہ, اشاریہ) for اشاریہ in range(270))
        덧셈 = '+'.join('قدر{}'.format(اشاریہ) for اشاریہ in range(270))
        self.자바대조('public class 시험 { public static int چلائیں() {' + 선언 +
                    'قدر_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] قدر = null; return قدر.length;', 102),
            ('int[] قدر = new int[1]; return قدر[1];', 103),
            ('int[] قدر = new int[1]; قدر[-1] = 3; return 0;', 103),
            ('int قدر = -1; return new int[قدر].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for جسم_قدر, 기대 in 경우들:
            with self.subTest(جسم_قدر=جسم_قدر):
                self.مرتب_کریں_ماخذ('public class 시험 { public static int چلائیں() { ' + جسم_قدر + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long قدر; public static int چلائیں() { return 0; }',
            'public static int چلائیں() { Object قدر = new Object(); return 0; }',
            'public static int چلائیں() { System.out.println("hello"); return 0; }',
            'public static int چلائیں() { try { return 1; } catch (Exception غلطی) { return 2; } }',
            'public static synchronized int چلائیں() { return 0; }',
            'public static int چلائیں() { return new byte[3].length; }',
            'static native int 외부(); public static int چلائیں() { return 외부(); }',
            'int قدر; public static int چلائیں() { return 0; }',
        ]
        for جسم_قدر in 경우들:
            with self.subTest(جسم_قدر=جسم_قدر):
                self.مرتب_کریں_ماخذ('public class 시험 { ' + جسم_قدر + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        اخراج_کا_مقام = self.ڈائریکٹری_قدر / 'native'
        اخراج_کا_مقام.write_bytes(b'original-output')
        self.مرتب_کریں_ماخذ('public class 시험 { public static int چلائیں() { return missing; } }', 성공=False)
        self.assertEqual(اخراج_کا_مقام.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.مرتب_کریں_ماخذ('public class 시험 { public static int چلائیں() { return 37; } }')
        self.assertEqual((self.ڈائریکٹری_قدر / 'native').read_bytes()[:5], b'\x7fELF\x01')
        لُک_اپ_جدول = subprocess.check_output(['readelf', '-l', str(self.ڈائریکٹری_قدر / 'native')])
        self.assertNotIn(b'INTERP', لُک_اپ_جدول)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.مرتب_کریں_ماخذ('public class 시험 { public static int چلائیں() { return صارف.실행권한(); } }',
                    {'صارف': 'public class صارف { public static native int 실행권한(); }'}, ہدف='user')
        کوائف = (self.ڈائریکٹری_قدر / 'native').read_bytes()
        self.assertEqual(کوائف[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', کوائف, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ڈائریکٹری_قدر / 'native')]))
        # صارف ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.مرتب_کریں_ماخذ('public class 시험 { public static int چلائیں() { return آلہ_قدر.포트읽기(1); } }',
                    {'آلہ_قدر': 'public class آلہ_قدر { public static native int 포트읽기(int قدر); }'}, 성공=False, ہدف='user')

    def test_내보내기검증(self):
        ماخذ_فائل = 'public class 시험 { public static int چلائیں() { return 0; } static int 호출(int قدر) { return قدر; } }'
        self.مرتب_کریں_ماخذ(ماخذ_فائل, ہدف='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ڈائریکٹری_قدر / 'native')]))
        self.مرتب_کریں_ماخذ(ماخذ_فائل, 성공=False, 내보냄='bad;name=시험.호출')
        self.مرتب_کریں_ماخذ(ماخذ_فائل, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
