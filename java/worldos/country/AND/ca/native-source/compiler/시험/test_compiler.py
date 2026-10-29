"""real_dades ELF Executa_ordre + OpenJDK RESULTAT 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.directori_VALOR = Path(self.임시.name)

    def generar_font(self, FONT, Annexa_introducció=None, 성공=True, objectiu='linux', 내보냄=None):
        camí_Llista = []
        for Nom, contingut_VALOR in dict({'시험': FONT}, **(Annexa_introducció or {})).items():
            Camí = self.directori_VALOR / (Nom + '.java')
            Camí.write_text(contingut_VALOR, encoding='utf-8')
            camí_Llista.append(str(Camí))
        Ordre = [sys.executable, str(컴파일러), '--target', objectiu, '--entry', '시험.Executa_2', '-o', str(self.directori_VALOR / 'native')]
        if 내보냄 is not None: Ordre += ['--export', 내보냄]
        RESULTAT = subprocess.run(Ordre + camí_Llista,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(RESULTAT.returncode, 0, RESULTAT.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(RESULTAT.returncode, 0)
            self.assertIn('generar_font s_ha_produït_un_error'.encode(), RESULTAT.stderr)
        return RESULTAT

    def 실행결과(self):
        return subprocess.run([str(self.directori_VALOR / 'native')], timeout=5).returncode

    def 자바대조(self, FONT, Annexa_introducció=None):
        self.generar_font(FONT, Annexa_introducció)
        (self.directori_VALOR / 'allotjar.java').write_text(
            'public class allotjar { public static void main(String[] 인수) { System.exit(시험.Executa_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.directori_VALOR)] +
                       [str(Camí) for Camí in self.directori_VALOR.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.directori_VALOR), 'allotjar'], timeout=5).returncode
        real_dades = self.실행결과()
        self.assertGreaterEqual(real_dades, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verificar)')
        self.assertEqual(real_dades, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Executa_2() {
                int SUMA_VALOR = 7;
                int VALOR = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    VALOR = VALOR * 1664525 + 1013904223;
                    SUMA_VALOR = SUMA_VALOR * 31 + 섞기(VALOR, INDEX);
                    SUMA_VALOR += (byte)VALOR + (short)VALOR + (char)VALOR;
                }
                return (SUMA_VALOR & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] VALOR = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Executa_2() {
                int SUMA_VALOR = 13;
                for (int 가 = 0; 가 < VALOR.length; 가++)
                    for (int 나 = 1; 나 < VALOR.length; 나++)
                        SUMA_VALOR = SUMA_VALOR * 31 + VALOR[가] / VALOR[나] + VALOR[가] % VALOR[나];
                return (SUMA_VALOR & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Crear_introducció(int Mida) { return new int[Mida]; }
            public static int Executa_2() {
                int[] 가 = Crear_introducció(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int VALOR = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALOR + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int VALOR = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Executa_2() { return 계산(1, 2, 3, 4, VALOR) + 보조.Lectura(); }
        }''', {'보조': '''public class 보조 {
            static int VALOR = 3;
            static int 초기값() { return ++VALOR; }
            static int Lectura() { return VALOR; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALOR = 보조.Lectura() + 1;
            public static int Executa_2() { return VALOR * 10 + 보조.Lectura(); }
        }''', {'보조': '''public class 보조 {
            static int VALOR = 시험.VALOR + 2;
            static int Lectura() { return VALOR; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int Executa_2() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int factorial(int VALOR) { return VALOR <= 1 ? 1 : VALOR * factorial(VALOR - 1); }
            static int 연속(int VALOR) {
                switch (VALOR) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALOR) {
                switch (VALOR) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Executa_2() { return (factorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        declaració = '\n'.join('int VALOR{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('VALOR{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int Executa_2() {' + declaració +
                    'VALOR_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] VALOR = null; return VALOR.length;', 102),
            ('int[] VALOR = new int[1]; return VALOR[1];', 103),
            ('int[] VALOR = new int[1]; VALOR[-1] = 3; return 0;', 103),
            ('int VALOR = -1; return new int[VALOR].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for text_VALOR, 기대 in 경우들:
            with self.subTest(text_VALOR=text_VALOR):
                self.generar_font('public class 시험 { public static int Executa_2() { ' + text_VALOR + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALOR; public static int Executa_2() { return 0; }',
            'public static int Executa_2() { Object VALOR = new Object(); return 0; }',
            'public static int Executa_2() { System.out.println("hello"); return 0; }',
            'public static int Executa_2() { try { return 1; } catch (Exception s_ha_produït_un_error) { return 2; } }',
            'public static synchronized int Executa_2() { return 0; }',
            'public static int Executa_2() { return new byte[3].length; }',
            'static native int extern_VALOR(); public static int Executa_2() { return extern_VALOR(); }',
            'int VALOR; public static int Executa_2() { return 0; }',
        ]
        for text_VALOR in 경우들:
            with self.subTest(text_VALOR=text_VALOR):
                self.generar_font('public class 시험 { ' + text_VALOR + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Sortida = self.directori_VALOR / 'native'
        Sortida.write_bytes(b'original-output')
        self.generar_font('public class 시험 { public static int Executa_2() { return missing; } }', 성공=False)
        self.assertEqual(Sortida.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.generar_font('public class 시험 { public static int Executa_2() { return 37; } }')
        self.assertEqual((self.directori_VALOR / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Cerca_taula = subprocess.check_output(['readelf', '-l', str(self.directori_VALOR / 'native')])
        self.assertNotIn(b'INTERP', Cerca_taula)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.generar_font('public class 시험 { public static int Executa_2() { return usuari.실행권한(); } }',
                    {'usuari': 'public class usuari { public static native int 실행권한(); }'}, objectiu='user')
        dades = (self.directori_VALOR / 'native').read_bytes()
        self.assertEqual(dades[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', dades, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.directori_VALOR / 'native')]))
        # usuari ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.generar_font('public class 시험 { public static int Executa_2() { return dispositiu_VALOR.포트읽기(1); } }',
                    {'dispositiu_VALOR': 'public class dispositiu_VALOR { public static native int 포트읽기(int VALOR); }'}, 성공=False, objectiu='user')

    def test_내보내기검증(self):
        FONT = 'public class 시험 { public static int Executa_2() { return 0; } static int 호출(int VALOR) { return VALOR; } }'
        self.generar_font(FONT, objectiu='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.directori_VALOR / 'native')]))
        self.generar_font(FONT, 성공=False, 내보냄='bad;name=시험.호출')
        self.generar_font(FONT, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
