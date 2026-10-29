// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.자바;

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

/** notandi 홈에서 Java 원문을 breyta_VALUE·þýða_uppruni·실행하는 작은 Swing vinnusvæði. */
public final class vinnusvæði {
    private final JFrame Gluggi = new JFrame("jkoros — 자바 vinnusvæði");
    private final JTextArea Uppruni = new JTextArea();
    private final JTextArea úttak = new JTextArea(8, 80);
    private final JTextField skrá_færsla_heiti = new JTextField("인사.java", 20);
    private final JTextField klasi_færsla_heiti = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService starfskraftur_VALUE = Executors.newSingleThreadExecutor();
    private volatile Process Ferli_VALUE;
    private final String safn = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Texti) { SwingUtilities.invokeLater(() -> úttak.append(Texti + "\n")); }
    private void hnappur(JPanel útgáfa_VALUE, String Heiti, Runnable 행동) {
        JButton hnappur = new JButton(Heiti);
        hnappur.addActionListener(atvik -> 행동.run());
        útgáfa_VALUE.add(hnappur);
    }
    private boolean Store_VALUE() {
        try {
            Path SLÓÐ = 작업폴더.resolve(skrá_færsla_heiti.getText());
            Files.createDirectories(SLÓÐ.getParent());
            Skrá.Skrift(SLÓÐ, Uppruni.getText());
            알림("Store_VALUE: " + SLÓÐ);
            return true;
        } catch (Exception Villa) { 알림(Villa.toString()); return false; }
    }
    private void Opna() {
        try { Uppruni.setText(Skrá.Lestur(작업폴더.resolve(skrá_færsla_heiti.getText()))); }
        catch (Exception Villa) { 알림(Villa.toString()); }
    }
    private int Skipun(List<String> Skipun) throws Exception {
        Ferli_VALUE = new ProcessBuilder(Skipun).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Lína = new BufferedReader(new InputStreamReader(Ferli_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Texti;
            while ((Texti = Lína.readLine()) != null) 알림(Texti);
        }
        int staða_VALUE_e10195a1 = Ferli_VALUE.waitFor(); Ferli_VALUE = null;
        알림("loka_forrit CODE_VALUE: " + staða_VALUE_e10195a1);
        return staða_VALUE_e10195a1;
    }
    private void Þýða_uppruni(boolean keyra_skipun, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = skrá_færsla_heiti.getText(), færsla_P_VALUE = klasi_færsla_heiti.getText();
        starfskraftur_VALUE.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Skipun(Arrays.asList("jclassc", "--target", "openjdk", "--entry", færsla_P_VALUE,
                        "--classpath", safn, "-o", "실행프로그램", 입력));
                } else if (Skipun(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", safn,
                        "-d", "classes", 입력)) == 0 && keyra_skipun) {
                    Skipun(Arrays.asList("java", "-cp", "classes:" + safn, færsla_P_VALUE));
                }
            } catch (Exception Villa) { 알림(Villa.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Ferli_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private vinnusvæði() throws IOException {
        Files.createDirectories(작업폴더);
        Font leturgerð_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        Uppruni.setFont(leturgerð_VALUE); úttak.setFont(leturgerð_VALUE); úttak.setEditable(false);
        Uppruni.setTabSize(4);
        Uppruni.setMargin(new Insets(10, 12, 10, 12));
        úttak.setMargin(new Insets(8, 12, 8, 12));
        Uppruni.setBackground(new Color(250, 251, 252));
        Uppruni.setForeground(new Color(32, 43, 58));
        JPanel skipun_svæði = new JPanel();
        skipun_svæði.add(new JLabel("Skrá")); skipun_svæði.add(skrá_færsla_heiti);
        skipun_svæði.add(new JLabel("주 klasi_VALUE")); skipun_svæði.add(klasi_færsla_heiti);
        hnappur(skipun_svæði, "Opna", this::Opna); hnappur(skipun_svæði, "Store_VALUE", this::Store_VALUE);
        hnappur(skipun_svæði, "þýða_uppruni", () -> Þýða_uppruni(false, false));
        hnappur(skipun_svæði, "keyra_skipun", () -> Þýða_uppruni(true, false));
        hnappur(skipun_svæði, "keyra_skipun Skrá stofna_færsla", () -> Þýða_uppruni(false, true));
        hnappur(skipun_svæði, "멈춤", this::멈춤);
        JSplitPane deiling_mæld_stærð = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Uppruni), new JScrollPane(úttak));
        deiling_mæld_stærð.setResizeWeight(0.75);
        Gluggi.add(skipun_svæði, BorderLayout.NORTH); Gluggi.add(deiling_mæld_stærð, BorderLayout.CENTER);
        Gluggi.setSize(1200, 750); Gluggi.setLocationRelativeTo(null);
        Gluggi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Gluggi.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent atvik) { 멈춤(); starfskraftur_VALUE.shutdownNow(); }
        });
        Opna(); Gluggi.setVisible(true);
    }
    public static void main(String[] Viðföng) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource sjálfgefið_letur = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object færsla_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(færsla_VALUE) instanceof Font) UIManager.put(færsla_VALUE, sjálfgefið_letur);
                }
                new vinnusvæði();
            } catch (Exception Villa) { Villa.printStackTrace(); }
        });
    }
}
