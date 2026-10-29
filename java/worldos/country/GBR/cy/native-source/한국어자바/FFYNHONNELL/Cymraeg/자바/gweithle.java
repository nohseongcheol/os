// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자바;

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

/** defnyddiwr 홈에서 Java 원문을 Golygu_VALUE·llunio_ffynhonnell·실행하는 작은 Swing gweithle. */
public final class gweithle {
    private final JFrame ffenestr = new JFrame("jkoros — 자바 gweithle");
    private final JTextArea FFYNHONNELL = new JTextArea();
    private final JTextArea Allbwn = new JTextArea(8, 80);
    private final JTextField ffeil_cofnod_enw = new JTextField("인사.java", 20);
    private final JTextField Dosbarth_cofnod_enw = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proses_VALUE;
    private final String llyfrgell = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Testun) { SwingUtilities.invokeLater(() -> Allbwn.append(Testun + "\n")); }
    private void botwm(JPanel fersiwn_VALUE, String Enw, Runnable 행동) {
        JButton botwm = new JButton(Enw);
        botwm.addActionListener(digwyddiad -> 행동.run());
        fersiwn_VALUE.add(botwm);
    }
    private boolean Store_VALUE() {
        try {
            Path LLWYBR = 작업폴더.resolve(ffeil_cofnod_enw.getText());
            Files.createDirectories(LLWYBR.getParent());
            Ffeil.Ysgrifennu(LLWYBR, FFYNHONNELL.getText());
            알림("Store_VALUE: " + LLWYBR);
            return true;
        } catch (Exception Gwall) { 알림(Gwall.toString()); return false; }
    }
    private void Agor() {
        try { FFYNHONNELL.setText(Ffeil.Darllen(작업폴더.resolve(ffeil_cofnod_enw.getText()))); }
        catch (Exception Gwall) { 알림(Gwall.toString()); }
    }
    private int Gorchymyn(List<String> Gorchymyn) throws Exception {
        Proses_VALUE = new ProcessBuilder(Gorchymyn).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader llinell = new BufferedReader(new InputStreamReader(Proses_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Testun;
            while ((Testun = llinell.readLine()) != null) 알림(Testun);
        }
        int cyflwr_VALUE = Proses_VALUE.waitFor(); Proses_VALUE = null;
        알림("gadael_Rhaglen cod_VALUE: " + cyflwr_VALUE);
        return cyflwr_VALUE;
    }
    private void Cyfieithu_ffynhonnell(boolean Gweithredu_gorchymyn, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = ffeil_cofnod_enw.getText(), cofnod_p_VALUE = Dosbarth_cofnod_enw.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Gorchymyn(Arrays.asList("jclassc", "--target", "openjdk", "--entry", cofnod_p_VALUE,
                        "--classpath", llyfrgell, "-o", "실행프로그램", 입력));
                } else if (Gorchymyn(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", llyfrgell,
                        "-d", "classes", 입력)) == 0 && Gweithredu_gorchymyn) {
                    Gorchymyn(Arrays.asList("java", "-cp", "classes:" + llyfrgell, cofnod_p_VALUE));
                }
            } catch (Exception Gwall) { 알림(Gwall.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proses_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private gweithle() throws IOException {
        Files.createDirectories(작업폴더);
        Font ffont_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        FFYNHONNELL.setFont(ffont_VALUE); Allbwn.setFont(ffont_VALUE); Allbwn.setEditable(false);
        FFYNHONNELL.setTabSize(4);
        FFYNHONNELL.setMargin(new Insets(10, 12, 10, 12));
        Allbwn.setMargin(new Insets(8, 12, 8, 12));
        FFYNHONNELL.setBackground(new Color(250, 251, 252));
        FFYNHONNELL.setForeground(new Color(32, 43, 58));
        JPanel gorchymyn_panel = new JPanel();
        gorchymyn_panel.add(new JLabel("Ffeil")); gorchymyn_panel.add(ffeil_cofnod_enw);
        gorchymyn_panel.add(new JLabel("주 Dosbarth_VALUE")); gorchymyn_panel.add(Dosbarth_cofnod_enw);
        botwm(gorchymyn_panel, "Agor", this::Agor); botwm(gorchymyn_panel, "Store_VALUE", this::Store_VALUE);
        botwm(gorchymyn_panel, "llunio_ffynhonnell", () -> Cyfieithu_ffynhonnell(false, false));
        botwm(gorchymyn_panel, "Gweithredu_gorchymyn", () -> Cyfieithu_ffynhonnell(true, false));
        botwm(gorchymyn_panel, "Gweithredu_gorchymyn Ffeil Creu_cofnod", () -> Cyfieithu_ffynhonnell(false, true));
        botwm(gorchymyn_panel, "멈춤", this::멈춤);
        JSplitPane rhannu_mesur = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FFYNHONNELL), new JScrollPane(Allbwn));
        rhannu_mesur.setResizeWeight(0.75);
        ffenestr.add(gorchymyn_panel, BorderLayout.NORTH); ffenestr.add(rhannu_mesur, BorderLayout.CENTER);
        ffenestr.setSize(1200, 750); ffenestr.setLocationRelativeTo(null);
        ffenestr.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ffenestr.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent digwyddiad) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Agor(); ffenestr.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ffont_diofyn = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object cofnod_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(cofnod_VALUE) instanceof Font) UIManager.put(cofnod_VALUE, ffont_diofyn);
                }
                new gweithle();
            } catch (Exception Gwall) { Gwall.printStackTrace(); }
        });
    }
}
