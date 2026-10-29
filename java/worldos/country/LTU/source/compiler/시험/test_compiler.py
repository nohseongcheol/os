"""faktinis_duomenys ELF Vykdyti_komanda + OpenJDK REZULTATAS 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompiliatorius = Path(__file__).resolve().parents[1] / 'kompiliatorius.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Katalogas_VALUE = Path(self.임시.name)

    def kompiliuoti_šaltinis(self, ŠALTINIS, sujungti_įrašas=None, 성공=True, tikslas='linux', 내보냄=None):
        kelias_Sąrašas = []
        for Pavadinimas_2, Turinys_VALUE in dict({'시험': ŠALTINIS}, **(sujungti_įrašas or {})).items():
            KELIAS = self.Katalogas_VALUE / (Pavadinimas_2 + '.java')
            KELIAS.write_text(Turinys_VALUE, encoding='utf-8')
            kelias_Sąrašas.append(str(KELIAS))
        Komanda = [sys.executable, str(kompiliatorius), '--target', tikslas, '--entry', '시험.Paleisti', '-o', str(self.Katalogas_VALUE / 'native')]
        if 내보냄 is not None: Komanda += ['--export', 내보냄]
        REZULTATAS = subprocess.run(Komanda + kelias_Sąrašas,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(REZULTATAS.returncode, 0, REZULTATAS.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(REZULTATAS.returncode, 0)
            self.assertIn('kompiliuoti_šaltinis KLAIDA'.encode(), REZULTATAS.stderr)
        return REZULTATAS

    def 실행결과(self):
        return subprocess.run([str(self.Katalogas_VALUE / 'native')], timeout=5).returncode

    def 자바대조(self, ŠALTINIS, sujungti_įrašas=None):
        self.kompiliuoti_šaltinis(ŠALTINIS, sujungti_įrašas)
        (self.Katalogas_VALUE / 'organizuoti.java').write_text(
            'public class organizuoti { public static void main(String[] Argumentai) { System.exit(시험.Paleisti()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Katalogas_VALUE)] +
                       [str(KELIAS) for KELIAS in self.Katalogas_VALUE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Katalogas_VALUE), 'organizuoti'], timeout=5).returncode
        faktinis_duomenys = self.실행결과()
        self.assertGreaterEqual(faktinis_duomenys, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 patvirtinti)')
        self.assertEqual(faktinis_duomenys, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int SECOND_operandas) {
                return ((가 + SECOND_operandas) ^ (가 - SECOND_operandas) ^ (가 * SECOND_operandas) ^ (가 & SECOND_operandas) ^ (가 | SECOND_operandas))
                    + (가 << SECOND_operandas) + (가 >> SECOND_operandas) + (가 >>> SECOND_operandas);
            }
            public static int Paleisti() {
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
            public static int Paleisti() {
                int SUM_VALUE = 13;
                for (int 가 = 0; 가 < VALUE.length; 가++)
                    for (int SECOND_operandas = 1; SECOND_operandas < VALUE.length; SECOND_operandas++)
                        SUM_VALUE = SUM_VALUE * 31 + VALUE[가] / VALUE[SECOND_operandas] + VALUE[가] % VALUE[SECOND_operandas];
                return (SUM_VALUE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] kurti_įrašas(int Dydis) { return new int[Dydis]; }
            public static int Paleisti() {
                int[] 가 = kurti_įrašas(8); int[] SECOND_operandas = 가; int[] 빈것 = new int[0];
                if (가 != SECOND_operandas || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VALUE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALUE + SECOND_operandas[2] + SECOND_operandas[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.초기값();
            static int 계산(int 가, int SECOND_operandas, int 다, int 라, int 마) {
                return 가 + SECOND_operandas * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Paleisti() { return 계산(1, 2, 3, 4, VALUE) + 보조.Skaitymas(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 3;
            static int 초기값() { return ++VALUE; }
            static int Skaitymas() { return VALUE; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALUE = 보조.Skaitymas() + 1;
            public static int Paleisti() { return VALUE * 10 + 보조.Skaitymas(); }
        }''', {'보조': '''public class 보조 {
            static int VALUE = 시험.VALUE + 2;
            static int Skaitymas() { return VALUE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Tekstas = "한글\\u0000😀";
            public static int Paleisti() {
                if (Tekstas != "한글\\u0000😀") return 99;
                return (Tekstas.length() + Tekstas.charAt(2) + Tekstas.charAt(3) + Tekstas.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int faktorialas(int VALUE) { return VALUE <= 1 ? 1 : VALUE * faktorialas(VALUE - 1); }
            static int 연속(int VALUE) {
                switch (VALUE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALUE) {
                switch (VALUE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Paleisti() { return (faktorialas(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklaracija = '\n'.join('int VALUE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALUE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Paleisti() {' + deklaracija +
                    'VALUE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nulis_operandas = 0; return 1 / nulis_operandas;', 101),
            ('int[] VALUE = null; return VALUE.length;', 102),
            ('int[] VALUE = new int[1]; return VALUE[1];', 103),
            ('int[] VALUE = new int[1]; VALUE[-1] = 3; return 0;', 103),
            ('int VALUE = -1; return new int[VALUE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for pranešimo_tekstas_VALUE, 기대 in 경우들:
            with self.subTest(pranešimo_tekstas_VALUE=pranešimo_tekstas_VALUE):
                self.kompiliuoti_šaltinis('public class 시험 { public static int Paleisti() { ' + pranešimo_tekstas_VALUE + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALUE; public static int Paleisti() { return 0; }',
            'public static int Paleisti() { Object VALUE = new Object(); return 0; }',
            'public static int Paleisti() { System.out.println("hello"); return 0; }',
            'public static int Paleisti() { try { return 1; } catch (Exception KLAIDA) { return 2; } }',
            'public static synchronized int Paleisti() { return 0; }',
            'public static int Paleisti() { return new byte[3].length; }',
            'static native int išorinis_VALUE(); public static int Paleisti() { return išorinis_VALUE(); }',
            'int VALUE; public static int Paleisti() { return 0; }',
        ]
        for pranešimo_tekstas_VALUE in 경우들:
            with self.subTest(pranešimo_tekstas_VALUE=pranešimo_tekstas_VALUE):
                self.kompiliuoti_šaltinis('public class 시험 { ' + pranešimo_tekstas_VALUE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Išvestis = self.Katalogas_VALUE / 'native'
        Išvestis.write_bytes(b'original-output')
        self.kompiliuoti_šaltinis('public class 시험 { public static int Paleisti() { return missing; } }', 성공=False)
        self.assertEqual(Išvestis.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompiliuoti_šaltinis('public class 시험 { public static int Paleisti() { return 37; } }')
        self.assertEqual((self.Katalogas_VALUE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LOOKUP_lentelė = subprocess.check_output(['readelf', '-l', str(self.Katalogas_VALUE / 'native')])
        self.assertNotIn(b'INTERP', LOOKUP_lentelė)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompiliuoti_šaltinis('public class 시험 { public static int Paleisti() { return naudotojas.실행권한(); } }',
                    {'naudotojas': 'public class naudotojas { public static native int 실행권한(); }'}, tikslas='user')
        duomenys = (self.Katalogas_VALUE / 'native').read_bytes()
        self.assertEqual(duomenys[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', duomenys, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Katalogas_VALUE / 'native')]))
        # naudotojas ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompiliuoti_šaltinis('public class 시험 { public static int Paleisti() { return įrenginys_VALUE.포트읽기(1); } }',
                    {'įrenginys_VALUE': 'public class įrenginys_VALUE { public static native int 포트읽기(int VALUE); }'}, 성공=False, tikslas='user')

    def test_내보내기검증(self):
        ŠALTINIS = 'public class 시험 { public static int Paleisti() { return 0; } static int 호출(int VALUE) { return VALUE; } }'
        self.kompiliuoti_šaltinis(ŠALTINIS, tikslas='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Katalogas_VALUE / 'native')]))
        self.kompiliuoti_šaltinis(ŠALTINIS, 성공=False, 내보냄='bad;name=시험.호출')
        self.kompiliuoti_šaltinis(ŠALTINIS, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
