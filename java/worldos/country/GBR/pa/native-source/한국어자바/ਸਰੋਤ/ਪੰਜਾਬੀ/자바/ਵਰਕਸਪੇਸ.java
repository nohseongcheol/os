// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자바;

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

/** ਉਪਭੋਗਤਾ 홈에서 Java 원문을 ਸੰਪਾਦਨ_ਕੀਮਤ·ਬਣਾਊਣਾ_ਸਰੋਤ·실행하는 작은 Swing ਵਰਕਸਪੇਸ. */
public final class ਵਰਕਸਪੇਸ {
    private final JFrame ਵਿੰਡੋ = new JFrame("jkoros — 자바 ਵਰਕਸਪੇਸ");
    private final JTextArea ਸਰੋਤ = new JTextArea();
    private final JTextArea ਆਉਟਪੁੱਟ = new JTextArea(8, 80);
    private final JTextField ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ = new JTextField("인사.java", 20);
    private final JTextField ਸ੍ਰੇਣੀ_ਦਾਖਲਾ_ਨਾਮ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ਕਾਰਵਾਈ_ਕੀਮਤ;
    private final String ਪੁਸਤਕਾਲਾ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ਟੈਕਸਟ) { SwingUtilities.invokeLater(() -> ਆਉਟਪੁੱਟ.append(ਟੈਕਸਟ + "\n")); }
    private void ਬਟਨ(JPanel ਵਰਜ਼ਨ_ਕੀਮਤ, String ਨਾਂ, Runnable 행동) {
        JButton ਬਟਨ = new JButton(ਨਾਂ);
        ਬਟਨ.addActionListener(ਇਵੈਂਟ -> 행동.run());
        ਵਰਜ਼ਨ_ਕੀਮਤ.add(ਬਟਨ);
    }
    private boolean ਸੰਭਾਲੋ_ਕੀਮਤ() {
        try {
            Path ਮਾਰਗ = 작업폴더.resolve(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ.getText());
            Files.createDirectories(ਮਾਰਗ.getParent());
            ਫਾਇਲ.ਲਿਖਣ(ਮਾਰਗ, ਸਰੋਤ.getText());
            알림("ਸੰਭਾਲੋ_ਕੀਮਤ: " + ਮਾਰਗ);
            return true;
        } catch (Exception ਗਲਤੀ) { 알림(ਗਲਤੀ.toString()); return false; }
    }
    private void ਖੋਲ੍ਹੋ() {
        try { ਸਰੋਤ.setText(ਫਾਇਲ.ਪੜ੍ਹਨ(작업폴더.resolve(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ.getText()))); }
        catch (Exception ਗਲਤੀ) { 알림(ਗਲਤੀ.toString()); }
    }
    private int ਕਮਾਂਡ(List<String> ਕਮਾਂਡ) throws Exception {
        ਕਾਰਵਾਈ_ਕੀਮਤ = new ProcessBuilder(ਕਮਾਂਡ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ਲਾਈਨ = new BufferedReader(new InputStreamReader(ਕਾਰਵਾਈ_ਕੀਮਤ.getInputStream(), StandardCharsets.UTF_8))) {
            String ਟੈਕਸਟ;
            while ((ਟੈਕਸਟ = ਲਾਈਨ.readLine()) != null) 알림(ਟੈਕਸਟ);
        }
        int ਸਥਿਤੀ_ਕੀਮਤ = ਕਾਰਵਾਈ_ਕੀਮਤ.waitFor(); ਕਾਰਵਾਈ_ਕੀਮਤ = null;
        알림("ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼ 코드: " + ਸਥਿਤੀ_ਕੀਮਤ);
        return ਸਥਿਤੀ_ਕੀਮਤ;
    }
    private void ਅਨੁਵਾਦ_ਸਰੋਤ(boolean ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼, boolean 실행파일) {
        if (!ਸੰਭਾਲੋ_ਕੀਮਤ()) return;
        String 입력 = ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ.getText(), ਦਾਖਲਾ_ਪੌਇੰਟ_ਕੀਮਤ = ਸ੍ਰੇਣੀ_ਦਾਖਲਾ_ਨਾਮ.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ਕਮਾਂਡ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ਦਾਖਲਾ_ਪੌਇੰਟ_ਕੀਮਤ,
                        "--classpath", ਪੁਸਤਕਾਲਾ, "-o", "실행프로그램", 입력));
                } else if (ਕਮਾਂਡ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ਪੁਸਤਕਾਲਾ,
                        "-d", "classes", 입력)) == 0 && ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼) {
                    ਕਮਾਂਡ(Arrays.asList("java", "-cp", "classes:" + ਪੁਸਤਕਾਲਾ, ਦਾਖਲਾ_ਪੌਇੰਟ_ਕੀਮਤ));
                }
            } catch (Exception ਗਲਤੀ) { 알림(ਗਲਤੀ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ਕਾਰਵਾਈ_ਕੀਮਤ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ਵਰਕਸਪੇਸ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ਫੌਂਟ_ਕੀਮਤ = new Font("Monospaced", Font.PLAIN, 16);
        ਸਰੋਤ.setFont(ਫੌਂਟ_ਕੀਮਤ); ਆਉਟਪੁੱਟ.setFont(ਫੌਂਟ_ਕੀਮਤ); ਆਉਟਪੁੱਟ.setEditable(false);
        ਸਰੋਤ.setTabSize(4);
        ਸਰੋਤ.setMargin(new Insets(10, 12, 10, 12));
        ਆਉਟਪੁੱਟ.setMargin(new Insets(8, 12, 8, 12));
        ਸਰੋਤ.setBackground(new Color(250, 251, 252));
        ਸਰੋਤ.setForeground(new Color(32, 43, 58));
        JPanel ਆਦੇਸ਼_ਪੈਨਲ = new JPanel();
        ਆਦੇਸ਼_ਪੈਨਲ.add(new JLabel("ਫਾਇਲ")); ਆਦੇਸ਼_ਪੈਨਲ.add(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ);
        ਆਦੇਸ਼_ਪੈਨਲ.add(new JLabel("주 ਸ੍ਰੇਣੀ_ਕੀਮਤ")); ਆਦੇਸ਼_ਪੈਨਲ.add(ਸ੍ਰੇਣੀ_ਦਾਖਲਾ_ਨਾਮ);
        ਬਟਨ(ਆਦੇਸ਼_ਪੈਨਲ, "ਖੋਲ੍ਹੋ", this::ਖੋਲ੍ਹੋ); ਬਟਨ(ਆਦੇਸ਼_ਪੈਨਲ, "ਸੰਭਾਲੋ_ਕੀਮਤ", this::ਸੰਭਾਲੋ_ਕੀਮਤ);
        ਬਟਨ(ਆਦੇਸ਼_ਪੈਨਲ, "ਬਣਾਊਣਾ_ਸਰੋਤ", () -> ਅਨੁਵਾਦ_ਸਰੋਤ(false, false));
        ਬਟਨ(ਆਦੇਸ਼_ਪੈਨਲ, "ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼", () -> ਅਨੁਵਾਦ_ਸਰੋਤ(true, false));
        ਬਟਨ(ਆਦੇਸ਼_ਪੈਨਲ, "ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ ਫਾਇਲ ਬਣਾਓ_ਦਾਖਲਾ", () -> ਅਨੁਵਾਦ_ਸਰੋਤ(false, true));
        ਬਟਨ(ਆਦੇਸ਼_ਪੈਨਲ, "멈춤", this::멈춤);
        JSplitPane ਤਕਸੀਮ_ਮਾਪ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ਸਰੋਤ), new JScrollPane(ਆਉਟਪੁੱਟ));
        ਤਕਸੀਮ_ਮਾਪ.setResizeWeight(0.75);
        ਵਿੰਡੋ.add(ਆਦੇਸ਼_ਪੈਨਲ, BorderLayout.NORTH); ਵਿੰਡੋ.add(ਤਕਸੀਮ_ਮਾਪ, BorderLayout.CENTER);
        ਵਿੰਡੋ.setSize(1200, 750); ਵਿੰਡੋ.setLocationRelativeTo(null);
        ਵਿੰਡੋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ਵਿੰਡੋ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ਇਵੈਂਟ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ਖੋਲ੍ਹੋ(); ਵਿੰਡੋ.setVisible(true);
    }
    public static void main(String[] ਆਰਗੂਮੈਂਟ) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ਡਿਫੌਲਟ_ਫੌਂਟ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ਦਾਖਲਾ_ਕੀਮਤ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ਦਾਖਲਾ_ਕੀਮਤ) instanceof Font) UIManager.put(ਦਾਖਲਾ_ਕੀਮਤ, ਡਿਫੌਲਟ_ਫੌਂਟ);
                }
                new ਵਰਕਸਪੇਸ();
            } catch (Exception ਗਲਤੀ) { ਗਲਤੀ.printStackTrace(); }
        });
    }
}
