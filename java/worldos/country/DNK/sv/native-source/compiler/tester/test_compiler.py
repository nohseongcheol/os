"""verklig_data ELF köra_kommando + OpenJDK RESULTAT 대조. 임시 tester 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilerare = Path(__file__).resolve().parents[1] / 'kompilerare.py'


class test_ursprunglig(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Katalog_värde = Path(self.임시.name)

    def kompilera_källa(self, källfil, Lägga_till_post=None, 성공=True, mål='linux', 내보냄=None):
        väg_ange = []
        for Namn, Innehåll_värde in dict({'tester': källfil}, **(Lägga_till_post or {})).items():
            sökväg_2 = self.Katalog_värde / (Namn + '.java')
            sökväg_2.write_text(Innehåll_värde, encoding='utf-8')
            väg_ange.append(str(sökväg_2))
        kommando = [sys.executable, str(kompilerare), '--target', mål, '--entry', 'tester.Kör', '-o', str(self.Katalog_värde / 'native')]
        if 내보냄 is not None: kommando += ['--export', 내보냄]
        RESULTAT = subprocess.run(kommando + väg_ange,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(RESULTAT.returncode, 0, RESULTAT.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(RESULTAT.returncode, 0)
            self.assertIn('kompilera_källa fel'.encode(), RESULTAT.stderr)
        return RESULTAT

    def körning_KR(self):
        return subprocess.run([str(self.Katalog_värde / 'native')], timeout=5).returncode

    def 자바대조(self, källfil, Lägga_till_post=None):
        self.kompilera_källa(källfil, Lägga_till_post)
        (self.Katalog_värde / 'värd.java').write_text(
            'public class värd { public static void main(String[] argument) { System.exit(tester.Kör()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Katalog_värde)] +
                       [str(sökväg_2) for sökväg_2 in self.Katalog_värde.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Katalog_värde), 'värd'], timeout=5).returncode
        verklig_data = self.körning_KR()
        self.assertGreaterEqual(verklig_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verifiera)')
        self.assertEqual(verklig_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class tester {
            static int 섞기(int 가, int SEKUND_operand) {
                return ((가 + SEKUND_operand) ^ (가 - SEKUND_operand) ^ (가 * SEKUND_operand) ^ (가 & SEKUND_operand) ^ (가 | SEKUND_operand))
                    + (가 << SEKUND_operand) + (가 >> SEKUND_operand) + (가 >>> SEKUND_operand);
            }
            public static int Kör() {
                int SUM_värde = 7;
                int värde = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    värde = värde * 1664525 + 1013904223;
                    SUM_värde = SUM_värde * 31 + 섞기(värde, INDEX);
                    SUM_värde += (byte)värde + (short)värde + (char)värde;
                }
                return (SUM_värde & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class tester {
            static int[] värde = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Kör() {
                int SUM_värde = 13;
                for (int 가 = 0; 가 < värde.length; 가++)
                    for (int SEKUND_operand = 1; SEKUND_operand < värde.length; SEKUND_operand++)
                        SUM_värde = SUM_värde * 31 + värde[가] / värde[SEKUND_operand] + värde[가] % värde[SEKUND_operand];
                return (SUM_värde & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class tester {
            static int[] Skapa_post(int Storlek) { return new int[Storlek]; }
            public static int Kör() {
                int[] 가 = Skapa_post(8); int[] SEKUND_operand = 가; int[] 빈것 = new int[0];
                if (가 != SEKUND_operand || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int värde = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return värde + SEKUND_operand[2] + SEKUND_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class tester {
            static int värde = 보조.초기값();
            static int 계산(int 가, int SEKUND_operand, int 다, int 라, int 마) {
                return 가 + SEKUND_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Kör() { return 계산(1, 2, 3, 4, värde) + 보조.Läs(); }
        }''', {'보조': '''public class 보조 {
            static int värde = 3;
            static int 초기값() { return ++värde; }
            static int Läs() { return värde; }
        }'''})

    def test_initiering_cykel(self):
        self.자바대조('''public class tester {
            static int värde = 보조.Läs() + 1;
            public static int Kör() { return värde * 10 + 보조.Läs(); }
        }''', {'보조': '''public class 보조 {
            static int värde = tester.värde + 2;
            static int Läs() { return värde; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class tester {
            static String text = "한글\\u0000😀";
            public static int Kör() {
                if (text != "한글\\u0000😀") return 99;
                return (text.length() + text.charAt(2) + text.charAt(3) + text.charAt(4)) % 251;
            }
        }''')

    def test_byta_AND_rekursion(self):
        self.자바대조('''public class tester {
            static int fakultet(int värde) { return värde <= 1 ? 1 : värde * fakultet(värde - 1); }
            static int 연속(int värde) {
                switch (värde) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int värde) {
                switch (värde) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Kör() { return (fakultet(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklaration = '\n'.join('int värde{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('värde{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class tester { public static int Kör() {' + deklaration +
                    'värde_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int noll_operand = 0; return 1 / noll_operand;', 101),
            ('int[] värde = null; return värde.length;', 102),
            ('int[] värde = new int[1]; return värde[1];', 103),
            ('int[] värde = new int[1]; värde[-1] = 3; return 0;', 103),
            ('int värde = -1; return new int[värde].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for brödtext_värde, 기대 in 경우들:
            with self.subTest(brödtext_värde=brödtext_värde):
                self.kompilera_källa('public class tester { public static int Kör() { ' + brödtext_värde + ' } }')
                self.assertEqual(self.körning_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long värde; public static int Kör() { return 0; }',
            'public static int Kör() { Object värde = new Object(); return 0; }',
            'public static int Kör() { System.out.println("hello"); return 0; }',
            'public static int Kör() { try { return 1; } catch (Exception fel) { return 2; } }',
            'public static synchronized int Kör() { return 0; }',
            'public static int Kör() { return new byte[3].length; }',
            'static native int extern_värde(); public static int Kör() { return extern_värde(); }',
            'int värde; public static int Kör() { return 0; }',
        ]
        for brödtext_värde in 경우들:
            with self.subTest(brödtext_värde=brödtext_värde):
                self.kompilera_källa('public class tester { ' + brödtext_värde + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        utmatningsposition = self.Katalog_värde / 'native'
        utmatningsposition.write_bytes(b'original-output')
        self.kompilera_källa('public class tester { public static int Kör() { return missing; } }', 성공=False)
        self.assertEqual(utmatningsposition.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompilera_källa('public class tester { public static int Kör() { return 37; } }')
        self.assertEqual((self.Katalog_värde / 'native').read_bytes()[:5], b'\x7fELF\x01')
        LETAUPP_tabell = subprocess.check_output(['readelf', '-l', str(self.Katalog_värde / 'native')])
        self.assertNotIn(b'INTERP', LETAUPP_tabell)
        self.assertEqual(self.körning_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompilera_källa('public class tester { public static int Kör() { return användarutrymme.körning_behörighet(); } }',
                    {'användarutrymme': 'public class användarutrymme { public static native int körning_behörighet(); }'}, mål='user')
        data = (self.Katalog_värde / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Katalog_värde / 'native')]))
        # användarutrymme ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompilera_källa('public class tester { public static int Kör() { return enhet_värde.läsa_maskinvara_port(1); } }',
                    {'enhet_värde': 'public class enhet_värde { public static native int läsa_maskinvara_port(int värde); }'}, 성공=False, mål='user')

    def test_exportera_validering(self):
        källfil = 'public class tester { public static int Kör() { return 0; } static int 호출(int värde) { return värde; } }'
        self.kompilera_källa(källfil, mål='kernel', 내보냄='kernel_dispatch=tester.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Katalog_värde / 'native')]))
        self.kompilera_källa(källfil, 성공=False, 내보냄='bad;name=tester.호출')
        self.kompilera_källa(källfil, 성공=False, 내보냄='missing=tester.없음')


if __name__ == '__main__':
    unittest.main()
