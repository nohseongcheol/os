// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.자바;

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

/** gebruikersruimte 홈에서 Java 원문을 Bewerk_WAARDE·compileren_bron·실행하는 작은 Swing werkgebied. */
public final class werkgebied {
    private final JFrame Venster = new JFrame("jkoros — 자바 werkgebied");
    private final JTextArea broncode = new JTextArea();
    private final JTextArea tekstuitvoer = new JTextArea(8, 80);
    private final JTextField Bestand_invoer_naam = new JTextField("인사.java", 20);
    private final JTextField les_invoer_naam = new JTextField("인사", 16);
    private final Path werkmap = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService werkrol_WAARDE = Executors.newSingleThreadExecutor();
    private volatile Process Proces_WAARDE;
    private final String bibliotheek = "/opt/jkoros/lib/한국어자바.jar";

    private void kennisgeving(String tekst) { SwingUtilities.invokeLater(() -> tekstuitvoer.append(tekst + "\n")); }
    private void knop(JPanel versie_WAARDE, String Naam, Runnable 행동) {
        JButton knop = new JButton(Naam);
        knop.addActionListener(Gebeurtenis -> 행동.run());
        versie_WAARDE.add(knop);
    }
    private boolean Store_WAARDE() {
        try {
            Path pad = werkmap.resolve(Bestand_invoer_naam.getText());
            Files.createDirectories(pad.getParent());
            bestand.Schrijven(pad, broncode.getText());
            kennisgeving("Store_WAARDE: " + pad);
            return true;
        } catch (Exception fout) { kennisgeving(fout.toString()); return false; }
    }
    private void Openen() {
        try { broncode.setText(bestand.Lezen(werkmap.resolve(Bestand_invoer_naam.getText()))); }
        catch (Exception fout) { kennisgeving(fout.toString()); }
    }
    private int opdracht(List<String> opdracht) throws Exception {
        Proces_WAARDE = new ProcessBuilder(opdracht).directory(werkmap.toFile()).redirectErrorStream(true).start();
        try (BufferedReader invoerregel = new BufferedReader(new InputStreamReader(Proces_WAARDE.getInputStream(), StandardCharsets.UTF_8))) {
            String tekst;
            while ((tekst = invoerregel.readLine()) != null) kennisgeving(tekst);
        }
        int Status_WAARDE = Proces_WAARDE.waitFor(); Proces_WAARDE = null;
        kennisgeving("Einde_app CODE_WAARDE: " + Status_WAARDE);
        return Status_WAARDE;
    }
    private void VERTALEN_bron(boolean Uitvoeren_opdracht, boolean uitvoerbaar_bestand) {
        if (!Store_WAARDE()) return;
        String invoer_WAARDE = Bestand_invoer_naam.getText(), beginpunt_WAARDE = les_invoer_naam.getText();
        werkrol_WAARDE.submit(() -> {
            try {
                Files.createDirectories(werkmap.resolve("classes"));
                if (uitvoerbaar_bestand) {
                    opdracht(Arrays.asList("jclassc", "--target", "openjdk", "--entry", beginpunt_WAARDE,
                        "--classpath", bibliotheek, "-o", "실행프로그램", invoer_WAARDE));
                } else if (opdracht(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotheek,
                        "-d", "classes", invoer_WAARDE)) == 0 && Uitvoeren_opdracht) {
                    opdracht(Arrays.asList("java", "-cp", "classes:" + bibliotheek, beginpunt_WAARDE));
                }
            } catch (Exception fout) { kennisgeving(fout.toString()); }
        });
    }
    private void Onderbreken_uitvoerbewerking() {
        Process actueel_item = Proces_WAARDE;
        if (actueel_item != null) { actueel_item.descendants().forEach(ProcessHandle::destroy); actueel_item.destroy(); }
    }
    private werkgebied() throws IOException {
        Files.createDirectories(werkmap);
        Font lettertype_WAARDE = new Font("Monospaced", Font.PLAIN, 16);
        broncode.setFont(lettertype_WAARDE); tekstuitvoer.setFont(lettertype_WAARDE); tekstuitvoer.setEditable(false);
        broncode.setTabSize(4);
        broncode.setMargin(new Insets(10, 12, 10, 12));
        tekstuitvoer.setMargin(new Insets(8, 12, 8, 12));
        broncode.setBackground(new Color(250, 251, 252));
        broncode.setForeground(new Color(32, 43, 58));
        JPanel opdracht_paneel = new JPanel();
        opdracht_paneel.add(new JLabel("bestand")); opdracht_paneel.add(Bestand_invoer_naam);
        opdracht_paneel.add(new JLabel("주 les_WAARDE")); opdracht_paneel.add(les_invoer_naam);
        knop(opdracht_paneel, "Openen", this::Openen); knop(opdracht_paneel, "Store_WAARDE", this::Store_WAARDE);
        knop(opdracht_paneel, "compileren_bron", () -> VERTALEN_bron(false, false));
        knop(opdracht_paneel, "Uitvoeren_opdracht", () -> VERTALEN_bron(true, false));
        knop(opdracht_paneel, "Uitvoeren_opdracht bestand maken_invoer", () -> VERTALEN_bron(false, true));
        knop(opdracht_paneel, "Onderbreken_uitvoerbewerking", this::Onderbreken_uitvoerbewerking);
        JSplitPane deling_HR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(broncode), new JScrollPane(tekstuitvoer));
        deling_HR.setResizeWeight(0.75);
        Venster.add(opdracht_paneel, BorderLayout.NORTH); Venster.add(deling_HR, BorderLayout.CENTER);
        Venster.setSize(1200, 750); Venster.setLocationRelativeTo(null);
        Venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Venster.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Gebeurtenis) { Onderbreken_uitvoerbewerking(); werkrol_WAARDE.shutdownNow(); }
        });
        Openen(); Venster.setVisible(true);
    }
    public static void main(String[] argumenten) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standaardlettertype = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object invoer_WAARDE_962f286b : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(invoer_WAARDE_962f286b) instanceof Font) UIManager.put(invoer_WAARDE_962f286b, standaardlettertype);
                }
                new werkgebied();
            } catch (Exception fout) { fout.printStackTrace(); }
        });
    }
}
