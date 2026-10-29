#!/usr/bin/env python3
"""QEMU의 actualData CPU permissionValue, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
import ftplib
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time

from executeCommand import projectRoot, command
from networkBridge import networkBridge
from EchoFixture import EchoFixture


def run():
    Output = projectRoot / 'build/verification/execution-network-review'
    Output.mkdir(parents=True, exist_ok=True)
    reportValue = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    sourceFiles = {
        'PrivilegeCheck': '''public class PrivilegeCheck {
 public static void main(String[] arguments) {
  System.out.println("EL0_PROBE_READY");
  int number = 0; while (true) { number++; }
 }
}''',
        'NetworkCheck': '''import java.net.*;
public class NetworkCheck {
 public static void main(String[] arguments) throws Exception {
  Socket connect = new Socket("10.0.2.2", Integer.parseInt(arguments[0]));
  connect.setSoTimeout(3000);
  byte[] text = "TCP hangulText\\n".getBytes("UTF-8");
  connect.getOutputStream().write(text);
  for (int positionIndex = 0; positionIndex < text.length; positionIndex++)
   if (connect.getInputStream().read() != (text[positionIndex] & 255)) throw new RuntimeException("TCP mismatch");
  connect.close();
  DatagramSocket endpoint = new DatagramSocket(); endpoint.setSoTimeout(3000);
  text = "UDP hangulText".getBytes("UTF-8");
  endpoint.send(new DatagramPacket(text, text.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(arguments[1])));
  byte[] reply = new byte[64]; DatagramPacket datagram = new DatagramPacket(reply, reply.length);
  endpoint.receive(datagram);
  if (datagram.getLength() != text.length) throw new RuntimeException("UDP length");
  for (int positionIndex = 0; positionIndex < text.length; positionIndex++)
   if (reply[positionIndex] != text[positionIndex]) throw new RuntimeException("UDP mismatch");
  endpoint.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'ReceiveCheck': '''import java.net.*;
public class ReceiveCheck {
 public static void main(String[] arguments) throws Exception {
  ServerSocket serverValue = new ServerSocket(9300); serverValue.setSoTimeout(5000);
  DatagramSocket endpoint = new DatagramSocket(9301); endpoint.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket connect = serverValue.accept(); connect.setSoTimeout(5000);
  connect.getOutputStream().write(connect.getInputStream().read() + 1);
  connect.close(); serverValue.close();
  byte[] data = new byte[64]; DatagramPacket datagram = new DatagramPacket(data, data.length);
  endpoint.receive(datagram); endpoint.send(datagram); endpoint.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for name, source in sourceFiles.items():
        (Output / (name + '.java')).write_text(source, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Output)] +
                          [str(Output / (name + '.java')) for name in sourceFiles])
    logRecord = bytearray()
    def emptyPortNumber(typeCategory=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, typeCategory) as searchValue:
            searchValue.bind(('127.0.0.4', 0))
            return searchValue.getsockname()[1]
    filePortNumber, tcpPort, udpPort = emptyPortNumber(), emptyPortNumber(), emptyPortNumber(socket.SOCK_DGRAM)
    processValue = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as temporaryValue, networkBridge(
                filePortNumber, ['tcp:{}:9300'.format(tcpPort), 'udp:{}:9301'.format(udpPort)],
                capture=True, hostAddress='127.0.0.4') as bridgeValue:
            controlPath = Path(temporaryValue) / 'qmp.sock'
            processValue = subprocess.Popen(command() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(controlPath)] + bridgeValue.forwardedArgument(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            chooseItem = selectors.DefaultSelector()
            chooseItem.register(processValue.stdout, selectors.EVENT_READ)
            def receive(showValue=b'jkoros-native> ', initialItem=0, limitValue=60):
                ending = time.monotonic() + limitValue
                while showValue not in logRecord[initialItem:]:
                    if time.monotonic() > ending or processValue.poll() is not None:
                        raise AssertionError('Missing ' + repr(showValue) + '\n' + logRecord[initialItem:].decode('utf-8', 'replace'))
                    for keyValue, _ in chooseItem.select(.05):
                        fragmentValue = keyValue.fileobj.read(65536)
                        if fragmentValue:
                            logRecord.extend(fragmentValue)
                return logRecord[initialItem:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def send(data):
                processValue.stdin.write(data)
                processValue.stdin.flush()
            def shell(text):
                print(text, flush=True)
                initialItem = len(logRecord)
                send((text + '\n').encode())
                return receive(initialItem=initialItem)
            receive()
            with socket.socket(socket.AF_UNIX) as controlValue:
                controlValue.settimeout(10)
                controlValue.connect(str(controlPath))
                streamValue = controlValue.makefile('rwb')
                json.loads(streamValue.readline())
                def request(instructionValue, arguments=None):
                    data = {'execute': instructionValue}
                    if arguments is not None:
                        data['arguments'] = arguments
                    streamValue.write((json.dumps(data) + '\n').encode())
                    streamValue.flush()
                    while True:
                        reply = json.loads(streamValue.readline())
                        if 'error' in reply:
                            raise AssertionError(reply)
                        if 'return' in reply:
                            return reply['return']
                request('qmp_capabilities')
                def readPermission():
                    request('stop')
                    try:
                        return request('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        request('cont')
                reportValue['shell_cpu'] = readPermission()
                assert 'EL1h' in reportValue['shell_cpu'], reportValue['shell_cpu']
                reportValue['initial_ps'] = shell('ps')
                assert 'kernel/shell' in reportValue['initial_ps']
                reportValue['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in reportValue['ipconfig']
                reportValue['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in reportValue['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as transferValue:
                    transferValue.encoding = 'utf-8'
                    transferValue.connect('127.0.0.4', filePortNumber, timeout=20)
                    transferValue.login()
                    for name in sourceFiles:
                        transferValue.storbinary('STOR ' + name + '.class', io.BytesIO((Output / (name + '.class')).read_bytes()))
                initialItem = len(logRecord)
                send('java PrivilegeCheck\n'.encode())
                receive(b'EL0_PROBE_READY\r\n', initialItem)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    reportValue['java_cpu'] = readPermission()
                    if 'EL0t' in reportValue['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in reportValue['java_cpu'], reportValue['java_cpu']
                receive(initialItem=initialItem)
                reportValue['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', reportValue['after_exit_ps'])
                reportValue['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with EchoFixture() as peerValue:
                    text = shell('java NetworkCheck {} {}'.format(peerValue.tcpPort, peerValue.udpPort))
                    assert 'OUTBOUND_TCP_UDP_PASS' in text and 'exit 0' in text, text
                    assert peerValue.hasReceived == {'tcp': 'TCP hangulText\n'.encode(), 'udp': 'UDP hangulText'.encode()}, peerValue.hasReceived
                    assert not peerValue.errors, peerValue.errors
                    reportValue['outbound_peers'] = {kindValue: data.decode() for kindValue, data in peerValue.hasReceived.items()}
                initialItem = len(logRecord)
                send('java ReceiveCheck\n'.encode())
                receive(b'INBOUND_READY\r\n', initialItem)
                with socket.create_connection(('127.0.0.4', tcpPort), timeout=5) as peerValue:
                    peerValue.sendall(b'A')
                    assert peerValue.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peerValue:
                    peerValue.settimeout(5)
                    peerValue.sendto(b'UDP-IN', ('127.0.0.4', udpPort))
                    assert peerValue.recvfrom(64)[0] == b'UDP-IN'
                text = receive(initialItem=initialItem)
                assert 'INBOUND_TCP_UDP_PASS' in text and 'exit 0' in text, text
                reportValue['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                initialItem = len(logRecord)
                send('java WindowExample\n'.encode())
                receive('GUI examples prepare: WindowExample\r\n'.encode(), initialItem)
                initialItem = len(logRecord)
                send(bytes([30, 2, 1, 0, 0, 0, 0]))
                receive(initialItem=initialItem)
                reportValue['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java WindowExample', reportValue['suspended_java_ps']), reportValue['suspended_java_ps']
                reportValue['top'] = shell('top -n 1')
                assert 'java WindowExample' in reportValue['top'] and 'kernel/shell' in reportValue['top']
                reportValue['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                reportValue['network_trace'] = bridgeValue.traceLog
                assert not bridgeValue.error, bridgeValue.error
                send(b'poweroff\n')
                assert processValue.wait(timeout=15) == 0
                reportValue['passed'] = True
            chooseItem.close()
    except Exception as error:
        reportValue['error'] = str(error)
        raise
    finally:
        if processValue is not None and processValue.poll() is None:
            processValue.terminate()
            try:
                processValue.wait(timeout=10)
            except subprocess.TimeoutExpired:
                processValue.kill()
                processValue.wait()
        (Output / 'serial.log').write_bytes(logRecord)
        (Output / 'report.json').write_text(json.dumps(reportValue, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({keyValue: reportValue[keyValue] for keyValue in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    run()
