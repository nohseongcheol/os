"""реален_податоци ELF Изврши_наредба + OpenJDK мерка 대조. 임시 시험 자료만 생성한다."""
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
        self.Именик_VALUE = Path(self.임시.name)

    def изгради_извор(self, ИЗВОР, 추가=None, 성공=True, цел='linux', 내보냄=None):
        патека_Список = []
        for Име, Содржина_VALUE in dict({'시험': ИЗВОР}, **(추가 or {})).items():
            ПАТЕКА = self.Именик_VALUE / (Име + '.java')
            ПАТЕКА.write_text(Содржина_VALUE, encoding='utf-8')
            патека_Список.append(str(ПАТЕКА))
        Команда = [sys.executable, str(컴파일러), '--target', цел, '--entry', '시험.Изврши_2', '-o', str(self.Именик_VALUE / 'native')]
        if 내보냄 is not None: Команда += ['--export', 내보냄]
        мерка = subprocess.run(Команда + патека_Список,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(мерка.returncode, 0, мерка.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(мерка.returncode, 0)
            self.assertIn('изгради_извор ГРЕШКА'.encode(), мерка.stderr)
        return мерка

    def 실행결과(self):
        return subprocess.run([str(self.Именик_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, ИЗВОР, 추가=None):
        self.изгради_извор(ИЗВОР, 추가)
        (self.Именик_VALUE / 'вдоми.java').write_text(
            'public class вдоми { public static void main(String[] Аргументи) { System.exit(시험.Изврши_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Именик_VALUE)] +
                       [str(ПАТЕКА) for ПАТЕКА in self.Именик_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Именик_VALUE), 'вдоми'], timeout=5).returncode
        реален_податоци = self.실행결과()
        self.assertGreaterEqual(реален_податоци, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 провери)')
        self.assertEqual(реален_податоци, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Изврши_2() {
                int SUM_VALUE = 7;
                int VALUE = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    VALUE = VALUE * 1664525 + 1013904223;
                    SUM_VALUE = SUM_VALUE * 31 + 섞기(VALUE, INDEX);
                    SUM_VALUE += (byte)VALUE + (short)VALUE + (char)VALUE;
                }
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] VALUE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Изврши_2() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int 나 = 1; 나 < VALUE.length; 나++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[나] + VALUE[가] % VALUE[나];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Create_внес(int Големина) { return new int[Големина]; }
            public static int Изврши_2() {
                int[] 가 = Create_внес(8); int[] 나 = 가; int[] празно_објект = new int[0];
                if (가 != 나 || 가 == null || празно_објект.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Изврши_2() { return 계산(1, 2, 3, 4, VALUE) + 보조.Читај(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Читај() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Читај() + 1;
            public static int Изврши_2() { return VALUE * 10 + 보조.Читај(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Читај() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Текст = "한글\\u0000😀";
            public static int Изврши_2() {
                if (Текст != "한글\\u0000😀") return 99;
                return (Текст.length() + Текст.charAt(2) + Текст.charAt(3) + Текст.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int факторијал(int VALUE) { return VALUE <= 1 ? 1 : VALUE * факторијал(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Изврши_2() { return (факторијал(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        декларација = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Изврши_2() {' + декларација +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for тело_VALUE, 기대 in 경우들:
            with self.subTest(тело_VALUE=тело_VALUE):
                self.изгради_извор('public class 시험 { public static int Изврши_2() { ' + тело_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Изврши_2() { return 0; }',
            'public static int Изврши_2() { Object VALUE = new Object(); return 0; }',
            'public static int Изврши_2() { System.out.println("hello"); return 0; }',
            'public static int Изврши_2() { try { return 1; } catch (Exception ГРЕШКА) { return 2; } }',
            'public static synchronized int Изврши_2() { return 0; }',
            'public static int Изврши_2() { return new byte[3].length; }',
            'static native int 외부(); public static int Изврши_2() { return 외부(); }',
            'int VALUE; public static int Изврши_2() { return 0; }',
        ]
        for тело_VALUE in 경우들:
            with self.subTest(тело_VALUE=тело_VALUE):
                self.изгради_извор('public class 시험 { ' + тело_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.Именик_VALUE / 'native'
        출력.write_bytes(b'original-output')
        self.изгради_извор('public class 시험 { public static int Изврши_2() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.изгради_извор('public class 시험 { public static int Изврши_2() { return 37; } }')
        self.assertEqual((self.Именик_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_табела = subprocess.check_output(['readelf', '-l', str(self.Именик_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_табела)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.изгради_извор('public class 시험 { public static int Изврши_2() { return корисник.실행권한(); } }',
                    {'корисник': 'public class корисник { public static native int 실행권한(); }'}, цел='user')
        податоци = (self.Именик_VALUE / 'native').read_bytes()
        self.assertEqual(податоци[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', податоци, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Именик_VALUE / 'native')]))
        # корисник ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.изгради_извор('public class 시험 { public static int Изврши_2() { return уред_VALUE.포트읽기(1); } }',
                    {'уред_VALUE': 'public class уред_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, цел='user')

    def test_내보내기검증(self):
        ИЗВОР = 'public class 시험 { public static int Изврши_2() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.изгради_извор(ИЗВОР, цел='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Именик_VALUE / 'native')]))
        self.изгради_извор(ИЗВОР, 성공=False, 내보냄='bad;name=시험.호출')
        self.изгради_извор(ИЗВОР, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
