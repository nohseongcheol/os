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
from bridge_3de4fe3a import bridge_3de4fe3a
from Esegui_comando import azione_radice, comando
from eco_schermo_fixture import eco_schermo_fixture
from 실행파일시험 import 리눅스예제


def avvia():
    KR_dati = azione_radice / 'build/verification/ftp'; KR_dati.mkdir(parents=True, exist_ok=True)
    convalida_Report = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((azione_radice / 'build/kernel8.img').read_bytes()).hexdigest()}
    trascrizione = bytearray()
    자바원문 = KR_dati / 'test_aggregare.java'
    자바원문.write_text('public class test_aggregare { public static void main(String[] argomenti) throws Exception { Italiano.nativo.uscitaTesto.scrivere_riga("JAR Esegui_comando: " + argomenti[0]); Italiano.nativo.file.Scrittura("jar.txt", "nativo kernel_VALORE file"); Italiano.nativo.uscitaTesto.scrivere_riga(Italiano.nativo.file.Lettura("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(azione_radice/'build/java-library/classes'), '-d', str(KR_dati), str(자바원문)])
    Archivio = io.BytesIO()
    with zipfile.ZipFile(Archivio, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_aggregare\r\n\r\n')
        자바꾸러미.write(str(KR_dati/'test_aggregare.class'), 'test_aggregare.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); numero_di_porta = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_porta = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagramma_porta = 임시자원.getsockname()[1]
    with bridge_3de4fe3a(numero_di_porta, ['tcp:{}:9300'.format(server_Stream_porta), 'udp:{}:9301'.format(server_datagramma_porta)], acquisire=True) as bridge:
        Processi = subprocess.Popen(comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bridge.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selettore = selectors.DefaultSelector(); selettore.register(Processi.stdout, selectors.EVENT_READ)
        def ricevere_documento(marcatore=b'jkoros-native> ', esecuzione_TIMEOUT=60):
            dati = bytearray(); chiudere_SCARTO = time.monotonic() + esecuzione_TIMEOUT
            while marcatore not in dati:
                if time.monotonic() > chiudere_SCARTO or Processi.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + dati.decode('utf-8', 'replace'))
                for 누름값, _ in selettore.select(.1):
                    blocco_VALORE_652d4b53 = 누름값.fileobj.read(4096)
                    if blocco_VALORE_652d4b53: dati.extend(blocco_VALORE_652d4b53); trascrizione.extend(blocco_VALORE_652d4b53)
                if b'PANIC:' in dati or b'FAIL ' in dati: raise AssertionError(dati)
            return dati.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Shell(riga_di_ingresso):
            Processi.stdin.write(riga_di_ingresso.encode() + b'\n'); Processi.stdin.flush(); return ricevere_documento()
        try:
            ricevere_documento(); assert 'FTP listening' in Shell('ftpd start')
            trasferimento_di_file_connessione = ftplib.FTP(); trasferimento_di_file_connessione.encoding = 'utf-8'; trasferimento_di_file_connessione.connect('127.0.0.1', numero_di_porta, timeout=20); trasferimento_di_file_connessione.login()
            payload_dati = bytes(range(256)) * 32
            trasferimento_di_file_connessione.storbinary('STOR binary.dat', io.BytesIO(payload_dati))
            risultato = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR binary.dat', risultato.extend)
            assert risultato == payload_dati; assert trasferimento_di_file_connessione.size('binary.dat') == len(payload_dati)
            convalida_Report['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            trasferimento_di_file_connessione.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Shell('cat 한글.txt')
            assert '한글.txt' in trasferimento_di_file_connessione.nlst()
            assert dict(trasferimento_di_file_connessione.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            convalida_Report['checks'].append('UTF-8 filename and content visible in guest shell')
            try: trasferimento_di_file_connessione.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            risultato = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR binary.dat', risultato.extend); assert risultato == payload_dati
            convalida_Report['checks'].append('oversized replacement rejected; previous file preserved')
            with trasferimento_di_file_connessione.transfercmd('STOR pending.txt') as Upload_File:
                # A control command must not change the active upload's destination.
                assert trasferimento_di_file_connessione.size('binary.dat') == len(payload_dati)
                Upload_File.sendall(b'UPLOAD TARGET PRESERVED')
            assert trasferimento_di_file_connessione.voidresp().startswith('226')
            risultato = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR pending.txt', risultato.extend)
            assert risultato == b'UPLOAD TARGET PRESERVED'
            risultato = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR binary.dat', risultato.extend)
            assert risultato == payload_dati
            trasferimento_di_file_connessione.delete('pending.txt')
            convalida_Report['checks'].append('interleaved SIZE cannot change the active STOR destination')
            trasferimento_di_file_connessione.storbinary('STOR messaggio_di_saluto_ae353e94.jar', io.BytesIO(Archivio.getvalue()))
            testo = Shell('java -jar messaggio_di_saluto_ae353e94.jar 누리')
            assert 'JAR Esegui_comando: 누리' in testo and 'nativo kernel_VALORE file' in testo and 'exit 0' in testo, testo
            testo = Shell('./messaggio_di_saluto_ae353e94.jar 세상')
            assert 'JAR Esegui_comando: 세상' in testo and 'exit 0' in testo, testo
            convalida_Report['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <File_ABI.h>\nstruct dati { int numero; double 비율; };\nint SUM_VALORE(int n) { return n ? n + SUM_VALORE(n-1) : 0; }\nint main(void) { struct dati VALORE = {SUM_VALORE(10), 1.25}; if (VALORE.numero != 55 || VALORE.비율 * 2 != 2.5) return 3; const char messaggio_di_saluto_ae353e94[] = "CC NATIVE PASS\\n"; int Guides = aperto_File("cc.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600); if (Guides < 0) return 1; scrivere_File_dati(Guides, messaggio_di_saluto_ae353e94, sizeof(messaggio_di_saluto_ae353e94)-1); Chiudi_File(Guides); scrivere_File_dati(1, messaggio_di_saluto_ae353e94, sizeof(messaggio_di_saluto_ae353e94)-1); return 0; }\n'
            trasferimento_di_file_connessione.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            testo = Shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in testo and 'exit 0' in testo, testo
            testo = Shell('run 한글.elf'); assert 'CC NATIVE PASS' in testo and 'exit 0' in testo, testo
            assert 'CC NATIVE PASS' in Shell('cat cc.txt')
            eseguibile = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR 한글.elf', eseguibile.extend)
            assert eseguibile[:4] == b'\x7fELF' and eseguibile[18:20] == b'\xb7\x00'
            trasferimento_di_file_connessione.storbinary('STOR copiare_VALORE.elf', io.BytesIO(eseguibile)); testo = Shell('run copiare_VALORE.elf'); assert 'CC NATIVE PASS' in testo and 'exit 0' in testo, testo
            trasferimento_di_file_connessione.storbinary('STOR Esegui_comando', io.BytesIO(eseguibile)); testo=Shell('./Esegui_comando');assert 'CC NATIVE PASS' in testo and 'exit 0' in testo,testo
            trasferimento_di_file_connessione.storbinary('STOR Nome.txt', io.BytesIO(eseguibile)); testo=Shell('./Nome.txt');assert 'CC NATIVE PASS' in testo and 'exit 0' in testo,testo
            Shell('rm Esegui_comando Nome.txt')
            convalida_Report['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Shell('rm binary.dat 한글.txt 한글.c 한글.elf copiare_VALORE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_dati/'linux-reference')
            trasferimento_di_file_connessione.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            testo=Shell('./리눅스인사');assert 'exit -8' in testo,testo
            testo=Shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in testo,testo
            assert 'LINUX ELF FILE IO' in Shell('cat linux.txt')
            trasferimento_di_file_connessione.delete('리눅스인사');trasferimento_di_file_connessione.delete('linux.txt')
            trasferimento_di_file_connessione.storbinary('STOR FALSO_VALORE.elf',io.BytesIO(b'plain text'))
            assert '실행할 numero 없습니다:' in Shell('./FALSO_VALORE.elf');trasferimento_di_file_connessione.delete('FALSO_VALORE.elf')
            convalida_Report['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with eco_schermo_fixture() as eco_schermo_server_voce:
                NET_fonte = KR_dati/'esterno_comunicazione.java'
                NET_fonte.write_text('''import java.net.*; import java.io.*;
public class esterno_comunicazione { public static void main(String[] args) throws Exception {
 Socket Connetti = Italiano.nativo.connessione_trasporto.Connetti("10.0.2.2", Integer.parseInt(args[0]));
 Connetti.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] codiceSorgente = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<codiceSorgente.length;i++) if (Connetti.getInputStream().read() != (codiceSorgente[i]&255)) throw new RuntimeException("TCP mismatch");
 Connetti.close();
 DatagramSocket endpoint = Italiano.nativo.comunicazione.Apri(0); Italiano.nativo.comunicazione.TIMEOUT(endpoint, 500);
 Italiano.nativo.comunicazione.inviare(endpoint, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Italiano.nativo.comunicazione.ricevere(endpoint).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 endpoint.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(azione_radice/'build/java-library/classes'),'-d',str(KR_dati),str(NET_fonte)])
                trasferimento_di_file_connessione.storbinary('STOR esterno_comunicazione.class', io.BytesIO((KR_dati/'esterno_comunicazione.class').read_bytes()))
                testo = Shell('java esterno_comunicazione {} {}'.format(eco_schermo_server_voce.porta_TCP, eco_schermo_server_voce.UDP_porta))
                assert 'EXTERNAL TCP UDP PASS' in testo and '10.0.2.2' in testo and 'exit 0' in testo, testo
                assert eco_schermo_server_voce.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, eco_schermo_server_voce.수신됨
                assert not eco_schermo_server_voce.오류들, eco_schermo_server_voce.오류들
            convalida_Report['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            trasferimento_di_file_connessione.delete('esterno_comunicazione.class')
            server_fonte=KR_dati/'server_test.java'
            server_fonte.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALORE = new ServerSocket(9300); DatagramSocket endpoint = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket guest_VALORE = server_VALORE.accept();
  guest_VALORE.getOutputStream().write(guest_VALORE.getInputStream().read()+1); guest_VALORE.close(); server_VALORE.close();
  byte[] Contenuto_VALORE = new byte[8]; DatagramPacket datagramma = new DatagramPacket(Contenuto_VALORE, Contenuto_VALORE.length); endpoint.receive(datagramma);
  endpoint.send(datagramma); endpoint.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_dati),str(server_fonte)])
            trasferimento_di_file_connessione.storbinary('STOR server_test.class',io.BytesIO((KR_dati/'server_test.class').read_bytes()))
            Processi.stdin.write('java server_test\n'.encode());Processi.stdin.flush();ricevere_documento(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_porta),timeout=5) as peer_VALORE:
                peer_VALORE.sendall(b'A');assert peer_VALORE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_VALORE:
                peer_VALORE.settimeout(5);peer_VALORE.sendto(b'UDP-IN',('127.0.0.1',server_datagramma_porta));assert peer_VALORE.recvfrom(512)[0]==b'UDP-IN'
            testo=ricevere_documento();assert 'INBOUND TCP UDP PASS' in testo and 'exit 0' in testo,testo
            convalida_Report['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            trasferimento_di_file_connessione.delete('server_test.class')
            istruzione_SEQUENZA = 'public class 빛 { public static void main(String[] argomenti) throws Exception { int SUM_VALORE = 0; int numero = 1; while (numero <= 10) { SUM_VALORE = SUM_VALORE + numero; numero = numero + 1; } Italiano.nativo.uscitaTesto.scrivere_numero(SUM_VALORE); Italiano.nativo.file.Scrittura("aot.txt", "한글 AOT file 😀"); Italiano.nativo.uscitaTesto.scrivere_riga(Italiano.nativo.file.Lettura("aot.txt")); } }'
            trasferimento_di_file_connessione.storbinary('STOR 빛.java', io.BytesIO(istruzione_SEQUENZA.encode()))
            testo = Shell('javac 빛.java'); assert 'exit 0' in testo and 'Compiled:' in testo, testo
            testo = Shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in testo and 'exit 0' in testo, testo
            testo = Shell('run 빛.elf'); assert '\n55\n' in testo and '한글 AOT file 😀' in testo and 'exit 0' in testo, testo
            nativo_fd019377 = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR 빛.elf', nativo_fd019377.extend)
            testo = Shell('jaot messaggio_di_saluto_ae353e94.jar -o 빛.elf'); assert 'exit 1' in testo and 'unsupported' in testo, testo
            보존자료 = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR 빛.elf', 보존자료.extend); assert nativo_fd019377 == 보존자료
            바이트코드 = bytearray(); trasferimento_di_file_connessione.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            trasferimento_di_file_connessione.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            testo = Shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in testo and 'exit 0' in testo, testo
            testo = Shell('run 빛.elf'); assert '\n55\n' in testo and '한글 AOT file 😀' in testo and 'exit 0' in testo, testo
            convalida_Report['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            convalida_Report['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statico_fonte=KR_dati/'statico_test.java'
            statico_fonte.write_text('''public class statico_test {
 static int azione_radice = 3;
 static int SUM_VALORE(int n) { return n == 0 ? 0 : n + SUM_VALORE(n-1); }
 public static void main(String[] argomenti) {
  int[] VALORE = new int[] {azione_radice, SUM_VALORE(10)};
  System.out.println(VALORE[0] + VALORE[1]); System.out.println(argomenti[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_dati),str(statico_fonte)])
            trasferimento_di_file_connessione.storbinary('STOR statico_test.class',io.BytesIO((KR_dati/'statico_test.class').read_bytes()))
            testo=Shell('jaot statico_test.class -o statico_test.elf');assert 'exit 0' in testo,testo
            testo=Shell('run statico_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in testo,testo
            trasferimento_di_file_connessione.delete('statico_test.class');trasferimento_di_file_connessione.delete('statico_test.elf')
            convalida_Report['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archivio.getvalue());손상자료[14]^=1
            trasferimento_di_file_connessione.storbinary('STOR messaggio_di_saluto_ae353e94.jar',io.BytesIO(손상자료))
            testo=Shell('java -jar messaggio_di_saluto_ae353e94.jar');assert 'Main-Class\nexit 1' in testo,testo
            convalida_Report['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            trasferimento_di_file_connessione.quit(); assert 'FTP stopped' in Shell('ftpd stop')
            assert not bridge.errore, bridge.errore
            convalida_Report.update(passed=True, frames_to_guest=bridge.커널수신틀수, frames_from_guest=bridge.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selettore.select(0):
                blocco_VALORE_652d4b53=누름값.fileobj.read(65536)
                if blocco_VALORE_652d4b53: trascrizione.extend(blocco_VALORE_652d4b53)
            bridge.Pause_evento.set()
            Processi.terminate()
            try: Processi.wait(timeout=5)
            except subprocess.TimeoutExpired: Processi.kill(); Processi.wait()
            selettore.close(); Processi.stdin.close(); Processi.stdout.close()
            convalida_Report['bridge_error'] = bridge.errore
            convalida_Report['frames_to_guest'] = bridge.커널수신틀수; convalida_Report['frames_from_guest'] = bridge.커널발신틀수
            (KR_dati/'packets.json').write_text(json.dumps(bridge.log_di_analisi,indent=2)+'\n')
            (KR_dati / 'serial.log').write_bytes(trascrizione)
            (KR_dati / 'report.json').write_text(json.dumps(convalida_Report, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': avvia()
