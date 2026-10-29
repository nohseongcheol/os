#!/usr/bin/env python3
"""QEMU의 वास्तविक_डेटा CPU परवानगी_मूल्य, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ, आदेश
from संचारजाळे_ब्रिज import संचारजाळे_ब्रिज
from प्रतिध्वनी_चाचणीसाधन import प्रतिध्वनी_चाचणीसाधन


def सुरू_करा():
    आउटपुट = प्रोजेक्ट_मूळ / 'build/verification/execution-network-review'
    आउटपुट.mkdir(parents=True, exist_ok=True)
    अहवाल_मूल्य = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    स्रोत_संचिका = {
        'विशेषाधिकार_तपासा': '''public class विशेषाधिकार_तपासा {
 public static void main(String[] बाबी) {
  System.out.println("EL0_PROBE_READY");
  int संख्या = 0; while (true) { संख्या++; }
 }
}''',
        'संचारजाळे_तपासा': '''import java.net.*;
public class संचारजाळे_तपासा {
 public static void main(String[] बाबी) throws Exception {
  Socket जोडा = new Socket("10.0.2.2", Integer.parseInt(बाबी[0]));
  जोडा.setSoTimeout(3000);
  byte[] पाठ्य = "TCP 한글\\n".getBytes("UTF-8");
  जोडा.getOutputStream().write(पाठ्य);
  for (int स्थान_अनुक्रमणिका = 0; स्थान_अनुक्रमणिका < पाठ्य.length; स्थान_अनुक्रमणिका++)
   if (जोडा.getInputStream().read() != (पाठ्य[स्थान_अनुक्रमणिका] & 255)) throw new RuntimeException("TCP mismatch");
  जोडा.close();
  DatagramSocket संचारटोक = new DatagramSocket(); संचारटोक.setSoTimeout(3000);
  पाठ्य = "UDP 한글".getBytes("UTF-8");
  संचारटोक.send(new DatagramPacket(पाठ्य, पाठ्य.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(बाबी[1])));
  byte[] प्रत्युत्तर_द्या = new byte[64]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(प्रत्युत्तर_द्या, प्रत्युत्तर_द्या.length);
  संचारटोक.receive(स्वतंत्रसंदेश);
  if (स्वतंत्रसंदेश.getLength() != पाठ्य.length) throw new RuntimeException("UDP length");
  for (int स्थान_अनुक्रमणिका = 0; स्थान_अनुक्रमणिका < पाठ्य.length; स्थान_अनुक्रमणिका++)
   if (प्रत्युत्तर_द्या[स्थान_अनुक्रमणिका] != पाठ्य[स्थान_अनुक्रमणिका]) throw new RuntimeException("UDP mismatch");
  संचारटोक.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'तपासा_स्वीकारा': '''import java.net.*;
public class तपासा_स्वीकारा {
 public static void main(String[] बाबी) throws Exception {
  ServerSocket सर्व्हर_मूल्य = new ServerSocket(9300); सर्व्हर_मूल्य.setSoTimeout(5000);
  DatagramSocket संचारटोक = new DatagramSocket(9301); संचारटोक.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket जोडा = सर्व्हर_मूल्य.accept(); जोडा.setSoTimeout(5000);
  जोडा.getOutputStream().write(जोडा.getInputStream().read() + 1);
  जोडा.close(); सर्व्हर_मूल्य.close();
  byte[] डेटा = new byte[64]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(डेटा, डेटा.length);
  संचारटोक.receive(स्वतंत्रसंदेश); संचारटोक.send(स्वतंत्रसंदेश); संचारटोक.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for नाव, स्रोत in स्रोत_संचिका.items():
        (आउटपुट / (नाव + '.java')).write_text(स्रोत, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(आउटपुट)] +
                          [str(आउटपुट / (नाव + '.java')) for नाव in स्रोत_संचिका])
    लॉग_नोंद = bytearray()
    def रिक्त_पोर्ट_नंबर(टाइप_करा_वर्गवारी=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, टाइप_करा_वर्गवारी) as शोध_मूल्य:
            शोध_मूल्य.bind(('127.0.0.4', 0))
            return शोध_मूल्य.getsockname()[1]
    संचिका_पोर्ट_नंबर, ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट, स्वतंत्रसंदेशसंचार_पॉर्ट = रिक्त_पोर्ट_नंबर(), रिक्त_पोर्ट_नंबर(), रिक्त_पोर्ट_नंबर(socket.SOCK_DGRAM)
    प्रक्रिया_मूल्य = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as तात्पुरते_मूल्य, संचारजाळे_ब्रिज(
                संचिका_पोर्ट_नंबर, ['tcp:{}:9300'.format(ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट), 'udp:{}:9301'.format(स्वतंत्रसंदेशसंचार_पॉर्ट)],
                कॅप्चर_करा=True, होस्ट_पत्ता='127.0.0.4') as ब्रिज_मूल्य:
            नियंत्रण_पथ = Path(तात्पुरते_मूल्य) / 'qmp.sock'
            प्रक्रिया_मूल्य = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(नियंत्रण_पथ)] + ब्रिज_मूल्य.अग्रेषित_वितर्क(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            निवडून_घ्या_आयटम = selectors.DefaultSelector()
            निवडून_घ्या_आयटम.register(प्रक्रिया_मूल्य.stdout, selectors.EVENT_READ)
            def स्वीकारा(मूल्य_शो=b'jkoros-native> ', प्रारंभिक_आयटम=0, मर्यादा_मूल्य=60):
                शेवट = time.monotonic() + मर्यादा_मूल्य
                while मूल्य_शो not in लॉग_नोंद[प्रारंभिक_आयटम:]:
                    if time.monotonic() > शेवट or प्रक्रिया_मूल्य.poll() is not None:
                        raise AssertionError('Missing ' + repr(मूल्य_शो) + '\n' + लॉग_नोंद[प्रारंभिक_आयटम:].decode('utf-8', 'replace'))
                    for कळ_मूल्य, _ in निवडून_घ्या_आयटम.select(.05):
                        तुकडा_मूल्य = कळ_मूल्य.fileobj.read(65536)
                        if तुकडा_मूल्य:
                            लॉग_नोंद.extend(तुकडा_मूल्य)
                return लॉग_नोंद[प्रारंभिक_आयटम:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def पाठवा(डेटा):
                प्रक्रिया_मूल्य.stdin.write(डेटा)
                प्रक्रिया_मूल्य.stdin.flush()
            def शेल(पाठ्य):
                print(पाठ्य, flush=True)
                प्रारंभिक_आयटम = len(लॉग_नोंद)
                पाठवा((पाठ्य + '\n').encode())
                return स्वीकारा(प्रारंभिक_आयटम=प्रारंभिक_आयटम)
            स्वीकारा()
            with socket.socket(socket.AF_UNIX) as नियंत्रण_मूल्य:
                नियंत्रण_मूल्य.settimeout(10)
                नियंत्रण_मूल्य.connect(str(नियंत्रण_पथ))
                प्रवाह_मूल्य = नियंत्रण_मूल्य.makefile('rwb')
                json.loads(प्रवाह_मूल्य.readline())
                def विनंती(निर्देश_मूल्य, बाबी=None):
                    डेटा = {'execute': निर्देश_मूल्य}
                    if बाबी is not None:
                        डेटा['arguments'] = बाबी
                    प्रवाह_मूल्य.write((json.dumps(डेटा) + '\n').encode())
                    प्रवाह_मूल्य.flush()
                    while True:
                        प्रत्युत्तर_द्या = json.loads(प्रवाह_मूल्य.readline())
                        if 'error' in प्रत्युत्तर_द्या:
                            raise AssertionError(प्रत्युत्तर_द्या)
                        if 'return' in प्रत्युत्तर_द्या:
                            return प्रत्युत्तर_द्या['return']
                विनंती('qmp_capabilities')
                def परवानगी_वाचा():
                    विनंती('stop')
                    try:
                        return विनंती('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        विनंती('cont')
                अहवाल_मूल्य['shell_cpu'] = परवानगी_वाचा()
                assert 'EL1h' in अहवाल_मूल्य['shell_cpu'], अहवाल_मूल्य['shell_cpu']
                अहवाल_मूल्य['initial_ps'] = शेल('ps')
                assert 'kernel/shell' in अहवाल_मूल्य['initial_ps']
                अहवाल_मूल्य['ipconfig'] = शेल('ipconfig')
                assert 'inet 10.0.2.15' in अहवाल_मूल्य['ipconfig']
                अहवाल_मूल्य['gateway_ping'] = शेल('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in अहवाल_मूल्य['gateway_ping']
                assert 'FTP listening' in शेल('ftpd start')
                with ftplib.FTP() as स्थानांतर_मूल्य:
                    स्थानांतर_मूल्य.encoding = 'utf-8'
                    स्थानांतर_मूल्य.connect('127.0.0.4', संचिका_पोर्ट_नंबर, timeout=20)
                    स्थानांतर_मूल्य.login()
                    for नाव in स्रोत_संचिका:
                        स्थानांतर_मूल्य.storbinary('STOR ' + नाव + '.class', io.BytesIO((आउटपुट / (नाव + '.class')).read_bytes()))
                प्रारंभिक_आयटम = len(लॉग_नोंद)
                पाठवा('java विशेषाधिकार_तपासा\n'.encode())
                स्वीकारा(b'EL0_PROBE_READY\r\n', प्रारंभिक_आयटम)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    अहवाल_मूल्य['java_cpu'] = परवानगी_वाचा()
                    if 'EL0t' in अहवाल_मूल्य['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in अहवाल_मूल्य['java_cpu'], अहवाल_मूल्य['java_cpu']
                स्वीकारा(प्रारंभिक_आयटम=प्रारंभिक_आयटम)
                अहवाल_मूल्य['after_exit_ps'] = शेल('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', अहवाल_मूल्य['after_exit_ps'])
                अहवाल_मूल्य['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with प्रतिध्वनी_चाचणीसाधन() as समकक्ष_मूल्य:
                    पाठ्य = शेल('java संचारजाळे_तपासा {} {}'.format(समकक्ष_मूल्य.ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट, समकक्ष_मूल्य.स्वतंत्रसंदेशसंचार_पॉर्ट))
                    assert 'OUTBOUND_TCP_UDP_PASS' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
                    assert समकक्ष_मूल्य.आहे_स्वीकारलेले == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, समकक्ष_मूल्य.आहे_स्वीकारलेले
                    assert not समकक्ष_मूल्य.त्रुटी_b805b1b5, समकक्ष_मूल्य.त्रुटी_b805b1b5
                    अहवाल_मूल्य['outbound_peers'] = {प्रकार_मूल्य: डेटा.decode() for प्रकार_मूल्य, डेटा in समकक्ष_मूल्य.आहे_स्वीकारलेले.items()}
                प्रारंभिक_आयटम = len(लॉग_नोंद)
                पाठवा('java तपासा_स्वीकारा\n'.encode())
                स्वीकारा(b'INBOUND_READY\r\n', प्रारंभिक_आयटम)
                with socket.create_connection(('127.0.0.4', ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट), timeout=5) as समकक्ष_मूल्य:
                    समकक्ष_मूल्य.sendall(b'A')
                    assert समकक्ष_मूल्य.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as समकक्ष_मूल्य:
                    समकक्ष_मूल्य.settimeout(5)
                    समकक्ष_मूल्य.sendto(b'UDP-IN', ('127.0.0.4', स्वतंत्रसंदेशसंचार_पॉर्ट))
                    assert समकक्ष_मूल्य.recvfrom(64)[0] == b'UDP-IN'
                पाठ्य = स्वीकारा(प्रारंभिक_आयटम=प्रारंभिक_आयटम)
                assert 'INBOUND_TCP_UDP_PASS' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
                अहवाल_मूल्य['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in शेल('terminal')
                शेल('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                प्रारंभिक_आयटम = len(लॉग_नोंद)
                पाठवा('java खिडकीउदाहरण\n'.encode())
                स्वीकारा('GUI उदाहरणे तयार_करणे: खिडकीउदाहरण\r\n'.encode(), प्रारंभिक_आयटम)
                प्रारंभिक_आयटम = len(लॉग_नोंद)
                पाठवा(bytes([30, 2, 1, 0, 0, 0, 0]))
                स्वीकारा(प्रारंभिक_आयटम=प्रारंभिक_आयटम)
                अहवाल_मूल्य['suspended_java_ps'] = शेल('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java खिडकीउदाहरण', अहवाल_मूल्य['suspended_java_ps']), अहवाल_मूल्य['suspended_java_ps']
                अहवाल_मूल्य['top'] = शेल('top -n 1')
                assert 'java खिडकीउदाहरण' in अहवाल_मूल्य['top'] and 'kernel/shell' in अहवाल_मूल्य['top']
                अहवाल_मूल्य['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                अहवाल_मूल्य['network_trace'] = ब्रिज_मूल्य.मागोवा_लॉग
                assert not ब्रिज_मूल्य.त्रुटी, ब्रिज_मूल्य.त्रुटी
                पाठवा(b'poweroff\n')
                assert प्रक्रिया_मूल्य.wait(timeout=15) == 0
                अहवाल_मूल्य['passed'] = True
            निवडून_घ्या_आयटम.close()
    except Exception as त्रुटी:
        अहवाल_मूल्य['error'] = str(त्रुटी)
        raise
    finally:
        if प्रक्रिया_मूल्य is not None and प्रक्रिया_मूल्य.poll() is None:
            प्रक्रिया_मूल्य.terminate()
            try:
                प्रक्रिया_मूल्य.wait(timeout=10)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मूल्य.kill()
                प्रक्रिया_मूल्य.wait()
        (आउटपुट / 'serial.log').write_bytes(लॉग_नोंद)
        (आउटपुट / 'report.json').write_text(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({कळ_मूल्य: अहवाल_मूल्य[कळ_मूल्य] for कळ_मूल्य in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    सुरू_करा()
