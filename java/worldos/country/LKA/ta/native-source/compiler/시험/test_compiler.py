"""அசல்_தரவு ELF இயக்கு_கட்டளை + OpenJDK அளவிடக்கூடியது 대조. 임시 시험 자료만 생성한다."""
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
        self.கோப்பகம்_மதிப்பு = Path(self.임시.name)

    def தொகு_மூலம்(self, மூலக்_கோப்பு, 추가=None, 성공=True, இலக்கு='linux', 내보냄=None):
        பாதை_பட்டியல் = []
        for பெயர், உள்ளடக்கம்_மதிப்பு in dict({'시험': மூலக்_கோப்பு}, **(추가 or {})).items():
            பாதை_2 = self.கோப்பகம்_மதிப்பு / (பெயர் + '.java')
            பாதை_2.write_text(உள்ளடக்கம்_மதிப்பு, encoding='utf-8')
            பாதை_பட்டியல்.append(str(பாதை_2))
        கட்டளை = [sys.executable, str(컴파일러), '--target', இலக்கு, '--entry', '시험.செயல்படுத்துக', '-o', str(self.கோப்பகம்_மதிப்பு / 'native')]
        if 내보냄 is not None: கட்டளை += ['--export', 내보냄]
        அளவிடக்கூடியது = subprocess.run(கட்டளை + பாதை_பட்டியல்,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(அளவிடக்கூடியது.returncode, 0, அளவிடக்கூடியது.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(அளவிடக்கூடியது.returncode, 0)
            self.assertIn('தொகு_மூலம் பிழை'.encode(), அளவிடக்கூடியது.stderr)
        return அளவிடக்கூடியது

    def 실행결과(self):
        return subprocess.run([str(self.கோப்பகம்_மதிப்பு / 'native')], timeout=5).returncode

    def 자바대조(self, மூலக்_கோப்பு, 추가=None):
        self.தொகு_மூலம்(மூலக்_கோப்பு, 추가)
        (self.கோப்பகம்_மதிப்பு / 'ஓம்பு.java').write_text(
            'public class ஓம்பு { public static void main(String[] செயலுருபுகள்) { System.exit(시험.செயல்படுத்துக()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.கோப்பகம்_மதிப்பு)] +
                       [str(பாதை_2) for பாதை_2 in self.கோப்பகம்_மதிப்பு.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.கோப்பகம்_மதிப்பு), 'ஓம்பு'], timeout=5).returncode
        அசல்_தரவு = self.실행결과()
        self.assertGreaterEqual(அசல்_தரவு, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 சரிபார்)')
        self.assertEqual(அசல்_தரவு, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int செயல்படுத்துக() {
                int 합 = 7;
                int மதிப்பு = 12345;
                for (int அடைவு = -65; அடைவு <= 65; அடைவு++) {
                    மதிப்பு = மதிப்பு * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(மதிப்பு, அடைவு);
                    합 += (byte)மதிப்பு + (short)மதிப்பு + (char)மதிப்பு;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] மதிப்பு = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int செயல்படுத்துக() {
                int 합 = 13;
                for (int 가 = 0; 가 < மதிப்பு.length; 가++)
                    for (int 나 = 1; 나 < மதிப்பு.length; 나++)
                        합 = 합 * 31 + மதிப்பு[가] / மதிப்பு[나] + மதிப்பு[가] % மதிப்பு[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] உருவாக்கு_உள்ளீடு(int அளவு) { return new int[அளவு]; }
            public static int செயல்படுத்துக() {
                int[] 가 = உருவாக்கு_உள்ளீடு(8); int[] 나 = 가; int[] வெறுமை_பொருள் = new int[0];
                if (가 != 나 || 가 == null || வெறுமை_பொருள்.length != 0 || 가[7] != 0) return 99;
                int மதிப்பு = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return மதிப்பு + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int மதிப்பு = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int செயல்படுத்துக() { return 계산(1, 2, 3, 4, மதிப்பு) + 보조.படி(); }
        }''', {'보조': '''public class 보조 {
            static int மதிப்பு = 3;
            static int 초기값() { return ++மதிப்பு; }
            static int படி() { return மதிப்பு; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int மதிப்பு = 보조.படி() + 1;
            public static int செயல்படுத்துக() { return மதிப்பு * 10 + 보조.படி(); }
        }''', {'보조': '''public class 보조 {
            static int மதிப்பு = 시험.மதிப்பு + 2;
            static int படி() { return மதிப்பு; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String உரை = "한글\\u0000😀";
            public static int செயல்படுத்துக() {
                if (உரை != "한글\\u0000😀") return 99;
                return (உரை.length() + உரை.charAt(2) + உரை.charAt(3) + உரை.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int இயல்_எண்_தொடர்பெருக்கம்(int மதிப்பு) { return மதிப்பு <= 1 ? 1 : மதிப்பு * இயல்_எண்_தொடர்பெருக்கம்(மதிப்பு - 1); }
            static int 연속(int மதிப்பு) {
                switch (மதிப்பு) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int மதிப்பு) {
                switch (மதிப்பு) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int செயல்படுத்துக() { return (இயல்_எண்_தொடர்பெருக்கம்(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        அறிவிப்பு = '\n'.join('int மதிப்பு{} = {};'.format(அடைவு, அடைவு) for அடைவு in range(270))
        덧셈 = '+'.join('மதிப்பு{}'.format(அடைவு) for அடைவு in range(270))
        self.자바대조('public class 시험 { public static int செயல்படுத்துக() {' + அறிவிப்பு +
                    'மதிப்பு_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] மதிப்பு = null; return மதிப்பு.length;', 102),
            ('int[] மதிப்பு = new int[1]; return மதிப்பு[1];', 103),
            ('int[] மதிப்பு = new int[1]; மதிப்பு[-1] = 3; return 0;', 103),
            ('int மதிப்பு = -1; return new int[மதிப்பு].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for அங்கம்_மதிப்பு, 기대 in 경우들:
            with self.subTest(அங்கம்_மதிப்பு=அங்கம்_மதிப்பு):
                self.தொகு_மூலம்('public class 시험 { public static int செயல்படுத்துக() { ' + அங்கம்_மதிப்பு + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long மதிப்பு; public static int செயல்படுத்துக() { return 0; }',
            'public static int செயல்படுத்துக() { Object மதிப்பு = new Object(); return 0; }',
            'public static int செயல்படுத்துக() { System.out.println("hello"); return 0; }',
            'public static int செயல்படுத்துக() { try { return 1; } catch (Exception பிழை) { return 2; } }',
            'public static synchronized int செயல்படுத்துக() { return 0; }',
            'public static int செயல்படுத்துக() { return new byte[3].length; }',
            'static native int 외부(); public static int செயல்படுத்துக() { return 외부(); }',
            'int மதிப்பு; public static int செயல்படுத்துக() { return 0; }',
        ]
        for அங்கம்_மதிப்பு in 경우들:
            with self.subTest(அங்கம்_மதிப்பு=அங்கம்_மதிப்பு):
                self.தொகு_மூலம்('public class 시험 { ' + அங்கம்_மதிப்பு + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        வெளியீட்டு_இடம் = self.கோப்பகம்_மதிப்பு / 'native'
        வெளியீட்டு_இடம்.write_bytes(b'original-output')
        self.தொகு_மூலம்('public class 시험 { public static int செயல்படுத்துக() { return missing; } }', 성공=False)
        self.assertEqual(வெளியீட்டு_இடம்.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.தொகு_மூலம்('public class 시험 { public static int செயல்படுத்துக() { return 37; } }')
        self.assertEqual((self.கோப்பகம்_மதிப்பு / 'native').read_bytes()[:5], b'\x7fELF\x01')
        தேடுதல்_அட்டவணை = subprocess.check_output(['readelf', '-l', str(self.கோப்பகம்_மதிப்பு / 'native')])
        self.assertNotIn(b'INTERP', தேடுதல்_அட்டவணை)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.தொகு_மூலம்('public class 시험 { public static int செயல்படுத்துக() { return பயனர்.실행권한(); } }',
                    {'பயனர்': 'public class பயனர் { public static native int 실행권한(); }'}, இலக்கு='user')
        தரவு = (self.கோப்பகம்_மதிப்பு / 'native').read_bytes()
        self.assertEqual(தரவு[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', தரவு, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.கோப்பகம்_மதிப்பு / 'native')]))
        # பயனர் ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.தொகு_மூலம்('public class 시험 { public static int செயல்படுத்துக() { return சாதனம்_மதிப்பு.포트읽기(1); } }',
                    {'சாதனம்_மதிப்பு': 'public class சாதனம்_மதிப்பு { public static native int 포트읽기(int மதிப்பு); }'}, 성공=False, இலக்கு='user')

    def test_내보내기검증(self):
        மூலக்_கோப்பு = 'public class 시험 { public static int செயல்படுத்துக() { return 0; } static int 호출(int மதிப்பு) { return மதிப்பு; } }'
        self.தொகு_மூலம்(மூலக்_கோப்பு, இலக்கு='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.கோப்பகம்_மதிப்பு / 'native')]))
        self.தொகு_மூலம்(மூலக்_கோப்பு, 성공=False, 내보냄='bad;name=시험.호출')
        self.தொகு_மூலம்(மூலக்_கோப்பு, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
