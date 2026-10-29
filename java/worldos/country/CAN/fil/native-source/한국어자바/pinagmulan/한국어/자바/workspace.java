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

/** gumagamit 홈에서 Java 원문을 edit_VALUE·bumuo_pinagmulan·실행하는 작은 Swing workspace. */
public final class workspace {
    private final JFrame window = new JFrame("jkoros — 자바 workspace");
    private final JTextArea pinagmulan = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField file_pagpasok_pangalan = new JTextField("인사.java", 20);
    private final JTextField kategorya_pagpasok_pangalan = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proseso_VALUE;
    private final String library = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void button(JPanel bersyon_VALUE, String pangalan, Runnable 행동) {
        JButton button = new JButton(pangalan);
        button.addActionListener(kaganapan -> 행동.run());
        bersyon_VALUE.add(button);
    }
    private boolean Store_VALUE() {
        try {
            Path path = 작업폴더.resolve(file_pagpasok_pangalan.getText());
            Files.createDirectories(path.getParent());
            file.sumulat(path, pinagmulan.getText());
            알림("Store_VALUE: " + path);
            return true;
        } catch (Exception error) { 알림(error.toString()); return false; }
    }
    private void buksan() {
        try { pinagmulan.setText(file.읽기(작업폴더.resolve(file_pagpasok_pangalan.getText()))); }
        catch (Exception error) { 알림(error.toString()); }
    }
    private int utos(List<String> utos) throws Exception {
        Proseso_VALUE = new ProcessBuilder(utos).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader linya = new BufferedReader(new InputStreamReader(Proseso_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = linya.readLine()) != null) 알림(SMS);
        }
        int katayuan_VALUE = Proseso_VALUE.waitFor(); Proseso_VALUE = null;
        알림("Paglabas_app CODE_VALUE: " + katayuan_VALUE);
        return katayuan_VALUE;
    }
    private void TRANSLATE_pinagmulan(boolean Mag_execute_utos, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = file_pagpasok_pangalan.getText(), pagpasok_point_VALUE = kategorya_pagpasok_pangalan.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    utos(Arrays.asList("jclassc", "--target", "openjdk", "--entry", pagpasok_point_VALUE,
                        "--classpath", library, "-o", "실행프로그램", 입력));
                } else if (utos(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", library,
                        "-d", "classes", 입력)) == 0 && Mag_execute_utos) {
                    utos(Arrays.asList("java", "-cp", "classes:" + library, pagpasok_point_VALUE));
                }
            } catch (Exception error) { 알림(error.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proseso_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private workspace() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        pinagmulan.setFont(font_VALUE); 출력.setFont(font_VALUE); 출력.setEditable(false);
        pinagmulan.setTabSize(4);
        pinagmulan.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        pinagmulan.setBackground(new Color(250, 251, 252));
        pinagmulan.setForeground(new Color(32, 43, 58));
        JPanel utos_panel = new JPanel();
        utos_panel.add(new JLabel("file")); utos_panel.add(file_pagpasok_pangalan);
        utos_panel.add(new JLabel("주 kategorya_VALUE_55654bf1")); utos_panel.add(kategorya_pagpasok_pangalan);
        button(utos_panel, "buksan", this::buksan); button(utos_panel, "Store_VALUE", this::Store_VALUE);
        button(utos_panel, "bumuo_pinagmulan", () -> TRANSLATE_pinagmulan(false, false));
        button(utos_panel, "Mag_execute_utos", () -> TRANSLATE_pinagmulan(true, false));
        button(utos_panel, "Mag_execute_utos file Create_pagpasok", () -> TRANSLATE_pinagmulan(false, true));
        button(utos_panel, "멈춤", this::멈춤);
        JSplitPane division_sukat = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(pinagmulan), new JScrollPane(출력));
        division_sukat.setResizeWeight(0.75);
        window.add(utos_panel, BorderLayout.NORTH); window.add(division_sukat, BorderLayout.CENTER);
        window.setSize(1200, 750); window.setLocationRelativeTo(null);
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent kaganapan) { 멈춤(); 일꾼.shutdownNow(); }
        });
        buksan(); window.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource default_font = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object pagpasok_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(pagpasok_VALUE) instanceof Font) UIManager.put(pagpasok_VALUE, default_font);
                }
                new workspace();
            } catch (Exception error) { error.printStackTrace(); }
        });
    }
}
