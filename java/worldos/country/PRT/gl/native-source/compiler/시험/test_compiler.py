"""real_datos ELF executar_comando + OpenJDK RESULTANTE 대조. 임시 시험 자료만 생성한다."""
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
        self.directorio_VALOR = Path(self.임시.name)

    def compilar_fonte(self, FONTE, Anexar_introdución=None, 성공=True, obxectivo_VALOR='linux', 내보냄=None):
        camiño_Lista = []
        for Nome, Contido_VALOR in dict({'시험': FONTE}, **(Anexar_introdución or {})).items():
            CAMIÑO = self.directorio_VALOR / (Nome + '.java')
            CAMIÑO.write_text(Contido_VALOR, encoding='utf-8')
            camiño_Lista.append(str(CAMIÑO))
        Orde = [sys.executable, str(컴파일러), '--target', obxectivo_VALOR, '--entry', '시험.Executar_2', '-o', str(self.directorio_VALOR / 'native')]
        if 내보냄 is not None: Orde += ['--export', 내보냄]
        RESULTANTE = subprocess.run(Orde + camiño_Lista,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(RESULTANTE.returncode, 0, RESULTANTE.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(RESULTANTE.returncode, 0)
            self.assertIn('compilar_fonte ERRO'.encode(), RESULTANTE.stderr)
        return RESULTANTE

    def 실행결과(self):
        return subprocess.run([str(self.directorio_VALOR / 'native')], timeout=5).returncode

    def 자바대조(self, FONTE, Anexar_introdución=None):
        self.compilar_fonte(FONTE, Anexar_introdución)
        (self.directorio_VALOR / 'hospedar.java').write_text(
            'public class hospedar { public static void main(String[] Argumentos) { System.exit(시험.Executar_2()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.directorio_VALOR)] +
                       [str(CAMIÑO) for CAMIÑO in self.directorio_VALOR.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.directorio_VALOR), 'hospedar'], timeout=5).returncode
        real_datos = self.실행결과()
        self.assertGreaterEqual(real_datos, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verificar)')
        self.assertEqual(real_datos, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Executar_2() {
                int SUMA_VALOR = 7;
                int VALOR = 12345;
                for (int ÍNDICE = -65; ÍNDICE <= 65; ÍNDICE++) {
                    VALOR = VALOR * 1664525 + 1013904223;
                    SUMA_VALOR = SUMA_VALOR * 31 + 섞기(VALOR, ÍNDICE);
                    SUMA_VALOR += (byte)VALOR + (short)VALOR + (char)VALOR;
                }
                return (SUMA_VALOR & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] VALOR = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Executar_2() {
                int SUMA_VALOR = 13;
                for (int 가 = 0; 가 < VALOR.length; 가++)
                    for (int 나 = 1; 나 < VALOR.length; 나++)
                        SUMA_VALOR = SUMA_VALOR * 31 + VALOR[가] / VALOR[나] + VALOR[가] % VALOR[나];
                return (SUMA_VALOR & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] crear_introdución(int Tamaño) { return new int[Tamaño]; }
            public static int Executar_2() {
                int[] 가 = crear_introdución(8); int[] 나 = 가; int[] baleiro_obxecto = new int[0];
                if (가 != 나 || 가 == null || baleiro_obxecto.length != 0 || 가[7] != 0) return 99;
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
            public static int Executar_2() { return 계산(1, 2, 3, 4, VALOR) + 보조.Lectura(); }
        }''', {'보조': '''public class 보조 {
            static int VALOR = 3;
            static int 초기값() { return ++VALOR; }
            static int Lectura() { return VALOR; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int VALOR = 보조.Lectura() + 1;
            public static int Executar_2() { return VALOR * 10 + 보조.Lectura(); }
        }''', {'보조': '''public class 보조 {
            static int VALOR = 시험.VALOR + 2;
            static int Lectura() { return VALOR; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Texto = "한글\\u0000😀";
            public static int Executar_2() {
                if (Texto != "한글\\u0000😀") return 99;
                return (Texto.length() + Texto.charAt(2) + Texto.charAt(3) + Texto.charAt(4)) % 251;
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
            public static int Executar_2() { return (factorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        declaración = '\n'.join('int VALOR{} = {};'.format(ÍNDICE, ÍNDICE) for ÍNDICE in range(270))
        덧셈 = '+'.join('VALOR{}'.format(ÍNDICE) for ÍNDICE in range(270))
        self.자바대조('public class 시험 { public static int Executar_2() {' + declaración +
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
        for corpo_VALOR, 기대 in 경우들:
            with self.subTest(corpo_VALOR=corpo_VALOR):
                self.compilar_fonte('public class 시험 { public static int Executar_2() { ' + corpo_VALOR + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALOR; public static int Executar_2() { return 0; }',
            'public static int Executar_2() { Object VALOR = new Object(); return 0; }',
            'public static int Executar_2() { System.out.println("hello"); return 0; }',
            'public static int Executar_2() { try { return 1; } catch (Exception ERRO) { return 2; } }',
            'public static synchronized int Executar_2() { return 0; }',
            'public static int Executar_2() { return new byte[3].length; }',
            'static native int externo_VALOR(); public static int Executar_2() { return externo_VALOR(); }',
            'int VALOR; public static int Executar_2() { return 0; }',
        ]
        for corpo_VALOR in 경우들:
            with self.subTest(corpo_VALOR=corpo_VALOR):
                self.compilar_fonte('public class 시험 { ' + corpo_VALOR + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Saída = self.directorio_VALOR / 'native'
        Saída.write_bytes(b'original-output')
        self.compilar_fonte('public class 시험 { public static int Executar_2() { return missing; } }', 성공=False)
        self.assertEqual(Saída.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.compilar_fonte('public class 시험 { public static int Executar_2() { return 37; } }')
        self.assertEqual((self.directorio_VALOR / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Busca_táboa = subprocess.check_output(['readelf', '-l', str(self.directorio_VALOR / 'native')])
        self.assertNotIn(b'INTERP', Busca_táboa)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.compilar_fonte('public class 시험 { public static int Executar_2() { return usuario.실행권한(); } }',
                    {'usuario': 'public class usuario { public static native int 실행권한(); }'}, obxectivo_VALOR='user')
        datos = (self.directorio_VALOR / 'native').read_bytes()
        self.assertEqual(datos[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', datos, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.directorio_VALOR / 'native')]))
        # usuario ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compilar_fonte('public class 시험 { public static int Executar_2() { return dispositivo_VALOR.포트읽기(1); } }',
                    {'dispositivo_VALOR': 'public class dispositivo_VALOR { public static native int 포트읽기(int VALOR); }'}, 성공=False, obxectivo_VALOR='user')

    def test_내보내기검증(self):
        FONTE = 'public class 시험 { public static int Executar_2() { return 0; } static int 호출(int VALOR) { return VALOR; } }'
        self.compilar_fonte(FONTE, obxectivo_VALOR='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.directorio_VALOR / 'native')]))
        self.compilar_fonte(FONTE, 성공=False, 내보냄='bad;name=시험.호출')
        self.compilar_fonte(FONTE, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
