"""skutečný_data ELF Provést_příkaz + OpenJDK VÝSLEDEK 대조. 임시 zkoušky 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

kompilátor = Path(__file__).resolve().parents[1] / 'kompilátor.py'


class test_nativní(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Adresář_HODNOTA = Path(self.임시.name)

    def kompilovat_zdroj(self, zdrojový_soubor, Připojit_položka=None, 성공=True, cílová_úroveň='linux', 내보냄=None):
        cesta_Seznam = []
        for Název, Obsah_HODNOTA in dict({'zkoušky': zdrojový_soubor}, **(Připojit_položka or {})).items():
            cesta_2 = self.Adresář_HODNOTA / (Název + '.java')
            cesta_2.write_text(Obsah_HODNOTA, encoding='utf-8')
            cesta_Seznam.append(str(cesta_2))
        příkaz = [sys.executable, str(kompilátor), '--target', cílová_úroveň, '--entry', 'zkoušky.Spustit_2', '-o', str(self.Adresář_HODNOTA / 'native')]
        if 내보냄 is not None: příkaz += ['--export', 내보냄]
        VÝSLEDEK = subprocess.run(příkaz + cesta_Seznam,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(VÝSLEDEK.returncode, 0, VÝSLEDEK.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(VÝSLEDEK.returncode, 0)
            self.assertIn('kompilovat_zdroj chyba'.encode(), VÝSLEDEK.stderr)
        return VÝSLEDEK

    def spuštění_KV(self):
        return subprocess.run([str(self.Adresář_HODNOTA / 'native')], timeout=5).returncode

    def 자바대조(self, zdrojový_soubor, Připojit_položka=None):
        self.kompilovat_zdroj(zdrojový_soubor, Připojit_položka)
        (self.Adresář_HODNOTA / 'hostit.java').write_text(
            'public class hostit { public static void main(String[] argumenty) { System.exit(zkoušky.Spustit_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Adresář_HODNOTA)] +
                       [str(cesta_2) for cesta_2 in self.Adresář_HODNOTA.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Adresář_HODNOTA), 'hostit'], timeout=5).returncode
        skutečný_data = self.spuštění_KV()
        self.assertGreaterEqual(skutečný_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ověřit)')
        self.assertEqual(skutečný_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class zkoušky {
            static int 섞기(int 가, int SEKUNDA_operand) {
                return ((가 + SEKUNDA_operand) ^ (가 - SEKUNDA_operand) ^ (가 * SEKUNDA_operand) ^ (가 & SEKUNDA_operand) ^ (가 | SEKUNDA_operand))
                    + (가 << SEKUNDA_operand) + (가 >> SEKUNDA_operand) + (가 >>> SEKUNDA_operand);
            }
            public static int Spustit_2() {
                int SUMA_HODNOTA = 7;
                int HODNOTA = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    HODNOTA = HODNOTA * 1664525 + 1013904223;
                    SUMA_HODNOTA = SUMA_HODNOTA * 31 + 섞기(HODNOTA, INDEX);
                    SUMA_HODNOTA += (byte)HODNOTA + (short)HODNOTA + (char)HODNOTA;
                }
                return (SUMA_HODNOTA & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class zkoušky {
            static int[] HODNOTA = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Spustit_2() {
                int SUMA_HODNOTA = 13;
                for (int 가 = 0; 가 < HODNOTA.length; 가++)
                    for (int SEKUNDA_operand = 1; SEKUNDA_operand < HODNOTA.length; SEKUNDA_operand++)
                        SUMA_HODNOTA = SUMA_HODNOTA * 31 + HODNOTA[가] / HODNOTA[SEKUNDA_operand] + HODNOTA[가] % HODNOTA[SEKUNDA_operand];
                return (SUMA_HODNOTA & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class zkoušky {
            static int[] Create_položka(int Velikost) { return new int[Velikost]; }
            public static int Spustit_2() {
                int[] 가 = Create_položka(8); int[] SEKUNDA_operand = 가; int[] 빈것 = new int[0];
                if (가 != SEKUNDA_operand || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int HODNOTA = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return HODNOTA + SEKUNDA_operand[2] + SEKUNDA_operand[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class zkoušky {
            static int HODNOTA = 보조.초기값();
            static int 계산(int 가, int SEKUNDA_operand, int 다, int 라, int 마) {
                return 가 + SEKUNDA_operand * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Spustit_2() { return 계산(1, 2, 3, 4, HODNOTA) + 보조.Čtení(); }
        }''', {'보조': '''public class 보조 {
            static int HODNOTA = 3;
            static int 초기값() { return ++HODNOTA; }
            static int Čtení() { return HODNOTA; }
        }'''})

    def test_inicializace_Cyklus(self):
        self.자바대조('''public class zkoušky {
            static int HODNOTA = 보조.Čtení() + 1;
            public static int Spustit_2() { return HODNOTA * 10 + 보조.Čtení(); }
        }''', {'보조': '''public class 보조 {
            static int HODNOTA = zkoušky.HODNOTA + 2;
            static int Čtení() { return HODNOTA; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class zkoušky {
            static String text = "한글\\u0000😀";
            public static int Spustit_2() {
                if (text != "한글\\u0000😀") return 99;
                return (text.length() + text.charAt(2) + text.charAt(3) + text.charAt(4)) % 251;
            }
        }''')

    def test_SWITCH_A_rekurze(self):
        self.자바대조('''public class zkoušky {
            static int faktoriál(int HODNOTA) { return HODNOTA <= 1 ? 1 : HODNOTA * faktoriál(HODNOTA - 1); }
            static int 연속(int HODNOTA) {
                switch (HODNOTA) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int HODNOTA) {
                switch (HODNOTA) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Spustit_2() { return (faktoriál(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        deklarace_4f4f026b = '\n'.join('int HODNOTA{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('HODNOTA{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class zkoušky { public static int Spustit_2() {' + deklarace_4f4f026b +
                    'HODNOTA_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int nula_operand = 0; return 1 / nula_operand;', 101),
            ('int[] HODNOTA = null; return HODNOTA.length;', 102),
            ('int[] HODNOTA = new int[1]; return HODNOTA[1];', 103),
            ('int[] HODNOTA = new int[1]; HODNOTA[-1] = 3; return 0;', 103),
            ('int HODNOTA = -1; return new int[HODNOTA].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for text_zprávy_HODNOTA, 기대 in 경우들:
            with self.subTest(text_zprávy_HODNOTA=text_zprávy_HODNOTA):
                self.kompilovat_zdroj('public class zkoušky { public static int Spustit_2() { ' + text_zprávy_HODNOTA + ' } }')
                self.assertEqual(self.spuštění_KV(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long HODNOTA; public static int Spustit_2() { return 0; }',
            'public static int Spustit_2() { Object HODNOTA = new Object(); return 0; }',
            'public static int Spustit_2() { System.out.println("hello"); return 0; }',
            'public static int Spustit_2() { try { return 1; } catch (Exception chyba) { return 2; } }',
            'public static synchronized int Spustit_2() { return 0; }',
            'public static int Spustit_2() { return new byte[3].length; }',
            'static native int externí_HODNOTA(); public static int Spustit_2() { return externí_HODNOTA(); }',
            'int HODNOTA; public static int Spustit_2() { return 0; }',
        ]
        for text_zprávy_HODNOTA in 경우들:
            with self.subTest(text_zprávy_HODNOTA=text_zprávy_HODNOTA):
                self.kompilovat_zdroj('public class zkoušky { ' + text_zprávy_HODNOTA + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        výstupní_pozice = self.Adresář_HODNOTA / 'native'
        výstupní_pozice.write_bytes(b'original-output')
        self.kompilovat_zdroj('public class zkoušky { public static int Spustit_2() { return missing; } }', 성공=False)
        self.assertEqual(výstupní_pozice.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.kompilovat_zdroj('public class zkoušky { public static int Spustit_2() { return 37; } }')
        self.assertEqual((self.Adresář_HODNOTA / 'native').read_bytes()[:5], b'\x7fELF\x01')
        VYHLEDAT_tabulka = subprocess.check_output(['readelf', '-l', str(self.Adresář_HODNOTA / 'native')])
        self.assertNotIn(b'INTERP', VYHLEDAT_tabulka)
        self.assertEqual(self.spuštění_KV(), 37)

    def test_사용자ELF와ABI분리(self):
        self.kompilovat_zdroj('public class zkoušky { public static int Spustit_2() { return uživatelský_prostor.spuštění_oprávnění(); } }',
                    {'uživatelský_prostor': 'public class uživatelský_prostor { public static native int spuštění_oprávnění(); }'}, cílová_úroveň='user')
        data = (self.Adresář_HODNOTA / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Adresář_HODNOTA / 'native')]))
        # uživatelský_prostor ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.kompilovat_zdroj('public class zkoušky { public static int Spustit_2() { return mobilní_HODNOTA.포트읽기(1); } }',
                    {'mobilní_HODNOTA': 'public class mobilní_HODNOTA { public static native int 포트읽기(int HODNOTA); }'}, 성공=False, cílová_úroveň='user')

    def test_exportovat_ověření(self):
        zdrojový_soubor = 'public class zkoušky { public static int Spustit_2() { return 0; } static int 호출(int HODNOTA) { return HODNOTA; } }'
        self.kompilovat_zdroj(zdrojový_soubor, cílová_úroveň='kernel', 내보냄='kernel_dispatch=zkoušky.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Adresář_HODNOTA / 'native')]))
        self.kompilovat_zdroj(zdrojový_soubor, 성공=False, 내보냄='bad;name=zkoušky.호출')
        self.kompilovat_zdroj(zdrojový_soubor, 성공=False, 내보냄='missing=zkoušky.없음')


if __name__ == '__main__':
    unittest.main()
