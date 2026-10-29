// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PRY.l_de;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;

/** WorldOS project-owned source. Standard Java API names are preserved. */
public final class Arbeitsplatz {
    private final JFrame Fenster = new JFrame();
    private final JTextArea Quelltext = new JTextArea();
    private final JTextArea Ausgabe = new JTextArea();
    private final JTextField Pfad = new JTextField("Quelltext.java", 26);
    private final JTextField Name = new JTextField("Quelltext", 15);
    private final JTextField Argumente = new JTextField(25);
    private final Properties Meldungen = new Properties();
    private final Path Verzeichnis = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService Arbeitsfaden = Executors.newSingleThreadExecutor();
    private volatile Process Prozess;

    private String Beschriftung(String Schlüssel) {
        return Meldungen.getProperty(Schlüssel, Schlüssel);
    }

    private void anhängen(String Text) {
        SwingUtilities.invokeLater(() -> {
            Ausgabe.append(Text);
            Ausgabe.setCaretPosition(Ausgabe.getDocument().getLength());
        });
    }

    private void Fehler(Exception Ausnahme) {
        anhängen(Beschriftung("error") + ": " + Ausnahme.toString() + "\n");
    }

    private void Schaltfläche(JPanel Bereich, String Schlüssel, Runnable Aktion) {
        JButton Schaltfläche = new JButton(Beschriftung(Schlüssel));
        Schaltfläche.addActionListener(Ereignis -> Aktion.run());
        Bereich.add(Schaltfläche);
    }

    private void laden() {
        try {
            Quelltext.setText(Files.readString(Verzeichnis.resolve(Pfad.getText()), StandardCharsets.UTF_8));
            Quelltext.setCaretPosition(0);
        } catch (Exception Ausnahme) { Fehler(Ausnahme); }
    }

    private boolean speichern() {
        try {
            Path Datei = Verzeichnis.resolve(Pfad.getText()).normalize();
            Files.createDirectories(Datei.getParent());
            Files.writeString(Datei, Quelltext.getText(), StandardCharsets.UTF_8);
            anhängen(Beschriftung("save") + ": " + Datei + "\n");
            return true;
        } catch (Exception Ausnahme) { Fehler(Ausnahme); return false; }
    }

    private int ausführen(List<String> Befehl) throws Exception {
        Prozess = new ProcessBuilder(Befehl).directory(Verzeichnis.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Leser = new BufferedReader(new InputStreamReader(Prozess.getInputStream(), StandardCharsets.UTF_8))) {
            String Zeile;
            while ((Zeile = Leser.readLine()) != null) anhängen(Zeile + "\n");
        }
        int Ergebnis = Prozess.waitFor();
        Prozess = null;
        anhängen(Beschriftung("result") + ": " + Ergebnis + "\n");
        return Ergebnis;
    }

    private void übersetzen(boolean starten) {
        if (!speichern()) return;
        String Datei = Verzeichnis.resolve(Pfad.getText()).toString();
        String Klassenname = Name.getText().trim();
        String Text = Argumente.getText();
        Arbeitsfaden.submit(() -> {
            try {
                Files.createDirectories(Verzeichnis.resolve("classes"));
                int Ergebnis = ausführen(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Verzeichnis.resolve("classes").toString(), Datei));
                if (starten && Ergebnis == 0) {
                    List<String> Befehl = new ArrayList<>(Arrays.asList("java", "-cp", Verzeichnis.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klassenname));
                    StreamTokenizer Syntaxleser = new StreamTokenizer(new StringReader(Text));
                    Syntaxleser.resetSyntax(); Syntaxleser.wordChars(33, 65535); Syntaxleser.whitespaceChars(0, 32);
                    Syntaxleser.quoteChar('"'); Syntaxleser.quoteChar('\'');
                    while (Syntaxleser.nextToken() != StreamTokenizer.TT_EOF) Befehl.add(Syntaxleser.sval);
                    ausführen(Befehl);
                }
            } catch (Exception Ausnahme) { Fehler(Ausnahme); }
        });
    }

    private void anhalten() {
        Process aktuellerProzess = Prozess;
        if (aktuellerProzess != null) {
            aktuellerProzess.descendants().forEach(ProcessHandle::destroyForcibly);
            aktuellerProzess.destroyForcibly();
        }
    }

    private void Befehlsfenster() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Verzeichnis.toFile()).start(); }
        catch (Exception Ausnahme) { Fehler(Ausnahme); }
    }

    private void auswählen() {
        JFileChooser Auswahlfenster = new JFileChooser(Verzeichnis.toFile());
        if (Auswahlfenster.showOpenDialog(Fenster) == JFileChooser.APPROVE_OPTION) {
            Pfad.setText(Auswahlfenster.getSelectedFile().getAbsolutePath());
            laden();
        }
    }

    private void vorbereiten() {
        try (Reader Leser = new InputStreamReader(Arbeitsplatz.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            Meldungen.load(Leser);
            Files.createDirectories(Verzeichnis);
        } catch (Exception Ausnahme) { throw new IllegalStateException(Ausnahme); }
        Fenster.setTitle(Beschriftung("workspace") + " · WorldOS " + Beschriftung("identity"));
        Fenster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fenster.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Ereignis) {
                anhalten(); Arbeitsfaden.shutdownNow(); System.exit(0);
            }
        });
        Quelltext.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Quelltext.setTabSize(4);
        Ausgabe.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Ausgabe.setEditable(false);
        JPanel Bereich = new JPanel(new GridLayout(0, 1));
        JPanel Datei = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Datei.add(new JLabel(Beschriftung("file"))); Datei.add(Pfad);
        Bereich.add(Datei);
        JPanel Werkzeugleiste = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Schaltfläche(Werkzeugleiste, "open", () -> auswählen());
        Schaltfläche(Werkzeugleiste, "save", () -> speichern());
        Schaltfläche(Werkzeugleiste, "compile", () -> übersetzen(false));
        Schaltfläche(Werkzeugleiste, "run", () -> übersetzen(true));
        Schaltfläche(Werkzeugleiste, "stop", () -> anhalten());
        Schaltfläche(Werkzeugleiste, "terminal", () -> Befehlsfenster());
        Bereich.add(Werkzeugleiste);
        JPanel Einstellungen = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Einstellungen.add(new JLabel(Beschriftung("class"))); Einstellungen.add(Name);
        Einstellungen.add(new JLabel(Beschriftung("arguments"))); Einstellungen.add(Argumente);
        Bereich.add(Einstellungen);
        JSplitPane teilen = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Quelltext), new JScrollPane(Ausgabe));
        teilen.setResizeWeight(0.72);
        Fenster.add(Bereich, BorderLayout.NORTH);
        Fenster.add(teilen, BorderLayout.CENTER);
        Bereich.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Beschriftung("locale"))));
        teilen.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Quelltext.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Ausgabe.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Größe = Toolkit.getDefaultToolkit().getScreenSize();
        Fenster.setSize(Math.min(1240, Größe.width - 40), Math.min(760, Größe.height - 60));
        Fenster.setLocationRelativeTo(null);
        Fenster.setVisible(true);
        laden();
        teilen.setDividerLocation(0.72);
        anhängen("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        anhängen(Beschriftung("help") + "\n");
    }

    public static void main(String[] Argumente) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Arbeitsplatz().vorbereiten());
    }
}
