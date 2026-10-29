"""اصلي_ڪوائف ELF تعميل_ڪرڻ_حڪم + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.ڊائريڪٽري_قدر = Path(self.임시.name)

    def گڏ_ڪريو_ماخذ(self, ماخذ, 추가=None, 성공=True, هدف='linux', 내보냄=None):
        راههه_فهرست = []
        for نالو, مواد_قدر in dict({'시험': ماخذ}, **(추가 or {})).items():
            راههه = self.ڊائريڪٽري_قدر / (نالو + '.java')
            راههه.write_text(مواد_قدر, encoding='utf-8')
            راههه_فهرست.append(str(راههه))
        حڪم = [sys.executable, str(컴파일러), '--target', هدف, '--entry', '시험.هلائڻ', '-o', str(self.ڊائريڪٽري_قدر / 'native')]
        if 내보냄 is not None: حڪم += ['--export', 내보냄]
        결과 = subprocess.run(حڪم + راههه_فهرست,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('گڏ_ڪريو_ماخذ نقص'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.ڊائريڪٽري_قدر / 'native')], timeout=5).returncode

    def 자바대조(self, ماخذ, 추가=None):
        self.گڏ_ڪريو_ماخذ(ماخذ, 추가)
        (self.ڊائريڪٽري_قدر / 'مهمان.java').write_text(
            'public class مهمان { public static void main(String[] 인수) { System.exit(시험.هلائڻ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ڊائريڪٽري_قدر)] +
                       [str(راههه) for راههه in self.ڊائريڪٽري_قدر.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ڊائريڪٽري_قدر), 'مهمان'], timeout=5).returncode
        اصلي_ڪوائف = self.실행결과()
        self.assertGreaterEqual(اصلي_ڪوائف, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 تصديق_ڪريو)')
        self.assertEqual(اصلي_ڪوائف, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int هلائڻ() {
                int 합 = 7;
                int قدر = 12345;
                for (int ابتدائي = -65; ابتدائي <= 65; ابتدائي++) {
                    قدر = قدر * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(قدر, ابتدائي);
                    합 += (byte)قدر + (short)قدر + (char)قدر;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] قدر = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int هلائڻ() {
                int 합 = 13;
                for (int 가 = 0; 가 < قدر.length; 가++)
                    for (int 나 = 1; 나 < قدر.length; 나++)
                        합 = 합 * 31 + قدر[가] / قدر[나] + قدر[가] % قدر[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ٺاھيو_داخلا(int سائيز) { return new int[سائيز]; }
            public static int هلائڻ() {
                int[] 가 = ٺاھيو_داخلا(8); int[] 나 = 가; int[] خالي_عنصر = new int[0];
                if (가 != 나 || 가 == null || خالي_عنصر.length != 0 || 가[7] != 0) return 99;
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
            public static int هلائڻ() { return 계산(1, 2, 3, 4, قدر) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int قدر = 3;
            static int 초기값() { return ++قدر; }
            static int 읽기() { return قدر; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int قدر = 보조.읽기() + 1;
            public static int هلائڻ() { return قدر * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int قدر = 시험.قدر + 2;
            static int 읽기() { return قدر; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String متن = "한글\\u0000😀";
            public static int هلائڻ() {
                if (متن != "한글\\u0000😀") return 99;
                return (متن.length() + متن.charAt(2) + متن.charAt(3) + متن.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ڪارخاني_جو(int قدر) { return قدر <= 1 ? 1 : قدر * ڪارخاني_جو(قدر - 1); }
            static int 연속(int قدر) {
                switch (قدر) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int قدر) {
                switch (قدر) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int هلائڻ() { return (ڪارخاني_جو(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int قدر{} = {};'.format(ابتدائي, ابتدائي) for ابتدائي in range(270))
        덧셈 = '+'.join('قدر{}'.format(ابتدائي) for ابتدائي in range(270))
        self.자바대조('public class 시험 { public static int هلائڻ() {' + 선언 +
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
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.گڏ_ڪريو_ماخذ('public class 시험 { public static int هلائڻ() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long قدر; public static int هلائڻ() { return 0; }',
            'public static int هلائڻ() { Object قدر = new Object(); return 0; }',
            'public static int هلائڻ() { System.out.println("hello"); return 0; }',
            'public static int هلائڻ() { try { return 1; } catch (Exception نقص) { return 2; } }',
            'public static synchronized int هلائڻ() { return 0; }',
            'public static int هلائڻ() { return new byte[3].length; }',
            'static native int 외부(); public static int هلائڻ() { return 외부(); }',
            'int قدر; public static int هلائڻ() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.گڏ_ڪريو_ماخذ('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ڊائريڪٽري_قدر / 'native'
        출력.write_bytes(b'original-output')
        self.گڏ_ڪريو_ماخذ('public class 시험 { public static int هلائڻ() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.گڏ_ڪريو_ماخذ('public class 시험 { public static int هلائڻ() { return 37; } }')
        self.assertEqual((self.ڊائريڪٽري_قدر / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.ڊائريڪٽري_قدر / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.گڏ_ڪريو_ماخذ('public class 시험 { public static int هلائڻ() { return صارف.실행권한(); } }',
                    {'صارف': 'public class صارف { public static native int 실행권한(); }'}, هدف='user')
        ڪوائف = (self.ڊائريڪٽري_قدر / 'native').read_bytes()
        self.assertEqual(ڪوائف[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ڪوائف, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ڊائريڪٽري_قدر / 'native')]))
        # صارف ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.گڏ_ڪريو_ماخذ('public class 시험 { public static int هلائڻ() { return آلو_قدر.포트읽기(1); } }',
                    {'آلو_قدر': 'public class آلو_قدر { public static native int 포트읽기(int قدر); }'}, 성공=False, هدف='user')

    def test_내보내기검증(self):
        ماخذ = 'public class 시험 { public static int هلائڻ() { return 0; } static int 호출(int قدر) { return قدر; } }'
        self.گڏ_ڪريو_ماخذ(ماخذ, هدف='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ڊائريڪٽري_قدر / 'native')]))
        self.گڏ_ڪريو_ماخذ(ماخذ, 성공=False, 내보냄='bad;name=시험.호출')
        self.گڏ_ڪريو_ماخذ(ماخذ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
