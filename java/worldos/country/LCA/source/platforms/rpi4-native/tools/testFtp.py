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
from networkBridge import networkBridge
from executeCommand import projectRoot, command
from EchoFixture import EchoFixture
from testElf import linuxExample


def run():
    resultData = projectRoot / 'build/verification/ftp'; resultData.mkdir(parents=True, exist_ok=True)
    validationReport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcript = bytearray()
    javaSource = resultData / 'testBundle.java'
    javaSource.write_text('public class testBundle { public static void main(String[] arguments) throws Exception { English.Native.Output.writeLine("JAR executeCommand: " + arguments[0]); English.Native.file.write("jar.txt", "Native kernelValue file"); English.Native.Output.writeLine(English.Native.file.read("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projectRoot/'build/java-library/classes'), '-d', str(resultData), str(javaSource)])
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as javaBundle:
        javaBundle.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: testBundle\r\n\r\n')
        javaBundle.write(str(resultData/'testBundle.class'), 'testBundle.class')
    with socket.socket() as temporary:
        temporary.bind(('127.0.0.1', 0)); portNumber = temporary.getsockname()[1]
    with socket.socket() as temporary:
        temporary.bind(('127.0.0.1', 0)); serverStreamPort = temporary.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temporary:
        temporary.bind(('127.0.0.1', 0)); serverDatagramPort = temporary.getsockname()[1]
    with networkBridge(portNumber, ['tcp:{}:9300'.format(serverStreamPort), 'udp:{}:9301'.format(serverDatagramPort)], capture=True) as bridge:
        process = subprocess.Popen(command() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bridge.forwardedArgument(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector(); selector.register(process.stdout, selectors.EVENT_READ)
        def receiveMessage(marker=b'jkoros-native> ', executionTimeout=60):
            data = bytearray(); endOffset = time.monotonic() + executionTimeout
            while marker not in data:
                if time.monotonic() > endOffset or process.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for pressedValue, _ in selector.select(.1):
                    fragmentValue = pressedValue.fileobj.read(4096)
                    if fragmentValue: data.extend(fragmentValue); transcript.extend(fragmentValue)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(line):
            process.stdin.write(line.encode() + b'\n'); process.stdin.flush(); return receiveMessage()
        try:
            receiveMessage(); assert 'FTP listening' in shell('ftpd start')
            fileTransferConnection = ftplib.FTP(); fileTransferConnection.encoding = 'utf-8'; fileTransferConnection.connect('127.0.0.1', portNumber, timeout=20); fileTransferConnection.login()
            payloadData = bytes(range(256)) * 32
            fileTransferConnection.storbinary('STOR binary.dat', io.BytesIO(payloadData))
            result = bytearray(); fileTransferConnection.retrbinary('RETR binary.dat', result.extend)
            assert result == payloadData; assert fileTransferConnection.size('binary.dat') == len(payloadData)
            validationReport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fileTransferConnection.storbinary('STOR hangulText.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat hangulText.txt')
            assert 'hangulText.txt' in fileTransferConnection.nlst()
            assert dict(fileTransferConnection.mlsd())['hangulText.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validationReport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fileTransferConnection.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as auxiliaryEntry: assert str(auxiliaryEntry).startswith('552'), str(auxiliaryEntry)
            else: raise AssertionError('oversized upload accepted')
            result = bytearray(); fileTransferConnection.retrbinary('RETR binary.dat', result.extend); assert result == payloadData
            validationReport['checks'].append('oversized replacement rejected; previous file preserved')
            with fileTransferConnection.transfercmd('STOR pending.txt') as uploadFiles:
                # A control command must not change the active upload's destination.
                assert fileTransferConnection.size('binary.dat') == len(payloadData)
                uploadFiles.sendall(b'UPLOAD TARGET PRESERVED')
            assert fileTransferConnection.voidresp().startswith('226')
            result = bytearray(); fileTransferConnection.retrbinary('RETR pending.txt', result.extend)
            assert result == b'UPLOAD TARGET PRESERVED'
            result = bytearray(); fileTransferConnection.retrbinary('RETR binary.dat', result.extend)
            assert result == payloadData
            fileTransferConnection.delete('pending.txt')
            validationReport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fileTransferConnection.storbinary('STOR Greeting.jar', io.BytesIO(archive.getvalue()))
            text = shell('java -jar Greeting.jar 누리')
            assert 'JAR executeCommand: 누리' in text and 'Native kernelValue file' in text and 'exit 0' in text, text
            text = shell('./Greeting.jar 세상')
            assert 'JAR executeCommand: 세상' in text and 'exit 0' in text, text
            validationReport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            originalData = '#include <FileABI.h>\nstruct data { int number; double 비율; };\nint sumValue(int n) { return n ? n + sumValue(n-1) : 0; }\nint main(void) { struct data value = {sumValue(10), 1.25}; if (value.number != 55 || value.비율 * 2 != 2.5) return 3; const char Greeting[] = "CC NATIVE PASS\\n"; int guides = openFile("cc.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600); if (guides < 0) return 1; writeFileData(guides, Greeting, sizeof(Greeting)-1); closeFile(guides); writeFileData(1, Greeting, sizeof(Greeting)-1); return 0; }\n'
            fileTransferConnection.storbinary('STOR hangulText.c', io.BytesIO(originalData.encode()))
            text = shell('cc hangulText.c -o hangulText.elf'); assert 'Compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = shell('run hangulText.elf'); assert 'CC NATIVE PASS' in text and 'exit 0' in text, text
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            executableFile = bytearray(); fileTransferConnection.retrbinary('RETR hangulText.elf', executableFile.extend)
            assert executableFile[:4] == b'\x7fELF' and executableFile[18:20] == b'\xb7\x00'
            fileTransferConnection.storbinary('STOR copyValue.elf', io.BytesIO(executableFile)); text = shell('run copyValue.elf'); assert 'CC NATIVE PASS' in text and 'exit 0' in text, text
            fileTransferConnection.storbinary('STOR executeCommand', io.BytesIO(executableFile)); text=shell('./executeCommand');assert 'CC NATIVE PASS' in text and 'exit 0' in text,text
            fileTransferConnection.storbinary('STOR name.txt', io.BytesIO(executableFile)); text=shell('./name.txt');assert 'CC NATIVE PASS' in text and 'exit 0' in text,text
            shell('rm executeCommand name.txt')
            validationReport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat hangulText.txt hangulText.c hangulText.elf copyValue.elf cc.txt jar.txt')
            linuxFile,expected=linuxExample(resultData/'linux-reference')
            fileTransferConnection.storbinary('STOR 리눅스인사',io.BytesIO(linuxFile.read_bytes()))
            text=shell('./리눅스인사');assert 'exit -8' in text,text
            text=shell('run --linux 리눅스인사 한글인수');assert expected+'exit 0' in text,text
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            fileTransferConnection.delete('리눅스인사');fileTransferConnection.delete('linux.txt')
            fileTransferConnection.storbinary('STOR falseValue.elf',io.BytesIO(b'plain text'))
            assert '실행할 number 없습니다:' in shell('./falseValue.elf');fileTransferConnection.delete('falseValue.elf')
            validationReport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with EchoFixture() as echoServerEntry:
                netSource = resultData/'ExternalCommunication.java'
                netSource.write_text('''import java.net.*; import java.io.*;
public class ExternalCommunication { public static void main(String[] args) throws Exception {
 Socket connect = English.Native.connectionTransport.connect("10.0.2.2", Integer.parseInt(args[0]));
 connect.getOutputStream().write("TCP hangulText\\n".getBytes("UTF-8"));
 byte[] source = "TCP hangulText\\n".getBytes("UTF-8");
 for (int i=0;i<source.length;i++) if (connect.getInputStream().read() != (source[i]&255)) throw new RuntimeException("TCP mismatch");
 connect.close();
 DatagramSocket endpoint = English.Native.communication.open(0); English.Native.communication.timeout(endpoint, 500);
 English.Native.communication.send(endpoint, "10.0.2.2", Integer.parseInt(args[1]), "UDP hangulText");
 if (!English.Native.communication.receive(endpoint).equals("UDP hangulText")) throw new RuntimeException("UDP mismatch");
 endpoint.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projectRoot/'build/java-library/classes'),'-d',str(resultData),str(netSource)])
                fileTransferConnection.storbinary('STOR ExternalCommunication.class', io.BytesIO((resultData/'ExternalCommunication.class').read_bytes()))
                text = shell('java ExternalCommunication {} {}'.format(echoServerEntry.tcpPort, echoServerEntry.udpPort))
                assert 'EXTERNAL TCP UDP PASS' in text and '10.0.2.2' in text and 'exit 0' in text, text
                assert echoServerEntry.hasReceived == {'tcp':'TCP hangulText\n'.encode(), 'udp':'UDP hangulText'.encode()}, echoServerEntry.hasReceived
                assert not echoServerEntry.errors, echoServerEntry.errors
            validationReport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fileTransferConnection.delete('ExternalCommunication.class')
            serverSource=resultData/'ServerTest.java'
            serverSource.write_text('''import java.net.*; public class ServerTest {
 public static void main(String[] args) throws Exception {
  ServerSocket serverValue = new ServerSocket(9300); DatagramSocket endpoint = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket guestValue = serverValue.accept();
  guestValue.getOutputStream().write(guestValue.getInputStream().read()+1); guestValue.close(); serverValue.close();
  byte[] contentValue = new byte[8]; DatagramPacket datagram = new DatagramPacket(contentValue, contentValue.length); endpoint.receive(datagram);
  endpoint.send(datagram); endpoint.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(resultData),str(serverSource)])
            fileTransferConnection.storbinary('STOR ServerTest.class',io.BytesIO((resultData/'ServerTest.class').read_bytes()))
            process.stdin.write('java ServerTest\n'.encode());process.stdin.flush();receiveMessage(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',serverStreamPort),timeout=5) as peerValue:
                peerValue.sendall(b'A');assert peerValue.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peerValue:
                peerValue.settimeout(5);peerValue.sendto(b'UDP-IN',('127.0.0.1',serverDatagramPort));assert peerValue.recvfrom(512)[0]==b'UDP-IN'
            text=receiveMessage();assert 'INBOUND TCP UDP PASS' in text and 'exit 0' in text,text
            validationReport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fileTransferConnection.delete('ServerTest.class')
            instructionSequence = 'public class Colour { public static void main(String[] arguments) throws Exception { int sumValue = 0; int number = 1; while (number <= 10) { sumValue = sumValue + number; number = number + 1; } English.Native.Output.writeNumber(sumValue); English.Native.file.write("aot.txt", "hangulText AOT file 😀"); English.Native.Output.writeLine(English.Native.file.read("aot.txt")); } }'
            fileTransferConnection.storbinary('STOR Colour.java', io.BytesIO(instructionSequence.encode()))
            text = shell('javac Colour.java'); assert 'exit 0' in text and 'Compiled:' in text, text
            text = shell('jaot Colour.class -o Colour.elf'); assert 'AOT compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = shell('run Colour.elf'); assert '\n55\n' in text and 'hangulText AOT file 😀' in text and 'exit 0' in text, text
            native = bytearray(); fileTransferConnection.retrbinary('RETR Colour.elf', native.extend)
            text = shell('jaot Greeting.jar -o Colour.elf'); assert 'exit 1' in text and 'unsupported' in text, text
            preservedData = bytearray(); fileTransferConnection.retrbinary('RETR Colour.elf', preservedData.extend); assert native == preservedData
            bytecode = bytearray(); fileTransferConnection.retrbinary('RETR Colour.class', bytecode.extend)
            packed = io.BytesIO()
            with zipfile.ZipFile(packed, 'w', zipfile.ZIP_DEFLATED) as javaBundle:
                javaBundle.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: Colour\r\n\r\n')
                javaBundle.writestr('Colour.class', bytecode)
            fileTransferConnection.storbinary('STOR Colour.jar', io.BytesIO(packed.getvalue()))
            text = shell('jaot Colour.jar -o Colour.elf'); assert 'AOT compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = shell('run Colour.elf'); assert '\n55\n' in text and 'hangulText AOT file 😀' in text and 'exit 0' in text, text
            validationReport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validationReport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            staticSource=resultData/'StaticTest.java'
            staticSource.write_text('''public class StaticTest {
 static int projectRoot = 3;
 static int sumValue(int n) { return n == 0 ? 0 : n + sumValue(n-1); }
 public static void main(String[] arguments) {
  int[] value = new int[] {projectRoot, sumValue(10)};
  System.out.println(value[0] + value[1]); System.out.println(arguments[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(resultData),str(staticSource)])
            fileTransferConnection.storbinary('STOR StaticTest.class',io.BytesIO((resultData/'StaticTest.class').read_bytes()))
            text=shell('jaot StaticTest.class -o StaticTest.elf');assert 'exit 0' in text,text
            text=shell('run StaticTest.elf 한글인수');assert '\n58\n한글인수\nexit 0' in text,text
            fileTransferConnection.delete('StaticTest.class');fileTransferConnection.delete('StaticTest.elf')
            validationReport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            broken=bytearray(archive.getvalue());broken[14]^=1
            fileTransferConnection.storbinary('STOR Greeting.jar',io.BytesIO(broken))
            text=shell('java -jar Greeting.jar');assert 'Main-Class\nexit 1' in text,text
            validationReport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fileTransferConnection.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not bridge.error, bridge.error
            validationReport.update(passed=True, frames_to_guest=bridge.framesToGuest, frames_from_guest=bridge.framesFromGuest)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for pressedValue,_ in selector.select(0):
                fragmentValue=pressedValue.fileobj.read(65536)
                if fragmentValue: transcript.extend(fragmentValue)
            bridge.pauseEvent.set()
            process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired: process.kill(); process.wait()
            selector.close(); process.stdin.close(); process.stdout.close()
            validationReport['bridge_error'] = bridge.error
            validationReport['frames_to_guest'] = bridge.framesToGuest; validationReport['frames_from_guest'] = bridge.framesFromGuest
            (resultData/'packets.json').write_text(json.dumps(bridge.traceLog,indent=2)+'\n')
            (resultData / 'serial.log').write_bytes(transcript)
            (resultData / 'report.json').write_text(json.dumps(validationReport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': run()
