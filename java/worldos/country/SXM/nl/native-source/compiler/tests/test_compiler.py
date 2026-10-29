"""werkelijk_gegevens ELF Uitvoeren_opdracht + OpenJDK resultaat 대조. 임시 tests 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

compiler = Path(__file__).resolve().parents[1] / 'compiler.py'


class test_systeemeigen(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.map_WAARDE = Path(self.임시.name)

    def compileren_bron(self, broncode, toevoegen_invoer=None, 성공=True, doel='linux', 내보냄=None):
        pad_Lijst = []
        for Naam, Inhoud_WAARDE in dict({'tests': broncode}, **(toevoegen_invoer or {})).items():
            pad = self.map_WAARDE / (Naam + '.java')
            pad.write_text(Inhoud_WAARDE, encoding='utf-8')
            pad_Lijst.append(str(pad))
        opdracht = [sys.executable, str(compiler), '--target', doel, '--entry', 'tests.starten', '-o', str(self.map_WAARDE / 'native')]
        if 내보냄 is not None: opdracht += ['--export', 내보냄]
        resultaat = subprocess.run(opdracht + pad_Lijst,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(resultaat.returncode, 0, resultaat.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(resultaat.returncode, 0)
            self.assertIn('compileren_bron fout'.encode(), resultaat.stderr)
        return resultaat

    def uitvoerbewerking_HR(self):
        return subprocess.run([str(self.map_WAARDE / 'native')], timeout=5).returncode

    def 자바대조(self, broncode, toevoegen_invoer=None):
        self.compileren_bron(broncode, toevoegen_invoer)
        (self.map_WAARDE / 'host.java').write_text(
            'public class host { public static void main(String[] argumenten) { System.exit(tests.starten()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.map_WAARDE)] +
                       [str(pad) for pad in self.map_WAARDE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.map_WAARDE), 'host'], timeout=5).returncode
        werkelijk_gegevens = self.uitvoerbewerking_HR()
        self.assertGreaterEqual(werkelijk_gegevens, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 bevestigen)')
        self.assertEqual(werkelijk_gegevens, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class tests {
            static int 섞기(int 가, int SECONDE_operand) {
                return ((가 + SECONDE_operand) ^ (가 - SECONDE_operand) ^ (가 * SECONDE_operand) ^ (가 & SECONDE_operand) ^ (가 | SECONDE_operand))
                    + (가 << SECONDE_operand) + (가 >> SECONDE_operand) + (가 >>> SECONDE_operand);
            }
            public static int starten() {
                int SOM_WAARDE = 7;
                int WAARDE = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    WAARDE = WAARDE * 1664525 + 1013904223;
                    SOM_WAARDE = SOM_WAARDE * 31 + 섞기(WAARDE, INDEX);
                    SOM_WAARDE += (byte)WAARDE + (short)WAARDE + (char)WAARDE;
                }
                return (SOM_WAARDE & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class tests {
            static int[] WAARDE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int starten() {
                int SOM_WAARDE = 13;
                for (int 가 = 0; 가 < WAARDE.length; 가++)
                    for (int SECONDE_operand = 1; SECONDE_operand < WAARDE.length; SECONDE_operand++)
                        SOM_WAARDE = SOM_WAARDE * 31 + WAARDE[가] / WAARDE[SECONDE_operand] + WAARDE[가] % WAARDE[SECONDE_operand];
                return (SOM_WAARDE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class tests {
            static int[] maken_invoer(int Grootte) { return new int[Grootte]; }
            public static int starten() {
                int[] 가 = maken_invoer(8); int[] SECONDE_operand = 가; int[] leeg_object = new int[0];
                if (가 != SECONDE_operand || 가 == null || leeg_object.length != 0 || 가[7] != 0) return 99;
                int WAARDE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return WAARDE + SECONDE_operand[2] + SECONDE_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class tests {
            static int WAARDE = 보조.초기값();
            static int 계산(int 가, int SECONDE_operand, int 다, int 라, int 마) {
                return 가 + SECONDE_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int starten() { return 계산(1, 2, 3, 4, WAARDE) + 보조.Lezen(); }
        }''', {'보조': '''public class 보조 {
            static int WAARDE = 3;
            static int 초기값() { return ++WAARDE; }
            static int Lezen() { return WAARDE; }
        }'''})

    def test_initialisatie_cyclus(self):
        self.자바대조('''public class tests {
            static int WAARDE = 보조.Lezen() + 1;
            public static int starten() { return WAARDE * 10 + 보조.Lezen(); }
        }''', {'보조': '''public class 보조 {
            static int WAARDE = tests.WAARDE + 2;
            static int Lezen() { return WAARDE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class tests {
            static String tekst = "한글\\u0000😀";
            public static int starten() {
                if (tekst != "한글\\u0000😀") return 99;
                return (tekst.length() + tekst.charAt(2) + tekst.charAt(3) + tekst.charAt(4)) % 251;
            }
        }''')

    def test_switch_EN_recursie(self):
        self.자바대조('''public class tests {
            static int faculteit(int WAARDE) { return WAARDE <= 1 ? 1 : WAARDE * faculteit(WAARDE - 1); }
            static int 연속(int WAARDE) {
                switch (WAARDE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int WAARDE) {
                switch (WAARDE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int starten() { return (faculteit(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        aangifte = '\n'.join('int WAARDE{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('WAARDE{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class tests { public static int starten() {' + aangifte +
                    'WAARDE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nul_operand = 0; return 1 / nul_operand;', 101),
            ('int[] WAARDE = null; return WAARDE.length;', 102),
            ('int[] WAARDE = new int[1]; return WAARDE[1];', 103),
            ('int[] WAARDE = new int[1]; WAARDE[-1] = 3; return 0;', 103),
            ('int WAARDE = -1; return new int[WAARDE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for hoofdtekst_WAARDE, 기대 in 경우들:
            with self.subTest(hoofdtekst_WAARDE=hoofdtekst_WAARDE):
                self.compileren_bron('public class tests { public static int starten() { ' + hoofdtekst_WAARDE + ' } }')
                self.assertEqual(self.uitvoerbewerking_HR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long WAARDE; public static int starten() { return 0; }',
            'public static int starten() { Object WAARDE = new Object(); return 0; }',
            'public static int starten() { System.out.println("hello"); return 0; }',
            'public static int starten() { try { return 1; } catch (Exception fout) { return 2; } }',
            'public static synchronized int starten() { return 0; }',
            'public static int starten() { return new byte[3].length; }',
            'static native int extern_WAARDE(); public static int starten() { return extern_WAARDE(); }',
            'int WAARDE; public static int starten() { return 0; }',
        ]
        for hoofdtekst_WAARDE in 경우들:
            with self.subTest(hoofdtekst_WAARDE=hoofdtekst_WAARDE):
                self.compileren_bron('public class tests { ' + hoofdtekst_WAARDE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        tekstuitvoer = self.map_WAARDE / 'native'
        tekstuitvoer.write_bytes(b'original-output')
        self.compileren_bron('public class tests { public static int starten() { return missing; } }', 성공=False)
        self.assertEqual(tekstuitvoer.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.compileren_bron('public class tests { public static int starten() { return 37; } }')
        self.assertEqual((self.map_WAARDE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        opzoektabel = subprocess.check_output(['readelf', '-l', str(self.map_WAARDE / 'native')])
        self.assertNotIn(b'INTERP', opzoektabel)
        self.assertEqual(self.uitvoerbewerking_HR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.compileren_bron('public class tests { public static int starten() { return gebruikersruimte.uitvoerbewerking_machtiging(); } }',
                    {'gebruikersruimte': 'public class gebruikersruimte { public static native int uitvoerbewerking_machtiging(); }'}, doel='user')
        gegevens = (self.map_WAARDE / 'native').read_bytes()
        self.assertEqual(gegevens[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', gegevens, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.map_WAARDE / 'native')]))
        # gebruikersruimte ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compileren_bron('public class tests { public static int starten() { return mobiel_WAARDE.포트읽기(1); } }',
                    {'mobiel_WAARDE': 'public class mobiel_WAARDE { public static native int 포트읽기(int WAARDE); }'}, 성공=False, doel='user')

    def test_exporteren_validatie(self):
        broncode = 'public class tests { public static int starten() { return 0; } static int 호출(int WAARDE) { return WAARDE; } }'
        self.compileren_bron(broncode, doel='kernel', 내보냄='kernel_dispatch=tests.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.map_WAARDE / 'native')]))
        self.compileren_bron(broncode, 성공=False, 내보냄='bad;name=tests.호출')
        self.compileren_bron(broncode, 성공=False, 내보냄='missing=tests.없음')


if __name__ == '__main__':
    unittest.main()
