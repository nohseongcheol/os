"""प्रत्यक्ष_डेटा ELF पाळो_दिवचो_आदेश + OpenJDK मेजप 대조. 임시 시험 자료만 생성한다."""
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
        self.नामावळ_मोल = Path(self.임시.name)

    def दाळचे_स्त्रोत(self, स्त्रोत, 추가=None, 성공=True, लक्ष्य='linux', 내보냄=None):
        पाथ_सुची = []
        for नांव, अनुक्रमणिका_मोल in dict({'시험': स्त्रोत}, **(추가 or {})).items():
            पाथ = self.नामावळ_मोल / (नांव + '.java')
            पाथ.write_text(अनुक्रमणिका_मोल, encoding='utf-8')
            पाथ_सुची.append(str(पाथ))
        आदेश = [sys.executable, str(컴파일러), '--target', लक्ष्य, '--entry', '시험.चलोवप', '-o', str(self.नामावळ_मोल / 'native')]
        if 내보냄 is not None: आदेश += ['--export', 내보냄]
        मेजप = subprocess.run(आदेश + पाथ_सुची,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(मेजप.returncode, 0, मेजप.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(मेजप.returncode, 0)
            self.assertIn('दाळचे_स्त्रोत चूक'.encode(), मेजप.stderr)
        return मेजप

    def 실행결과(self):
        return subprocess.run([str(self.नामावळ_मोल / 'native')], timeout=5).returncode

    def 자바대조(self, स्त्रोत, 추가=None):
        self.दाळचे_स्त्रोत(स्त्रोत, 추가)
        (self.नामावळ_मोल / 'येजमान.java').write_text(
            'public class येजमान { public static void main(String[] 인수) { System.exit(시험.चलोवप()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.नामावळ_मोल)] +
                       [str(पाथ) for पाथ in self.नामावळ_मोल.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.नामावळ_मोल), 'येजमान'], timeout=5).returncode
        प्रत्यक्ष_डेटा = self.실행결과()
        self.assertGreaterEqual(प्रत्यक्ष_डेटा, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 पुनर्तपासणी_करची)')
        self.assertEqual(प्रत्यक्ष_डेटा, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int चलोवप() {
                int SUM_मोल = 7;
                int मोल = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    मोल = मोल * 1664525 + 1013904223;
                    SUM_मोल = SUM_मोल * 31 + 섞기(मोल, INDEX);
                    SUM_मोल += (byte)मोल + (short)मोल + (char)मोल;
                }
                return (SUM_मोल & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] मोल = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int चलोवप() {
                int SUM_मोल = 13;
                for (int 가 = 0; 가 < मोल.length; 가++)
                    for (int 나 = 1; 나 < मोल.length; 나++)
                        SUM_मोल = SUM_मोल * 31 + मोल[가] / मोल[나] + मोल[가] % मोल[나];
                return (SUM_मोल & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] निर्माण_करचें_प्रवेश(int आवाठ) { return new int[आवाठ]; }
            public static int चलोवप() {
                int[] 가 = निर्माण_करचें_प्रवेश(8); int[] 나 = 가; int[] रिकामें_ऑब्जॅक्ट = new int[0];
                if (가 != 나 || 가 == null || रिकामें_ऑब्जॅक्ट.length != 0 || 가[7] != 0) return 99;
                int मोल = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return मोल + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int मोल = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int चलोवप() { return 계산(1, 2, 3, 4, मोल) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int मोल = 3;
            static int 초기값() { return ++मोल; }
            static int 읽기() { return मोल; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int मोल = 보조.읽기() + 1;
            public static int चलोवप() { return मोल * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int मोल = 시험.मोल + 2;
            static int 읽기() { return मोल; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int चलोवप() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int क्रमगुणीत(int मोल) { return मोल <= 1 ? 1 : मोल * क्रमगुणीत(मोल - 1); }
            static int 연속(int मोल) {
                switch (मोल) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int मोल) {
                switch (मोल) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int चलोवप() { return (क्रमगुणीत(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int मोल{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('मोल{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int चलोवप() {' + 선언 +
                    'मोल_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] मोल = null; return मोल.length;', 102),
            ('int[] मोल = new int[1]; return मोल[1];', 103),
            ('int[] मोल = new int[1]; मोल[-1] = 3; return 0;', 103),
            ('int मोल = -1; return new int[मोल].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.दाळचे_स्त्रोत('public class 시험 { public static int चलोवप() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long मोल; public static int चलोवप() { return 0; }',
            'public static int चलोवप() { Object मोल = new Object(); return 0; }',
            'public static int चलोवप() { System.out.println("hello"); return 0; }',
            'public static int चलोवप() { try { return 1; } catch (Exception चूक) { return 2; } }',
            'public static synchronized int चलोवप() { return 0; }',
            'public static int चलोवप() { return new byte[3].length; }',
            'static native int 외부(); public static int चलोवप() { return 외부(); }',
            'int मोल; public static int चलोवप() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.दाळचे_स्त्रोत('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.नामावळ_मोल / 'native'
        출력.write_bytes(b'original-output')
        self.दाळचे_स्त्रोत('public class 시험 { public static int चलोवप() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.दाळचे_स्त्रोत('public class 시험 { public static int चलोवप() { return 37; } }')
        self.assertEqual((self.नामावळ_मोल / 'native').read_bytes()[:5], b'\x7fELF\x01')
        लूकअप_तकटो = subprocess.check_output(['readelf', '-l', str(self.नामावळ_मोल / 'native')])
        self.assertNotIn(b'INTERP', लूकअप_तकटो)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.दाळचे_स्त्रोत('public class 시험 { public static int चलोवप() { return उपेगकर्तो.실행권한(); } }',
                    {'उपेगकर्तो': 'public class उपेगकर्तो { public static native int 실행권한(); }'}, लक्ष्य='user')
        डेटा = (self.नामावळ_मोल / 'native').read_bytes()
        self.assertEqual(डेटा[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', डेटा, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.नामावळ_मोल / 'native')]))
        # उपेगकर्तो ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.दाळचे_स्त्रोत('public class 시험 { public static int चलोवप() { return मोबायल_मोल.포트읽기(1); } }',
                    {'मोबायल_मोल': 'public class मोबायल_मोल { public static native int 포트읽기(int मोल); }'}, 성공=False, लक्ष्य='user')

    def test_내보내기검증(self):
        स्त्रोत = 'public class 시험 { public static int चलोवप() { return 0; } static int 호출(int मोल) { return मोल; } }'
        self.दाळचे_स्त्रोत(स्त्रोत, लक्ष्य='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.नामावळ_मोल / 'native')]))
        self.दाळचे_स्त्रोत(स्त्रोत, 성공=False, 내보냄='bad;name=시험.호출')
        self.दाळचे_स्त्रोत(स्त्रोत, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
