#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from puenteRed import puenteRed
from ejecutarComando import raízProyecto, comando
from DispositivoPruebaRepetirEntrada import DispositivoPruebaRepetirEntrada
from pruebaELF import ejemploLinux


def ponerEnMarcha():
    datosResultado = raízProyecto / 'build/verification/ftp'; datosResultado.mkdir(parents=True, exist_ok=True)
    informeValidación = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcripción = bytearray()
    fuenteJava = datosResultado / 'pruebaPaquete.java'
    fuenteJava.write_text('public class pruebaPaquete { public static void main(String[] argumentos) throws Exception { español.propio.Salida.escribirLínea("JAR ejecutarComando: " + argumentos[0]); español.propio.Archivo.escribir("jar.txt", "propio valorNúcleo Archivo"); español.propio.Salida.escribirLínea(español.propio.Archivo.leer("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(raízProyecto/'build/java-library/classes'), '-d', str(datosResultado), str(fuenteJava)])
    archivoComprimido = io.BytesIO()
    with zipfile.ZipFile(archivoComprimido, 'w', zipfile.ZIP_DEFLATED) as paqueteJava:
        paqueteJava.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: pruebaPaquete\r\n\r\n')
        paqueteJava.write(str(datosResultado/'pruebaPaquete.class'), 'pruebaPaquete.class')
    with socket.socket() as temporal:
        temporal.bind(('127.0.0.1', 0)); númeroPuerto = temporal.getsockname()[1]
    with socket.socket() as temporal:
        temporal.bind(('127.0.0.1', 0)); puertoFlujoServidor = temporal.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temporal:
        temporal.bind(('127.0.0.1', 0)); puertoDatagramaServidor = temporal.getsockname()[1]
    with puenteRed(númeroPuerto, ['tcp:{}:9300'.format(puertoFlujoServidor), 'udp:{}:9301'.format(puertoDatagramaServidor)], capturarDatos=True) as puente:
        proceso = subprocess.Popen(comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + puente.argumentoReenviado(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector(); selector.register(proceso.stdout, selectors.EVENT_READ)
        def recibirMensaje(marcador=b'jkoros-native> ', tiempoEsperaEjecución=60):
            Datos = bytearray(); desfaseFin = time.monotonic() + tiempoEsperaEjecución
            while marcador not in Datos:
                if time.monotonic() > desfaseFin or proceso.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + Datos.decode('utf-8', 'replace'))
                for valorPulsado, _ in selector.select(.1):
                    valorFragmento = valorPulsado.fileobj.read(4096)
                    if valorFragmento: Datos.extend(valorFragmento); transcripción.extend(valorFragmento)
                if b'PANIC:' in Datos or b'FAIL ' in Datos: raise AssertionError(Datos)
            return Datos.decode('utf-8', 'replace').replace('\r\n', '\n')
        def intérpreteComandos(línea):
            proceso.stdin.write(línea.encode() + b'\n'); proceso.stdin.flush(); return recibirMensaje()
        try:
            recibirMensaje(); assert 'FTP listening' in intérpreteComandos('ftpd start')
            conexiónTransferenciaArchivo = ftplib.FTP(); conexiónTransferenciaArchivo.encoding = 'utf-8'; conexiónTransferenciaArchivo.connect('127.0.0.1', númeroPuerto, timeout=20); conexiónTransferenciaArchivo.login()
            datosCargaÚtil = bytes(range(256)) * 32
            conexiónTransferenciaArchivo.storbinary('STOR binary.dat', io.BytesIO(datosCargaÚtil))
            resultado = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR binary.dat', resultado.extend)
            assert resultado == datosCargaÚtil; assert conexiónTransferenciaArchivo.size('binary.dat') == len(datosCargaÚtil)
            informeValidación['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            conexiónTransferenciaArchivo.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in intérpreteComandos('cat 한글.txt')
            assert '한글.txt' in conexiónTransferenciaArchivo.nlst()
            assert dict(conexiónTransferenciaArchivo.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            informeValidación['checks'].append('UTF-8 filename and content visible in guest shell')
            try: conexiónTransferenciaArchivo.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as entradaElementoAuxiliar: assert str(entradaElementoAuxiliar).startswith('552'), str(entradaElementoAuxiliar)
            else: raise AssertionError('oversized upload accepted')
            resultado = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR binary.dat', resultado.extend); assert resultado == datosCargaÚtil
            informeValidación['checks'].append('oversized replacement rejected; previous file preserved')
            with conexiónTransferenciaArchivo.transfercmd('STOR pending.txt') as archivosSubir:
                # A control command must not change the active upload's destination.
                assert conexiónTransferenciaArchivo.size('binary.dat') == len(datosCargaÚtil)
                archivosSubir.sendall(b'UPLOAD TARGET PRESERVED')
            assert conexiónTransferenciaArchivo.voidresp().startswith('226')
            resultado = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR pending.txt', resultado.extend)
            assert resultado == b'UPLOAD TARGET PRESERVED'
            resultado = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR binary.dat', resultado.extend)
            assert resultado == datosCargaÚtil
            conexiónTransferenciaArchivo.delete('pending.txt')
            informeValidación['checks'].append('interleaved SIZE cannot change the active STOR destination')
            conexiónTransferenciaArchivo.storbinary('STOR Saludo.jar', io.BytesIO(archivoComprimido.getvalue()))
            texto = intérpreteComandos('java -jar Saludo.jar 누리')
            assert 'JAR ejecutarComando: 누리' in texto and 'propio valorNúcleo Archivo' in texto and 'exit 0' in texto, texto
            texto = intérpreteComandos('./Saludo.jar 세상')
            assert 'JAR ejecutarComando: 세상' in texto and 'exit 0' in texto, texto
            informeValidación['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            datosOriginal = '#include <ABIArchivo.h>\nstruct Datos { int númeroValor; double 비율; };\nint valorTotalSuma(int n) { return n ? n + valorTotalSuma(n-1) : 0; }\nint main(void) { struct Datos valor = {valorTotalSuma(10), 1.25}; if (valor.númeroValor != 55 || valor.비율 * 2 != 2.5) return 3; const char Saludo[] = "CC NATIVE PASS\\n"; int Documentación = abrirArchivo("cc.txt", EscribirLeer | AusenteSiCrear | ContenidoTruncar, 0600); if (Documentación < 0) return 1; escribirDatosArchivo(Documentación, Saludo, sizeof(Saludo)-1); cerrarArchivo(Documentación); escribirDatosArchivo(1, Saludo, sizeof(Saludo)-1); return 0; }\n'
            conexiónTransferenciaArchivo.storbinary('STOR textoHangul.c', io.BytesIO(datosOriginal.encode()))
            texto = intérpreteComandos('cc textoHangul.c -o textoHangul.elf'); assert 'Compiled native ARM64 ELF:' in texto and 'exit 0' in texto, texto
            texto = intérpreteComandos('run textoHangul.elf'); assert 'CC NATIVE PASS' in texto and 'exit 0' in texto, texto
            assert 'CC NATIVE PASS' in intérpreteComandos('cat cc.txt')
            archivoCódigoEjecutable = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR textoHangul.elf', archivoCódigoEjecutable.extend)
            assert archivoCódigoEjecutable[:4] == b'\x7fELF' and archivoCódigoEjecutable[18:20] == b'\xb7\x00'
            conexiónTransferenciaArchivo.storbinary('STOR copiarValor.elf', io.BytesIO(archivoCódigoEjecutable)); texto = intérpreteComandos('run copiarValor.elf'); assert 'CC NATIVE PASS' in texto and 'exit 0' in texto, texto
            conexiónTransferenciaArchivo.storbinary('STOR ejecutarComando', io.BytesIO(archivoCódigoEjecutable)); texto=intérpreteComandos('./ejecutarComando');assert 'CC NATIVE PASS' in texto and 'exit 0' in texto,texto
            conexiónTransferenciaArchivo.storbinary('STOR nombre.txt', io.BytesIO(archivoCódigoEjecutable)); texto=intérpreteComandos('./nombre.txt');assert 'CC NATIVE PASS' in texto and 'exit 0' in texto,texto
            intérpreteComandos('rm ejecutarComando nombre.txt')
            informeValidación['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            intérpreteComandos('rm binary.dat textoHangul.txt textoHangul.c textoHangul.elf copiarValor.elf cc.txt jar.txt')
            archivoLinux,esperado=ejemploLinux(datosResultado/'linux-reference')
            conexiónTransferenciaArchivo.storbinary('STOR 리눅스인사',io.BytesIO(archivoLinux.read_bytes()))
            texto=intérpreteComandos('./리눅스인사');assert 'exit -8' in texto,texto
            texto=intérpreteComandos('run --linux 리눅스인사 한글인수');assert esperado+'exit 0' in texto,texto
            assert 'LINUX ELF FILE IO' in intérpreteComandos('cat linux.txt')
            conexiónTransferenciaArchivo.delete('리눅스인사');conexiónTransferenciaArchivo.delete('linux.txt')
            conexiónTransferenciaArchivo.storbinary('STOR valorFalso.elf',io.BytesIO(b'plain text'))
            assert '실행할 númeroValor 없습니다:' in intérpreteComandos('./valorFalso.elf');conexiónTransferenciaArchivo.delete('valorFalso.elf')
            informeValidación['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with DispositivoPruebaRepetirEntrada() as entradaElementoServidorRepetirEntrada:
                fuenteRedCorta = datosResultado/'ComunicaciónExterno.java'
                fuenteRedCorta.write_text('''import java.net.*; import java.io.*;
public class ComunicaciónExterno { public static void main(String[] args) throws Exception {
 Socket conectar = español.propio.transporteConexión.conectar("10.0.2.2", Integer.parseInt(args[0]));
 conectar.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] fuente = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<fuente.length;i++) if (conectar.getInputStream().read() != (fuente[i]&255)) throw new RuntimeException("TCP mismatch");
 conectar.close();
 DatagramSocket extremo = español.propio.Comunicación.abrir(0); español.propio.Comunicación.tiempoEspera(extremo, 500);
 español.propio.Comunicación.enviar(extremo, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!español.propio.Comunicación.recibir(extremo).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 extremo.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(raízProyecto/'build/java-library/classes'),'-d',str(datosResultado),str(fuenteRedCorta)])
                conexiónTransferenciaArchivo.storbinary('STOR ComunicaciónExterno.class', io.BytesIO((datosResultado/'ComunicaciónExterno.class').read_bytes()))
                texto = intérpreteComandos('java ComunicaciónExterno {} {}'.format(entradaElementoServidorRepetirEntrada.puertoTCP, entradaElementoServidorRepetirEntrada.puertoUDP))
                assert 'EXTERNAL TCP UDP PASS' in texto and '10.0.2.2' in texto and 'exit 0' in texto, texto
                assert entradaElementoServidorRepetirEntrada.tieneRecibido == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, entradaElementoServidorRepetirEntrada.tieneRecibido
                assert not entradaElementoServidorRepetirEntrada.errores, entradaElementoServidorRepetirEntrada.errores
            informeValidación['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            conexiónTransferenciaArchivo.delete('ComunicaciónExterno.class')
            fuenteServidor=datosResultado/'PruebaServidor.java'
            fuenteServidor.write_text('''import java.net.*; public class PruebaServidor {
 public static void main(String[] args) throws Exception {
  ServerSocket valorServidor = new ServerSocket(9300); DatagramSocket extremo = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket valorInvitado = valorServidor.accept();
  valorInvitado.getOutputStream().write(valorInvitado.getInputStream().read()+1); valorInvitado.close(); valorServidor.close();
  byte[] valorContenidoValor = new byte[8]; DatagramPacket datagrama = new DatagramPacket(valorContenidoValor, valorContenidoValor.length); extremo.receive(datagrama);
  extremo.send(datagrama); extremo.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(datosResultado),str(fuenteServidor)])
            conexiónTransferenciaArchivo.storbinary('STOR PruebaServidor.class',io.BytesIO((datosResultado/'PruebaServidor.class').read_bytes()))
            proceso.stdin.write('java PruebaServidor\n'.encode());proceso.stdin.flush();recibirMensaje(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',puertoFlujoServidor),timeout=5) as valorParRed:
                valorParRed.sendall(b'A');assert valorParRed.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as valorParRed:
                valorParRed.settimeout(5);valorParRed.sendto(b'UDP-IN',('127.0.0.1',puertoDatagramaServidor));assert valorParRed.recvfrom(512)[0]==b'UDP-IN'
            texto=recibirMensaje();assert 'INBOUND TCP UDP PASS' in texto and 'exit 0' in texto,texto
            informeValidación['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            conexiónTransferenciaArchivo.delete('PruebaServidor.class')
            secuenciaInstrucciónMáquina = 'public class Color { public static void main(String[] argumentos) throws Exception { int valorTotalSuma = 0; int númeroValor = 1; while (númeroValor <= 10) { valorTotalSuma = valorTotalSuma + númeroValor; númeroValor = númeroValor + 1; } español.propio.Salida.escribirNúmero(valorTotalSuma); español.propio.Archivo.escribir("aot.txt", "한글 AOT Archivo 😀"); español.propio.Salida.escribirLínea(español.propio.Archivo.leer("aot.txt")); } }'
            conexiónTransferenciaArchivo.storbinary('STOR Color.java', io.BytesIO(secuenciaInstrucciónMáquina.encode()))
            texto = intérpreteComandos('javac Color.java'); assert 'exit 0' in texto and 'Compiled:' in texto, texto
            texto = intérpreteComandos('jaot Color.class -o Color.elf'); assert 'AOT compiled native ARM64 ELF:' in texto and 'exit 0' in texto, texto
            texto = intérpreteComandos('run Color.elf'); assert '\n55\n' in texto and '한글 AOT Archivo 😀' in texto and 'exit 0' in texto, texto
            nativo = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR Color.elf', nativo.extend)
            texto = intérpreteComandos('jaot Saludo.jar -o Color.elf'); assert 'exit 1' in texto and 'unsupported' in texto, texto
            datosPreservado = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR Color.elf', datosPreservado.extend); assert nativo == datosPreservado
            códigoBytes = bytearray(); conexiónTransferenciaArchivo.retrbinary('RETR Color.class', códigoBytes.extend)
            empaquetado = io.BytesIO()
            with zipfile.ZipFile(empaquetado, 'w', zipfile.ZIP_DEFLATED) as paqueteJava:
                paqueteJava.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: Color\r\n\r\n')
                paqueteJava.writestr('Color.class', códigoBytes)
            conexiónTransferenciaArchivo.storbinary('STOR Color.jar', io.BytesIO(empaquetado.getvalue()))
            texto = intérpreteComandos('jaot Color.jar -o Color.elf'); assert 'AOT compiled native ARM64 ELF:' in texto and 'exit 0' in texto, texto
            texto = intérpreteComandos('run Color.elf'); assert '\n55\n' in texto and '한글 AOT Archivo 😀' in texto and 'exit 0' in texto, texto
            informeValidación['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            informeValidación['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            fuenteEstático=datosResultado/'PruebaEstático.java'
            fuenteEstático.write_text('''public class PruebaEstático {
 static int raízProyecto = 3;
 static int valorTotalSuma(int n) { return n == 0 ? 0 : n + valorTotalSuma(n-1); }
 public static void main(String[] argumentos) {
  int[] valor = new int[] {raízProyecto, valorTotalSuma(10)};
  System.out.println(valor[0] + valor[1]); System.out.println(argumentos[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(datosResultado),str(fuenteEstático)])
            conexiónTransferenciaArchivo.storbinary('STOR PruebaEstático.class',io.BytesIO((datosResultado/'PruebaEstático.class').read_bytes()))
            texto=intérpreteComandos('jaot PruebaEstático.class -o PruebaEstático.elf');assert 'exit 0' in texto,texto
            texto=intérpreteComandos('run PruebaEstático.elf 한글인수');assert '\n58\n한글인수\nexit 0' in texto,texto
            conexiónTransferenciaArchivo.delete('PruebaEstático.class');conexiónTransferenciaArchivo.delete('PruebaEstático.elf')
            informeValidación['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            dañado=bytearray(archivoComprimido.getvalue());dañado[14]^=1
            conexiónTransferenciaArchivo.storbinary('STOR Saludo.jar',io.BytesIO(dañado))
            texto=intérpreteComandos('java -jar Saludo.jar');assert 'Main-Class\nexit 1' in texto,texto
            informeValidación['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            conexiónTransferenciaArchivo.quit(); assert 'FTP stopped' in intérpreteComandos('ftpd stop')
            assert not puente.error, puente.error
            informeValidación.update(passed=True, frames_to_guest=puente.invitadoHaciaMarcos, frames_from_guest=puente.invitadoDesdeMarcos)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for valorPulsado,_ in selector.select(0):
                valorFragmento=valorPulsado.fileobj.read(65536)
                if valorFragmento: transcripción.extend(valorFragmento)
            puente.eventoPausar.set()
            proceso.terminate()
            try: proceso.wait(timeout=5)
            except subprocess.TimeoutExpired: proceso.kill(); proceso.wait()
            selector.close(); proceso.stdin.close(); proceso.stdout.close()
            informeValidación['bridge_error'] = puente.error
            informeValidación['frames_to_guest'] = puente.invitadoHaciaMarcos; informeValidación['frames_from_guest'] = puente.invitadoDesdeMarcos
            (datosResultado/'packets.json').write_text(json.dumps(puente.diarioTraza,indent=2)+'\n')
            (datosResultado / 'serial.log').write_bytes(transcripción)
            (datosResultado / 'report.json').write_text(json.dumps(informeValidación, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ponerEnMarcha()
