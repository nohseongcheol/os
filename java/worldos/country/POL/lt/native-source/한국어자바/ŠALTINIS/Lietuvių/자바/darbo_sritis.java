// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.자바;

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

/** naudotojas 홈에서 Java 원문을 redaguoti_VALUE·kompiliuoti_šaltinis·실행하는 작은 Swing darbo_sritis. */
public final class darbo_sritis {
    private final JFrame Langas = new JFrame("jkoros — 자바 darbo_sritis");
    private final JTextArea ŠALTINIS = new JTextArea();
    private final JTextArea Išvestis = new JTextArea(8, 80);
    private final JTextField Failas_įrašas_pavadinimas = new JTextField("인사.java", 20);
    private final JTextField klasė_įrašas_pavadinimas = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService darbininkas_VALUE = Executors.newSingleThreadExecutor();
    private volatile Process Procesas_VALUE;
    private final String biblioteka = "/opt/jkoros/lib/한국어자바.jar";

    private void pranešimas(String Tekstas) { SwingUtilities.invokeLater(() -> Išvestis.append(Tekstas + "\n")); }
    private void mygtukas(JPanel versija_VALUE, String Pavadinimas_2, Runnable 행동) {
        JButton mygtukas = new JButton(Pavadinimas_2);
        mygtukas.addActionListener(Įvykis -> 행동.run());
        versija_VALUE.add(mygtukas);
    }
    private boolean Store_VALUE() {
        try {
            Path KELIAS = 작업폴더.resolve(Failas_įrašas_pavadinimas.getText());
            Files.createDirectories(KELIAS.getParent());
            Failas.Rašymas(KELIAS, ŠALTINIS.getText());
            pranešimas("Store_VALUE: " + KELIAS);
            return true;
        } catch (Exception KLAIDA) { pranešimas(KLAIDA.toString()); return false; }
    }
    private void Atverti() {
        try { ŠALTINIS.setText(Failas.Skaitymas(작업폴더.resolve(Failas_įrašas_pavadinimas.getText()))); }
        catch (Exception KLAIDA) { pranešimas(KLAIDA.toString()); }
    }
    private int Komanda(List<String> Komanda) throws Exception {
        Procesas_VALUE = new ProcessBuilder(Komanda).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Eilutė = new BufferedReader(new InputStreamReader(Procesas_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekstas;
            while ((Tekstas = Eilutė.readLine()) != null) pranešimas(Tekstas);
        }
        int Būsena_VALUE = Procesas_VALUE.waitFor(); Procesas_VALUE = null;
        pranešimas("Baigti_programa_086bb533 CODE_VALUE: " + Būsena_VALUE);
        return Būsena_VALUE;
    }
    private void Versti_šaltinis(boolean Vykdyti_komanda, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = Failas_įrašas_pavadinimas.getText(), įrašas_p_VALUE = klasė_įrašas_pavadinimas.getText();
        darbininkas_VALUE.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Komanda(Arrays.asList("jclassc", "--target", "openjdk", "--entry", įrašas_p_VALUE,
                        "--classpath", biblioteka, "-o", "실행프로그램", 입력));
                } else if (Komanda(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteka,
                        "-d", "classes", 입력)) == 0 && Vykdyti_komanda) {
                    Komanda(Arrays.asList("java", "-cp", "classes:" + biblioteka, įrašas_p_VALUE));
                }
            } catch (Exception KLAIDA) { pranešimas(KLAIDA.toString()); }
        });
    }
    private void 멈춤() {
        Process dabartinis_prekė = Procesas_VALUE;
        if (dabartinis_prekė != null) { dabartinis_prekė.descendants().forEach(ProcessHandle::destroy); dabartinis_prekė.destroy(); }
    }
    private darbo_sritis() throws IOException {
        Files.createDirectories(작업폴더);
        Font šriftas_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        ŠALTINIS.setFont(šriftas_VALUE); Išvestis.setFont(šriftas_VALUE); Išvestis.setEditable(false);
        ŠALTINIS.setTabSize(4);
        ŠALTINIS.setMargin(new Insets(10, 12, 10, 12));
        Išvestis.setMargin(new Insets(8, 12, 8, 12));
        ŠALTINIS.setBackground(new Color(250, 251, 252));
        ŠALTINIS.setForeground(new Color(32, 43, 58));
        JPanel komanda_skydas = new JPanel();
        komanda_skydas.add(new JLabel("Failas")); komanda_skydas.add(Failas_įrašas_pavadinimas);
        komanda_skydas.add(new JLabel("주 klasė_VALUE")); komanda_skydas.add(klasė_įrašas_pavadinimas);
        mygtukas(komanda_skydas, "Atverti", this::Atverti); mygtukas(komanda_skydas, "Store_VALUE", this::Store_VALUE);
        mygtukas(komanda_skydas, "kompiliuoti_šaltinis", () -> Versti_šaltinis(false, false));
        mygtukas(komanda_skydas, "Vykdyti_komanda", () -> Versti_šaltinis(true, false));
        mygtukas(komanda_skydas, "Vykdyti_komanda Failas kurti_įrašas", () -> Versti_šaltinis(false, true));
        mygtukas(komanda_skydas, "멈춤", this::멈춤);
        JSplitPane dalyba_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ŠALTINIS), new JScrollPane(Išvestis));
        dalyba_KR.setResizeWeight(0.75);
        Langas.add(komanda_skydas, BorderLayout.NORTH); Langas.add(dalyba_KR, BorderLayout.CENTER);
        Langas.setSize(1200, 750); Langas.setLocationRelativeTo(null);
        Langas.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Langas.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Įvykis) { 멈춤(); darbininkas_VALUE.shutdownNow(); }
        });
        Atverti(); Langas.setVisible(true);
    }
    public static void main(String[] Argumentai) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource numatytasis_šriftas = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object įrašas_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(įrašas_VALUE) instanceof Font) UIManager.put(įrašas_VALUE, numatytasis_šriftas);
                }
                new darbo_sritis();
            } catch (Exception KLAIDA) { KLAIDA.printStackTrace(); }
        });
    }
}
