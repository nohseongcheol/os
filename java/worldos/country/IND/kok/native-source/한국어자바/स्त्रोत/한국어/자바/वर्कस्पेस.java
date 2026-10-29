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

/** उपेगकर्तो 홈에서 Java 원문을 संपादन_करचें_मोल·दाळचे_स्त्रोत·실행하는 작은 Swing वर्कस्पेस. */
public final class वर्कस्पेस {
    private final JFrame विंडो = new JFrame("jkoros — 자바 वर्कस्पेस");
    private final JTextArea स्त्रोत = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField फायल_प्रवेश_नांव = new JTextField("인사.java", 20);
    private final JTextField वर्ग_प्रवेश_नांव = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया_मोल;
    private final String लायब्ररी = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void बटन(JPanel वर्जन_मोल, String नांव, Runnable 행동) {
        JButton बटन = new JButton(नांव);
        बटन.addActionListener(प्रसंग -> 행동.run());
        वर्जन_मोल.add(बटन);
    }
    private boolean Store_मोल() {
        try {
            Path पाथ = 작업폴더.resolve(फायल_प्रवेश_नांव.getText());
            Files.createDirectories(पाथ.getParent());
            फायल.बरोवचें(पाथ, स्त्रोत.getText());
            알림("Store_मोल: " + पाथ);
            return true;
        } catch (Exception चूक) { 알림(चूक.toString()); return false; }
    }
    private void उगडचें() {
        try { स्त्रोत.setText(फायल.읽기(작업폴더.resolve(फायल_प्रवेश_नांव.getText()))); }
        catch (Exception चूक) { 알림(चूक.toString()); }
    }
    private int आदेश(List<String> आदेश) throws Exception {
        प्रक्रिया_मोल = new ProcessBuilder(आदेश).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader रेग = new BufferedReader(new InputStreamReader(प्रक्रिया_मोल.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = रेग.readLine()) != null) 알림(SMS);
        }
        int स्थिती_मोल_e10195a1 = प्रक्रिया_मोल.waitFor(); प्रक्रिया_मोल = null;
        알림("प्रस्थान_करचें_एप्लिकेशन CODE_मोल: " + स्थिती_मोल_e10195a1);
        return स्थिती_मोल_e10195a1;
    }
    private void अणकारप_स्त्रोत(boolean पाळो_दिवचो_आदेश, boolean 실행파일) {
        if (!Store_मोल()) return;
        String 입력 = फायल_प्रवेश_नांव.getText(), प्रवेश_पॉयंट_मोल = वर्ग_प्रवेश_नांव.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    आदेश(Arrays.asList("jclassc", "--target", "openjdk", "--entry", प्रवेश_पॉयंट_मोल,
                        "--classpath", लायब्ररी, "-o", "실행프로그램", 입력));
                } else if (आदेश(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", लायब्ररी,
                        "-d", "classes", 입력)) == 0 && पाळो_दिवचो_आदेश) {
                    आदेश(Arrays.asList("java", "-cp", "classes:" + लायब्ररी, प्रवेश_पॉयंट_मोल));
                }
            } catch (Exception चूक) { 알림(चूक.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = प्रक्रिया_मोल;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private वर्कस्पेस() throws IOException {
        Files.createDirectories(작업폴더);
        Font फाँट_मोल = new Font("Monospaced", Font.PLAIN, 16);
        स्त्रोत.setFont(फाँट_मोल); 출력.setFont(फाँट_मोल); 출력.setEditable(false);
        स्त्रोत.setTabSize(4);
        स्त्रोत.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        स्त्रोत.setBackground(new Color(250, 251, 252));
        स्त्रोत.setForeground(new Color(32, 43, 58));
        JPanel आदेश_कक्ष = new JPanel();
        आदेश_कक्ष.add(new JLabel("फायल")); आदेश_कक्ष.add(फायल_प्रवेश_नांव);
        आदेश_कक्ष.add(new JLabel("주 वर्ग_मोल_55654bf1")); आदेश_कक्ष.add(वर्ग_प्रवेश_नांव);
        बटन(आदेश_कक्ष, "उगडचें", this::उगडचें); बटन(आदेश_कक्ष, "Store_मोल", this::Store_मोल);
        बटन(आदेश_कक्ष, "दाळचे_स्त्रोत", () -> अणकारप_स्त्रोत(false, false));
        बटन(आदेश_कक्ष, "पाळो_दिवचो_आदेश", () -> अणकारप_स्त्रोत(true, false));
        बटन(आदेश_कक्ष, "पाळो_दिवचो_आदेश फायल निर्माण_करचें_प्रवेश", () -> अणकारप_स्त्रोत(false, true));
        बटन(आदेश_कक्ष, "멈춤", this::멈춤);
        JSplitPane भागाकार_मेजप = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्त्रोत), new JScrollPane(출력));
        भागाकार_मेजप.setResizeWeight(0.75);
        विंडो.add(आदेश_कक्ष, BorderLayout.NORTH); विंडो.add(भागाकार_मेजप, BorderLayout.CENTER);
        विंडो.setSize(1200, 750); विंडो.setLocationRelativeTo(null);
        विंडो.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        विंडो.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent प्रसंग) { 멈춤(); 일꾼.shutdownNow(); }
        });
        उगडचें(); विंडो.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource डिफॉल्ट_फाँट = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object प्रवेश_मोल : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(प्रवेश_मोल) instanceof Font) UIManager.put(प्रवेश_मोल, डिफॉल्ट_फाँट);
                }
                new वर्कस्पेस();
            } catch (Exception चूक) { चूक.printStackTrace(); }
        });
    }
}
