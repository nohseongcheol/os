"""real_dados ELF Executar_comando + OpenJDK resultado 대조. 임시 testes 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

compilador = Path(__file__).resolve().parents[1] / 'compilador.py'


class teste_nativo(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.Diretório_VALOR = Path(self.임시.name)

    def compilar_fonte(self, códigoFonte, Acrescentar_entrada=None, 성공=True, meta='linux', 내보냄=None):
        caminho_Lista = []
        for Nome, Conteúdo_VALOR in dict({'testes': códigoFonte}, **(Acrescentar_entrada or {})).items():
            caminho = self.Diretório_VALOR / (Nome + '.java')
            caminho.write_text(Conteúdo_VALOR, encoding='utf-8')
            caminho_Lista.append(str(caminho))
        comando = [sys.executable, str(compilador), '--target', meta, '--entry', 'testes.iniciar', '-o', str(self.Diretório_VALOR / 'native')]
        if 내보냄 is not None: comando += ['--export', 내보냄]
        resultado = subprocess.run(comando + caminho_Lista,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(resultado.returncode, 0, resultado.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(resultado.returncode, 0)
            self.assertIn('compilar_fonte erro'.encode(), resultado.stderr)
        return resultado

    def execução_RC(self):
        return subprocess.run([str(self.Diretório_VALOR / 'native')], timeout=5).returncode

    def 자바대조(self, códigoFonte, Acrescentar_entrada=None):
        self.compilar_fonte(códigoFonte, Acrescentar_entrada)
        (self.Diretório_VALOR / 'host.java').write_text(
            'public class host { public static void main(String[] argumentos) { System.exit(testes.iniciar()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Diretório_VALOR)] +
                       [str(caminho) for caminho in self.Diretório_VALOR.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Diretório_VALOR), 'host'], timeout=5).returncode
        real_dados = self.execução_RC()
        self.assertGreaterEqual(real_dados, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 verificar)')
        self.assertEqual(real_dados, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class testes {
            static int 섞기(int 가, int SEGUNDO_operando) {
                return ((가 + SEGUNDO_operando) ^ (가 - SEGUNDO_operando) ^ (가 * SEGUNDO_operando) ^ (가 & SEGUNDO_operando) ^ (가 | SEGUNDO_operando))
                    + (가 << SEGUNDO_operando) + (가 >> SEGUNDO_operando) + (가 >>> SEGUNDO_operando);
            }
            public static int iniciar() {
                int SUM_VALOR = 7;
                int VALOR = 12345;
                for (int ÍNDICE = -65; ÍNDICE <= 65; ÍNDICE++) {
                    VALOR = VALOR * 1664525 + 1013904223;
                    SUM_VALOR = SUM_VALOR * 31 + 섞기(VALOR, ÍNDICE);
                    SUM_VALOR += (byte)VALOR + (short)VALOR + (char)VALOR;
                }
                return (SUM_VALOR & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class testes {
            static int[] VALOR = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int iniciar() {
                int SUM_VALOR = 13;
                for (int 가 = 0; 가 < VALOR.length; 가++)
                    for (int SEGUNDO_operando = 1; SEGUNDO_operando < VALOR.length; SEGUNDO_operando++)
                        SUM_VALOR = SUM_VALOR * 31 + VALOR[가] / VALOR[SEGUNDO_operando] + VALOR[가] % VALOR[SEGUNDO_operando];
                return (SUM_VALOR & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class testes {
            static int[] Criar_entrada(int Tamanho) { return new int[Tamanho]; }
            public static int iniciar() {
                int[] 가 = Criar_entrada(8); int[] SEGUNDO_operando = 가; int[] vazio_objeto = new int[0];
                if (가 != SEGUNDO_operando || 가 == null || vazio_objeto.length != 0 || 가[7] != 0) return 99;
                int VALOR = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return VALOR + SEGUNDO_operando[2] + SEGUNDO_operando[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class testes {
            static int VALOR = 보조.초기값();
            static int 계산(int 가, int SEGUNDO_operando, int 다, int 라, int 마) {
                return 가 + SEGUNDO_operando * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int iniciar() { return 계산(1, 2, 3, 4, VALOR) + 보조.Leitura(); }
        }''', {'보조': '''public class 보조 {
            static int VALOR = 3;
            static int 초기값() { return ++VALOR; }
            static int Leitura() { return VALOR; }
        }'''})

    def teste_inicialização_Ciclo(self):
        self.자바대조('''public class testes {
            static int VALOR = 보조.Leitura() + 1;
            public static int iniciar() { return VALOR * 10 + 보조.Leitura(); }
        }''', {'보조': '''public class 보조 {
            static int VALOR = testes.VALOR + 2;
            static int Leitura() { return VALOR; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class testes {
            static String texto = "한글\\u0000😀";
            public static int iniciar() {
                if (texto != "한글\\u0000😀") return 99;
                return (texto.length() + texto.charAt(2) + texto.charAt(3) + texto.charAt(4)) % 251;
            }
        }''')

    def teste_mudar_E_recursão(self):
        self.자바대조('''public class testes {
            static int fatorial(int VALOR) { return VALOR <= 1 ? 1 : VALOR * fatorial(VALOR - 1); }
            static int 연속(int VALOR) {
                switch (VALOR) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int VALOR) {
                switch (VALOR) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int iniciar() { return (fatorial(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        declaração = '\n'.join('int VALOR{} = {};'.format(ÍNDICE, ÍNDICE) for ÍNDICE in range(270))
        덧셈 = '+'.join('VALOR{}'.format(ÍNDICE) for ÍNDICE in range(270))
        self.자바대조('public class testes { public static int iniciar() {' + declaração +
                    'VALOR_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int zero_operando = 0; return 1 / zero_operando;', 101),
            ('int[] VALOR = null; return VALOR.length;', 102),
            ('int[] VALOR = new int[1]; return VALOR[1];', 103),
            ('int[] VALOR = new int[1]; VALOR[-1] = 3; return 0;', 103),
            ('int VALOR = -1; return new int[VALOR].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for corpo_VALOR, 기대 in 경우들:
            with self.subTest(corpo_VALOR=corpo_VALOR):
                self.compilar_fonte('public class testes { public static int iniciar() { ' + corpo_VALOR + ' } }')
                self.assertEqual(self.execução_RC(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long VALOR; public static int iniciar() { return 0; }',
            'public static int iniciar() { Object VALOR = new Object(); return 0; }',
            'public static int iniciar() { System.out.println("hello"); return 0; }',
            'public static int iniciar() { try { return 1; } catch (Exception erro) { return 2; } }',
            'public static synchronized int iniciar() { return 0; }',
            'public static int iniciar() { return new byte[3].length; }',
            'static native int externo_VALOR(); public static int iniciar() { return externo_VALOR(); }',
            'int VALOR; public static int iniciar() { return 0; }',
        ]
        for corpo_VALOR in 경우들:
            with self.subTest(corpo_VALOR=corpo_VALOR):
                self.compilar_fonte('public class testes { ' + corpo_VALOR + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        saídaTexto = self.Diretório_VALOR / 'native'
        saídaTexto.write_bytes(b'original-output')
        self.compilar_fonte('public class testes { public static int iniciar() { return missing; } }', 성공=False)
        self.assertEqual(saídaTexto.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.compilar_fonte('public class testes { public static int iniciar() { return 37; } }')
        self.assertEqual((self.Diretório_VALOR / 'native').read_bytes()[:5], b'\x7fELF\x01')
        tabela_de_pesquisa = subprocess.check_output(['readelf', '-l', str(self.Diretório_VALOR / 'native')])
        self.assertNotIn(b'INTERP', tabela_de_pesquisa)
        self.assertEqual(self.execução_RC(), 37)

    def test_사용자ELF와ABI분리(self):
        self.compilar_fonte('public class testes { public static int iniciar() { return espaço_do_utilizador.execução_Permissão(); } }',
                    {'espaço_do_utilizador': 'public class espaço_do_utilizador { public static native int execução_Permissão(); }'}, meta='user')
        dados = (self.Diretório_VALOR / 'native').read_bytes()
        self.assertEqual(dados[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', dados, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Diretório_VALOR / 'native')]))
        # espaço_do_utilizador ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compilar_fonte('public class testes { public static int iniciar() { return celular_VALOR.leitura_hardware_porta(1); } }',
                    {'celular_VALOR': 'public class celular_VALOR { public static native int leitura_hardware_porta(int VALOR); }'}, 성공=False, meta='user')

    def teste_exportar_validação(self):
        códigoFonte = 'public class testes { public static int iniciar() { return 0; } static int 호출(int VALOR) { return VALOR; } }'
        self.compilar_fonte(códigoFonte, meta='kernel', 내보냄='kernel_dispatch=testes.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Diretório_VALOR / 'native')]))
        self.compilar_fonte(códigoFonte, 성공=False, 내보냄='bad;name=testes.호출')
        self.compilar_fonte(códigoFonte, 성공=False, 내보냄='missing=testes.없음')


if __name__ == '__main__':
    unittest.main()
