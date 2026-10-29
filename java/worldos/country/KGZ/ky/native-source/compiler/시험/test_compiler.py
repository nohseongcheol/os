"""актуалдуу_берилмелер ELF аткаруу_буйрук + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.каталог_маани = Path(self.임시.name)

    def тургузуу_башат(self, Булак, 추가=None, 성공=True, максат='linux', 내보냄=None):
        жол_Тизме = []
        for Аты, Мазмун_маани in dict({'시험': Булак}, **(추가 or {})).items():
            ЖОЛ = self.каталог_маани / (Аты + '.java')
            ЖОЛ.write_text(Мазмун_маани, encoding='utf-8')
            жол_Тизме.append(str(ЖОЛ))
        Команда = [sys.executable, str(컴파일러), '--target', максат, '--entry', '시험.Жүргүзүү', '-o', str(self.каталог_маани / 'native')]
        if 내보냄 is not None: Команда += ['--export', 내보냄]
        결과 = subprocess.run(Команда + жол_Тизме,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('тургузуу_башат Ката'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.каталог_маани / 'native')], timeout=5).returncode

    def 자바대조(self, Булак, 추가=None):
        self.тургузуу_башат(Булак, 추가)
        (self.каталог_маани / 'кабылдоо.java').write_text(
            'public class кабылдоо { public static void main(String[] 인수) { System.exit(시험.Жүргүзүү()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.каталог_маани)] +
                       [str(ЖОЛ) for ЖОЛ in self.каталог_маани.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.каталог_маани), 'кабылдоо'], timeout=5).returncode
        актуалдуу_берилмелер = self.실행결과()
        self.assertGreaterEqual(актуалдуу_берилмелер, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 тууралыгын_аныктоо)')
        self.assertEqual(актуалдуу_берилмелер, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Жүргүзүү() {
                int 합 = 7;
                int маани = 12345;
                for (int индекс = -65; индекс <= 65; индекс++) {
                    маани = маани * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(маани, индекс);
                    합 += (byte)маани + (short)маани + (char)маани;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] маани = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Жүргүзүү() {
                int 합 = 13;
                for (int 가 = 0; 가 < маани.length; 가++)
                    for (int 나 = 1; 나 < маани.length; 나++)
                        합 = 합 * 31 + маани[가] / маани[나] + маани[가] % маани[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] түзүү_киргизме_жазуу(int Өлчөмү) { return new int[Өлчөмү]; }
            public static int Жүргүзүү() {
                int[] 가 = түзүү_киргизме_жазуу(8); int[] 나 = 가; int[] бош_объект = new int[0];
                if (가 != 나 || 가 == null || бош_объект.length != 0 || 가[7] != 0) return 99;
                int маани = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return маани + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int маани = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Жүргүзүү() { return 계산(1, 2, 3, 4, маани) + 보조.Окуу(); }
        }''', {'보조': '''public class 보조 {
            static int маани = 3;
            static int 초기값() { return ++маани; }
            static int Окуу() { return маани; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int маани = 보조.Окуу() + 1;
            public static int Жүргүзүү() { return маани * 10 + 보조.Окуу(); }
        }''', {'보조': '''public class 보조 {
            static int маани = 시험.маани + 2;
            static int Окуу() { return маани; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Текст = "한글\\u0000😀";
            public static int Жүргүзүү() {
                if (Текст != "한글\\u0000😀") return 99;
                return (Текст.length() + Текст.charAt(2) + Текст.charAt(3) + Текст.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int факториал(int маани) { return маани <= 1 ? 1 : маани * факториал(маани - 1); }
            static int 연속(int маани) {
                switch (маани) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int маани) {
                switch (маани) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Жүргүзүү() { return (факториал(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int маани{} = {};'.format(индекс, индекс) for индекс in range(270))
        덧셈 = '+'.join('маани{}'.format(индекс) for индекс in range(270))
        self.자바대조('public class 시험 { public static int Жүргүзүү() {' + 선언 +
                    'маани_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] маани = null; return маани.length;', 102),
            ('int[] маани = new int[1]; return маани[1];', 103),
            ('int[] маани = new int[1]; маани[-1] = 3; return 0;', 103),
            ('int маани = -1; return new int[маани].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.тургузуу_башат('public class 시험 { public static int Жүргүзүү() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long маани; public static int Жүргүзүү() { return 0; }',
            'public static int Жүргүзүү() { Object маани = new Object(); return 0; }',
            'public static int Жүргүзүү() { System.out.println("hello"); return 0; }',
            'public static int Жүргүзүү() { try { return 1; } catch (Exception Ката) { return 2; } }',
            'public static synchronized int Жүргүзүү() { return 0; }',
            'public static int Жүргүзүү() { return new byte[3].length; }',
            'static native int 외부(); public static int Жүргүзүү() { return 외부(); }',
            'int маани; public static int Жүргүзүү() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.тургузуу_башат('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Чыгыш = self.каталог_маани / 'native'
        Чыгыш.write_bytes(b'original-output')
        self.тургузуу_башат('public class 시험 { public static int Жүргүзүү() { return missing; } }', 성공=False)
        self.assertEqual(Чыгыш.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.тургузуу_башат('public class 시험 { public static int Жүргүзүү() { return 37; } }')
        self.assertEqual((self.каталог_маани / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.каталог_маани / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.тургузуу_башат('public class 시험 { public static int Жүргүзүү() { return колдонуучу.실행권한(); } }',
                    {'колдонуучу': 'public class колдонуучу { public static native int 실행권한(); }'}, максат='user')
        берилмелер = (self.каталог_маани / 'native').read_bytes()
        self.assertEqual(берилмелер[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', берилмелер, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.каталог_маани / 'native')]))
        # колдонуучу ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.тургузуу_башат('public class 시험 { public static int Жүргүзүү() { return түзмөк_маани.포트읽기(1); } }',
                    {'түзмөк_маани': 'public class түзмөк_маани { public static native int 포트읽기(int маани); }'}, 성공=False, максат='user')

    def test_내보내기검증(self):
        Булак = 'public class 시험 { public static int Жүргүзүү() { return 0; } static int 호출(int маани) { return маани; } }'
        self.тургузуу_башат(Булак, максат='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.каталог_маани / 'native')]))
        self.тургузуу_башат(Булак, 성공=False, 내보냄='bad;name=시험.호출')
        self.тургузуу_башат(Булак, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
