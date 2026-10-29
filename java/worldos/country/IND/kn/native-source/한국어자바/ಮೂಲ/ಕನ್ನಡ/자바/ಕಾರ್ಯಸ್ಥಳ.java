// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자바;

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

/** ಬಳಕೆದಾರ 홈에서 Java 원문을 ಸಂಪಾದನೆ_ಮೌಲ್ಯ·ಸಂಕಲಿಸು_ಮೂಲ·실행하는 작은 Swing ಕಾರ್ಯಸ್ಥಳ. */
public final class ಕಾರ್ಯಸ್ಥಳ {
    private final JFrame ವಿಂಡೋ = new JFrame("jkoros — 자바 ಕಾರ್ಯಸ್ಥಳ");
    private final JTextArea ಮೂಲ = new JTextArea();
    private final JTextArea ಔಟ್_ಪುಟ್ = new JTextArea(8, 80);
    private final JTextField ಫೈಲ್_ನಮೂದು_ಹೆಸರು = new JTextField("인사.java", 20);
    private final JTextField ವರ್ಗ_ನಮೂದು_ಹೆಸರು = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ;
    private final String ಲೈಬ್ರರಿ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ಪಠ್ಯ) { SwingUtilities.invokeLater(() -> ಔಟ್_ಪುಟ್.append(ಪಠ್ಯ + "\n")); }
    private void ಬಟನ್(JPanel ಆವೃತ್ತಿ_ಮೌಲ್ಯ, String ಹೆಸರು, Runnable 행동) {
        JButton ಬಟನ್ = new JButton(ಹೆಸರು);
        ಬಟನ್.addActionListener(ಸಂಗತಿ -> 행동.run());
        ಆವೃತ್ತಿ_ಮೌಲ್ಯ.add(ಬಟನ್);
    }
    private boolean ಸ್ಟೋರ್_ಮೌಲ್ಯ() {
        try {
            Path ಮಾರ್ಗ = 작업폴더.resolve(ಫೈಲ್_ನಮೂದು_ಹೆಸರು.getText());
            Files.createDirectories(ಮಾರ್ಗ.getParent());
            ಕಡತ.ಬರೆ(ಮಾರ್ಗ, ಮೂಲ.getText());
            알림("ಸ್ಟೋರ್_ಮೌಲ್ಯ: " + ಮಾರ್ಗ);
            return true;
        } catch (Exception ದೋಷ) { 알림(ದೋಷ.toString()); return false; }
    }
    private void ತೆರೆ() {
        try { ಮೂಲ.setText(ಕಡತ.ಓದು(작업폴더.resolve(ಫೈಲ್_ನಮೂದು_ಹೆಸರು.getText()))); }
        catch (Exception ದೋಷ) { 알림(ದೋಷ.toString()); }
    }
    private int ಆಜ್ಞೆ(List<String> ಆಜ್ಞೆ) throws Exception {
        ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = new ProcessBuilder(ಆಜ್ಞೆ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ಸಾಲು = new BufferedReader(new InputStreamReader(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.getInputStream(), StandardCharsets.UTF_8))) {
            String ಪಠ್ಯ;
            while ((ಪಠ್ಯ = ಸಾಲು.readLine()) != null) 알림(ಪಠ್ಯ);
        }
        int ಸ್ಥಿತಿ_ಮೌಲ್ಯ = ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.waitFor(); ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = null;
        알림("ನಿರ್ಗಮನ_ಅಪ್ಲಿ ಕೋಡ್_ಮೌಲ್ಯ: " + ಸ್ಥಿತಿ_ಮೌಲ್ಯ);
        return ಸ್ಥಿತಿ_ಮೌಲ್ಯ;
    }
    private void ಅನುವಾದಿಸು_ಮೂಲ(boolean ಪೂರೈಸು_ಆದೇಶ, boolean 실행파일) {
        if (!ಸ್ಟೋರ್_ಮೌಲ್ಯ()) return;
        String 입력 = ಫೈಲ್_ನಮೂದು_ಹೆಸರು.getText(), ನಮೂದು_ಬಿಂದು_ಮೌಲ್ಯ = ವರ್ಗ_ನಮೂದು_ಹೆಸರು.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ಆಜ್ಞೆ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ನಮೂದು_ಬಿಂದು_ಮೌಲ್ಯ,
                        "--classpath", ಲೈಬ್ರರಿ, "-o", "실행프로그램", 입력));
                } else if (ಆಜ್ಞೆ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ಲೈಬ್ರರಿ,
                        "-d", "classes", 입력)) == 0 && ಪೂರೈಸು_ಆದೇಶ) {
                    ಆಜ್ಞೆ(Arrays.asList("java", "-cp", "classes:" + ಲೈಬ್ರರಿ, ನಮೂದು_ಬಿಂದು_ಮೌಲ್ಯ));
                }
            } catch (Exception ದೋಷ) { 알림(ದೋಷ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ಕಾರ್ಯಸ್ಥಳ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ಫಾಂಟ್_ಮೌಲ್ಯ = new Font("Monospaced", Font.PLAIN, 16);
        ಮೂಲ.setFont(ಫಾಂಟ್_ಮೌಲ್ಯ); ಔಟ್_ಪುಟ್.setFont(ಫಾಂಟ್_ಮೌಲ್ಯ); ಔಟ್_ಪುಟ್.setEditable(false);
        ಮೂಲ.setTabSize(4);
        ಮೂಲ.setMargin(new Insets(10, 12, 10, 12));
        ಔಟ್_ಪುಟ್.setMargin(new Insets(8, 12, 8, 12));
        ಮೂಲ.setBackground(new Color(250, 251, 252));
        ಮೂಲ.setForeground(new Color(32, 43, 58));
        JPanel ಆದೇಶ_ಪ್ಯಾನಲ್ = new JPanel();
        ಆದೇಶ_ಪ್ಯಾನಲ್.add(new JLabel("ಕಡತ")); ಆದೇಶ_ಪ್ಯಾನಲ್.add(ಫೈಲ್_ನಮೂದು_ಹೆಸರು);
        ಆದೇಶ_ಪ್ಯಾನಲ್.add(new JLabel("주 ವರ್ಗ_ಮೌಲ್ಯ_55654bf1")); ಆದೇಶ_ಪ್ಯಾನಲ್.add(ವರ್ಗ_ನಮೂದು_ಹೆಸರು);
        ಬಟನ್(ಆದೇಶ_ಪ್ಯಾನಲ್, "ತೆರೆ", this::ತೆರೆ); ಬಟನ್(ಆದೇಶ_ಪ್ಯಾನಲ್, "ಸ್ಟೋರ್_ಮೌಲ್ಯ", this::ಸ್ಟೋರ್_ಮೌಲ್ಯ);
        ಬಟನ್(ಆದೇಶ_ಪ್ಯಾನಲ್, "ಸಂಕಲಿಸು_ಮೂಲ", () -> ಅನುವಾದಿಸು_ಮೂಲ(false, false));
        ಬಟನ್(ಆದೇಶ_ಪ್ಯಾನಲ್, "ಪೂರೈಸು_ಆದೇಶ", () -> ಅನುವಾದಿಸು_ಮೂಲ(true, false));
        ಬಟನ್(ಆದೇಶ_ಪ್ಯಾನಲ್, "ಪೂರೈಸು_ಆದೇಶ ಕಡತ ರಚಿಸು_ನಮೂದು", () -> ಅನುವಾದಿಸು_ಮೂಲ(false, true));
        ಬಟನ್(ಆದೇಶ_ಪ್ಯಾನಲ್, "멈춤", this::멈춤);
        JSplitPane ಭಾಗಾಕಾರ_ಮಾಪನ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ಮೂಲ), new JScrollPane(ಔಟ್_ಪುಟ್));
        ಭಾಗಾಕಾರ_ಮಾಪನ.setResizeWeight(0.75);
        ವಿಂಡೋ.add(ಆದೇಶ_ಪ್ಯಾನಲ್, BorderLayout.NORTH); ವಿಂಡೋ.add(ಭಾಗಾಕಾರ_ಮಾಪನ, BorderLayout.CENTER);
        ವಿಂಡೋ.setSize(1200, 750); ವಿಂಡೋ.setLocationRelativeTo(null);
        ವಿಂಡೋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ವಿಂಡೋ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ಸಂಗತಿ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ತೆರೆ(); ವಿಂಡೋ.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ಡೀಫಾಲ್ಟ್_ಫಾಂಟ್ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ನಮೂದು_ಮೌಲ್ಯ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ನಮೂದು_ಮೌಲ್ಯ) instanceof Font) UIManager.put(ನಮೂದು_ಮೌಲ್ಯ, ಡೀಫಾಲ್ಟ್_ಫಾಂಟ್);
                }
                new ಕಾರ್ಯಸ್ಥಳ();
            } catch (Exception ದೋಷ) { ದೋಷ.printStackTrace(); }
        });
    }
}
