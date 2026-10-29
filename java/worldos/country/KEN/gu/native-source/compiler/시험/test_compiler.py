"""વાસ્તવિક_ડેટા ELF અમલ_કરો_આદેશ + OpenJDK પરિમાણ 대조. 임시 시험 자료만 생성한다."""
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
        self.નિર્દેશિકા_મૂલ્ય = Path(self.임시.name)

    def બિલ્ડ_કરો_સ્રોત(self, સ્રોત, 추가=None, 성공=True, લક્ષ્ય='linux', 내보냄=None):
        પાથ_સૂચી = []
        for નામ, સામગ્રી_મૂલ્ય in dict({'시험': સ્રોત}, **(추가 or {})).items():
            પથ = self.નિર્દેશિકા_મૂલ્ય / (નામ + '.java')
            પથ.write_text(સામગ્રી_મૂલ્ય, encoding='utf-8')
            પાથ_સૂચી.append(str(પથ))
        આદેશ = [sys.executable, str(컴파일러), '--target', લક્ષ્ય, '--entry', '시험.ચલાવો_2', '-o', str(self.નિર્દેશિકા_મૂલ્ય / 'native')]
        if 내보냄 is not None: આદેશ += ['--export', 내보냄]
        પરિમાણ = subprocess.run(આદેશ + પાથ_સૂચી,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(પરિમાણ.returncode, 0, પરિમાણ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(પરિમાણ.returncode, 0)
            self.assertIn('બિલ્ડ_કરો_સ્રોત ભૂલ'.encode(), પરિમાણ.stderr)
        return પરિમાણ

    def 실행결과(self):
        return subprocess.run([str(self.નિર્દેશિકા_મૂલ્ય / 'native')], timeout=5).returncode

    def 자바대조(self, સ્રોત, 추가=None):
        self.બિલ્ડ_કરો_સ્રોત(સ્રોત, 추가)
        (self.નિર્દેશિકા_મૂલ્ય / 'હોસ્ટ.java').write_text(
            'public class હોસ્ટ { public static void main(String[] દલીલો) { System.exit(시험.ચલાવો_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.નિર્દેશિકા_મૂલ્ય)] +
                       [str(પથ) for પથ in self.નિર્દેશિકા_મૂલ્ય.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.નિર્દેશિકા_મૂલ્ય), 'હોસ્ટ'], timeout=5).returncode
        વાસ્તવિક_ડેટા = self.실행결과()
        self.assertGreaterEqual(વાસ્તવિક_ડેટા, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ચકાસવું)')
        self.assertEqual(વાસ્તવિક_ડેટા, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ચલાવો_2() {
                int 합 = 7;
                int મૂલ્ય = 12345;
                for (int અનુક્રમણિકા = -65; અનુક્રમણિકા <= 65; અનુક્રમણિકા++) {
                    મૂલ્ય = મૂલ્ય * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(મૂલ્ય, અનુક્રમણિકા);
                    합 += (byte)મૂલ્ય + (short)મૂલ્ય + (char)મૂલ્ય;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] મૂલ્ય = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ચલાવો_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < મૂલ્ય.length; 가++)
                    for (int 나 = 1; 나 < મૂલ્ય.length; 나++)
                        합 = 합 * 31 + મૂલ્ય[가] / મૂલ્ય[나] + મૂલ્ય[가] % મૂલ્ય[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] બનાવો_પ્રવેશ(int માપ) { return new int[માપ]; }
            public static int ચલાવો_2() {
                int[] 가 = બનાવો_પ્રવેશ(8); int[] 나 = 가; int[] ખાલી_ઑબ્જેક્ટ = new int[0];
                if (가 != 나 || 가 == null || ખાલી_ઑબ્જેક્ટ.length != 0 || 가[7] != 0) return 99;
                int મૂલ્ય = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return મૂલ્ય + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int મૂલ્ય = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ચલાવો_2() { return 계산(1, 2, 3, 4, મૂલ્ય) + 보조.વાંચો(); }
        }''', {'보조': '''public class 보조 {
            static int મૂલ્ય = 3;
            static int 초기값() { return ++મૂલ્ય; }
            static int વાંચો() { return મૂલ્ય; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int મૂલ્ય = 보조.વાંચો() + 1;
            public static int ચલાવો_2() { return મૂલ્ય * 10 + 보조.વાંચો(); }
        }''', {'보조': '''public class 보조 {
            static int મૂલ્ય = 시험.મૂલ્ય + 2;
            static int વાંચો() { return મૂલ્ય; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String લખાણ = "한글\\u0000😀";
            public static int ચલાવો_2() {
                if (લખાણ != "한글\\u0000😀") return 99;
                return (લખાણ.length() + લખાણ.charAt(2) + લખાણ.charAt(3) + લખાણ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int અવયવ_2474c4d7(int મૂલ્ય) { return મૂલ્ય <= 1 ? 1 : મૂલ્ય * અવયવ_2474c4d7(મૂલ્ય - 1); }
            static int 연속(int મૂલ્ય) {
                switch (મૂલ્ય) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int મૂલ્ય) {
                switch (મૂલ્ય) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ચલાવો_2() { return (અવયવ_2474c4d7(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int મૂલ્ય{} = {};'.format(અનુક્રમણિકા, અનુક્રમણિકા) for અનુક્રમણિકા in range(270))
        덧셈 = '+'.join('મૂલ્ય{}'.format(અનુક્રમણિકા) for અનુક્રમણિકા in range(270))
        self.자바대조('public class 시험 { public static int ચલાવો_2() {' + 선언 +
                    'મૂલ્ય_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] મૂલ્ય = null; return મૂલ્ય.length;', 102),
            ('int[] મૂલ્ય = new int[1]; return મૂલ્ય[1];', 103),
            ('int[] મૂલ્ય = new int[1]; મૂલ્ય[-1] = 3; return 0;', 103),
            ('int મૂલ્ય = -1; return new int[મૂલ્ય].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for મુખ્ય_ભાગ_મૂલ્ય, 기대 in 경우들:
            with self.subTest(મુખ્ય_ભાગ_મૂલ્ય=મુખ્ય_ભાગ_મૂલ્ય):
                self.બિલ્ડ_કરો_સ્રોત('public class 시험 { public static int ચલાવો_2() { ' + મુખ્ય_ભાગ_મૂલ્ય + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long મૂલ્ય; public static int ચલાવો_2() { return 0; }',
            'public static int ચલાવો_2() { Object મૂલ્ય = new Object(); return 0; }',
            'public static int ચલાવો_2() { System.out.println("hello"); return 0; }',
            'public static int ચલાવો_2() { try { return 1; } catch (Exception ભૂલ) { return 2; } }',
            'public static synchronized int ચલાવો_2() { return 0; }',
            'public static int ચલાવો_2() { return new byte[3].length; }',
            'static native int 외부(); public static int ચલાવો_2() { return 외부(); }',
            'int મૂલ્ય; public static int ચલાવો_2() { return 0; }',
        ]
        for મુખ્ય_ભાગ_મૂલ્ય in 경우들:
            with self.subTest(મુખ્ય_ભાગ_મૂલ્ય=મુખ્ય_ભાગ_મૂલ્ય):
                self.બિલ્ડ_કરો_સ્રોત('public class 시험 { ' + મુખ્ય_ભાગ_મૂલ્ય + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        આઉટપુટ = self.નિર્દેશિકા_મૂલ્ય / 'native'
        આઉટપુટ.write_bytes(b'original-output')
        self.બિલ્ડ_કરો_સ્રોત('public class 시험 { public static int ચલાવો_2() { return missing; } }', 성공=False)
        self.assertEqual(આઉટપુટ.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.બિલ્ડ_કરો_સ્રોત('public class 시험 { public static int ચલાવો_2() { return 37; } }')
        self.assertEqual((self.નિર્દેશિકા_મૂલ્ય / 'native').read_bytes()[:5], b'\x7fELF\x01')
        લુકઅપ_કોષ્ટક = subprocess.check_output(['readelf', '-l', str(self.નિર્દેશિકા_મૂલ્ય / 'native')])
        self.assertNotIn(b'INTERP', લુકઅપ_કોષ્ટક)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.બિલ્ડ_કરો_સ્રોત('public class 시험 { public static int ચલાવો_2() { return ઉપયોગકર્તા.실행권한(); } }',
                    {'ઉપયોગકર્તા': 'public class ઉપયોગકર્તા { public static native int 실행권한(); }'}, લક્ષ્ય='user')
        ડેટા = (self.નિર્દેશિકા_મૂલ્ય / 'native').read_bytes()
        self.assertEqual(ડેટા[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ડેટા, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.નિર્દેશિકા_મૂલ્ય / 'native')]))
        # ઉપયોગકર્તા ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.બિલ્ડ_કરો_સ્રોત('public class 시험 { public static int ચલાવો_2() { return ડિવાઇસ_મૂલ્ય.포트읽기(1); } }',
                    {'ડિવાઇસ_મૂલ્ય': 'public class ડિવાઇસ_મૂલ્ય { public static native int 포트읽기(int મૂલ્ય); }'}, 성공=False, લક્ષ્ય='user')

    def test_내보내기검증(self):
        સ્રોત = 'public class 시험 { public static int ચલાવો_2() { return 0; } static int 호출(int મૂલ્ય) { return મૂલ્ય; } }'
        self.બિલ્ડ_કરો_સ્રોત(સ્રોત, લક્ષ્ય='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.નિર્દેશિકા_મૂલ્ય / 'native')]))
        self.બિલ્ડ_કરો_સ્રોત(સ્રોત, 성공=False, 내보냄='bad;name=시험.호출')
        self.બિલ્ડ_કરો_સ્રોત(સ્રોત, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
