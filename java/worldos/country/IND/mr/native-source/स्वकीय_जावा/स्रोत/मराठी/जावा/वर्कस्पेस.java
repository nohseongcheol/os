// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.जावा;

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

/** वापरकर्त्याच्या गृहसंचयिकेत Java स्रोत संपादित, संकलित आणि चालवण्यासाठी लहान Swing कार्यक्षेत्र. */
public final class वर्कस्पेस {
    private final JFrame विंडो = new JFrame("jkoros — जावा वर्कस्पेस");
    private final JTextArea स्रोत = new JTextArea();
    private final JTextArea आउटपुट = new JTextArea(8, 80);
    private final JTextField संचिका_प्रविष्टी_नाव = new JTextField("अभिवादन_ae353e94.java", 20);
    private final JTextField वर्ग_प्रविष्टी_नाव = new JTextField("अभिवादन_ae353e94", 16);
    private final Path कार्यरत_निर्देशिका = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService कार्यसूत्र_मूल्य = Executors.newSingleThreadExecutor();
    private volatile Process प्रक्रिया_मूल्य;
    private final String लायब्ररी = "/opt/jkoros/lib/स्वकीय_जावा.jar";

    private void सूचना(String पाठ्य) { SwingUtilities.invokeLater(() -> आउटपुट.append(पाठ्य + "\n")); }
    private void बटण(JPanel आवृत्ती_मूल्य, String नाव, Runnable वर्तन_मूल्य) {
        JButton बटण = new JButton(नाव);
        बटण.addActionListener(इव्हेंट -> वर्तन_मूल्य.run());
        आवृत्ती_मूल्य.add(बटण);
    }
    private boolean साठवणे_मूल्य() {
        try {
            Path मार्ग = कार्यरत_निर्देशिका.resolve(संचिका_प्रविष्टी_नाव.getText());
            Files.createDirectories(मार्ग.getParent());
            फाइल.लेखन(मार्ग, स्रोत.getText());
            सूचना("साठवणे_मूल्य: " + मार्ग);
            return true;
        } catch (Exception त्रुटी) { सूचना(त्रुटी.toString()); return false; }
    }
    private void उघडा() {
        try { स्रोत.setText(फाइल.वाचन(कार्यरत_निर्देशिका.resolve(संचिका_प्रविष्टी_नाव.getText()))); }
        catch (Exception त्रुटी) { सूचना(त्रुटी.toString()); }
    }
    private int आदेश(List<String> आदेश) throws Exception {
        प्रक्रिया_मूल्य = new ProcessBuilder(आदेश).directory(कार्यरत_निर्देशिका.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ओळ = new BufferedReader(new InputStreamReader(प्रक्रिया_मूल्य.getInputStream(), StandardCharsets.UTF_8))) {
            String पाठ्य;
            while ((पाठ्य = ओळ.readLine()) != null) सूचना(पाठ्य);
        }
        int राज्य_मूल्य = प्रक्रिया_मूल्य.waitFor(); प्रक्रिया_मूल्य = null;
        सूचना("निर्गमन_करा_अनुप्रयोग संहिता_मूल्य: " + राज्य_मूल्य);
        return राज्य_मूल्य;
    }
    private void भाषांतर_करा_स्रोत(boolean आज्ञा_कार्यवाही_करा, boolean निष्पादनीय_संचिका) {
        if (!साठवणे_मूल्य()) return;
        String आदान_मूल्य = संचिका_प्रविष्टी_नाव.getText(), प्रविष्टी_गुण_मूल्य = वर्ग_प्रविष्टी_नाव.getText();
        कार्यसूत्र_मूल्य.submit(() -> {
            try {
                Files.createDirectories(कार्यरत_निर्देशिका.resolve("classes"));
                if (निष्पादनीय_संचिका) {
                    आदेश(Arrays.asList("jclassc", "--target", "openjdk", "--entry", प्रविष्टी_गुण_मूल्य,
                        "--classpath", लायब्ररी, "-o", "실행프로그램", आदान_मूल्य));
                } else if (आदेश(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", लायब्ररी,
                        "-d", "classes", आदान_मूल्य)) == 0 && आज्ञा_कार्यवाही_करा) {
                    आदेश(Arrays.asList("java", "-cp", "classes:" + लायब्ररी, प्रविष्टी_गुण_मूल्य));
                }
            } catch (Exception त्रुटी) { सूचना(त्रुटी.toString()); }
        });
    }
    private void विराम_निष्पादन() {
        Process सध्याचे_आयटम = प्रक्रिया_मूल्य;
        if (सध्याचे_आयटम != null) { सध्याचे_आयटम.descendants().forEach(ProcessHandle::destroy); सध्याचे_आयटम.destroy(); }
    }
    private वर्कस्पेस() throws IOException {
        Files.createDirectories(कार्यरत_निर्देशिका);
        Font फॉन्ट_मूल्य = new Font("Monospaced", Font.PLAIN, 16);
        स्रोत.setFont(फॉन्ट_मूल्य); आउटपुट.setFont(फॉन्ट_मूल्य); आउटपुट.setEditable(false);
        स्रोत.setTabSize(4);
        स्रोत.setMargin(new Insets(10, 12, 10, 12));
        आउटपुट.setMargin(new Insets(8, 12, 8, 12));
        स्रोत.setBackground(new Color(250, 251, 252));
        स्रोत.setForeground(new Color(32, 43, 58));
        JPanel आज्ञा_पॅनेल = new JPanel();
        आज्ञा_पॅनेल.add(new JLabel("फाइल")); आज्ञा_पॅनेल.add(संचिका_प्रविष्टी_नाव);
        आज्ञा_पॅनेल.add(new JLabel("주 वर्ग_मूल्य")); आज्ञा_पॅनेल.add(वर्ग_प्रविष्टी_नाव);
        बटण(आज्ञा_पॅनेल, "उघडा", this::उघडा); बटण(आज्ञा_पॅनेल, "साठवणे_मूल्य", this::साठवणे_मूल्य);
        बटण(आज्ञा_पॅनेल, "स्रोत_बांधणी", () -> भाषांतर_करा_स्रोत(false, false));
        बटण(आज्ञा_पॅनेल, "आज्ञा_कार्यवाही_करा", () -> भाषांतर_करा_स्रोत(true, false));
        बटण(आज्ञा_पॅनेल, "आज्ञा_कार्यवाही_करा फाइल प्रविष्टी_तयार_करा", () -> भाषांतर_करा_स्रोत(false, true));
        बटण(आज्ञा_पॅनेल, "विराम_निष्पादन", this::विराम_निष्पादन);
        JSplitPane भागाकार_मोजमाप = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(स्रोत), new JScrollPane(आउटपुट));
        भागाकार_मोजमाप.setResizeWeight(0.75);
        विंडो.add(आज्ञा_पॅनेल, BorderLayout.NORTH); विंडो.add(भागाकार_मोजमाप, BorderLayout.CENTER);
        विंडो.setSize(1200, 750); विंडो.setLocationRelativeTo(null);
        विंडो.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        विंडो.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent इव्हेंट) { विराम_निष्पादन(); कार्यसूत्र_मूल्य.shutdownNow(); }
        });
        उघडा(); विंडो.setVisible(true);
    }
    public static void main(String[] बाबी) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource डिफॉल्ट_फॉन्ट = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object प्रविष्टी_मूल्य : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(प्रविष्टी_मूल्य) instanceof Font) UIManager.put(प्रविष्टी_मूल्य, डिफॉल्ट_फॉन्ट);
                }
                new वर्कस्पेस();
            } catch (Exception त्रुटी) { त्रुटी.printStackTrace(); }
        });
    }
}
