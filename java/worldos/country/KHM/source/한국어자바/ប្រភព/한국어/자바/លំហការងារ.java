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

/** អ្នកប្រើ 홈에서 Java 원문을 កែសម្រួល_តំលៃ·ចងក្រង_ប្រភព·실행하는 작은 Swing លំហការងារ. */
public final class លំហការងារ {
    private final JFrame វីនដូ = new JFrame("jkoros — 자바 លំហការងារ");
    private final JTextArea ប្រភព = new JTextArea();
    private final JTextArea លទ្ធផល = new JTextArea(8, 80);
    private final JTextField ឯកសារ_ការបញ្ចូល_ឈ្មោះ = new JTextField("인사.java", 20);
    private final JTextField ថ្នាក់_ការបញ្ចូល_ឈ្មោះ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ដំណើរការ_តំលៃ;
    private final String បណ្ណាល័យ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String អត្ថបទ) { SwingUtilities.invokeLater(() -> លទ្ធផល.append(អត្ថបទ + "\n")); }
    private void ប៊ូតុង(JPanel កំណែ_តំលៃ, String ឈ្មោះ, Runnable 행동) {
        JButton ប៊ូតុង = new JButton(ឈ្មោះ);
        ប៊ូតុង.addActionListener(ព្រឹត្តិការណ៍ -> 행동.run());
        កំណែ_តំលៃ.add(ប៊ូតុង);
    }
    private boolean ផ្ទុក_តំលៃ() {
        try {
            Path ផ្លូវ = 작업폴더.resolve(ឯកសារ_ការបញ្ចូល_ឈ្មោះ.getText());
            Files.createDirectories(ផ្លូវ.getParent());
            ឯកសារ.សរសេរ(ផ្លូវ, ប្រភព.getText());
            알림("ផ្ទុក_តំលៃ: " + ផ្លូវ);
            return true;
        } catch (Exception កំហុស) { 알림(កំហុស.toString()); return false; }
    }
    private void បើក() {
        try { ប្រភព.setText(ឯកសារ.អាន(작업폴더.resolve(ឯកសារ_ការបញ្ចូល_ឈ្មោះ.getText()))); }
        catch (Exception កំហុស) { 알림(កំហុស.toString()); }
    }
    private int ពាក្យ_បញ្ជា(List<String> ពាក្យ_បញ្ជា) throws Exception {
        ដំណើរការ_តំលៃ = new ProcessBuilder(ពាក្យ_បញ្ជា).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader បន្ទាត់ = new BufferedReader(new InputStreamReader(ដំណើរការ_តំលៃ.getInputStream(), StandardCharsets.UTF_8))) {
            String អត្ថបទ;
            while ((អត្ថបទ = បន្ទាត់.readLine()) != null) 알림(អត្ថបទ);
        }
        int ភាព_តំលៃ = ដំណើរការ_តំលៃ.waitFor(); ដំណើរការ_តំលៃ = null;
        알림("ចេញ_កម្មវិធី កូដ_តំលៃ: " + ភាព_តំលៃ);
        return ភាព_តំលៃ;
    }
    private void បកប្រែ_ប្រភព(boolean អនុវត្ត_ពាក្យបញ្ជា, boolean 실행파일) {
        if (!ផ្ទុក_តំលៃ()) return;
        String 입력 = ឯកសារ_ការបញ្ចូល_ឈ្មោះ.getText(), ការបញ្ចូល_ចំនុច_តំលៃ = ថ្នាក់_ការបញ្ចូល_ឈ្មោះ.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ពាក្យ_បញ្ជា(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ការបញ្ចូល_ចំនុច_តំលៃ,
                        "--classpath", បណ្ណាល័យ, "-o", "실행프로그램", 입력));
                } else if (ពាក្យ_បញ្ជា(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", បណ្ណាល័យ,
                        "-d", "classes", 입력)) == 0 && អនុវត្ត_ពាក្យបញ្ជា) {
                    ពាក្យ_បញ្ជា(Arrays.asList("java", "-cp", "classes:" + បណ្ណាល័យ, ការបញ្ចូល_ចំនុច_តំលៃ));
                }
            } catch (Exception កំហុស) { 알림(កំហុស.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ដំណើរការ_តំលៃ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private លំហការងារ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ពុម្ពអក្សរ_តំលៃ = new Font("Monospaced", Font.PLAIN, 16);
        ប្រភព.setFont(ពុម្ពអក្សរ_តំលៃ); លទ្ធផល.setFont(ពុម្ពអក្សរ_តំលៃ); លទ្ធផល.setEditable(false);
        ប្រភព.setTabSize(4);
        ប្រភព.setMargin(new Insets(10, 12, 10, 12));
        លទ្ធផល.setMargin(new Insets(8, 12, 8, 12));
        ប្រភព.setBackground(new Color(250, 251, 252));
        ប្រភព.setForeground(new Color(32, 43, 58));
        JPanel ពាក្យបញ្ជា_ផ្ទាំង = new JPanel();
        ពាក្យបញ្ជា_ផ្ទាំង.add(new JLabel("ឯកសារ")); ពាក្យបញ្ជា_ផ្ទាំង.add(ឯកសារ_ការបញ្ចូល_ឈ្មោះ);
        ពាក្យបញ្ជា_ផ្ទាំង.add(new JLabel("주 ថ្នាក់_តំលៃ")); ពាក្យបញ្ជា_ផ្ទាំង.add(ថ្នាក់_ការបញ្ចូល_ឈ្មោះ);
        ប៊ូតុង(ពាក្យបញ្ជា_ផ្ទាំង, "បើក", this::បើក); ប៊ូតុង(ពាក្យបញ្ជា_ផ្ទាំង, "ផ្ទុក_តំលៃ", this::ផ្ទុក_តំលៃ);
        ប៊ូតុង(ពាក្យបញ្ជា_ផ្ទាំង, "ចងក្រង_ប្រភព", () -> បកប្រែ_ប្រភព(false, false));
        ប៊ូតុង(ពាក្យបញ្ជា_ផ្ទាំង, "អនុវត្ត_ពាក្យបញ្ជា", () -> បកប្រែ_ប្រភព(true, false));
        ប៊ូតុង(ពាក្យបញ្ជា_ផ្ទាំង, "អនុវត្ត_ពាក្យបញ្ជា ឯកសារ បង្កើត_ការបញ្ចូល", () -> បកប្រែ_ប្រភព(false, true));
        ប៊ូតុង(ពាក្យបញ្ជា_ផ្ទាំង, "멈춤", this::멈춤);
        JSplitPane ការចែក_ការវាស់វែង = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ប្រភព), new JScrollPane(លទ្ធផល));
        ការចែក_ការវាស់វែង.setResizeWeight(0.75);
        វីនដូ.add(ពាក្យបញ្ជា_ផ្ទាំង, BorderLayout.NORTH); វីនដូ.add(ការចែក_ការវាស់វែង, BorderLayout.CENTER);
        វីនដូ.setSize(1200, 750); វីនដូ.setLocationRelativeTo(null);
        វីនដូ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        វីនដូ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ព្រឹត្តិការណ៍) { 멈춤(); 일꾼.shutdownNow(); }
        });
        បើក(); វីនដូ.setVisible(true);
    }
    public static void main(String[] អាគុយម៉ង់) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ពុម្ភអក្សរស្វ័យប្រវត្ត = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ការបញ្ចូល_តំលៃ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ការបញ្ចូល_តំលៃ) instanceof Font) UIManager.put(ការបញ្ចូល_តំលៃ, ពុម្ភអក្សរស្វ័យប្រវត្ត);
                }
                new លំហការងារ();
            } catch (Exception កំហុស) { កំហុស.printStackTrace(); }
        });
    }
}
