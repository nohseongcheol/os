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
public class ThửXâyDựngBảnĐịa {
    public static void main(String[] cácĐốiSố) throws Exception {
        Path TàiLiệu = Files.createTempFile("한글-", ".txt");
        Files.writeString(TàiLiệu, "안녕하세요 😀", StandardCharsets.UTF_8);
        if (!Files.readString(TàiLiệu).equals("안녕하세요 😀")) throw new AssertionError("file");
        Files.delete(TàiLiệu);
        long trịSố = 0x123456789abcdef0L;
        if (Long.reverseBytes(Long.reverseBytes(trịSố)) != trịSố || Math.sqrt(81.0) != 9.0)
            throw new AssertionError("numeric");
        try (ServerSocket giáTrịMáyChủ = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Throwable[] lỗi = new Throwable[1];
            Thread TácVụ = new Thread(() -> {
                try (Socket nốiKết = new Socket(InetAddress.getLoopbackAddress(), giáTrịMáyChủ.getLocalPort())) {
                    new DataOutputStream(nốiKết.getOutputStream()).writeUTF("한글 giáTrịỔCắmMạng");
                } catch (Throwable e) { lỗi[0] = e; }
            });
            giáTrịMáyChủ.setSoTimeout(10000); TácVụ.start();
            try (Socket kếtNốiĐãChấpNhận = giáTrịMáyChủ.accept()) {
                kếtNốiĐãChấpNhận.setSoTimeout(10000);
                if (!new DataInputStream(kếtNốiĐãChấpNhận.getInputStream()).readUTF().equals("한글 giáTrịỔCắmMạng"))
                    throw new AssertionError("socket");
            }
            TácVụ.join(10000);
            if (TácVụ.isAlive() || lỗi[0] != null) throw new AssertionError("thread", lỗi[0]);
        }
        SwingUtilities.invokeAndWait(() -> {
            boolean[] làĐãNhấn = {false};
            JButton nút = new JButton("한글 nút");
            nút.addActionListener(e -> làĐãNhấn[0] = true); nút.doClick();
            if (!làĐãNhấn[0] || !SwingUtilities.isEventDispatchThread()) throw new AssertionError("Swing");
            if (cácĐốiSố.length != 0) {
                JFrame cửaSổ = new JFrame("OpenJDK tựThân xâyDựngHệThống KiểmThử");
                cửaSổ.add(nút); cửaSổ.pack(); cửaSổ.setVisible(true); cửaSổ.dispose();
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
        source = out / 'ThửXâyDựngBảnĐịa.java'; source.write_text(SOURCE, encoding='utf-8')
        subprocess.check_call([str(jdk / 'bin/javac'), '-encoding', 'UTF-8', '-d', str(out), str(source)], timeout=60)
        cmd = [str(jdk / 'bin/java'), '-Xverify:all', '-Djava.awt.headless=' + ('false' if args.window else 'true'), '-cp', str(out), 'ThửXâyDựngBảnĐịa']
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
