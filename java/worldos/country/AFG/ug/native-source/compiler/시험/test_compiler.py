"""ھەقىقىي_مەلۇمات ELF ئىجرا_قىلىش_بۇيرۇق + OpenJDK ئۆلچەم 대조. 임시 시험 자료만 생성한다."""
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
        self.مۇندەرىجە_قىممىتى = Path(self.임시.name)

    def قۇرماق_مەنبە(self, مەنبە, 추가=None, 성공=True, نىشان='linux', 내보냄=None):
        يول_تىزىم = []
        for ئاتى, مەزمۇن_قىممىتى in dict({'시험': مەنبە}, **(추가 or {})).items():
            يول = self.مۇندەرىجە_قىممىتى / (ئاتى + '.java')
            يول.write_text(مەزمۇن_قىممىتى, encoding='utf-8')
            يول_تىزىم.append(str(يول))
        بۇيرۇق = [sys.executable, str(컴파일러), '--target', نىشان, '--entry', '시험.ئىجرا_قىل_2', '-o', str(self.مۇندەرىجە_قىممىتى / 'native')]
        if 내보냄 is not None: بۇيرۇق += ['--export', 내보냄]
        ئۆلچەم = subprocess.run(بۇيرۇق + يول_تىزىم,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ئۆلچەم.returncode, 0, ئۆلچەم.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ئۆلچەم.returncode, 0)
            self.assertIn('قۇرماق_مەنبە خاتالىق'.encode(), ئۆلچەم.stderr)
        return ئۆلچەم

    def 실행결과(self):
        return subprocess.run([str(self.مۇندەرىجە_قىممىتى / 'native')], timeout=5).returncode

    def 자바대조(self, مەنبە, 추가=None):
        self.قۇرماق_مەنبە(مەنبە, 추가)
        (self.مۇندەرىجە_قىممىتى / 'باقار.java').write_text(
            'public class باقار { public static void main(String[] ئۆزگەرگۈچىلەر) { System.exit(시험.ئىجرا_قىل_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.مۇندەرىجە_قىممىتى)] +
                       [str(يول) for يول in self.مۇندەرىجە_قىممىتى.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.مۇندەرىجە_قىممىتى), 'باقار'], timeout=5).returncode
        ھەقىقىي_مەلۇمات = self.실행결과()
        self.assertGreaterEqual(ھەقىقىي_مەلۇمات, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 دەلىللىمەك)')
        self.assertEqual(ھەقىقىي_مەلۇمات, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ئىجرا_قىل_2() {
                int 합 = 7;
                int قىممىتى = 12345;
                for (int ئىندېكس = -65; ئىندېكس <= 65; ئىندېكس++) {
                    قىممىتى = قىممىتى * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(قىممىتى, ئىندېكس);
                    합 += (byte)قىممىتى + (short)قىممىتى + (char)قىممىتى;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] قىممىتى = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ئىجرا_قىل_2() {
                int 합 = 13;
                for (int 가 = 0; 가 < قىممىتى.length; 가++)
                    for (int 나 = 1; 나 < قىممىتى.length; 나++)
                        합 = 합 * 31 + قىممىتى[가] / قىممىتى[나] + قىممىتى[가] % قىممىتى[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] قۇرۇش_كىرگۈزۈش(int چوڭلۇقى) { return new int[چوڭلۇقى]; }
            public static int ئىجرا_قىل_2() {
                int[] 가 = قۇرۇش_كىرگۈزۈش(8); int[] 나 = 가; int[] بوش_ئوبيېكت = new int[0];
                if (가 != 나 || 가 == null || بوش_ئوبيېكت.length != 0 || 가[7] != 0) return 99;
                int قىممىتى = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return قىممىتى + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int قىممىتى = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ئىجرا_قىل_2() { return 계산(1, 2, 3, 4, قىممىتى) + 보조.ئوقۇ(); }
        }''', {'보조': '''public class 보조 {
            static int قىممىتى = 3;
            static int 초기값() { return ++قىممىتى; }
            static int ئوقۇ() { return قىممىتى; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int قىممىتى = 보조.ئوقۇ() + 1;
            public static int ئىجرا_قىل_2() { return قىممىتى * 10 + 보조.ئوقۇ(); }
        }''', {'보조': '''public class 보조 {
            static int قىممىتى = 시험.قىممىتى + 2;
            static int ئوقۇ() { return قىممىتى; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String تېكىست = "한글\\u0000😀";
            public static int ئىجرا_قىل_2() {
                if (تېكىست != "한글\\u0000😀") return 99;
                return (تېكىست.length() + تېكىست.charAt(2) + تېكىست.charAt(3) + تېكىست.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int فاكتورىيال(int قىممىتى) { return قىممىتى <= 1 ? 1 : قىممىتى * فاكتورىيال(قىممىتى - 1); }
            static int 연속(int قىممىتى) {
                switch (قىممىتى) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int قىممىتى) {
                switch (قىممىتى) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ئىجرا_قىل_2() { return (فاكتورىيال(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int قىممىتى{} = {};'.format(ئىندېكس, ئىندېكس) for ئىندېكس in range(270))
        덧셈 = '+'.join('قىممىتى{}'.format(ئىندېكس) for ئىندېكس in range(270))
        self.자바대조('public class 시험 { public static int ئىجرا_قىل_2() {' + 선언 +
                    'قىممىتى_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] قىممىتى = null; return قىممىتى.length;', 102),
            ('int[] قىممىتى = new int[1]; return قىممىتى[1];', 103),
            ('int[] قىممىتى = new int[1]; قىممىتى[-1] = 3; return 0;', 103),
            ('int قىممىتى = -1; return new int[قىممىتى].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.قۇرماق_مەنبە('public class 시험 { public static int ئىجرا_قىل_2() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long قىممىتى; public static int ئىجرا_قىل_2() { return 0; }',
            'public static int ئىجرا_قىل_2() { Object قىممىتى = new Object(); return 0; }',
            'public static int ئىجرا_قىل_2() { System.out.println("hello"); return 0; }',
            'public static int ئىجرا_قىل_2() { try { return 1; } catch (Exception خاتالىق) { return 2; } }',
            'public static synchronized int ئىجرا_قىل_2() { return 0; }',
            'public static int ئىجرا_قىل_2() { return new byte[3].length; }',
            'static native int 외부(); public static int ئىجرا_قىل_2() { return 외부(); }',
            'int قىممىتى; public static int ئىجرا_قىل_2() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.قۇرماق_مەنبە('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        چىقار = self.مۇندەرىجە_قىممىتى / 'native'
        چىقار.write_bytes(b'original-output')
        self.قۇرماق_مەنبە('public class 시험 { public static int ئىجرا_قىل_2() { return missing; } }', 성공=False)
        self.assertEqual(چىقار.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.قۇرماق_مەنبە('public class 시험 { public static int ئىجرا_قىل_2() { return 37; } }')
        self.assertEqual((self.مۇندەرىجە_قىممىتى / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ئىزدەش_جەدۋەل = subprocess.check_output(['readelf', '-l', str(self.مۇندەرىجە_قىممىتى / 'native')])
        self.assertNotIn(b'INTERP', ئىزدەش_جەدۋەل)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.قۇرماق_مەنبە('public class 시험 { public static int ئىجرا_قىل_2() { return ئىشلەتكۈچى.실행권한(); } }',
                    {'ئىشلەتكۈچى': 'public class ئىشلەتكۈچى { public static native int 실행권한(); }'}, نىشان='user')
        مەلۇمات = (self.مۇندەرىجە_قىممىتى / 'native').read_bytes()
        self.assertEqual(مەلۇمات[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', مەلۇمات, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.مۇندەرىجە_قىممىتى / 'native')]))
        # ئىشلەتكۈچى ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.قۇرماق_مەنبە('public class 시험 { public static int ئىجرا_قىل_2() { return كۆچمە_قىممىتى.포트읽기(1); } }',
                    {'كۆچمە_قىممىتى': 'public class كۆچمە_قىممىتى { public static native int 포트읽기(int قىممىتى); }'}, 성공=False, نىشان='user')

    def test_내보내기검증(self):
        مەنبە = 'public class 시험 { public static int ئىجرا_قىل_2() { return 0; } static int 호출(int قىممىتى) { return قىممىتى; } }'
        self.قۇرماق_مەنبە(مەنبە, نىشان='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.مۇندەرىجە_قىممىتى / 'native')]))
        self.قۇرماق_مەنبە(مەنبە, 성공=False, 내보냄='bad;name=시험.호출')
        self.قۇرماق_مەنبە(مەنبە, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
