"""фактично_дані ELF Виконати_команда + OpenJDK результат 대조. 임시 випробування 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

компілятор = Path(__file__).resolve().parents[1] / 'компілятор.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Каталог_значення = Path(self.임시.name)

    def компілювати_джерело(self, вихіднийКод, додавати_запис=None, 성공=True, мета='linux', 내보냄=None):
        шлях_список = []
        for Назва, Вміст_значення in dict({'випробування': вихіднийКод}, **(додавати_запис or {})).items():
            шлях = self.Каталог_значення / (Назва + '.java')
            шлях.write_text(Вміст_значення, encoding='utf-8')
            шлях_список.append(str(шлях))
        команда = [sys.executable, str(компілятор), '--target', мета, '--entry', 'випробування.запустити', '-o', str(self.Каталог_значення / 'native')]
        if 내보냄 is not None: команда += ['--export', 내보냄]
        результат = subprocess.run(команда + шлях_список,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(результат.returncode, 0, результат.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(результат.returncode, 0)
            self.assertIn('компілювати_джерело ПОМИЛКА'.encode(), результат.stderr)
        return результат

    def 실행결과(self):
        return subprocess.run([str(self.Каталог_значення / 'native')], timeout=5).returncode

    def 자바대조(self, вихіднийКод, додавати_запис=None):
        self.компілювати_джерело(вихіднийКод, додавати_запис)
        (self.Каталог_значення / 'хост.java').write_text(
            'public class хост { public static void main(String[] аргументи) { System.exit(випробування.запустити()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Каталог_значення)] +
                       [str(шлях) for шлях in self.Каталог_значення.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Каталог_значення), 'хост'], timeout=5).returncode
        фактично_дані = self.실행결과()
        self.assertGreaterEqual(фактично_дані, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 перевіряти)')
        self.assertEqual(фактично_дані, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class випробування {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int запустити() {
                int 합 = 7;
                int значення = 12345;
                for (int індекс = -65; індекс <= 65; індекс++) {
                    значення = значення * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(значення, індекс);
                    합 += (byte)значення + (short)значення + (char)значення;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class випробування {
            static int[] значення = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int запустити() {
                int 합 = 13;
                for (int 가 = 0; 가 < значення.length; 가++)
                    for (int 나 = 1; 나 < значення.length; 나++)
                        합 = 합 * 31 + значення[가] / значення[나] + значення[가] % значення[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class випробування {
            static int[] Створення_запис(int Розмір) { return new int[Розмір]; }
            public static int запустити() {
                int[] 가 = Створення_запис(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int значення = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return значення + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class випробування {
            static int значення = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int запустити() { return 계산(1, 2, 3, 4, значення) + 보조.Читання(); }
        }''', {'보조': '''public class 보조 {
            static int значення = 3;
            static int 초기값() { return ++значення; }
            static int Читання() { return значення; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class випробування {
            static int значення = 보조.Читання() + 1;
            public static int запустити() { return значення * 10 + 보조.Читання(); }
        }''', {'보조': '''public class 보조 {
            static int значення = випробування.значення + 2;
            static int Читання() { return значення; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class випробування {
            static String текст = "한글\\u0000😀";
            public static int запустити() {
                if (текст != "한글\\u0000😀") return 99;
                return (текст.length() + текст.charAt(2) + текст.charAt(3) + текст.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class випробування {
            static int факторіал(int значення) { return значення <= 1 ? 1 : значення * факторіал(значення - 1); }
            static int 연속(int значення) {
                switch (значення) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int значення) {
                switch (значення) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int запустити() { return (факторіал(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        оголошення_4f4f026b = '\n'.join('int значення{} = {};'.format(індекс, індекс) for індекс in range(270))
        덧셈 = '+'.join('значення{}'.format(індекс) for індекс in range(270))
        self.자바대조('public class випробування { public static int запустити() {' + оголошення_4f4f026b +
                    'значення_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int нуль_операнд = 0; return 1 / нуль_операнд;', 101),
            ('int[] значення = null; return значення.length;', 102),
            ('int[] значення = new int[1]; return значення[1];', 103),
            ('int[] значення = new int[1]; значення[-1] = 3; return 0;', 103),
            ('int значення = -1; return new int[значення].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for тіло_повідомлення_значення, 기대 in 경우들:
            with self.subTest(тіло_повідомлення_значення=тіло_повідомлення_значення):
                self.компілювати_джерело('public class випробування { public static int запустити() { ' + тіло_повідомлення_значення + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long значення; public static int запустити() { return 0; }',
            'public static int запустити() { Object значення = new Object(); return 0; }',
            'public static int запустити() { System.out.println("hello"); return 0; }',
            'public static int запустити() { try { return 1; } catch (Exception ПОМИЛКА) { return 2; } }',
            'public static synchronized int запустити() { return 0; }',
            'public static int запустити() { return new byte[3].length; }',
            'static native int зовнішній_значення(); public static int запустити() { return зовнішній_значення(); }',
            'int значення; public static int запустити() { return 0; }',
        ]
        for тіло_повідомлення_значення in 경우들:
            with self.subTest(тіло_повідомлення_значення=тіло_повідомлення_значення):
                self.компілювати_джерело('public class випробування { ' + тіло_повідомлення_значення + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Вивід = self.Каталог_значення / 'native'
        Вивід.write_bytes(b'original-output')
        self.компілювати_джерело('public class випробування { public static int запустити() { return missing; } }', 성공=False)
        self.assertEqual(Вивід.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.компілювати_джерело('public class випробування { public static int запустити() { return 37; } }')
        self.assertEqual((self.Каталог_значення / 'native').read_bytes()[:5], b'\x7fELF\x01')
        таблиця_підстановки = subprocess.check_output(['readelf', '-l', str(self.Каталог_значення / 'native')])
        self.assertNotIn(b'INTERP', таблиця_підстановки)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.компілювати_джерело('public class випробування { public static int запустити() { return простір_користувача.실행권한(); } }',
                    {'простір_користувача': 'public class простір_користувача { public static native int 실행권한(); }'}, мета='user')
        дані = (self.Каталог_значення / 'native').read_bytes()
        self.assertEqual(дані[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', дані, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Каталог_значення / 'native')]))
        # простір_користувача ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.компілювати_джерело('public class випробування { public static int запустити() { return пристрій_значення.포트읽기(1); } }',
                    {'пристрій_значення': 'public class пристрій_значення { public static native int 포트읽기(int значення); }'}, 성공=False, мета='user')

    def test_내보내기검증(self):
        вихіднийКод = 'public class випробування { public static int запустити() { return 0; } static int 호출(int значення) { return значення; } }'
        self.компілювати_джерело(вихіднийКод, мета='kernel', 내보냄='kernel_dispatch=випробування.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Каталог_значення / 'native')]))
        self.компілювати_джерело(вихіднийКод, 성공=False, 내보냄='bad;name=випробування.호출')
        self.компілювати_джерело(вихіднийКод, 성공=False, 내보냄='missing=випробування.없음')


if __name__ == '__main__':
    unittest.main()
