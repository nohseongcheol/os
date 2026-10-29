"""rzeczywisty_dane ELF Wykonaj_polecenie + OpenJDK WYNIK 대조. 임시 testy 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilator = Path(__file__).resolve().parents[1] / 'kompilator.py'


class test_natywny(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Katalog_WARTOŚĆ = Path(self.임시.name)

    def kompilować_źródło(self, plik_źródłowy, dołączać_wpis=None, 성공=True, wartość_docelowa='linux', 내보냄=None):
        ścieżka_Lista = []
        for Nazwa, treść_WARTOŚĆ_cb0f2404 in dict({'testy': plik_źródłowy}, **(dołączać_wpis or {})).items():
            ścieżka_2 = self.Katalog_WARTOŚĆ / (Nazwa + '.java')
            ścieżka_2.write_text(treść_WARTOŚĆ_cb0f2404, encoding='utf-8')
            ścieżka_Lista.append(str(ścieżka_2))
        polecenie = [sys.executable, str(kompilator), '--target', wartość_docelowa, '--entry', 'testy.Uruchom_2', '-o', str(self.Katalog_WARTOŚĆ / 'native')]
        if 내보냄 is not None: polecenie += ['--export', 내보냄]
        WYNIK = subprocess.run(polecenie + ścieżka_Lista,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(WYNIK.returncode, 0, WYNIK.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(WYNIK.returncode, 0)
            self.assertIn('kompilować_źródło błąd'.encode(), WYNIK.stderr)
        return WYNIK

    def wykonanie_KR(self):
        return subprocess.run([str(self.Katalog_WARTOŚĆ / 'native')], timeout=5).returncode

    def 자바대조(self, plik_źródłowy, dołączać_wpis=None):
        self.kompilować_źródło(plik_źródłowy, dołączać_wpis)
        (self.Katalog_WARTOŚĆ / 'host.java').write_text(
            'public class host { public static void main(String[] argumenty) { System.exit(testy.Uruchom_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Katalog_WARTOŚĆ)] +
                       [str(ścieżka_2) for ścieżka_2 in self.Katalog_WARTOŚĆ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Katalog_WARTOŚĆ), 'host'], timeout=5).returncode
        rzeczywisty_dane = self.wykonanie_KR()
        self.assertGreaterEqual(rzeczywisty_dane, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 확인)')
        self.assertEqual(rzeczywisty_dane, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class testy {
            static int 섞기(int 가, int SEKUNDA_operand) {
                return ((가 + SEKUNDA_operand) ^ (가 - SEKUNDA_operand) ^ (가 * SEKUNDA_operand) ^ (가 & SEKUNDA_operand) ^ (가 | SEKUNDA_operand))
                    + (가 << SEKUNDA_operand) + (가 >> SEKUNDA_operand) + (가 >>> SEKUNDA_operand);
            }
            public static int Uruchom_2() {
                int SUMA_WARTOŚĆ = 7;
                int WARTOŚĆ = 12345;
                for (int INDEKS = -65; INDEKS <= 65; INDEKS++) {
                    WARTOŚĆ = WARTOŚĆ * 1664525 + 1013904223;
                    SUMA_WARTOŚĆ = SUMA_WARTOŚĆ * 31 + 섞기(WARTOŚĆ, INDEKS);
                    SUMA_WARTOŚĆ += (byte)WARTOŚĆ + (short)WARTOŚĆ + (char)WARTOŚĆ;
                }
                return (SUMA_WARTOŚĆ & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class testy {
            static int[] WARTOŚĆ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Uruchom_2() {
                int SUMA_WARTOŚĆ = 13;
                for (int 가 = 0; 가 < WARTOŚĆ.length; 가++)
                    for (int SEKUNDA_operand = 1; SEKUNDA_operand < WARTOŚĆ.length; SEKUNDA_operand++)
                        SUMA_WARTOŚĆ = SUMA_WARTOŚĆ * 31 + WARTOŚĆ[가] / WARTOŚĆ[SEKUNDA_operand] + WARTOŚĆ[가] % WARTOŚĆ[SEKUNDA_operand];
                return (SUMA_WARTOŚĆ & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class testy {
            static int[] Twórca_wpis(int Rozmiar) { return new int[Rozmiar]; }
            public static int Uruchom_2() {
                int[] 가 = Twórca_wpis(8); int[] SEKUNDA_operand = 가; int[] 빈것 = new int[0];
                if (가 != SEKUNDA_operand || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int WARTOŚĆ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return WARTOŚĆ + SEKUNDA_operand[2] + SEKUNDA_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class testy {
            static int WARTOŚĆ = 보조.초기값();
            static int 계산(int 가, int SEKUNDA_operand, int 다, int 라, int 마) {
                return 가 + SEKUNDA_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Uruchom_2() { return 계산(1, 2, 3, 4, WARTOŚĆ) + 보조.Odczyt(); }
        }''', {'보조': '''public class 보조 {
            static int WARTOŚĆ = 3;
            static int 초기값() { return ++WARTOŚĆ; }
            static int Odczyt() { return WARTOŚĆ; }
        }'''})

    def test_inicjowanie_Cykl(self):
        self.자바대조('''public class testy {
            static int WARTOŚĆ = 보조.Odczyt() + 1;
            public static int Uruchom_2() { return WARTOŚĆ * 10 + 보조.Odczyt(); }
        }''', {'보조': '''public class 보조 {
            static int WARTOŚĆ = testy.WARTOŚĆ + 2;
            static int Odczyt() { return WARTOŚĆ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class testy {
            static String tekst = "한글\\u0000😀";
            public static int Uruchom_2() {
                if (tekst != "한글\\u0000😀") return 99;
                return (tekst.length() + tekst.charAt(2) + tekst.charAt(3) + tekst.charAt(4)) % 251;
            }
        }''')

    def test_zmiana_ORAZ_rekursja(self):
        self.자바대조('''public class testy {
            static int silnia(int WARTOŚĆ) { return WARTOŚĆ <= 1 ? 1 : WARTOŚĆ * silnia(WARTOŚĆ - 1); }
            static int 연속(int WARTOŚĆ) {
                switch (WARTOŚĆ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int WARTOŚĆ) {
                switch (WARTOŚĆ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Uruchom_2() { return (silnia(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklaracja = '\n'.join('int WARTOŚĆ{} = {};'.format(INDEKS, INDEKS) for INDEKS in range(270))
        덧셈 = '+'.join('WARTOŚĆ{}'.format(INDEKS) for INDEKS in range(270))
        self.자바대조('public class testy { public static int Uruchom_2() {' + deklaracja +
                    'WARTOŚĆ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int zero_operand = 0; return 1 / zero_operand;', 101),
            ('int[] WARTOŚĆ = null; return WARTOŚĆ.length;', 102),
            ('int[] WARTOŚĆ = new int[1]; return WARTOŚĆ[1];', 103),
            ('int[] WARTOŚĆ = new int[1]; WARTOŚĆ[-1] = 3; return 0;', 103),
            ('int WARTOŚĆ = -1; return new int[WARTOŚĆ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for treść_WARTOŚĆ, 기대 in 경우들:
            with self.subTest(treść_WARTOŚĆ=treść_WARTOŚĆ):
                self.kompilować_źródło('public class testy { public static int Uruchom_2() { ' + treść_WARTOŚĆ + ' } }')
                self.assertEqual(self.wykonanie_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long WARTOŚĆ; public static int Uruchom_2() { return 0; }',
            'public static int Uruchom_2() { Object WARTOŚĆ = new Object(); return 0; }',
            'public static int Uruchom_2() { System.out.println("hello"); return 0; }',
            'public static int Uruchom_2() { try { return 1; } catch (Exception błąd) { return 2; } }',
            'public static synchronized int Uruchom_2() { return 0; }',
            'public static int Uruchom_2() { return new byte[3].length; }',
            'static native int zewnętrzny_WARTOŚĆ(); public static int Uruchom_2() { return zewnętrzny_WARTOŚĆ(); }',
            'int WARTOŚĆ; public static int Uruchom_2() { return 0; }',
        ]
        for treść_WARTOŚĆ in 경우들:
            with self.subTest(treść_WARTOŚĆ=treść_WARTOŚĆ):
                self.kompilować_źródło('public class testy { ' + treść_WARTOŚĆ + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        pozycja_wyjścia = self.Katalog_WARTOŚĆ / 'native'
        pozycja_wyjścia.write_bytes(b'original-output')
        self.kompilować_źródło('public class testy { public static int Uruchom_2() { return missing; } }', 성공=False)
        self.assertEqual(pozycja_wyjścia.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompilować_źródło('public class testy { public static int Uruchom_2() { return 37; } }')
        self.assertEqual((self.Katalog_WARTOŚĆ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        WYSZUKAJ_tabela = subprocess.check_output(['readelf', '-l', str(self.Katalog_WARTOŚĆ / 'native')])
        self.assertNotIn(b'INTERP', WYSZUKAJ_tabela)
        self.assertEqual(self.wykonanie_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompilować_źródło('public class testy { public static int Uruchom_2() { return przestrzeń_użytkownika.wykonanie_pozwolenie(); } }',
                    {'przestrzeń_użytkownika': 'public class przestrzeń_użytkownika { public static native int wykonanie_pozwolenie(); }'}, wartość_docelowa='user')
        dane = (self.Katalog_WARTOŚĆ / 'native').read_bytes()
        self.assertEqual(dane[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', dane, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Katalog_WARTOŚĆ / 'native')]))
        # przestrzeń_użytkownika ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompilować_źródło('public class testy { public static int Uruchom_2() { return urządzenie_WARTOŚĆ.포트읽기(1); } }',
                    {'urządzenie_WARTOŚĆ': 'public class urządzenie_WARTOŚĆ { public static native int 포트읽기(int WARTOŚĆ); }'}, 성공=False, wartość_docelowa='user')

    def test_eksportować_walidacja(self):
        plik_źródłowy = 'public class testy { public static int Uruchom_2() { return 0; } static int 호출(int WARTOŚĆ) { return WARTOŚĆ; } }'
        self.kompilować_źródło(plik_źródłowy, wartość_docelowa='kernel', 내보냄='kernel_dispatch=testy.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Katalog_WARTOŚĆ / 'native')]))
        self.kompilować_źródło(plik_źródłowy, 성공=False, 내보냄='bad;name=testy.호출')
        self.kompilować_źródło(plik_źródłowy, 성공=False, 내보냄='missing=testy.없음')


if __name__ == '__main__':
    unittest.main()
