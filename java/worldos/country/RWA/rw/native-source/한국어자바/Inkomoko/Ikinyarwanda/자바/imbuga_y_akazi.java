// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자바;

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

/** ukoresha 홈에서 Java 원문을 guhindura_agaciro·gusohora_inkomoko·실행하는 작은 Swing imbuga_y_akazi. */
public final class imbuga_y_akazi {
    private final JFrame idirishya = new JFrame("jkoros — 자바 imbuga_y_akazi");
    private final JTextArea Inkomoko = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField dosiye_icyinjizwa_izina = new JTextField("인사.java", 20);
    private final JTextField icyiciro_icyinjizwa_izina = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Inzira_agaciro;
    private final String isomero = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Umwandiko) { SwingUtilities.invokeLater(() -> 출력.append(Umwandiko + "\n")); }
    private void buto(JPanel verisiyo_agaciro, String Izina, Runnable 행동) {
        JButton buto = new JButton(Izina);
        buto.addActionListener(icyabaye -> 행동.run());
        verisiyo_agaciro.add(buto);
    }
    private boolean Store_agaciro() {
        try {
            Path Inzira = 작업폴더.resolve(dosiye_icyinjizwa_izina.getText());
            Files.createDirectories(Inzira.getParent());
            Idosiye.kwandika(Inzira, Inkomoko.getText());
            알림("Store_agaciro: " + Inzira);
            return true;
        } catch (Exception IKOSA) { 알림(IKOSA.toString()); return false; }
    }
    private void Gufungura() {
        try { Inkomoko.setText(Idosiye.읽기(작업폴더.resolve(dosiye_icyinjizwa_izina.getText()))); }
        catch (Exception IKOSA) { 알림(IKOSA.toString()); }
    }
    private int Icyo_wifuza(List<String> Icyo_wifuza) throws Exception {
        Inzira_agaciro = new ProcessBuilder(Icyo_wifuza).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader umurongo = new BufferedReader(new InputStreamReader(Inzira_agaciro.getInputStream(), StandardCharsets.UTF_8))) {
            String Umwandiko;
            while ((Umwandiko = umurongo.readLine()) != null) 알림(Umwandiko);
        }
        int imimerere_agaciro = Inzira_agaciro.waitFor(); Inzira_agaciro = null;
        알림("gusohoka_porogaramu 코드: " + imimerere_agaciro);
        return imimerere_agaciro;
    }
    private void Gusemura_inkomoko(boolean gukora_ibwiriza, boolean 실행파일) {
        if (!Store_agaciro()) return;
        String 입력 = dosiye_icyinjizwa_izina.getText(), icyinjizwa_inota_agaciro = icyiciro_icyinjizwa_izina.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Icyo_wifuza(Arrays.asList("jclassc", "--target", "openjdk", "--entry", icyinjizwa_inota_agaciro,
                        "--classpath", isomero, "-o", "실행프로그램", 입력));
                } else if (Icyo_wifuza(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", isomero,
                        "-d", "classes", 입력)) == 0 && gukora_ibwiriza) {
                    Icyo_wifuza(Arrays.asList("java", "-cp", "classes:" + isomero, icyinjizwa_inota_agaciro));
                }
            } catch (Exception IKOSA) { 알림(IKOSA.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Inzira_agaciro;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private imbuga_y_akazi() throws IOException {
        Files.createDirectories(작업폴더);
        Font imyandikire_agaciro = new Font("Monospaced", Font.PLAIN, 16);
        Inkomoko.setFont(imyandikire_agaciro); 출력.setFont(imyandikire_agaciro); 출력.setEditable(false);
        Inkomoko.setTabSize(4);
        Inkomoko.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        Inkomoko.setBackground(new Color(250, 251, 252));
        Inkomoko.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("Idosiye")); 명령판.add(dosiye_icyinjizwa_izina);
        명령판.add(new JLabel("주 icyiciro_agaciro_55654bf1")); 명령판.add(icyiciro_icyinjizwa_izina);
        buto(명령판, "Gufungura", this::Gufungura); buto(명령판, "Store_agaciro", this::Store_agaciro);
        buto(명령판, "gusohora_inkomoko", () -> Gusemura_inkomoko(false, false));
        buto(명령판, "gukora_ibwiriza", () -> Gusemura_inkomoko(true, false));
        buto(명령판, "gukora_ibwiriza Idosiye kurema_icyinjizwa", () -> Gusemura_inkomoko(false, true));
        buto(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Inkomoko), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        idirishya.add(명령판, BorderLayout.NORTH); idirishya.add(나눔, BorderLayout.CENTER);
        idirishya.setSize(1200, 750); idirishya.setLocationRelativeTo(null);
        idirishya.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        idirishya.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent icyabaye) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Gufungura(); idirishya.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource imyandikire_isanzweho = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object icyinjizwa_agaciro : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(icyinjizwa_agaciro) instanceof Font) UIManager.put(icyinjizwa_agaciro, imyandikire_isanzweho);
                }
                new imbuga_y_akazi();
            } catch (Exception IKOSA) { IKOSA.printStackTrace(); }
        });
    }
}
