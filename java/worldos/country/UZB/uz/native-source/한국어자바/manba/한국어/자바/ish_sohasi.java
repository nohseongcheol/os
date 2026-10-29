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

/** foydalanuvchi 홈에서 Java 원문을 tahrirlamoq_VALUE·yig_moq_manba·실행하는 작은 Swing ish_sohasi. */
public final class ish_sohasi {
    private final JFrame oyna = new JFrame("jkoros — 자바 ish_sohasi");
    private final JTextArea manba = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField fayl_kiritish_nom = new JTextField("인사.java", 20);
    private final JTextField Sinf_kiritish_nom = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Jarayon_VALUE;
    private final String kutubxona = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Matn) { SwingUtilities.invokeLater(() -> 출력.append(Matn + "\n")); }
    private void tugma(JPanel versiya_VALUE, String Nomi, Runnable 행동) {
        JButton tugma = new JButton(Nomi);
        tugma.addActionListener(hodisa -> 행동.run());
        versiya_VALUE.add(tugma);
    }
    private boolean Store_VALUE() {
        try {
            Path yo_l = 작업폴더.resolve(fayl_kiritish_nom.getText());
            Files.createDirectories(yo_l.getParent());
            Fayl.Yozish(yo_l, manba.getText());
            알림("Store_VALUE: " + yo_l);
            return true;
        } catch (Exception Xato) { 알림(Xato.toString()); return false; }
    }
    private void Ochish() {
        try { manba.setText(Fayl.Oʻqish(작업폴더.resolve(fayl_kiritish_nom.getText()))); }
        catch (Exception Xato) { 알림(Xato.toString()); }
    }
    private int Buyruq(List<String> Buyruq) throws Exception {
        Jarayon_VALUE = new ProcessBuilder(Buyruq).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader satr = new BufferedReader(new InputStreamReader(Jarayon_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Matn;
            while ((Matn = satr.readLine()) != null) 알림(Matn);
        }
        int holat_VALUE_e10195a1 = Jarayon_VALUE.waitFor(); Jarayon_VALUE = null;
        알림("Chiqish_ilova kod_VALUE: " + holat_VALUE_e10195a1);
        return holat_VALUE_e10195a1;
    }
    private void Tarjima_manba(boolean bajarmoq_buyruq, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = fayl_kiritish_nom.getText(), kiritish_nuqta_VALUE = Sinf_kiritish_nom.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Buyruq(Arrays.asList("jclassc", "--target", "openjdk", "--entry", kiritish_nuqta_VALUE,
                        "--classpath", kutubxona, "-o", "실행프로그램", 입력));
                } else if (Buyruq(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", kutubxona,
                        "-d", "classes", 입력)) == 0 && bajarmoq_buyruq) {
                    Buyruq(Arrays.asList("java", "-cp", "classes:" + kutubxona, kiritish_nuqta_VALUE));
                }
            } catch (Exception Xato) { 알림(Xato.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Jarayon_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ish_sohasi() throws IOException {
        Files.createDirectories(작업폴더);
        Font shrift_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        manba.setFont(shrift_VALUE); 출력.setFont(shrift_VALUE); 출력.setEditable(false);
        manba.setTabSize(4);
        manba.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        manba.setBackground(new Color(250, 251, 252));
        manba.setForeground(new Color(32, 43, 58));
        JPanel buyruq_panel = new JPanel();
        buyruq_panel.add(new JLabel("Fayl")); buyruq_panel.add(fayl_kiritish_nom);
        buyruq_panel.add(new JLabel("주 Sinf_VALUE")); buyruq_panel.add(Sinf_kiritish_nom);
        tugma(buyruq_panel, "Ochish", this::Ochish); tugma(buyruq_panel, "Store_VALUE", this::Store_VALUE);
        tugma(buyruq_panel, "yig_moq_manba", () -> Tarjima_manba(false, false));
        tugma(buyruq_panel, "bajarmoq_buyruq", () -> Tarjima_manba(true, false));
        tugma(buyruq_panel, "bajarmoq_buyruq Fayl Yaratish_kiritish", () -> Tarjima_manba(false, true));
        tugma(buyruq_panel, "멈춤", this::멈춤);
        JSplitPane boʻlish_o_lchov = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(manba), new JScrollPane(출력));
        boʻlish_o_lchov.setResizeWeight(0.75);
        oyna.add(buyruq_panel, BorderLayout.NORTH); oyna.add(boʻlish_o_lchov, BorderLayout.CENTER);
        oyna.setSize(1200, 750); oyna.setLocationRelativeTo(null);
        oyna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        oyna.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent hodisa) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Ochish(); oyna.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource sukut_bo_yicha_shrift = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object kiritish_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(kiritish_VALUE) instanceof Font) UIManager.put(kiritish_VALUE, sukut_bo_yicha_shrift);
                }
                new ish_sohasi();
            } catch (Exception Xato) { Xato.printStackTrace(); }
        });
    }
}
