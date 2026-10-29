// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.자바;

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

/** kasutaja 홈에서 Java 원문을 muudatus_VALUE·kompileerima_lähe·실행하는 작은 Swing tööruum. */
public final class tööruum {
    private final JFrame aken = new JFrame("jkoros — 자바 tööruum");
    private final JTextArea ALLIKAS = new JTextArea();
    private final JTextArea Väljund = new JTextArea(8, 80);
    private final JTextField Fail_kirje_nimetus = new JTextField("인사.java", 20);
    private final JTextField tund_kirje_nimetus = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService töötaja_VALUE = Executors.newSingleThreadExecutor();
    private volatile Process Joonis_VALUE;
    private final String teek = "/opt/jkoros/lib/한국어자바.jar";

    private void teatamine(String Tekst) { SwingUtilities.invokeLater(() -> Väljund.append(Tekst + "\n")); }
    private void nupp(JPanel versioon_VALUE, String Nimi_2, Runnable 행동) {
        JButton nupp = new JButton(Nimi_2);
        nupp.addActionListener(Sündmus -> 행동.run());
        versioon_VALUE.add(nupp);
    }
    private boolean salv_VALUE() {
        try {
            Path RADA = 작업폴더.resolve(Fail_kirje_nimetus.getText());
            Files.createDirectories(RADA.getParent());
            Fail.Kirjutamine(RADA, ALLIKAS.getText());
            teatamine("salv_VALUE: " + RADA);
            return true;
        } catch (Exception VIGA) { teatamine(VIGA.toString()); return false; }
    }
    private void Ava() {
        try { ALLIKAS.setText(Fail.Lugemine(작업폴더.resolve(Fail_kirje_nimetus.getText()))); }
        catch (Exception VIGA) { teatamine(VIGA.toString()); }
    }
    private int Käsk(List<String> Käsk) throws Exception {
        Joonis_VALUE = new ProcessBuilder(Käsk).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Joon = new BufferedReader(new InputStreamReader(Joonis_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = Joon.readLine()) != null) teatamine(Tekst);
        }
        int Olek_VALUE = Joonis_VALUE.waitFor(); Joonis_VALUE = null;
        teatamine("Välju_programm CODE_VALUE: " + Olek_VALUE);
        return Olek_VALUE;
    }
    private void Tõlgi_lähe(boolean Täida_käsk, boolean 실행파일) {
        if (!salv_VALUE()) return;
        String 입력 = Fail_kirje_nimetus.getText(), kirje_p_VALUE = tund_kirje_nimetus.getText();
        töötaja_VALUE.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Käsk(Arrays.asList("jclassc", "--target", "openjdk", "--entry", kirje_p_VALUE,
                        "--classpath", teek, "-o", "실행프로그램", 입력));
                } else if (Käsk(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", teek,
                        "-d", "classes", 입력)) == 0 && Täida_käsk) {
                    Käsk(Arrays.asList("java", "-cp", "classes:" + teek, kirje_p_VALUE));
                }
            } catch (Exception VIGA) { teatamine(VIGA.toString()); }
        });
    }
    private void 멈춤() {
        Process tähtaja_piires_kaup = Joonis_VALUE;
        if (tähtaja_piires_kaup != null) { tähtaja_piires_kaup.descendants().forEach(ProcessHandle::destroy); tähtaja_piires_kaup.destroy(); }
    }
    private tööruum() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        ALLIKAS.setFont(font_VALUE); Väljund.setFont(font_VALUE); Väljund.setEditable(false);
        ALLIKAS.setTabSize(4);
        ALLIKAS.setMargin(new Insets(10, 12, 10, 12));
        Väljund.setMargin(new Insets(8, 12, 8, 12));
        ALLIKAS.setBackground(new Color(250, 251, 252));
        ALLIKAS.setForeground(new Color(32, 43, 58));
        JPanel käsk_paneel = new JPanel();
        käsk_paneel.add(new JLabel("Fail")); käsk_paneel.add(Fail_kirje_nimetus);
        käsk_paneel.add(new JLabel("주 tund_VALUE")); käsk_paneel.add(tund_kirje_nimetus);
        nupp(käsk_paneel, "Ava", this::Ava); nupp(käsk_paneel, "salv_VALUE", this::salv_VALUE);
        nupp(käsk_paneel, "kompileerima_lähe", () -> Tõlgi_lähe(false, false));
        nupp(käsk_paneel, "Täida_käsk", () -> Tõlgi_lähe(true, false));
        nupp(käsk_paneel, "Täida_käsk Fail avama_kirje", () -> Tõlgi_lähe(false, true));
        nupp(käsk_paneel, "멈춤", this::멈춤);
        JSplitPane allüksus_näitaja = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ALLIKAS), new JScrollPane(Väljund));
        allüksus_näitaja.setResizeWeight(0.75);
        aken.add(käsk_paneel, BorderLayout.NORTH); aken.add(allüksus_näitaja, BorderLayout.CENTER);
        aken.setSize(1200, 750); aken.setLocationRelativeTo(null);
        aken.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        aken.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Sündmus) { 멈춤(); töötaja_VALUE.shutdownNow(); }
        });
        Ava(); aken.setVisible(true);
    }
    public static void main(String[] Argumendid) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource vaikefont = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object kirje_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(kirje_VALUE) instanceof Font) UIManager.put(kirje_VALUE, vaikefont);
                }
                new tööruum();
            } catch (Exception VIGA) { VIGA.printStackTrace(); }
        });
    }
}
