"""фактический_данные ELF 실행 + OpenJDK результат 대조. 임시 испытания 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

компилятор = Path(__file__).resolve().parents[1] / 'компилятор.py'


class тест_собственный(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Каталог_ЗНАЧЕН = Path(self.임시.name)

    def компилировать_источник(self, исходныйКод, добавить_ввод=None, 성공=True, целевое_значение='linux', 내보냄=None):
        путь_Список = []
        for Название, контент_ЗНАЧЕН in dict({'испытания': исходныйКод}, **(добавить_ввод or {})).items():
            путь = self.Каталог_ЗНАЧЕН / (Название + '.java')
            путь.write_text(контент_ЗНАЧЕН, encoding='utf-8')
            путь_Список.append(str(путь))
        команда = [sys.executable, str(компилятор), '--target', целевое_значение, '--entry', 'испытания.запустить', '-o', str(self.Каталог_ЗНАЧЕН / 'native')]
        if 내보냄 is not None: команда += ['--export', 내보냄]
        результат = subprocess.run(команда + путь_Список,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(результат.returncode, 0, результат.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(результат.returncode, 0)
            self.assertIn('компилировать_источник ошибка'.encode(), результат.stderr)
        return результат

    def выполнение_KR(self):
        return subprocess.run([str(self.Каталог_ЗНАЧЕН / 'native')], timeout=5).returncode

    def 자바대조(self, исходныйКод, добавить_ввод=None):
        self.компилировать_источник(исходныйКод, добавить_ввод)
        (self.Каталог_ЗНАЧЕН / 'узел.java').write_text(
            'public class узел { public static void main(String[] аргументы) { System.exit(испытания.запустить()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Каталог_ЗНАЧЕН)] +
                       [str(путь) for путь in self.Каталог_ЗНАЧЕН.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Каталог_ЗНАЧЕН), 'узел'], timeout=5).returncode
        фактический_данные = self.выполнение_KR()
        self.assertGreaterEqual(фактический_данные, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 проверять)')
        self.assertEqual(фактический_данные, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class испытания {
            static int 섞기(int 가, int СЕКУНДЫ_операнд) {
                return ((가 + СЕКУНДЫ_операнд) ^ (가 - СЕКУНДЫ_операнд) ^ (가 * СЕКУНДЫ_операнд) ^ (가 & СЕКУНДЫ_операнд) ^ (가 | СЕКУНДЫ_операнд))
                    + (가 << СЕКУНДЫ_операнд) + (가 >> СЕКУНДЫ_операнд) + (가 >>> СЕКУНДЫ_операнд);
            }
            public static int запустить() {
                int SUM_ЗНАЧЕН = 7;
                int ЗНАЧЕН = 12345;
                for (int ИНДЕКС = -65; ИНДЕКС <= 65; ИНДЕКС++) {
                    ЗНАЧЕН = ЗНАЧЕН * 1664525 + 1013904223;
                    SUM_ЗНАЧЕН = SUM_ЗНАЧЕН * 31 + 섞기(ЗНАЧЕН, ИНДЕКС);
                    SUM_ЗНАЧЕН += (byte)ЗНАЧЕН + (short)ЗНАЧЕН + (char)ЗНАЧЕН;
                }
                return (SUM_ЗНАЧЕН & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class испытания {
            static int[] ЗНАЧЕН = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int запустить() {
                int SUM_ЗНАЧЕН = 13;
                for (int 가 = 0; 가 < ЗНАЧЕН.length; 가++)
                    for (int СЕКУНДЫ_операнд = 1; СЕКУНДЫ_операнд < ЗНАЧЕН.length; СЕКУНДЫ_операнд++)
                        SUM_ЗНАЧЕН = SUM_ЗНАЧЕН * 31 + ЗНАЧЕН[가] / ЗНАЧЕН[СЕКУНДЫ_операнд] + ЗНАЧЕН[가] % ЗНАЧЕН[СЕКУНДЫ_операнд];
                return (SUM_ЗНАЧЕН & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class испытания {
            static int[] Create_ввод(int Размер) { return new int[Размер]; }
            public static int запустить() {
                int[] 가 = Create_ввод(8); int[] СЕКУНДЫ_операнд = 가; int[] пустой_объект = new int[0];
                if (가 != СЕКУНДЫ_операнд || 가 == null || пустой_объект.length != 0 || 가[7] != 0) return 99;
                int ЗНАЧЕН = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ЗНАЧЕН + СЕКУНДЫ_операнд[2] + СЕКУНДЫ_операнд[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class испытания {
            static int ЗНАЧЕН = 보조.초기값();
            static int 계산(int 가, int СЕКУНДЫ_операнд, int 다, int 라, int 마) {
                return 가 + СЕКУНДЫ_операнд * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int запустить() { return 계산(1, 2, 3, 4, ЗНАЧЕН) + 보조.Чтение(); }
        }''', {'보조': '''public class 보조 {
            static int ЗНАЧЕН = 3;
            static int 초기값() { return ++ЗНАЧЕН; }
            static int Чтение() { return ЗНАЧЕН; }
        }'''})

    def тест_инициализация_цикл(self):
        self.자바대조('''public class испытания {
            static int ЗНАЧЕН = 보조.Чтение() + 1;
            public static int запустить() { return ЗНАЧЕН * 10 + 보조.Чтение(); }
        }''', {'보조': '''public class 보조 {
            static int ЗНАЧЕН = испытания.ЗНАЧЕН + 2;
            static int Чтение() { return ЗНАЧЕН; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class испытания {
            static String текст = "한글\\u0000😀";
            public static int запустить() {
                if (текст != "한글\\u0000😀") return 99;
                return (текст.length() + текст.charAt(2) + текст.charAt(3) + текст.charAt(4)) % 251;
            }
        }''')

    def тест_перейти_И_рекурсия(self):
        self.자바대조('''public class испытания {
            static int факториал(int ЗНАЧЕН) { return ЗНАЧЕН <= 1 ? 1 : ЗНАЧЕН * факториал(ЗНАЧЕН - 1); }
            static int 연속(int ЗНАЧЕН) {
                switch (ЗНАЧЕН) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ЗНАЧЕН) {
                switch (ЗНАЧЕН) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int запустить() { return (факториал(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        декларация = '\n'.join('int ЗНАЧЕН{} = {};'.format(ИНДЕКС, ИНДЕКС) for ИНДЕКС in range(270))
        덧셈 = '+'.join('ЗНАЧЕН{}'.format(ИНДЕКС) for ИНДЕКС in range(270))
        self.자바대조('public class испытания { public static int запустить() {' + декларация +
                    'ЗНАЧЕН_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int нуль_операнд = 0; return 1 / нуль_операнд;', 101),
            ('int[] ЗНАЧЕН = null; return ЗНАЧЕН.length;', 102),
            ('int[] ЗНАЧЕН = new int[1]; return ЗНАЧЕН[1];', 103),
            ('int[] ЗНАЧЕН = new int[1]; ЗНАЧЕН[-1] = 3; return 0;', 103),
            ('int ЗНАЧЕН = -1; return new int[ЗНАЧЕН].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for текст_сообщения_ЗНАЧЕН, 기대 in 경우들:
            with self.subTest(текст_сообщения_ЗНАЧЕН=текст_сообщения_ЗНАЧЕН):
                self.компилировать_источник('public class испытания { public static int запустить() { ' + текст_сообщения_ЗНАЧЕН + ' } }')
                self.assertEqual(self.выполнение_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ЗНАЧЕН; public static int запустить() { return 0; }',
            'public static int запустить() { Object ЗНАЧЕН = new Object(); return 0; }',
            'public static int запустить() { System.out.println("hello"); return 0; }',
            'public static int запустить() { try { return 1; } catch (Exception ошибка) { return 2; } }',
            'public static synchronized int запустить() { return 0; }',
            'public static int запустить() { return new byte[3].length; }',
            'static native int внешний_ЗНАЧЕН(); public static int запустить() { return внешний_ЗНАЧЕН(); }',
            'int ЗНАЧЕН; public static int запустить() { return 0; }',
        ]
        for текст_сообщения_ЗНАЧЕН in 경우들:
            with self.subTest(текст_сообщения_ЗНАЧЕН=текст_сообщения_ЗНАЧЕН):
                self.компилировать_источник('public class испытания { ' + текст_сообщения_ЗНАЧЕН + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        текстовыйВывод = self.Каталог_ЗНАЧЕН / 'native'
        текстовыйВывод.write_bytes(b'original-output')
        self.компилировать_источник('public class испытания { public static int запустить() { return missing; } }', 성공=False)
        self.assertEqual(текстовыйВывод.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.компилировать_источник('public class испытания { public static int запустить() { return 37; } }')
        self.assertEqual((self.Каталог_ЗНАЧЕН / 'native').read_bytes()[:5], b'\x7fELF\x01')
        таблица_подстановки = subprocess.check_output(['readelf', '-l', str(self.Каталог_ЗНАЧЕН / 'native')])
        self.assertNotIn(b'INTERP', таблица_подстановки)
        self.assertEqual(self.выполнение_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.компилировать_источник('public class испытания { public static int запустить() { return пространство_пользователя.выполнение_Полномочие(); } }',
                    {'пространство_пользователя': 'public class пространство_пользователя { public static native int выполнение_Полномочие(); }'}, целевое_значение='user')
        данные = (self.Каталог_ЗНАЧЕН / 'native').read_bytes()
        self.assertEqual(данные[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', данные, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Каталог_ЗНАЧЕН / 'native')]))
        # пространство_пользователя ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.компилировать_источник('public class испытания { public static int запустить() { return устройство_ЗНАЧЕН.чтение_аппаратный_порт(1); } }',
                    {'устройство_ЗНАЧЕН': 'public class устройство_ЗНАЧЕН { public static native int чтение_аппаратный_порт(int ЗНАЧЕН); }'}, 성공=False, целевое_значение='user')

    def тест_экспортировать_проверка(self):
        исходныйКод = 'public class испытания { public static int запустить() { return 0; } static int 호출(int ЗНАЧЕН) { return ЗНАЧЕН; } }'
        self.компилировать_источник(исходныйКод, целевое_значение='kernel', 내보냄='kernel_dispatch=испытания.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Каталог_ЗНАЧЕН / 'native')]))
        self.компилировать_источник(исходныйКод, 성공=False, 내보냄='bad;name=испытания.호출')
        self.компилировать_источник(исходныйКод, 성공=False, 내보냄='missing=испытания.없음')


if __name__ == '__main__':
    unittest.main()
