"""datosEfectivo ELF ejecutarComando + OpenJDK resultado 대조. valorTemporal Pruebas 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

Compilador = Path(__file__).resolve().parents[1] / 'Compilador.py'


class pruebaNativo(unittest.TestCase):
    def setUp(self):
        self.valorTemporal = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.valorTemporal.cleanup)
        self.valorDirectorio = Path(self.valorTemporal.name)

    def compilarFuente(self, fuente, añadirFinalEntradaElemento=None, valorÉxito=True, valorObjetivo='linux', valorExportado=None):
        listaRuta = []
        for nombre, valorContenidoValor in dict({'Pruebas': fuente}, **(añadirFinalEntradaElemento or {})).items():
            ruta = self.valorDirectorio / (nombre + '.java')
            ruta.write_text(valorContenidoValor, encoding='utf-8')
            listaRuta.append(str(ruta))
        comando = [sys.executable, str(Compilador), '--target', valorObjetivo, '--entry', 'Pruebas.ponerEnMarcha', '-o', str(self.valorDirectorio / 'native')]
        if valorExportado is not None: comando += ['--export', valorExportado]
        resultado = subprocess.run(comando + listaRuta,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if valorÉxito:
            self.assertEqual(resultado.returncode, 0, resultado.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(resultado.returncode, 0)
            self.assertIn('compilarFuente error'.encode(), resultado.stderr)
        return resultado

    def resultadoEjecución(self):
        return subprocess.run([str(self.valorDirectorio / 'native')], timeout=5).returncode

    def comparaciónJava(self, fuente, añadirFinalEntradaElemento=None):
        self.compilarFuente(fuente, añadirFinalEntradaElemento)
        (self.valorDirectorio / 'Anfitrión.java').write_text(
            'public class Anfitrión { public static void main(String[] argumentos) { System.exit(Pruebas.ponerEnMarcha()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.valorDirectorio)] +
                       [str(ruta) for ruta in self.valorDirectorio.glob('*.java')], check=True, timeout=30)
        expectativa = subprocess.run(['java', '-cp', str(self.valorDirectorio), 'Anfitrión'], timeout=5).returncode
        datosEfectivo = self.resultadoEjecución()
        self.assertGreaterEqual(datosEfectivo, 0, '신호로 tieneSalido (샌드박스의 32비트 syscall valorLímite 여부 verificar)')
        self.assertEqual(datosEfectivo, expectativa)

    def pruebaDesplazamientosYAritméticaEnteroValor(self):
        self.comparaciónJava('''public class Pruebas {
            static int aritméticaMezclar(int operandoPrimero, int operandoSegundo) {
                return ((operandoPrimero + operandoSegundo) ^ (operandoPrimero - operandoSegundo) ^ (operandoPrimero * operandoSegundo) ^ (operandoPrimero & operandoSegundo) ^ (operandoPrimero | operandoSegundo))
                    + (operandoPrimero << operandoSegundo) + (operandoPrimero >> operandoSegundo) + (operandoPrimero >>> operandoSegundo);
            }
            public static int ponerEnMarcha() {
                int valorTotalSuma = 7;
                int valor = 12345;
                for (int número = -65; número <= 65; número++) {
                    valor = valor * 1664525 + 1013904223;
                    valorTotalSuma = valorTotalSuma * 31 + aritméticaMezclar(valor, número);
                    valorTotalSuma += (byte)valor + (short)valor + (char)valor;
                }
                return (valorTotalSuma & 0x7fffffff) % 251;
            }
        }''')

    def pruebaValoresExtremoDivisión(self):
        self.comparaciónJava('''public class Pruebas {
            static int[] valor = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ponerEnMarcha() {
                int valorTotalSuma = 13;
                for (int operandoPrimero = 0; operandoPrimero < valor.length; operandoPrimero++)
                    for (int operandoSegundo = 1; operandoSegundo < valor.length; operandoSegundo++)
                        valorTotalSuma = valorTotalSuma * 31 + valor[operandoPrimero] / valor[operandoSegundo] + valor[operandoPrimero] % valor[operandoSegundo];
                return (valorTotalSuma & 0x7fffffff) % 251;
            }
        }''')

    def pruebaReferenciasYArreglos(self):
        self.comparaciónJava('''public class Pruebas {
            static int[] crearEntradaElemento(int tamaño) { return new int[tamaño]; }
            public static int ponerEnMarcha() {
                int[] operandoPrimero = crearEntradaElemento(8); int[] operandoSegundo = operandoPrimero; int[] objetoVacíoEstado = new int[0];
                if (operandoPrimero != operandoSegundo || operandoPrimero == null || objetoVacíoEstado.length != 0 || operandoPrimero[7] != 0) return 99;
                int valor = (operandoPrimero[2] = 40); operandoPrimero[2]++; ++operandoPrimero[3]; operandoPrimero[2] += 7;
                return valor + operandoSegundo[2] + operandoSegundo[3];
            }
        }''')

    def pruebaOrdenArgumentoYCamposEstático(self):
        self.comparaciónJava('''public class Pruebas {
            static int valor = valorAuxiliar.valorInicialValor();
            static int resultadoCálculo(int operandoPrimero, int operandoSegundo, int operandoTercero, int operandoCuarto, int operandoQuinto) {
                return operandoPrimero + operandoSegundo * 2 + operandoTercero * 3 + operandoCuarto * 4 + operandoQuinto * 5;
            }
            public static int ponerEnMarcha() { return resultadoCálculo(1, 2, 3, 4, valor) + valorAuxiliar.leer(); }
        }''', {'valorAuxiliar': '''public class valorAuxiliar {
            static int valor = 3;
            static int valorInicialValor() { return ++valor; }
            static int leer() { return valor; }
        }'''})

    def pruebaCicloInicialización(self):
        self.comparaciónJava('''public class Pruebas {
            static int valor = valorAuxiliar.leer() + 1;
            public static int ponerEnMarcha() { return valor * 10 + valorAuxiliar.leer(); }
        }''', {'valorAuxiliar': '''public class valorAuxiliar {
            static int valor = Pruebas.valor + 2;
            static int leer() { return valor; }
        }'''})

    def pruebaCadenas8UTFModificado(self):
        self.comparaciónJava('''public class Pruebas {
            static String texto = "한글\\u0000😀";
            public static int ponerEnMarcha() {
                if (texto != "한글\\u0000😀") return 99;
                return (texto.length() + texto.charAt(2) + texto.charAt(3) + texto.charAt(4)) % 251;
            }
        }''')

    def pruebaRecursiónYConmutar(self):
        self.comparaciónJava('''public class Pruebas {
            static int factorial(int valor) { return valor <= 1 ? 1 : valor * factorial(valor - 1); }
            static int casosConmutarDenso(int valor) {
                switch (valor) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int casosConmutarDisperso(int valor) {
                switch (valor) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ponerEnMarcha() { return (factorial(5) + casosConmutarDenso(0) + casosConmutarDenso(2) + casosConmutarDenso(9) + casosConmutarDisperso(-1000) + casosConmutarDisperso(0)) % 251; }
        }''')

    def pruebaVariablesLocalAncho(self):
        Declaraciones = '\n'.join('int valor{} = {};'.format(número, número) for número in range(270))
        resultadoSuma = '+'.join('valor{}'.format(número) for número in range(270))
        self.comparaciónJava('public class Pruebas { public static int ponerEnMarcha() {' + Declaraciones +
                    'valor269 += 300; return (' + resultadoSuma + ') % 251; } }')

    def pruebaNúmerosErrorEntornoEjecución(self):
        entradasCaso = [
            ('int operandoCero = 0; return 1 / operandoCero;', 101),
            ('int[] valor = null; return valor.length;', 102),
            ('int[] valor = new int[1]; return valor[1];', 103),
            ('int[] valor = new int[1]; valor[-1] = 3; return 0;', 103),
            ('int valor = -1; return new int[valor].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] operandoPrimero = new int[65535]; return new int[1].length;', 105),
        ]
        for valorCuerpo, expectativa in entradasCaso:
            with self.subTest(valorCuerpo=valorCuerpo):
                self.compilarFuente('public class Pruebas { public static int ponerEnMarcha() { ' + valorCuerpo + ' } }')
                self.assertEqual(self.resultadoEjecución(), expectativa)

    def pruebaRechazadoFuncionalidadNoAdmitido(self):
        entradasCaso = [
            'static long valor; public static int ponerEnMarcha() { return 0; }',
            'public static int ponerEnMarcha() { Object valor = new Object(); return 0; }',
            'public static int ponerEnMarcha() { System.out.println("hello"); return 0; }',
            'public static int ponerEnMarcha() { try { return 1; } catch (Exception error) { return 2; } }',
            'public static synchronized int ponerEnMarcha() { return 0; }',
            'public static int ponerEnMarcha() { return new byte[3].length; }',
            'static native int valorExterno(); public static int ponerEnMarcha() { return valorExterno(); }',
            'int valor; public static int ponerEnMarcha() { return 0; }',
        ]
        for valorCuerpo in entradasCaso:
            with self.subTest(valorCuerpo=valorCuerpo):
                self.compilarFuente('public class Pruebas { ' + valorCuerpo + ' }', valorÉxito=False)

    def pruebaFalloActivadoPreservadoSalidaExistente(self):
        Salida = self.valorDirectorio / 'native'
        Salida.write_bytes(b'original-output')
        self.compilarFuente('public class Pruebas { public static int ponerEnMarcha() { return missing; } }', valorÉxito=False)
        self.assertEqual(Salida.read_bytes(), b'original-output')

    def pruebaEjecuciónAutónomoYELF(self):
        self.compilarFuente('public class Pruebas { public static int ponerEnMarcha() { return 37; } }')
        self.assertEqual((self.valorDirectorio / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Tabla = subprocess.check_output(['readelf', '-l', str(self.valorDirectorio / 'native')])
        self.assertNotIn(b'INTERP', Tabla)
        self.assertEqual(self.resultadoEjecución(), 37)

    def pruebaSeparaciónABIYELFUsuario(self):
        self.compilarFuente('public class Pruebas { public static int ponerEnMarcha() { return Usuario.permisoEjecución(); } }',
                    {'Usuario': 'public class Usuario { public static native int permisoEjecución(); }'}, valorObjetivo='user')
        Datos = (self.valorDirectorio / 'native').read_bytes()
        self.assertEqual(Datos[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', Datos, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.valorDirectorio / 'native')]))
        # Usuario ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compilarFuente('public class Pruebas { public static int ponerEnMarcha() { return Dispositivo.leerPuertoEquipoFísico(1); } }',
                    {'Dispositivo': 'public class Dispositivo { public static native int leerPuertoEquipoFísico(int valor); }'}, valorÉxito=False, valorObjetivo='user')

    def pruebaValidaciónExportar(self):
        fuente = 'public class Pruebas { public static int ponerEnMarcha() { return 0; } static int invocar(int valor) { return valor; } }'
        self.compilarFuente(fuente, valorObjetivo='kernel', valorExportado='kernel_dispatch=Pruebas.invocar')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.valorDirectorio / 'native')]))
        self.compilarFuente(fuente, valorÉxito=False, valorExportado='bad;name=Pruebas.invocar')
        self.compilarFuente(fuente, valorÉxito=False, valorExportado='missing=Pruebas.métodoAusente')


if __name__ == '__main__':
    unittest.main()
