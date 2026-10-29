"""वास्तविक_डेटा ELF निष्पादित_करें_आदेश + OpenJDK परिणाम 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

कंपाइलर = Path(__file__).resolve().parents[1] / 'कंपाइलर.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.डायरेक्टरी_मान = Path(self.임시.name)

    def कंपाइल_स्रोत(self, स्रोत, जोड़ें_एन्ट्री=None, 성공=True, लक्ष्य='linux', 내보냄=None):
        पथ_सूची = []
        for नाम, सामग्री_मान in dict({'시험': स्रोत}, **(जोड़ें_एन्ट्री or {})).items():
            पथ = self.डायरेक्टरी_मान / (नाम + '.java')
            पथ.write_text(सामग्री_मान, encoding='utf-8')
            पथ_सूची.append(str(पथ))
        आदेश = [sys.executable, str(कंपाइलर), '--target', लक्ष्य, '--entry', '시험.चलाएँ', '-o', str(self.डायरेक्टरी_मान / 'native')]
        if 내보냄 is not None: आदेश += ['--export', 내보냄]
        परिणाम = subprocess.run(आदेश + पथ_सूची,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(परिणाम.returncode, 0, परिणाम.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(परिणाम.returncode, 0)
            self.assertIn('कंपाइल_स्रोत त्रुटि'.encode(), परिणाम.stderr)
        return परिणाम

    def 실행결과(self):
        return subprocess.run([str(self.डायरेक्टरी_मान / 'native')], timeout=5).returncode

    def 자바대조(self, स्रोत, जोड़ें_एन्ट्री=None):
        self.कंपाइल_स्रोत(स्रोत, जोड़ें_एन्ट्री)
        (self.डायरेक्टरी_मान / 'आयोजक.java').write_text(
            'public class आयोजक { public static void main(String[] तर्क) { System.exit(시험.चलाएँ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.डायरेक्टरी_मान)] +
                       [str(पथ) for पथ in self.डायरेक्टरी_मान.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.डायरेक्टरी_मान), 'आयोजक'], timeout=5).returncode
        वास्तविक_डेटा = self.실행결과()
        self.assertGreaterEqual(वास्तविक_डेटा, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 सत्यापित_करें)')
        self.assertEqual(वास्तविक_डेटा, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int चलाएँ() {
                int 합 = 7;
                int मान = 12345;
                for (int इंडेक्स = -65; इंडेक्स <= 65; इंडेक्स++) {
                    मान = मान * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(मान, इंडेक्स);
                    합 += (byte)मान + (short)मान + (char)मान;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] मान = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int चलाएँ() {
                int 합 = 13;
                for (int 가 = 0; 가 < मान.length; 가++)
                    for (int 나 = 1; 나 < मान.length; 나++)
                        합 = 합 * 31 + मान[가] / मान[나] + मान[가] % मान[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] बनाएँ_एन्ट्री(int आकार) { return new int[आकार]; }
            public static int चलाएँ() {
                int[] 가 = बनाएँ_एन्ट्री(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
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
            public static int चलाएँ() { return 계산(1, 2, 3, 4, मान) + 보조.पढ़ें(); }
        }''', {'보조': '''public class 보조 {
            static int मान = 3;
            static int 초기값() { return ++मान; }
            static int पढ़ें() { return मान; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int मान = 보조.पढ़ें() + 1;
            public static int चलाएँ() { return मान * 10 + 보조.पढ़ें(); }
        }''', {'보조': '''public class 보조 {
            static int मान = 시험.मान + 2;
            static int पढ़ें() { return मान; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String पाठ = "한글\\u0000😀";
            public static int चलाएँ() {
                if (पाठ != "한글\\u0000😀") return 99;
                return (पाठ.length() + पाठ.charAt(2) + पाठ.charAt(3) + पाठ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int क्रमगुणन(int मान) { return मान <= 1 ? 1 : मान * क्रमगुणन(मान - 1); }
            static int 연속(int मान) {
                switch (मान) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int मान) {
                switch (मान) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int चलाएँ() { return (क्रमगुणन(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        घोषणा = '\n'.join('int मान{} = {};'.format(इंडेक्स, इंडेक्स) for इंडेक्स in range(270))
        덧셈 = '+'.join('मान{}'.format(इंडेक्स) for इंडेक्स in range(270))
        self.자바대조('public class 시험 { public static int चलाएँ() {' + घोषणा +
                    'मान_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int शून्य_ऑपरेंड = 0; return 1 / शून्य_ऑपरेंड;', 101),
            ('int[] मान = null; return मान.length;', 102),
            ('int[] मान = new int[1]; return मान[1];', 103),
            ('int[] मान = new int[1]; मान[-1] = 3; return 0;', 103),
            ('int मान = -1; return new int[मान].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for मुख्य_संदेश_मान, 기대 in 경우들:
            with self.subTest(मुख्य_संदेश_मान=मुख्य_संदेश_मान):
                self.कंपाइल_स्रोत('public class 시험 { public static int चलाएँ() { ' + मुख्य_संदेश_मान + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long मान; public static int चलाएँ() { return 0; }',
            'public static int चलाएँ() { Object मान = new Object(); return 0; }',
            'public static int चलाएँ() { System.out.println("hello"); return 0; }',
            'public static int चलाएँ() { try { return 1; } catch (Exception त्रुटि) { return 2; } }',
            'public static synchronized int चलाएँ() { return 0; }',
            'public static int चलाएँ() { return new byte[3].length; }',
            'static native int बाहरी_मान(); public static int चलाएँ() { return बाहरी_मान(); }',
            'int मान; public static int चलाएँ() { return 0; }',
        ]
        for मुख्य_संदेश_मान in 경우들:
            with self.subTest(मुख्य_संदेश_मान=मुख्य_संदेश_मान):
                self.कंपाइल_स्रोत('public class 시험 { ' + मुख्य_संदेश_मान + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        निर्गम = self.डायरेक्टरी_मान / 'native'
        निर्गम.write_bytes(b'original-output')
        self.कंपाइल_स्रोत('public class 시험 { public static int चलाएँ() { return missing; } }', 성공=False)
        self.assertEqual(निर्गम.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.कंपाइल_स्रोत('public class 시험 { public static int चलाएँ() { return 37; } }')
        self.assertEqual((self.डायरेक्टरी_मान / 'native').read_bytes()[:5], b'\x7fELF\x01')
        लुकअप_तालिका = subprocess.check_output(['readelf', '-l', str(self.डायरेक्टरी_मान / 'native')])
        self.assertNotIn(b'INTERP', लुकअप_तालिका)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.कंपाइल_स्रोत('public class 시험 { public static int चलाएँ() { return उपयोगकर्ता.실행권한(); } }',
                    {'उपयोगकर्ता': 'public class उपयोगकर्ता { public static native int 실행권한(); }'}, लक्ष्य='user')
        आँकड़े = (self.डायरेक्टरी_मान / 'native').read_bytes()
        self.assertEqual(आँकड़े[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', आँकड़े, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.डायरेक्टरी_मान / 'native')]))
        # उपयोगकर्ता ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.कंपाइल_स्रोत('public class 시험 { public static int चलाएँ() { return उपकरण_मान.포트읽기(1); } }',
                    {'उपकरण_मान': 'public class उपकरण_मान { public static native int 포트읽기(int मान); }'}, 성공=False, लक्ष्य='user')

    def test_내보내기검증(self):
        स्रोत = 'public class 시험 { public static int चलाएँ() { return 0; } static int 호출(int मान) { return मान; } }'
        self.कंपाइल_स्रोत(स्रोत, लक्ष्य='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.डायरेक्टरी_मान / 'native')]))
        self.कंपाइल_स्रोत(स्रोत, 성공=False, 내보냄='bad;name=시험.호출')
        self.कंपाइल_स्रोत(स्रोत, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
