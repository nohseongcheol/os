#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ejecutarComando, valorFallo/valorRecurso valorFrontera Pruebas."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from pruebaRedUsuario import MáquinaVirtual, posición


def valorEditar(máquina, nombre, valorContenidoValor, valorAlmacenar=True):
    ponerEnMarcha = len(máquina.registroEntradaDiario)
    máquina.valorSerie.sendall(('edit ' + nombre + '\n').encode())
    máquina.esperarEstadoValor('...> ', ponerEnMarcha)
    for línea in valorContenidoValor.splitlines():
        assert len(línea) <= 128
        ponerEnMarcha = len(máquina.registroEntradaDiario)
        máquina.valorSerie.sendall((línea + '\n').encode())
        máquina.esperarEstadoValor('...> ', ponerEnMarcha)
    ponerEnMarcha = len(máquina.registroEntradaDiario)
    máquina.valorSerie.sendall(b'.save\n' if valorAlmacenar else b'.cancel\n')
    resultado = máquina.esperarEstadoValor('jkoros> ', ponerEnMarcha)
    assert ('Saved:' if valorAlmacenar else 'Cancelled; original preserved') in resultado, resultado


def direcciónArchivo():
    resultado = subprocess.check_output(['nm', '-n', str(posición / 'build/kernel.elf')], universal_newlines=True)
    for línea in resultado.splitlines():
        if línea.endswith(' ram_files'):
            return int(línea.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def archivoInvitado(máquina, valorRanura, tamaño, ruta):
    # Pruebas VM의 메모리에서 datosEfectivo 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    dirección = direcciónArchivo() + valorRanura * 16384
    máquina.valorMonitor.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(dirección, tamaño, ruta)).encode())
    terminación = time.monotonic() + 5
    while time.monotonic() < terminación:
        if ruta.exists() and ruta.stat().st_size == tamaño:
            return ruta.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def pruebaPonerEnMarcha(valorClaseTipo):
    máquina = MáquinaVirtual(posición / ('build/kernel.elf' if valorClaseTipo == 'elf' else 'build/kernel.iso'), valorClaseTipo, valorRed=False)
    resultado = {}
    try:
        máquina.comando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        máquina.comando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        máquina.comando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        máquina.comando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        máquina.comando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        máquina.comando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        máquina.comando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        valorContenidoValor = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        valorEditar(máquina, 'Calc.java', valorContenidoValor)
        máquina.comando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        expectativa = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Salida = máquina.comando('java Calc 6 guest', ['\r\n' + '\r\n'.join(expectativa) + '\r\n', 'Exit: 0'])
        resultado['guest_output'] = Salida
        listaEntradaElemento = máquina.comando('ls', ['Calc.class'])
        tamaño = int(re.search(r'Calc\.class\s+(\d+) bytes', listaEntradaElemento).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as valorDirectorio:
            ruta = Path(valorDirectorio) / 'Calc.class'
            Datos = archivoInvitado(máquina, 3, tamaño, ruta)
            datosEfectivo = subprocess.check_output(['java', '-Xverify:all', '-cp', valorDirectorio, 'Calc', '6', 'guest'], universal_newlines=True)
            assert datosEfectivo.splitlines() == expectativa, datosEfectivo
            resultado['class_sha256'] = hashlib.sha256(Datos).hexdigest()
            resultado['openjdk_output'] = datosEfectivo
        # 실패한 valorEditar/컴파일은 기존 class를 보존한다.
        valorEditar(máquina, 'Calc.java', 'not Java at all', valorAlmacenar=False)
        máquina.comando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for resultadoInválido in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            valorEditar(máquina, 'Calc.java', resultadoInválido)
            máquina.comando('javac Calc.java', ['javac error:', 'Exit: 1'])
            máquina.comando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # valorIteración 실행은 Usuario valorMontículo/프레임을 매번 초기화한다.
        for númeroValor in range(12):
            máquina.comando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        máquina.comando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        máquina.comando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        valorEditar(máquina, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        máquina.comando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        máquina.comando('java Calc', ['instruction limit', 'Exit: 1'])
        máquina.comando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        valorEditar(máquina, 'Bad.class', 'garbage')
        máquina.comando('java Bad', ['JVM error:', 'Exit: 1'])
        máquina.comando('rm Bad.class', ['Removed'])
        máquina.comando('java Bad', ['cannot read class: -2'])
        # valorEditar 입력의 넘친 부분을 잘라서 저장하지 않는다.
        ponerEnMarcha = len(máquina.registroEntradaDiario)
        máquina.valorSerie.sendall(b'edit Hello.java\n')
        máquina.esperarEstadoValor('...> ', ponerEnMarcha)
        ponerEnMarcha = len(máquina.registroEntradaDiario)
        máquina.valorSerie.sendall(b'x' * 129 + b'\n')
        máquina.esperarEstadoValor('...> ', ponerEnMarcha)
        máquina.comando('.save', ['Too much input; original preserved'])
        máquina.comando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        valorEditar(máquina, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for númeroValor in range(3):
            valorEditar(máquina, 'f' + str(númeroValor), 'occupied')
        máquina.comando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        máquina.comando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in máquina.registroEntradaDiario.decode('utf-8', 'replace')
        resultado['serial'] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(valorClaseTipo))
        return resultado
    finally:
        máquina.cerrar()


def códigoMayor(Datos):
    """손상 시험용 main Code의 datosEfectivo Archivo 오프셋/길이만 읽는다."""
    valorPosición = 8
    def leerCortoSinSigno():
        nonlocal valorPosición
        valor = struct.unpack_from('>H', Datos, valorPosición)[0]
        valorPosición += 2
        return valor
    def leerEnteroValorSinSigno():
        nonlocal valorPosición
        valor = struct.unpack_from('>I', Datos, valorPosición)[0]
        valorPosición += 4
        return valor
    valoresCarácter = {}
    for númeroValor in range(1, leerCortoSinSigno()):
        valorClaseTipo = Datos[valorPosición]
        valorPosición += 1
        if valorClaseTipo == 1:
            longitud = leerCortoSinSigno()
            valoresCarácter[númeroValor] = Datos[valorPosición:valorPosición + longitud]
            valorPosición += longitud
        elif valorClaseTipo in (7, 8): valorPosición += 2
        elif valorClaseTipo in (3, 9, 10, 12): valorPosición += 4
        else: raise AssertionError(valorClaseTipo)
    valorPosición += 6
    númeroElementosElementoLista = leerCortoSinSigno()
    valorPosición += númeroElementosElementoLista * 2
    assert leerCortoSinSigno() == 0
    for númeroValor in range(leerCortoSinSigno()):
        leerCortoSinSigno()
        nombre = leerCortoSinSigno()
        leerCortoSinSigno()
        for númeroValor in range(leerCortoSinSigno()):
            valorAtributo = leerCortoSinSigno()
            tamaño = leerEnteroValorSinSigno()
            if valoresCarácter[nombre] == b'main' and valoresCarácter[valorAtributo] == b'Code':
                return valorPosición + 8, struct.unpack_from('>I', Datos, valorPosición + 4)[0]
            valorPosición += tamaño
    raise AssertionError('main Code missing')


def pruebaCargaEnCurso():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as valorTemporal:
        valorDirectorio = Path(valorTemporal)
        (valorDirectorio / 'build').mkdir()
        fuente = valorDirectorio / 'Imported.java'
        fuente.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(fuente)], check=True)
        original = (valorDirectorio / 'Imported.class').read_bytes()
        valorCódigo, longitud = códigoMayor(original)
        valorVariante = {}
        Datos = bytearray(original); Datos[0] = 0; valorVariante['BadMagic'] = Datos
        Datos = bytearray(original); Datos[7] = 61; valorVariante['BadVer'] = Datos
        Datos = bytearray(original); Datos[8:10] = b'\xff\xff'; valorVariante['BadPool'] = Datos
        Datos = bytearray(original); Datos[valorCódigo:valorCódigo + longitud] = bytes(longitud)
        Datos[valorCódigo:valorCódigo + 3] = b'\xa7\x00\x01'; Datos[valorCódigo + longitud - 1] = 177; valorVariante['BadJump'] = Datos
        Datos = bytearray(original); Datos[valorCódigo:valorCódigo + longitud] = bytes(longitud)
        Datos[valorCódigo] = 87; Datos[valorCódigo + longitud - 1] = 177; valorVariante['BadStack'] = Datos
        # nombre 검사를 통과시켜 datosEfectivo ejecutarComando 중의 pilaOperando 오류까지 검사한다.
        valorVariante['BadStack'] = valorVariante['BadStack'].replace(b'Imported', b'BadStack')
        valorEntradaElemento = ['Imported.class=' + str(valorDirectorio / 'Imported.class'), 'Imported.java=' + str(fuente)]
        for nombre, Datos in valorVariante.items():
            ruta = valorDirectorio / (nombre + '.class'); ruta.write_bytes(Datos)
            valorEntradaElemento.append(nombre + '.class=' + str(ruta))
        valorGrupo = valorDirectorio / 'build/java-files.bin'
        subprocess.run([sys.executable, str(posición / 'Herramientas/EmpaquetarArchivosJava.py'), '-o', str(valorGrupo)] + valorEntradaElemento, check=True)
        subprocess.run(['as', '--32', '-o', str(valorDirectorio / 'user.o'), str(posición / 'Arranque/Usuario.s')], cwd=str(valorDirectorio), check=True)
        valorNúcleo = valorDirectorio / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posición / 'Arranque/DisposiciónEnlace.ld'), '-o', str(valorNúcleo),
                        str(posición / 'build/boot.o'), str(posición / 'build/java.o'), str(valorDirectorio / 'user.o'), str(posición / 'build/apps.o')], check=True)
        máquina = MáquinaVirtual(valorNúcleo, valorRed=False)
        try:
            máquina.comando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            máquina.comando('cat Imported.java', ['int[] values = new int[3]'])
            for nombre, valorExpresiónFrase in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                máquina.comando('java ' + nombre, [valorExpresiónFrase, 'Exit: 1'])
                máquina.comando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return máquina.registroEntradaDiario.decode('utf-8', 'replace')
        finally:
            máquina.cerrar()


if __name__ == '__main__':
    analizarValor = argparse.ArgumentParser()
    analizarValor.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumentos = analizarValor.parse_args()
    resultado = {valorClaseTipo: pruebaPonerEnMarcha(valorClaseTipo) for valorClaseTipo in (('elf', 'iso') if argumentos.boot == 'both' else (argumentos.boot,))}
    resultado['import'] = pruebaCargaEnCurso()
    (posición / 'build/PruebaJava.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n')
