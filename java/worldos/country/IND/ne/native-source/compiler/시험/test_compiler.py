"""वास्तविक_लगत ELF कार्यान्वयन_गर्नुहोस्_आदेश + OpenJDK मापन 대조. 임시 시험 자료만 생성한다."""
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
        self.डाइरेक्टरी_मान = Path(self.임시.name)

    def बनाउनुहोस्_स्रोत(self, स्रोत, 추가=None, 성공=True, लक्ष्य='linux', 내보냄=None):
        बाटो_सूची = []
        for नाम, सामग्री_मान in dict({'시험': स्रोत}, **(추가 or {})).items():
            मार्ग = self.डाइरेक्टरी_मान / (नाम + '.java')
            मार्ग.write_text(सामग्री_मान, encoding='utf-8')
            बाटो_सूची.append(str(मार्ग))
        आदेश = [sys.executable, str(컴파일러), '--target', लक्ष्य, '--entry', '시험.चलाउनुहोस्', '-o', str(self.डाइरेक्टरी_मान / 'native')]
        if 내보냄 is not None: आदेश += ['--export', 내보냄]
        मापन = subprocess.run(आदेश + बाटो_सूची,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(मापन.returncode, 0, मापन.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(मापन.returncode, 0)
            self.assertIn('बनाउनुहोस्_स्रोत त्रुटि'.encode(), मापन.stderr)
        return मापन

    def 실행결과(self):
        return subprocess.run([str(self.डाइरेक्टरी_मान / 'native')], timeout=5).returncode

    def 자바대조(self, स्रोत, 추가=None):
        self.बनाउनुहोस्_स्रोत(स्रोत, 추가)
        (self.डाइरेक्टरी_मान / 'होस्ट.java').write_text(
            'public class होस्ट { public static void main(String[] तर्क) { System.exit(시험.चलाउनुहोस्()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.डाइरेक्टरी_मान)] +
                       [str(मार्ग) for मार्ग in self.डाइरेक्टरी_मान.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.डाइरेक्टरी_मान), 'होस्ट'], timeout=5).returncode
        वास्तविक_लगत = self.실행결과()
        self.assertGreaterEqual(वास्तविक_लगत, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 रुजू_गर्नुहोस्)')
        self.assertEqual(वास्तविक_लगत, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int चलाउनुहोस्() {
                int 합 = 7;
                int मान = 12345;
                for (int अनुक्रमणिका = -65; अनुक्रमणिका <= 65; अनुक्रमणिका++) {
                    मान = मान * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(मान, अनुक्रमणिका);
                    합 += (byte)मान + (short)मान + (char)मान;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] मान = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int चलाउनुहोस्() {
                int 합 = 13;
                for (int 가 = 0; 가 < मान.length; 가++)
                    for (int 나 = 1; 나 < मान.length; 나++)
                        합 = 합 * 31 + मान[가] / मान[나] + मान[가] % मान[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] सिर्जना_प्रविष्टि(int आकार) { return new int[आकार]; }
            public static int चलाउनुहोस्() {
                int[] 가 = सिर्जना_प्रविष्टि(8); int[] 나 = 가; int[] रिक्त_वस्तु = new int[0];
                if (가 != 나 || 가 == null || रिक्त_वस्तु.length != 0 || 가[7] != 0) return 99;
                int मान = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return मान + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int मान = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int चलाउनुहोस्() { return 계산(1, 2, 3, 4, मान) + 보조.पढनुहोस्(); }
        }''', {'보조': '''public class 보조 {
            static int मान = 3;
            static int 초기값() { return ++मान; }
            static int पढनुहोस्() { return मान; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int मान = 보조.पढनुहोस्() + 1;
            public static int चलाउनुहोस्() { return मान * 10 + 보조.पढनुहोस्(); }
        }''', {'보조': '''public class 보조 {
            static int मान = 시험.मान + 2;
            static int पढनुहोस्() { return मान; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String पाठ = "한글\\u0000😀";
            public static int चलाउनुहोस्() {
                if (पाठ != "한글\\u0000😀") return 99;
                return (पाठ.length() + पाठ.charAt(2) + पाठ.charAt(3) + पाठ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int क्रम_गुणित(int मान) { return मान <= 1 ? 1 : मान * क्रम_गुणित(मान - 1); }
            static int 연속(int मान) {
                switch (मान) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int मान) {
                switch (मान) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int चलाउनुहोस्() { return (क्रम_गुणित(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int मान{} = {};'.format(अनुक्रमणिका, अनुक्रमणिका) for अनुक्रमणिका in range(270))
        덧셈 = '+'.join('मान{}'.format(अनुक्रमणिका) for अनुक्रमणिका in range(270))
        self.자바대조('public class 시험 { public static int चलाउनुहोस्() {' + 선언 +
                    'मान_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] मान = null; return मान.length;', 102),
            ('int[] मान = new int[1]; return मान[1];', 103),
            ('int[] मान = new int[1]; मान[-1] = 3; return 0;', 103),
            ('int मान = -1; return new int[मान].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.बनाउनुहोस्_स्रोत('public class 시험 { public static int चलाउनुहोस्() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long मान; public static int चलाउनुहोस्() { return 0; }',
            'public static int चलाउनुहोस्() { Object मान = new Object(); return 0; }',
            'public static int चलाउनुहोस्() { System.out.println("hello"); return 0; }',
            'public static int चलाउनुहोस्() { try { return 1; } catch (Exception त्रुटि) { return 2; } }',
            'public static synchronized int चलाउनुहोस्() { return 0; }',
            'public static int चलाउनुहोस्() { return new byte[3].length; }',
            'static native int 외부(); public static int चलाउनुहोस्() { return 외부(); }',
            'int मान; public static int चलाउनुहोस्() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.बनाउनुहोस्_स्रोत('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.डाइरेक्टरी_मान / 'native'
        출력.write_bytes(b'original-output')
        self.बनाउनुहोस्_स्रोत('public class 시험 { public static int चलाउनुहोस्() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.बनाउनुहोस्_स्रोत('public class 시험 { public static int चलाउनुहोस्() { return 37; } }')
        self.assertEqual((self.डाइरेक्टरी_मान / 'native').read_bytes()[:5], b'\x7fELF\x01')
        विवरण_हेर्ने_सुविधा_तालिका = subprocess.check_output(['readelf', '-l', str(self.डाइरेक्टरी_मान / 'native')])
        self.assertNotIn(b'INTERP', विवरण_हेर्ने_सुविधा_तालिका)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.बनाउनुहोस्_स्रोत('public class 시험 { public static int चलाउनुहोस्() { return प्रयोगकर्ता.실행권한(); } }',
                    {'प्रयोगकर्ता': 'public class प्रयोगकर्ता { public static native int 실행권한(); }'}, लक्ष्य='user')
        लगत = (self.डाइरेक्टरी_मान / 'native').read_bytes()
        self.assertEqual(लगत[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', लगत, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.डाइरेक्टरी_मान / 'native')]))
        # प्रयोगकर्ता ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.बनाउनुहोस्_स्रोत('public class 시험 { public static int चलाउनुहोस्() { return मोबाइल_मान.포트읽기(1); } }',
                    {'मोबाइल_मान': 'public class मोबाइल_मान { public static native int 포트읽기(int मान); }'}, 성공=False, लक्ष्य='user')

    def test_내보내기검증(self):
        स्रोत = 'public class 시험 { public static int चलाउनुहोस्() { return 0; } static int 호출(int मान) { return मान; } }'
        self.बनाउनुहोस्_स्रोत(स्रोत, लक्ष्य='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.डाइरेक्टरी_मान / 'native')]))
        self.बनाउनुहोस्_स्रोत(स्रोत, 성공=False, 내보냄='bad;name=시험.호출')
        self.बनाउनुहोस्_स्रोत(स्रोत, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
