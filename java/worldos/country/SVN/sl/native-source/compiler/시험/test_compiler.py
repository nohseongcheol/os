"""dejanski_podatki ELF Izvedi_ukaz + OpenJDK REZULTAT 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

prevajalnik = Path(__file__).resolve().parents[1] / 'prevajalnik.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Imenik_VALUE = Path(self.임시.name)

    def prevajati_vir(self, VIR, dodati_vnos=None, 성공=True, tarča='linux', 내보냄=None):
        pot_Seznam = []
        for Ime, vsebina_VALUE in dict({'시험': VIR}, **(dodati_vnos or {})).items():
            POT = self.Imenik_VALUE / (Ime + '.java')
            POT.write_text(vsebina_VALUE, encoding='utf-8')
            pot_Seznam.append(str(POT))
        Ukaz = [sys.executable, str(prevajalnik), '--target', tarča, '--entry', '시험.Zaženi', '-o', str(self.Imenik_VALUE / 'native')]
        if 내보냄 is not None: Ukaz += ['--export', 내보냄]
        REZULTAT = subprocess.run(Ukaz + pot_Seznam,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(REZULTAT.returncode, 0, REZULTAT.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(REZULTAT.returncode, 0)
            self.assertIn('prevajati_vir NAPAKA'.encode(), REZULTAT.stderr)
        return REZULTAT

    def 실행결과(self):
        return subprocess.run([str(self.Imenik_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, VIR, dodati_vnos=None):
        self.prevajati_vir(VIR, dodati_vnos)
        (self.Imenik_VALUE / 'gostiti.java').write_text(
            'public class gostiti { public static void main(String[] Argumenti) { System.exit(시험.Zaženi()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Imenik_VALUE)] +
                       [str(POT) for POT in self.Imenik_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Imenik_VALUE), 'gostiti'], timeout=5).returncode
        dejanski_podatki = self.실행결과()
        self.assertGreaterEqual(dejanski_podatki, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 확인)')
        self.assertEqual(dejanski_podatki, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SECOND_operand) {
                return ((가 + SECOND_operand) ^ (가 - SECOND_operand) ^ (가 * SECOND_operand) ^ (가 & SECOND_operand) ^ (가 | SECOND_operand))
                    + (가 << SECOND_operand) + (가 >> SECOND_operand) + (가 >>> SECOND_operand);
            }
            public static int Zaženi() {
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
            public static int Zaženi() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operand = 1; SECOND_operand < VALUE.length; SECOND_operand++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operand] + VALUE[가] % VALUE[SECOND_operand];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Ustvari_vnos(int Velikost) { return new int[Velikost]; }
            public static int Zaženi() {
                int[] 가 = Ustvari_vnos(8); int[] SECOND_operand = 가; int[] prazen_predmet = new int[0];
                if (가 != SECOND_operand || 가 == null || prazen_predmet.length != 0 || 가[7] != 0) return 99;
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
            public static int Zaženi() { return 계산(1, 2, 3, 4, VALUE) + 보조.Branje(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Branje() { return VALUE; }
        }'''})

    def preskusiti_inicializacija_Krog(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Branje() + 1;
            public static int Zaženi() { return VALUE * 10 + 보조.Branje(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Branje() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Besedilo = "한글\\u0000😀";
            public static int Zaženi() {
                if (Besedilo != "한글\\u0000😀") return 99;
                return (Besedilo.length() + Besedilo.charAt(2) + Besedilo.charAt(3) + Besedilo.charAt(4)) % 251;
            }
        }''')

    def preskusiti_SWITCH_AND_rekurzija(self):
        self.자바대조('''public class 시험 {
            static int fakulteta(int VALUE) { return VALUE <= 1 ? 1 : VALUE * fakulteta(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Zaženi() { return (fakulteta(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklaracija = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Zaženi() {' + deklaracija +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nič_operand = 0; return 1 / nič_operand;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for telo_VALUE, 기대 in 경우들:
            with self.subTest(telo_VALUE=telo_VALUE):
                self.prevajati_vir('public class 시험 { public static int Zaženi() { ' + telo_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Zaženi() { return 0; }',
            'public static int Zaženi() { Object VALUE = new Object(); return 0; }',
            'public static int Zaženi() { System.out.println("hello"); return 0; }',
            'public static int Zaženi() { try { return 1; } catch (Exception NAPAKA) { return 2; } }',
            'public static synchronized int Zaženi() { return 0; }',
            'public static int Zaženi() { return new byte[3].length; }',
            'static native int zunanji_VALUE(); public static int Zaženi() { return zunanji_VALUE(); }',
            'int VALUE; public static int Zaženi() { return 0; }',
        ]
        for telo_VALUE in 경우들:
            with self.subTest(telo_VALUE=telo_VALUE):
                self.prevajati_vir('public class 시험 { ' + telo_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Izpis = self.Imenik_VALUE / 'native'
        Izpis.write_bytes(b'original-output')
        self.prevajati_vir('public class 시험 { public static int Zaženi() { return missing; } }', 성공=False)
        self.assertEqual(Izpis.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.prevajati_vir('public class 시험 { public static int Zaženi() { return 37; } }')
        self.assertEqual((self.Imenik_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        iskalna_tabela = subprocess.check_output(['readelf', '-l', str(self.Imenik_VALUE / 'native')])
        self.assertNotIn(b'INTERP', iskalna_tabela)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.prevajati_vir('public class 시험 { public static int Zaženi() { return uporabnik.실행권한(); } }',
                    {'uporabnik': 'public class uporabnik { public static native int 실행권한(); }'}, tarča='user')
        podatki = (self.Imenik_VALUE / 'native').read_bytes()
        self.assertEqual(podatki[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', podatki, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Imenik_VALUE / 'native')]))
        # uporabnik ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.prevajati_vir('public class 시험 { public static int Zaženi() { return naprava_VALUE.포트읽기(1); } }',
                    {'naprava_VALUE': 'public class naprava_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, tarča='user')

    def preskusiti_izvoziti_preverjanje_veljavnosti(self):
        VIR = 'public class 시험 { public static int Zaženi() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.prevajati_vir(VIR, tarča='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Imenik_VALUE / 'native')]))
        self.prevajati_vir(VIR, 성공=False, 내보냄='bad;name=시험.호출')
        self.prevajati_vir(VIR, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
