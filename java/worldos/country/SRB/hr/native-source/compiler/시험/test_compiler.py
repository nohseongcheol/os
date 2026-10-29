"""stvaran_podaci ELF Izvrši_naredba + OpenJDK REZULTAT 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilator = Path(__file__).resolve().parents[1] / 'kompilator.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.imenik_VALUE = Path(self.임시.name)

    def programski_prevesti_izvor(self, IZVOR, dodati_unos=None, 성공=True, cilj='linux', 내보냄=None):
        put_Popis = []
        for Ime, Sadržaj_VALUE in dict({'시험': IZVOR}, **(dodati_unos or {})).items():
            PUTANJA = self.imenik_VALUE / (Ime + '.java')
            PUTANJA.write_text(Sadržaj_VALUE, encoding='utf-8')
            put_Popis.append(str(PUTANJA))
        Naredba = [sys.executable, str(kompilator), '--target', cilj, '--entry', '시험.Pokreni', '-o', str(self.imenik_VALUE / 'native')]
        if 내보냄 is not None: Naredba += ['--export', 내보냄]
        REZULTAT = subprocess.run(Naredba + put_Popis,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(REZULTAT.returncode, 0, REZULTAT.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(REZULTAT.returncode, 0)
            self.assertIn('programski_prevesti_izvor GREŠKA'.encode(), REZULTAT.stderr)
        return REZULTAT

    def 실행결과(self):
        return subprocess.run([str(self.imenik_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, IZVOR, dodati_unos=None):
        self.programski_prevesti_izvor(IZVOR, dodati_unos)
        (self.imenik_VALUE / 'domaćin.java').write_text(
            'public class domaćin { public static void main(String[] Argumenti) { System.exit(시험.Pokreni()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.imenik_VALUE)] +
                       [str(PUTANJA) for PUTANJA in self.imenik_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.imenik_VALUE), 'domaćin'], timeout=5).returncode
        stvaran_podaci = self.실행결과()
        self.assertGreaterEqual(stvaran_podaci, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 provjeriti)')
        self.assertEqual(stvaran_podaci, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SECOND_operand) {
                return ((가 + SECOND_operand) ^ (가 - SECOND_operand) ^ (가 * SECOND_operand) ^ (가 & SECOND_operand) ^ (가 | SECOND_operand))
                    + (가 << SECOND_operand) + (가 >> SECOND_operand) + (가 >>> SECOND_operand);
            }
            public static int Pokreni() {
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
            public static int Pokreni() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operand = 1; SECOND_operand < VALUE.length; SECOND_operand++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operand] + VALUE[가] % VALUE[SECOND_operand];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Create_unos(int Veličina) { return new int[Veličina]; }
            public static int Pokreni() {
                int[] 가 = Create_unos(8); int[] SECOND_operand = 가; int[] 빈것 = new int[0];
                if (가 != SECOND_operand || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + SECOND_operand[2] + SECOND_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int SECOND_operand, int 다, int 라, int 마) {
                return 가 + SECOND_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Pokreni() { return 계산(1, 2, 3, 4, VALUE) + 보조.Čitaj(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Čitaj() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Čitaj() + 1;
            public static int Pokreni() { return VALUE * 10 + 보조.Čitaj(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Čitaj() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tekst = "한글\\u0000😀";
            public static int Pokreni() {
                if (Tekst != "한글\\u0000😀") return 99;
                return (Tekst.length() + Tekst.charAt(2) + Tekst.charAt(3) + Tekst.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktorijel(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktorijel(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Pokreni() { return (faktorijel(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklaracija = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Pokreni() {' + deklaracija +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nula_operand = 0; return 1 / nula_operand;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for tijelo_VALUE, 기대 in 경우들:
            with self.subTest(tijelo_VALUE=tijelo_VALUE):
                self.programski_prevesti_izvor('public class 시험 { public static int Pokreni() { ' + tijelo_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Pokreni() { return 0; }',
            'public static int Pokreni() { Object VALUE = new Object(); return 0; }',
            'public static int Pokreni() { System.out.println("hello"); return 0; }',
            'public static int Pokreni() { try { return 1; } catch (Exception GREŠKA) { return 2; } }',
            'public static synchronized int Pokreni() { return 0; }',
            'public static int Pokreni() { return new byte[3].length; }',
            'static native int vanjski_VALUE(); public static int Pokreni() { return vanjski_VALUE(); }',
            'int VALUE; public static int Pokreni() { return 0; }',
        ]
        for tijelo_VALUE in 경우들:
            with self.subTest(tijelo_VALUE=tijelo_VALUE):
                self.programski_prevesti_izvor('public class 시험 { ' + tijelo_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Izlaz = self.imenik_VALUE / 'native'
        Izlaz.write_bytes(b'original-output')
        self.programski_prevesti_izvor('public class 시험 { public static int Pokreni() { return missing; } }', 성공=False)
        self.assertEqual(Izlaz.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.programski_prevesti_izvor('public class 시험 { public static int Pokreni() { return 37; } }')
        self.assertEqual((self.imenik_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_tablica = subprocess.check_output(['readelf', '-l', str(self.imenik_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_tablica)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.programski_prevesti_izvor('public class 시험 { public static int Pokreni() { return korisnik.실행권한(); } }',
                    {'korisnik': 'public class korisnik { public static native int 실행권한(); }'}, cilj='user')
        podaci = (self.imenik_VALUE / 'native').read_bytes()
        self.assertEqual(podaci[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', podaci, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.imenik_VALUE / 'native')]))
        # korisnik ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.programski_prevesti_izvor('public class 시험 { public static int Pokreni() { return uređaj_VALUE.포트읽기(1); } }',
                    {'uređaj_VALUE': 'public class uređaj_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, cilj='user')

    def test_내보내기검증(self):
        IZVOR = 'public class 시험 { public static int Pokreni() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.programski_prevesti_izvor(IZVOR, cilj='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.imenik_VALUE / 'native')]))
        self.programski_prevesti_izvor(IZVOR, 성공=False, 내보냄='bad;name=시험.호출')
        self.programski_prevesti_izvor(IZVOR, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
