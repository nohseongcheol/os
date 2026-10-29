#!/usr/bin/env python3
"""Execute a source-built host JDK; this is deliberately not a native-kernel test."""
import argparse
import json
from pathlib import Path
import subprocess
from openjdk_probe import digest

SOURCE = r'''
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.net.*;
import java.io.*;
import javax.swing.*;
public class स्वकीय_बांधणी_चाचणी {
    public static void main(String[] बाबी) throws Exception {
        Path मार्गदर्शिका = Files.createTempFile("한글-", ".txt");
        Files.writeString(मार्गदर्शिका, "안녕하세요 😀", StandardCharsets.UTF_8);
        if (!Files.readString(मार्गदर्शिका).equals("안녕하세요 😀")) throw new AssertionError("file");
        Files.delete(मार्गदर्शिका);
        long संख्या = 0x123456789abcdef0L;
        if (Long.reverseBytes(Long.reverseBytes(संख्या)) != संख्या || Math.sqrt(81.0) != 9.0)
            throw new AssertionError("numeric");
        try (ServerSocket सर्व्हर_मूल्य = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Throwable[] त्रुटी = new Throwable[1];
            Thread पारपाडा_कार्य = new Thread(() -> {
                try (Socket जोडा = new Socket(InetAddress.getLoopbackAddress(), सर्व्हर_मूल्य.getLocalPort())) {
                    new DataOutputStream(जोडा.getOutputStream()).writeUTF("한글 संचारद्वार_मूल्य");
                } catch (Throwable e) { त्रुटी[0] = e; }
            });
            सर्व्हर_मूल्य.setSoTimeout(10000); पारपाडा_कार्य.start();
            try (Socket स्वीकारलेले_कनेक्शन = सर्व्हर_मूल्य.accept()) {
                स्वीकारलेले_कनेक्शन.setSoTimeout(10000);
                if (!new DataInputStream(स्वीकारलेले_कनेक्शन.getInputStream()).readUTF().equals("한글 संचारद्वार_मूल्य"))
                    throw new AssertionError("socket");
            }
            पारपाडा_कार्य.join(10000);
            if (पारपाडा_कार्य.isAlive() || त्रुटी[0] != null) throw new AssertionError("thread", त्रुटी[0]);
        }
        SwingUtilities.invokeAndWait(() -> {
            boolean[] आहे_दाबलेले = {false};
            JButton बटण = new JButton("한글 बटण");
            बटण.addActionListener(e -> आहे_दाबलेले[0] = true); बटण.doClick();
            if (!आहे_दाबलेले[0] || !SwingUtilities.isEventDispatchThread()) throw new AssertionError("Swing");
            if (बाबी.length != 0) {
                JFrame विंडो = new JFrame("OpenJDK स्वकीय सिस्टम_बांधणी चाचण्या");
                विंडो.add(बटण); विंडो.pack(); विंडो.setVisible(true); विंडो.dispose();
            }
        });
        System.out.println("OpenJDK SOURCE SMOKE PASS");
    }
}
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jdk', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--window', action='store_true', help='Also create a JFrame; requires DISPLAY')
    args = p.parse_args(); jdk = args.jdk.resolve(); out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    report = {'passed': False, 'executed_on': 'build host Linux', 'own_kernel_tested': False,
              'jdk': str(jdk), 'window_tested': args.window,
              'java_sha256': digest(jdk / 'bin/java'), 'libjvm_sha256': digest(jdk / 'lib/server/libjvm.so')}
    path = out / 'report.json'; path.write_text(json.dumps(report, indent=2) + '\n')
    try:
        report['java_version'] = subprocess.check_output([str(jdk / 'bin/java'), '-version'], stderr=subprocess.STDOUT, timeout=30).decode()
        report['javac_version'] = subprocess.check_output([str(jdk / 'bin/javac'), '-version'], stderr=subprocess.STDOUT, timeout=30).decode()
        source = out / 'स्वकीय_बांधणी_चाचणी.java'; source.write_text(SOURCE, encoding='utf-8')
        subprocess.check_call([str(jdk / 'bin/javac'), '-encoding', 'UTF-8', '-d', str(out), str(source)], timeout=60)
        cmd = [str(jdk / 'bin/java'), '-Xverify:all', '-Djava.awt.headless=' + ('false' if args.window else 'true'), '-cp', str(out), 'स्वकीय_बांधणी_चाचणी']
        if args.window: cmd += ['window']
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=60).decode()
        (out / 'program.log').write_text(result)
        if 'OpenJDK SOURCE SMOKE PASS' not in result: raise RuntimeError(result)
        report.update(passed=True, checks=['source-built java and javac execute', 'long/double and standard library',
            'Unicode file IO', 'native Java Thread plus Linux loopback TCP', 'Swing EDT and ActionListener'])
        if args.window: report['checks'].append('headful JFrame create/show/dispose')
        print(result.strip())
    finally:
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': main()
