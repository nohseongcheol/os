// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.자바;

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

/** používateľ 홈에서 Java 원문을 úprava_VALUE·kompilovať_zdroj·실행하는 작은 Swing pracovný_priestor. */
public final class pracovný_priestor {
    private final JFrame Okno = new JFrame("jkoros — 자바 pracovný_priestor");
    private final JTextArea ZDROJ = new JTextArea();
    private final JTextArea Výstup = new JTextArea(8, 80);
    private final JTextField Súbor_položka_názov = new JTextField("인사.java", 20);
    private final JTextField lekcia_položka_názov = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VALUE;
    private final String knižnica = "/opt/jkoros/lib/한국어자바.jar";

    private void upozornenie(String Spracovanie_textu) { SwingUtilities.invokeLater(() -> Výstup.append(Spracovanie_textu + "\n")); }
    private void Tlačidlo(JPanel verzia_VALUE, String Názov, Runnable 행동) {
        JButton Tlačidlo = new JButton(Názov);
        Tlačidlo.addActionListener(Udalosť -> 행동.run());
        verzia_VALUE.add(Tlačidlo);
    }
    private boolean Store_VALUE() {
        try {
            Path Cesta = 작업폴더.resolve(Súbor_položka_názov.getText());
            Files.createDirectories(Cesta.getParent());
            Súbor.Zápis(Cesta, ZDROJ.getText());
            upozornenie("Store_VALUE: " + Cesta);
            return true;
        } catch (Exception chyba) { upozornenie(chyba.toString()); return false; }
    }
    private void Otvoriť() {
        try { ZDROJ.setText(Súbor.Čítanie(작업폴더.resolve(Súbor_položka_názov.getText()))); }
        catch (Exception chyba) { upozornenie(chyba.toString()); }
    }
    private int Príkaz(List<String> Príkaz) throws Exception {
        Proces_VALUE = new ProcessBuilder(Príkaz).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader riadok = new BufferedReader(new InputStreamReader(Proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Spracovanie_textu;
            while ((Spracovanie_textu = riadok.readLine()) != null) upozornenie(Spracovanie_textu);
        }
        int Stav_VALUE = Proces_VALUE.waitFor(); Proces_VALUE = null;
        upozornenie("Skončiť_program kód_VALUE: " + Stav_VALUE);
        return Stav_VALUE;
    }
    private void Preložiť_zdroj(boolean Vykonať_príkaz, boolean spustiteľný_súbor) {
        if (!Store_VALUE()) return;
        String vstup_VALUE = Súbor_položka_názov.getText(), položka_bod_VALUE = lekcia_položka_názov.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (spustiteľný_súbor) {
                    Príkaz(Arrays.asList("jclassc", "--target", "openjdk", "--entry", položka_bod_VALUE,
                        "--classpath", knižnica, "-o", "실행프로그램", vstup_VALUE));
                } else if (Príkaz(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", knižnica,
                        "-d", "classes", vstup_VALUE)) == 0 && Vykonať_príkaz) {
                    Príkaz(Arrays.asList("java", "-cp", "classes:" + knižnica, položka_bod_VALUE));
                }
            } catch (Exception chyba) { upozornenie(chyba.toString()); }
        });
    }
    private void 멈춤() {
        Process v_termíne_splatnosti_položka = Proces_VALUE;
        if (v_termíne_splatnosti_položka != null) { v_termíne_splatnosti_položka.descendants().forEach(ProcessHandle::destroy); v_termíne_splatnosti_položka.destroy(); }
    }
    private pracovný_priestor() throws IOException {
        Files.createDirectories(작업폴더);
        Font písmo_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        ZDROJ.setFont(písmo_VALUE); Výstup.setFont(písmo_VALUE); Výstup.setEditable(false);
        ZDROJ.setTabSize(4);
        ZDROJ.setMargin(new Insets(10, 12, 10, 12));
        Výstup.setMargin(new Insets(8, 12, 8, 12));
        ZDROJ.setBackground(new Color(250, 251, 252));
        ZDROJ.setForeground(new Color(32, 43, 58));
        JPanel príkaz_panel = new JPanel();
        príkaz_panel.add(new JLabel("Súbor")); príkaz_panel.add(Súbor_položka_názov);
        príkaz_panel.add(new JLabel("주 lekcia_VALUE")); príkaz_panel.add(lekcia_položka_názov);
        Tlačidlo(príkaz_panel, "Otvoriť", this::Otvoriť); Tlačidlo(príkaz_panel, "Store_VALUE", this::Store_VALUE);
        Tlačidlo(príkaz_panel, "kompilovať_zdroj", () -> Preložiť_zdroj(false, false));
        Tlačidlo(príkaz_panel, "Vykonať_príkaz", () -> Preložiť_zdroj(true, false));
        Tlačidlo(príkaz_panel, "Vykonať_príkaz Súbor Create_položka", () -> Preložiť_zdroj(false, true));
        Tlačidlo(príkaz_panel, "멈춤", this::멈춤);
        JSplitPane delenie_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ZDROJ), new JScrollPane(Výstup));
        delenie_KR.setResizeWeight(0.75);
        Okno.add(príkaz_panel, BorderLayout.NORTH); Okno.add(delenie_KR, BorderLayout.CENTER);
        Okno.setSize(1200, 750); Okno.setLocationRelativeTo(null);
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Udalosť) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Otvoriť(); Okno.setVisible(true);
    }
    public static void main(String[] Argumenty) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource predvolené_písmo = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object položka_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(položka_VALUE) instanceof Font) UIManager.put(položka_VALUE, predvolené_písmo);
                }
                new pracovný_priestor();
            } catch (Exception chyba) { chyba.printStackTrace(); }
        });
    }
}
