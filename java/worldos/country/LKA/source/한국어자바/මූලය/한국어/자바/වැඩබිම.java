// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;

/** පරිශීලක 홈에서 Java 원문을 සකසන්න_අගය·සාදන්න_මූලය·실행하는 작은 Swing වැඩබිම. */
public final class වැඩබිම {
    private final JFrame කවුළුව = new JFrame("jkoros — 자바 වැඩබිම");
    private final JTextArea මූලය = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ගොනුව_පිවිසුම_නම = new JTextField("인사.java", 20);
    private final JTextField පන්තිය_පිවිසුම_නම = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ක්_රියාවලිය_අගය;
    private final String ලේඛාගාරය = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String පෙළ) { SwingUtilities.invokeLater(() -> 출력.append(පෙළ + "\n")); }
    private void බොත්තම(JPanel අනුවාදය_අගය, String නම, Runnable 행동) {
        JButton බොත්තම = new JButton(නම);
        බොත්තම.addActionListener(සිදුවීම -> 행동.run());
        අනුවාදය_අගය.add(බොත්තම);
    }
    private boolean ගබඩා_කරන්න_අගය() {
        try {
            Path මාර්_ගය = 작업폴더.resolve(ගොනුව_පිවිසුම_නම.getText());
            Files.createDirectories(මාර්_ගය.getParent());
            ගොනු.ලිවීම(මාර්_ගය, මූලය.getText());
            알림("ගබඩා_කරන්න_අගය: " + මාර්_ගය);
            return true;
        } catch (Exception දෝෂය) { 알림(දෝෂය.toString()); return false; }
    }
    private void විවෘත_කරන්න() {
        try { මූලය.setText(ගොනු.කියවීම(작업폴더.resolve(ගොනුව_පිවිසුම_නම.getText()))); }
        catch (Exception දෝෂය) { 알림(දෝෂය.toString()); }
    }
    private int විධානය(List<String> විධානය) throws Exception {
        ක්_රියාවලිය_අගය = new ProcessBuilder(විධානය).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader පේළිය = new BufferedReader(new InputStreamReader(ක්_රියාවලිය_අගය.getInputStream(), StandardCharsets.UTF_8))) {
            String පෙළ;
            while ((පෙළ = පේළිය.readLine()) != null) 알림(පෙළ);
        }
        int තත්වය_අගය = ක්_රියාවලිය_අගය.waitFor(); ක්_රියාවලිය_අගය = null;
        알림("පිටවීම_යෙදු 코드: " + තත්වය_අගය);
        return තත්වය_අගය;
    }
    private void පරිවර්තනය_මූලය(boolean ක්_රියාත්මක_කරන්න_විධානය, boolean 실행파일) {
        if (!ගබඩා_කරන්න_අගය()) return;
        String 입력 = ගොනුව_පිවිසුම_නම.getText(), පිවිසුම_ලකුණ_අගය = පන්තිය_පිවිසුම_නම.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    විධානය(Arrays.asList("jclassc", "--target", "openjdk", "--entry", පිවිසුම_ලකුණ_අගය,
                        "--classpath", ලේඛාගාරය, "-o", "실행프로그램", 입력));
                } else if (විධානය(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ලේඛාගාරය,
                        "-d", "classes", 입력)) == 0 && ක්_රියාත්මක_කරන්න_විධානය) {
                    විධානය(Arrays.asList("java", "-cp", "classes:" + ලේඛාගාරය, පිවිසුම_ලකුණ_අගය));
                }
            } catch (Exception දෝෂය) { 알림(දෝෂය.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ක්_රියාවලිය_අගය;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private වැඩබිම() throws IOException {
        Files.createDirectories(작업폴더);
        Font ෆොන්ටය_අගය = new Font("Monospaced", Font.PLAIN, 16);
        මූලය.setFont(ෆොන්ටය_අගය); 출력.setFont(ෆොන්ටය_අගය); 출력.setEditable(false);
        මූලය.setTabSize(4);
        මූලය.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        මූලය.setBackground(new Color(250, 251, 252));
        මූලය.setForeground(new Color(32, 43, 58));
        JPanel විධානය_පැනලය = new JPanel();
        විධානය_පැනලය.add(new JLabel("ගොනු")); විධානය_පැනලය.add(ගොනුව_පිවිසුම_නම);
        විධානය_පැනලය.add(new JLabel("주 පන්තිය_අගය")); විධානය_පැනලය.add(පන්තිය_පිවිසුම_නම);
        බොත්තම(විධානය_පැනලය, "විවෘත_කරන්න", this::විවෘත_කරන්න); බොත්තම(විධානය_පැනලය, "ගබඩා_කරන්න_අගය", this::ගබඩා_කරන්න_අගය);
        බොත්තම(විධානය_පැනලය, "සාදන්න_මූලය", () -> පරිවර්තනය_මූලය(false, false));
        බොත්තම(විධානය_පැනලය, "ක්_රියාත්මක_කරන්න_විධානය", () -> පරිවර්තනය_මූලය(true, false));
        බොත්තම(විධානය_පැනලය, "ක්_රියාත්මක_කරන්න_විධානය ගොනු සාදන්න_පිවිසුම", () -> පරිවර්තනය_මූලය(false, true));
        බොත්තම(විධානය_පැනලය, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(මූලය), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        කවුළුව.add(විධානය_පැනලය, BorderLayout.NORTH); කවුළුව.add(나눔, BorderLayout.CENTER);
        කවුළුව.setSize(1200, 750); කවුළුව.setLocationRelativeTo(null);
        කවුළුව.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        කවුළුව.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent සිදුවීම) { 멈춤(); 일꾼.shutdownNow(); }
        });
        විවෘත_කරන්න(); කවුළුව.setVisible(true);
    }
    public static void main(String[] විස්තාරක) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource පෙරනිමි_ෆොන්ටය = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object පිවිසුම_අගය : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(පිවිසුම_අගය) instanceof Font) UIManager.put(පිවිසුම_අගය, පෙරනිමි_ෆොන්ටය);
                }
                new වැඩබිම();
            } catch (Exception දෝෂය) { දෝෂය.printStackTrace(); }
        });
    }
}
