// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.자바;

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

/** प्रयोगकर्ता 홈에서 Java 원문을 सम्पादन_गर्नुहोस्_मान·बनाउनुहोस्_स्रोत·실행하는 작은 Swing कार्यस्थल. */
public final class कार्यस्थल {
    private final JFrame सन्झ्याल = new JFrame("jkoros — 자바 कार्यस्थल");
    private final JTextArea स्रोत = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField फाइल_प्रविष्टि_नाम = new JTextField("인사.java", 20);
    private final JTextField वर्ग_प्रविष्टि_नाम = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया_मान;
    private final String पुस्तकालय = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String पाठ) { SwingUtilities.invokeLater(() -> 출력.append(पाठ + "\n")); }
    private void बटन(JPanel संस्करण_मान, String नाम, Runnable 행동) {
        JButton बटन = new JButton(नाम);
        बटन.addActionListener(घटना -> 행동.run());
        संस्करण_मान.add(बटन);
    }
    private boolean भण्डार_गर्नुहोस्_मान() {
        try {
            Path मार्ग = 작업폴더.resolve(फाइल_प्रविष्टि_नाम.getText());
            Files.createDirectories(मार्ग.getParent());
            फाइल.लेख्नुहोस्(मार्ग, स्रोत.getText());
            알림("भण्डार_गर्नुहोस्_मान: " + मार्ग);
            return true;
        } catch (Exception त्रुटि) { 알림(त्रुटि.toString()); return false; }
    }
    private void खोल्नुहोस्() {
        try { स्रोत.setText(फाइल.पढनुहोस्(작업폴더.resolve(फाइल_प्रविष्टि_नाम.getText()))); }
        catch (Exception त्रुटि) { 알림(त्रुटि.toString()); }
    }
    private int आदेश(List<String> आदेश) throws Exception {
        प्रक्रिया_मान = new ProcessBuilder(आदेश).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader रेखा = new BufferedReader(new InputStreamReader(प्रक्रिया_मान.getInputStream(), StandardCharsets.UTF_8))) {
            String पाठ;
            while ((पाठ = रेखा.readLine()) != null) 알림(पाठ);
        }
        int स्थिति_मान = प्रक्रिया_मान.waitFor(); प्रक्रिया_मान = null;
        알림("बाहिर_जानुहोस्_अनुप्रयोग 코드: " + स्थिति_मान);
        return स्थिति_मान;
    }
    private void अनुवाद_स्रोत(boolean कार्यान्वयन_गर्नुहोस्_आदेश, boolean 실행파일) {
        if (!भण्डार_गर्नुहोस्_मान()) return;
        String 입력 = फाइल_प्रविष्टि_नाम.getText(), प्रविष्टि_अंक_मान = वर्ग_प्रविष्टि_नाम.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    आदेश(Arrays.asList("jclassc", "--target", "openjdk", "--entry", प्रविष्टि_अंक_मान,
                        "--classpath", पुस्तकालय, "-o", "실행프로그램", 입력));
                } else if (आदेश(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", पुस्तकालय,
                        "-d", "classes", 입력)) == 0 && कार्यान्वयन_गर्नुहोस्_आदेश) {
                    आदेश(Arrays.asList("java", "-cp", "classes:" + पुस्तकालय, प्रविष्टि_अंक_मान));
                }
            } catch (Exception त्रुटि) { 알림(त्रुटि.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = प्रक्रिया_मान;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private कार्यस्थल() throws IOException {
        Files.createDirectories(작업폴더);
        Font फन्ट_मान = new Font("Monospaced", Font.PLAIN, 16);
        स्रोत.setFont(फन्ट_मान); 출력.setFont(फन्ट_मान); 출력.setEditable(false);
        स्रोत.setTabSize(4);
        स्रोत.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        स्रोत.setBackground(new Color(250, 251, 252));
        स्रोत.setForeground(new Color(32, 43, 58));
        JPanel आदेश_प्यानल = new JPanel();
        आदेश_प्यानल.add(new JLabel("फाइल")); आदेश_प्यानल.add(फाइल_प्रविष्टि_नाम);
        आदेश_प्यानल.add(new JLabel("주 वर्ग_मान")); आदेश_प्यानल.add(वर्ग_प्रविष्टि_नाम);
        बटन(आदेश_प्यानल, "खोल्नुहोस्", this::खोल्नुहोस्); बटन(आदेश_प्यानल, "भण्डार_गर्नुहोस्_मान", this::भण्डार_गर्नुहोस्_मान);
        बटन(आदेश_प्यानल, "बनाउनुहोस्_स्रोत", () -> अनुवाद_स्रोत(false, false));
        बटन(आदेश_प्यानल, "कार्यान्वयन_गर्नुहोस्_आदेश", () -> अनुवाद_स्रोत(true, false));
        बटन(आदेश_प्यानल, "कार्यान्वयन_गर्नुहोस्_आदेश फाइल सिर्जना_प्रविष्टि", () -> अनुवाद_स्रोत(false, true));
        बटन(आदेश_प्यानल, "멈춤", this::멈춤);
        JSplitPane विभाग_मापन = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्रोत), new JScrollPane(출력));
        विभाग_मापन.setResizeWeight(0.75);
        सन्झ्याल.add(आदेश_प्यानल, BorderLayout.NORTH); सन्झ्याल.add(विभाग_मापन, BorderLayout.CENTER);
        सन्झ्याल.setSize(1200, 750); सन्झ्याल.setLocationRelativeTo(null);
        सन्झ्याल.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        सन्झ्याल.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent घटना) { 멈춤(); 일꾼.shutdownNow(); }
        });
        खोल्नुहोस्(); सन्झ्याल.setVisible(true);
    }
    public static void main(String[] तर्क) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource पूर्वनिर्धारित_फन्ट = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object प्रविष्टि_मान : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(प्रविष्टि_मान) instanceof Font) UIManager.put(प्रविष्टि_मान, पूर्वनिर्धारित_फन्ट);
                }
                new कार्यस्थल();
            } catch (Exception त्रुटि) { त्रुटि.printStackTrace(); }
        });
    }
}
