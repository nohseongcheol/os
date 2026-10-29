// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.자바;

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

/** उपयोगकर्ता 홈에서 Java 원문을 संपादन_मान·कंपाइल_स्रोत·실행하는 작은 Swing कार्यस्थान. */
public final class कार्यस्थान {
    private final JFrame खिड़की = new JFrame("jkoros — 자바 कार्यस्थान");
    private final JTextArea स्रोत = new JTextArea();
    private final JTextArea निर्गम = new JTextArea(8, 80);
    private final JTextField फ़ाइल_एन्ट्री_नाम = new JTextField("अभिनन्दन_ae353e94.java", 20);
    private final JTextField कक्षा_एन्ट्री_नाम = new JTextField("अभिनन्दन_ae353e94", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया_मान;
    private final String लाइब्रेरी = "/opt/jkoros/lib/한국어자바.jar";

    private void सूचना(String पाठ) { SwingUtilities.invokeLater(() -> निर्गम.append(पाठ + "\n")); }
    private void बटन(JPanel संस्करण_मान, String नाम, Runnable 행동) {
        JButton बटन = new JButton(नाम);
        बटन.addActionListener(घटना -> 행동.run());
        संस्करण_मान.add(बटन);
    }
    private boolean स्टोर_मान() {
        try {
            Path पथ = 작업폴더.resolve(फ़ाइल_एन्ट्री_नाम.getText());
            Files.createDirectories(पथ.getParent());
            संचिका.लिखें(पथ, स्रोत.getText());
            सूचना("स्टोर_मान: " + पथ);
            return true;
        } catch (Exception त्रुटि) { सूचना(त्रुटि.toString()); return false; }
    }
    private void खोलें() {
        try { स्रोत.setText(संचिका.पढ़ें(작업폴더.resolve(फ़ाइल_एन्ट्री_नाम.getText()))); }
        catch (Exception त्रुटि) { सूचना(त्रुटि.toString()); }
    }
    private int आदेश(List<String> आदेश) throws Exception {
        प्रक्रिया_मान = new ProcessBuilder(आदेश).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader पंक्ति = new BufferedReader(new InputStreamReader(प्रक्रिया_मान.getInputStream(), StandardCharsets.UTF_8))) {
            String पाठ;
            while ((पाठ = पंक्ति.readLine()) != null) सूचना(पाठ);
        }
        int अवस्था_मान = प्रक्रिया_मान.waitFor(); प्रक्रिया_मान = null;
        सूचना("निर्गमन_ऐप कोड_मान: " + अवस्था_मान);
        return अवस्था_मान;
    }
    private void अनुवाद_स्रोत(boolean निष्पादित_करें_आदेश, boolean निष्पादन_योग्य_फ़ाइल) {
        if (!स्टोर_मान()) return;
        String 입력 = फ़ाइल_एन्ट्री_नाम.getText(), प्रवेश_बिदुं_मान = कक्षा_एन्ट्री_नाम.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (निष्पादन_योग्य_फ़ाइल) {
                    आदेश(Arrays.asList("jclassc", "--target", "openjdk", "--entry", प्रवेश_बिदुं_मान,
                        "--classpath", लाइब्रेरी, "-o", "실행프로그램", 입력));
                } else if (आदेश(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", लाइब्रेरी,
                        "-d", "classes", 입력)) == 0 && निष्पादित_करें_आदेश) {
                    आदेश(Arrays.asList("java", "-cp", "classes:" + लाइब्रेरी, प्रवेश_बिदुं_मान));
                }
            } catch (Exception त्रुटि) { सूचना(त्रुटि.toString()); }
        });
    }
    private void 멈춤() {
        Process अद्यतित_आइटम = प्रक्रिया_मान;
        if (अद्यतित_आइटम != null) { अद्यतित_आइटम.descendants().forEach(ProcessHandle::destroy); अद्यतित_आइटम.destroy(); }
    }
    private कार्यस्थान() throws IOException {
        Files.createDirectories(작업폴더);
        Font फ़ॉन्ट_मान = new Font("Monospaced", Font.PLAIN, 16);
        स्रोत.setFont(फ़ॉन्ट_मान); निर्गम.setFont(फ़ॉन्ट_मान); निर्गम.setEditable(false);
        स्रोत.setTabSize(4);
        स्रोत.setMargin(new Insets(10, 12, 10, 12));
        निर्गम.setMargin(new Insets(8, 12, 8, 12));
        स्रोत.setBackground(new Color(250, 251, 252));
        स्रोत.setForeground(new Color(32, 43, 58));
        JPanel आदेश_पैनल = new JPanel();
        आदेश_पैनल.add(new JLabel("संचिका")); आदेश_पैनल.add(फ़ाइल_एन्ट्री_नाम);
        आदेश_पैनल.add(new JLabel("주 कक्षा_मान")); आदेश_पैनल.add(कक्षा_एन्ट्री_नाम);
        बटन(आदेश_पैनल, "खोलें", this::खोलें); बटन(आदेश_पैनल, "स्टोर_मान", this::स्टोर_मान);
        बटन(आदेश_पैनल, "कंपाइल_स्रोत", () -> अनुवाद_स्रोत(false, false));
        बटन(आदेश_पैनल, "निष्पादित_करें_आदेश", () -> अनुवाद_स्रोत(true, false));
        बटन(आदेश_पैनल, "निष्पादित_करें_आदेश संचिका बनाएँ_एन्ट्री", () -> अनुवाद_स्रोत(false, true));
        बटन(आदेश_पैनल, "멈춤", this::멈춤);
        JSplitPane विभाग_परिणाम = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्रोत), new JScrollPane(निर्गम));
        विभाग_परिणाम.setResizeWeight(0.75);
        खिड़की.add(आदेश_पैनल, BorderLayout.NORTH); खिड़की.add(विभाग_परिणाम, BorderLayout.CENTER);
        खिड़की.setSize(1200, 750); खिड़की.setLocationRelativeTo(null);
        खिड़की.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        खिड़की.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent घटना) { 멈춤(); 일꾼.shutdownNow(); }
        });
        खोलें(); खिड़की.setVisible(true);
    }
    public static void main(String[] तर्क) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource डिफ़ॉल्ट_फ़ॉन्ट = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object एन्ट्री_मान : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(एन्ट्री_मान) instanceof Font) UIManager.put(एन्ट्री_मान, डिफ़ॉल्ट_फ़ॉन्ट);
                }
                new कार्यस्थान();
            } catch (Exception त्रुटि) { त्रुटि.printStackTrace(); }
        });
    }
}
