"""действителен_данни ELF изпълнявам_команда + OpenJDK РЕЗУЛТАТ 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

компилатор = Path(__file__).resolve().parents[1] / 'компилатор.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.указател_стойност = Path(self.임시.name)

    def компилирам_източник(self, ИЗТОЧНИК, добавям_запис=None, 성공=True, цел='linux', 내보냄=None):
        път_Списък = []
        for Име, Съдържание_стойност in dict({'시험': ИЗТОЧНИК}, **(добавям_запис or {})).items():
            ПЪТ = self.указател_стойност / (Име + '.java')
            ПЪТ.write_text(Съдържание_стойност, encoding='utf-8')
            път_Списък.append(str(ПЪТ))
        Команда = [sys.executable, str(компилатор), '--target', цел, '--entry', '시험.Стартиране', '-o', str(self.указател_стойност / 'native')]
        if 내보냄 is not None: Команда += ['--export', 내보냄]
        РЕЗУЛТАТ = subprocess.run(Команда + път_Списък,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(РЕЗУЛТАТ.returncode, 0, РЕЗУЛТАТ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(РЕЗУЛТАТ.returncode, 0)
            self.assertIn('компилирам_източник ГРЕШКА'.encode(), РЕЗУЛТАТ.stderr)
        return РЕЗУЛТАТ

    def 실행결과(self):
        return subprocess.run([str(self.указател_стойност / 'native')], timeout=5).returncode

    def 자바대조(self, ИЗТОЧНИК, добавям_запис=None):
        self.компилирам_източник(ИЗТОЧНИК, добавям_запис)
        (self.указател_стойност / 'хост.java').write_text(
            'public class хост { public static void main(String[] Параметри) { System.exit(시험.Стартиране()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.указател_стойност)] +
                       [str(ПЪТ) for ПЪТ in self.указател_стойност.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.указател_стойност), 'хост'], timeout=5).returncode
        действителен_данни = self.실행결과()
        self.assertGreaterEqual(действителен_данни, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 проверявам)')
        self.assertEqual(действителен_данни, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Стартиране() {
                int 합 = 7;
                int стойност = 12345;
                for (int индекс = -65; индекс <= 65; индекс++) {
                    стойност = стойност * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(стойност, индекс);
                    합 += (byte)стойност + (short)стойност + (char)стойност;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] стойност = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Стартиране() {
                int 합 = 13;
                for (int 가 = 0; 가 < стойност.length; 가++)
                    for (int 나 = 1; 나 < стойност.length; 나++)
                        합 = 합 * 31 + стойност[가] / стойност[나] + стойност[가] % стойност[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Създаване_запис(int Размер) { return new int[Размер]; }
            public static int Стартиране() {
                int[] 가 = Създаване_запис(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int стойност = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return стойност + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int стойност = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Стартиране() { return 계산(1, 2, 3, 4, стойност) + 보조.Четене(); }
        }''', {'보조': '''public class 보조 {
            static int стойност = 3;
            static int 초기값() { return ++стойност; }
            static int Четене() { return стойност; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int стойност = 보조.Четене() + 1;
            public static int Стартиране() { return стойност * 10 + 보조.Четене(); }
        }''', {'보조': '''public class 보조 {
            static int стойност = 시험.стойност + 2;
            static int Четене() { return стойност; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Текст = "한글\\u0000😀";
            public static int Стартиране() {
                if (Текст != "한글\\u0000😀") return 99;
                return (Текст.length() + Текст.charAt(2) + Текст.charAt(3) + Текст.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int факториел(int стойност) { return стойност <= 1 ? 1 : стойност * факториел(стойност - 1); }
            static int 연속(int стойност) {
                switch (стойност) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int стойност) {
                switch (стойност) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Стартиране() { return (факториел(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        декларация = '\n'.join('int стойност{} = {};'.format(индекс, индекс) for индекс in range(270))
        덧셈 = '+'.join('стойност{}'.format(индекс) for индекс in range(270))
        self.자바대조('public class 시험 { public static int Стартиране() {' + декларация +
                    'стойност_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int нула_операнд = 0; return 1 / нула_операнд;', 101),
            ('int[] стойност = null; return стойност.length;', 102),
            ('int[] стойност = new int[1]; return стойност[1];', 103),
            ('int[] стойност = new int[1]; стойност[-1] = 3; return 0;', 103),
            ('int стойност = -1; return new int[стойност].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for основен_текст_стойност, 기대 in 경우들:
            with self.subTest(основен_текст_стойност=основен_текст_стойност):
                self.компилирам_източник('public class 시험 { public static int Стартиране() { ' + основен_текст_стойност + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long стойност; public static int Стартиране() { return 0; }',
            'public static int Стартиране() { Object стойност = new Object(); return 0; }',
            'public static int Стартиране() { System.out.println("hello"); return 0; }',
            'public static int Стартиране() { try { return 1; } catch (Exception ГРЕШКА) { return 2; } }',
            'public static synchronized int Стартиране() { return 0; }',
            'public static int Стартиране() { return new byte[3].length; }',
            'static native int външен_стойност(); public static int Стартиране() { return външен_стойност(); }',
            'int стойност; public static int Стартиране() { return 0; }',
        ]
        for основен_текст_стойност in 경우들:
            with self.subTest(основен_текст_стойност=основен_текст_стойност):
                self.компилирам_източник('public class 시험 { ' + основен_текст_стойност + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Изход = self.указател_стойност / 'native'
        Изход.write_bytes(b'original-output')
        self.компилирам_източник('public class 시험 { public static int Стартиране() { return missing; } }', 성공=False)
        self.assertEqual(Изход.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.компилирам_източник('public class 시험 { public static int Стартиране() { return 37; } }')
        self.assertEqual((self.указател_стойност / 'native').read_bytes()[:5], b'\x7fELF\x01')
        таблица_за_справка = subprocess.check_output(['readelf', '-l', str(self.указател_стойност / 'native')])
        self.assertNotIn(b'INTERP', таблица_за_справка)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.компилирам_източник('public class 시험 { public static int Стартиране() { return потребител.실행권한(); } }',
                    {'потребител': 'public class потребител { public static native int 실행권한(); }'}, цел='user')
        данни = (self.указател_стойност / 'native').read_bytes()
        self.assertEqual(данни[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', данни, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.указател_стойност / 'native')]))
        # потребител ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.компилирам_източник('public class 시험 { public static int Стартиране() { return устройство_стойност.포트읽기(1); } }',
                    {'устройство_стойност': 'public class устройство_стойност { public static native int 포트읽기(int стойност); }'}, 성공=False, цел='user')

    def test_내보내기검증(self):
        ИЗТОЧНИК = 'public class 시험 { public static int Стартиране() { return 0; } static int 호출(int стойност) { return стойност; } }'
        self.компилирам_източник(ИЗТОЧНИК, цел='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.указател_стойност / 'native')]))
        self.компилирам_източник(ИЗТОЧНИК, 성공=False, 내보냄='bad;name=시험.호출')
        self.компилирам_източник(ИЗТОЧНИК, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
