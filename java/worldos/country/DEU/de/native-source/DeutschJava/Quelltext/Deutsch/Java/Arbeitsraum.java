// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.Java;

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

/** Kleine Swing-Arbeitsumgebung zum Bearbeiten, Übersetzen und Ausführen von Java-Quellen im Benutzerverzeichnis. */
public final class Arbeitsraum {
    private final JFrame fenster = new JFrame("jkoros — Java Arbeitsraum");
    private final JTextArea Quelltext = new JTextArea();
    private final JTextArea Ausgabe = new JTextArea(8, 80);
    private final JTextField dateiEintragName = new JTextField("Gruß.java", 20);
    private final JTextField klasseEintragName = new JTextField("Gruß", 16);
    private final Path arbeitendVerzeichnis = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService hintergrundarbeiterWert = Executors.newSingleThreadExecutor();
    private volatile Process prozessWert;
    private final String bibliothek = "/opt/jkoros/lib/DeutschJava.jar";

    private void mitteilung(String Text) { SwingUtilities.invokeLater(() -> Ausgabe.append(Text + "\n")); }
    private void schaltfläche(JPanel versionWert, String Name, Runnable verhaltenWert) {
        JButton schaltfläche = new JButton(Name);
        schaltfläche.addActionListener(ereignis -> verhaltenWert.run());
        versionWert.add(schaltfläche);
    }
    private boolean ablegenDatenWert() {
        try {
            Path pfad = arbeitendVerzeichnis.resolve(dateiEintragName.getText());
            Files.createDirectories(pfad.getParent());
            Datei.schreiben(pfad, Quelltext.getText());
            mitteilung("ablegenDatenWert: " + pfad);
            return true;
        } catch (Exception fehler) { mitteilung(fehler.toString()); return false; }
    }
    private void öffnen() {
        try { Quelltext.setText(Datei.lesen(arbeitendVerzeichnis.resolve(dateiEintragName.getText()))); }
        catch (Exception fehler) { mitteilung(fehler.toString()); }
    }
    private int befehl(List<String> befehl) throws Exception {
        prozessWert = new ProcessBuilder(befehl).directory(arbeitendVerzeichnis.toFile()).redirectErrorStream(true).start();
        try (BufferedReader zeile = new BufferedReader(new InputStreamReader(prozessWert.getInputStream(), StandardCharsets.UTF_8))) {
            String Text;
            while ((Text = zeile.readLine()) != null) mitteilung(Text);
        }
        int statuswertWert = prozessWert.waitFor(); prozessWert = null;
        mitteilung("verlassenProzessProgramm kodeWert: " + statuswertWert);
        return statuswertWert;
    }
    private void quelltextÜbersetzenText(boolean befehlAusführen, boolean ausführdateiDatei) {
        if (!ablegenDatenWert()) return;
        String Eingabewert = dateiEintragName.getText(), eintragPunktWert = klasseEintragName.getText();
        hintergrundarbeiterWert.submit(() -> {
            try {
                Files.createDirectories(arbeitendVerzeichnis.resolve("classes"));
                if (ausführdateiDatei) {
                    befehl(Arrays.asList("jclassc", "--target", "openjdk", "--entry", eintragPunktWert,
                        "--classpath", bibliothek, "-o", "실행프로그램", Eingabewert));
                } else if (befehl(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliothek,
                        "-d", "classes", Eingabewert)) == 0 && befehlAusführen) {
                    befehl(Arrays.asList("java", "-cp", "classes:" + bibliothek, eintragPunktWert));
                }
            } catch (Exception fehler) { mitteilung(fehler.toString()); }
        });
    }
    private void pausierenAusführung() {
        Process aktuellElementeintrag = prozessWert;
        if (aktuellElementeintrag != null) { aktuellElementeintrag.descendants().forEach(ProcessHandle::destroy); aktuellElementeintrag.destroy(); }
    }
    private Arbeitsraum() throws IOException {
        Files.createDirectories(arbeitendVerzeichnis);
        Font schriftartWert = new Font("Monospaced", Font.PLAIN, 16);
        Quelltext.setFont(schriftartWert); Ausgabe.setFont(schriftartWert); Ausgabe.setEditable(false);
        Quelltext.setTabSize(4);
        Quelltext.setMargin(new Insets(10, 12, 10, 12));
        Ausgabe.setMargin(new Insets(8, 12, 8, 12));
        Quelltext.setBackground(new Color(250, 251, 252));
        Quelltext.setForeground(new Color(32, 43, 58));
        JPanel befehlBedienfeld = new JPanel();
        befehlBedienfeld.add(new JLabel("Datei")); befehlBedienfeld.add(dateiEintragName);
        befehlBedienfeld.add(new JLabel("주 klasseWert")); befehlBedienfeld.add(klasseEintragName);
        schaltfläche(befehlBedienfeld, "öffnen", this::öffnen); schaltfläche(befehlBedienfeld, "ablegenDatenWert", this::ablegenDatenWert);
        schaltfläche(befehlBedienfeld, "quelltextÜbersetzen", () -> quelltextÜbersetzenText(false, false));
        schaltfläche(befehlBedienfeld, "befehlAusführen", () -> quelltextÜbersetzenText(true, false));
        schaltfläche(befehlBedienfeld, "befehlAusführen Datei eintragErstellen", () -> quelltextÜbersetzenText(false, true));
        schaltfläche(befehlBedienfeld, "pausierenAusführung", this::pausierenAusführung);
        JSplitPane divisionErgebnis = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Quelltext), new JScrollPane(Ausgabe));
        divisionErgebnis.setResizeWeight(0.75);
        fenster.add(befehlBedienfeld, BorderLayout.NORTH); fenster.add(divisionErgebnis, BorderLayout.CENTER);
        fenster.setSize(1200, 750); fenster.setLocationRelativeTo(null);
        fenster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fenster.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ereignis) { pausierenAusführung(); hintergrundarbeiterWert.shutdownNow(); }
        });
        öffnen(); fenster.setVisible(true);
    }
    public static void main(String[] argumente) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standardwertSchriftart = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object eintragWert : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(eintragWert) instanceof Font) UIManager.put(eintragWert, standardwertSchriftart);
                }
                new Arbeitsraum();
            } catch (Exception fehler) { fehler.printStackTrace(); }
        });
    }
}
