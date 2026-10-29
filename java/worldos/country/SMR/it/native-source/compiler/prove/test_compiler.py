"""effettivo_dati ELF Esegui_comando + OpenJDK risultato 대조. 임시 prove 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

compilatore = Path(__file__).resolve().parents[1] / 'compilatore.py'


class test_nativo(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.elenco_VALORE = Path(self.임시.name)

    def compilare_fonte(self, codiceSorgente, Aggiunta_voce=None, 성공=True, target='linux', 내보냄=None):
        percorso_elenco = []
        for Nome, Contenuto_VALORE in dict({'prove': codiceSorgente}, **(Aggiunta_voce or {})).items():
            percorso = self.elenco_VALORE / (Nome + '.java')
            percorso.write_text(Contenuto_VALORE, encoding='utf-8')
            percorso_elenco.append(str(percorso))
        comando = [sys.executable, str(compilatore), '--target', target, '--entry', 'prove.avvia', '-o', str(self.elenco_VALORE / 'native')]
        if 내보냄 is not None: comando += ['--export', 내보냄]
        risultato = subprocess.run(comando + percorso_elenco,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(risultato.returncode, 0, risultato.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(risultato.returncode, 0)
            self.assertIn('compilare_fonte errore'.encode(), risultato.stderr)
        return risultato

    def esecuzione_KR(self):
        return subprocess.run([str(self.elenco_VALORE / 'native')], timeout=5).returncode

    def 자바대조(self, codiceSorgente, Aggiunta_voce=None):
        self.compilare_fonte(codiceSorgente, Aggiunta_voce)
        (self.elenco_VALORE / 'host.java').write_text(
            'public class host { public static void main(String[] argomenti) { System.exit(prove.avvia()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.elenco_VALORE)] +
                       [str(percorso) for percorso in self.elenco_VALORE.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.elenco_VALORE), 'host'], timeout=5).returncode
        effettivo_dati = self.esecuzione_KR()
        self.assertGreaterEqual(effettivo_dati, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verificare)')
        self.assertEqual(effettivo_dati, 기대)

    def test_intero_aritmetico_E_Turni(self):
        self.자바대조('''public class prove {
            static int mix_aritmetico(int 가, int SECONDO_operando) {
                return ((가 + SECONDO_operando) ^ (가 - SECONDO_operando) ^ (가 * SECONDO_operando) ^ (가 & SECONDO_operando) ^ (가 | SECONDO_operando))
                    + (가 << SECONDO_operando) + (가 >> SECONDO_operando) + (가 >>> SECONDO_operando);
            }
            public static int avvia() {
                int SUM_VALORE = 7;
                int VALORE = 12345;
                for (int INDICE = -65; INDICE <= 65; INDICE++) {
                    VALORE = VALORE * 1664525 + 1013904223;
                    SUM_VALORE = SUM_VALORE * 31 + mix_aritmetico(VALORE, INDICE);
                    SUM_VALORE += (byte)VALORE + (short)VALORE + (char)VALORE;
                }
                return (SUM_VALORE & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class prove {
            static int[] VALORE = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int avvia() {
                int SUM_VALORE = 13;
                for (int 가 = 0; 가 < VALORE.length; 가++)
                    for (int SECONDO_operando = 1; SECONDO_operando < VALORE.length; SECONDO_operando++)
                        SUM_VALORE = SUM_VALORE * 31 + VALORE[가] / VALORE[SECONDO_operando] + VALORE[가] % VALORE[SECONDO_operando];
                return (SUM_VALORE & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class prove {
            static int[] Crea_voce(int Dimensione) { return new int[Dimensione]; }
            public static int avvia() {
                int[] 가 = Crea_voce(8); int[] SECONDO_operando = 가; int[] vuota_oggetto = new int[0];
                if (가 != SECONDO_operando || 가 == null || vuota_oggetto.length != 0 || 가[7] != 0) return 99;
                int VALORE = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALORE + SECONDO_operando[2] + SECONDO_operando[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class prove {
            static int VALORE = 보조.초기값();
            static int 계산(int 가, int SECONDO_operando, int 다, int 라, int 마) {
                return 가 + SECONDO_operando * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int avvia() { return 계산(1, 2, 3, 4, VALORE) + 보조.Lettura(); }
        }''', {'보조': '''public class 보조 {
            static int VALORE = 3;
            static int 초기값() { return ++VALORE; }
            static int Lettura() { return VALORE; }
        }'''})

    def test_inizializzazione_Cicli(self):
        self.자바대조('''public class prove {
            static int VALORE = 보조.Lettura() + 1;
            public static int avvia() { return VALORE * 10 + 보조.Lettura(); }
        }''', {'보조': '''public class 보조 {
            static int VALORE = prove.VALORE + 2;
            static int Lettura() { return VALORE; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class prove {
            static String testo = "한글\\u0000😀";
            public static int avvia() {
                if (testo != "한글\\u0000😀") return 99;
                return (testo.length() + testo.charAt(2) + testo.charAt(3) + testo.charAt(4)) % 251;
            }
        }''')

    def test_SWITCH_E_ricorsione(self):
        self.자바대조('''public class prove {
            static int fattoriale(int VALORE) { return VALORE <= 1 ? 1 : VALORE * fattoriale(VALORE - 1); }
            static int 연속(int VALORE) {
                switch (VALORE) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALORE) {
                switch (VALORE) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int avvia() { return (fattoriale(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        dichiarazione = '\n'.join('int VALORE{} = {};'.format(INDICE, INDICE) for INDICE in range(270))
        덧셈 = '+'.join('VALORE{}'.format(INDICE) for INDICE in range(270))
        self.자바대조('public class prove { public static int avvia() {' + dichiarazione +
                    'VALORE_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int zero_operando = 0; return 1 / zero_operando;', 101),
            ('int[] VALORE = null; return VALORE.length;', 102),
            ('int[] VALORE = new int[1]; return VALORE[1];', 103),
            ('int[] VALORE = new int[1]; VALORE[-1] = 3; return 0;', 103),
            ('int VALORE = -1; return new int[VALORE].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for corpo_VALORE, 기대 in 경우들:
            with self.subTest(corpo_VALORE=corpo_VALORE):
                self.compilare_fonte('public class prove { public static int avvia() { ' + corpo_VALORE + ' } }')
                self.assertEqual(self.esecuzione_KR(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALORE; public static int avvia() { return 0; }',
            'public static int avvia() { Object VALORE = new Object(); return 0; }',
            'public static int avvia() { System.out.println("hello"); return 0; }',
            'public static int avvia() { try { return 1; } catch (Exception errore) { return 2; } }',
            'public static synchronized int avvia() { return 0; }',
            'public static int avvia() { return new byte[3].length; }',
            'static native int esterno_VALORE(); public static int avvia() { return esterno_VALORE(); }',
            'int VALORE; public static int avvia() { return 0; }',
        ]
        for corpo_VALORE in 경우들:
            with self.subTest(corpo_VALORE=corpo_VALORE):
                self.compilare_fonte('public class prove { ' + corpo_VALORE + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        uscitaTesto = self.elenco_VALORE / 'native'
        uscitaTesto.write_bytes(b'original-output')
        self.compilare_fonte('public class prove { public static int avvia() { return missing; } }', 성공=False)
        self.assertEqual(uscitaTesto.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.compilare_fonte('public class prove { public static int avvia() { return 37; } }')
        self.assertEqual((self.elenco_VALORE / 'native').read_bytes()[:5], b'\x7fELF\x01')
        tabella_di_ricerca = subprocess.check_output(['readelf', '-l', str(self.elenco_VALORE / 'native')])
        self.assertNotIn(b'INTERP', tabella_di_ricerca)
        self.assertEqual(self.esecuzione_KR(), 37)

    def test_사용자ELF와ABI분리(self):
        self.compilare_fonte('public class prove { public static int avvia() { return spazio_utente.esecuzione_privilegio(); } }',
                    {'spazio_utente': 'public class spazio_utente { public static native int esecuzione_privilegio(); }'}, target='user')
        dati = (self.elenco_VALORE / 'native').read_bytes()
        self.assertEqual(dati[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', dati, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.elenco_VALORE / 'native')]))
        # spazio_utente ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compilare_fonte('public class prove { public static int avvia() { return cellulare_VALORE.포트읽기(1); } }',
                    {'cellulare_VALORE': 'public class cellulare_VALORE { public static native int 포트읽기(int VALORE); }'}, 성공=False, target='user')

    def test_esportare_convalida(self):
        codiceSorgente = 'public class prove { public static int avvia() { return 0; } static int 호출(int VALORE) { return VALORE; } }'
        self.compilare_fonte(codiceSorgente, target='kernel', 내보냄='kernel_dispatch=prove.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.elenco_VALORE / 'native')]))
        self.compilare_fonte(codiceSorgente, 성공=False, 내보냄='bad;name=prove.호출')
        self.compilare_fonte(codiceSorgente, 성공=False, 내보냄='missing=prove.없음')


if __name__ == '__main__':
    unittest.main()
