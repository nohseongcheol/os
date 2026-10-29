// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CUW.l_nl;
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
public final class Werkruimte {
    private final JFrame Venster = new JFrame();
    private final JTextArea broncode = new JTextArea();
    private final JTextArea tekstuitvoer = new JTextArea();
    private final JTextField pad = new JTextField("broncode.java", 26);
    private final JTextField Naam = new JTextField("broncode", 15);
    private final JTextField argumenten = new JTextField(25);
    private final Properties meldingen = new Properties();
    private final Path map = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService achtergrondwerker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Etiket(String Sleutel) {
        return meldingen.getProperty(Sleutel, Sleutel);
    }

    private void achteraan_toevoegen(String tekst) {
        SwingUtilities.invokeLater(() -> {
            tekstuitvoer.append(tekst);
            tekstuitvoer.setCaretPosition(tekstuitvoer.getDocument().getLength());
        });
    }

    private void fout(Exception exception) {
        achteraan_toevoegen(Etiket("error") + ": " + exception.toString() + "\n");
    }

    private void knop(JPanel Paneel, String Sleutel, Runnable Actie) {
        JButton knop = new JButton(Etiket(Sleutel));
        knop.addActionListener(Gebeurtenis -> Actie.run());
        Paneel.add(knop);
    }

    private void broncodeLaden() {
        try {
            broncode.setText(Files.readString(map.resolve(pad.getText()), StandardCharsets.UTF_8));
            broncode.setCaretPosition(0);
        } catch (Exception exception) { fout(exception); }
    }

    private boolean Opslaan() {
        try {
            Path bestand = map.resolve(pad.getText()).normalize();
            Files.createDirectories(bestand.getParent());
            Files.writeString(bestand, broncode.getText(), StandardCharsets.UTF_8);
            achteraan_toevoegen(Etiket("save") + ": " + bestand + "\n");
            return true;
        } catch (Exception exception) { fout(exception); return false; }
    }

    private int Uitvoeren(List<String> opdracht) throws Exception {
        Proces = new ProcessBuilder(opdracht).directory(map.toFile()).redirectErrorStream(true).start();
        try (BufferedReader tekstlezer = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String invoerregel;
            while ((invoerregel = tekstlezer.readLine()) != null) achteraan_toevoegen(invoerregel + "\n");
        }
        int resultaat = Proces.waitFor();
        Proces = null;
        achteraan_toevoegen(Etiket("result") + ": " + resultaat + "\n");
        return resultaat;
    }

    private void compileren(boolean starten) {
        if (!Opslaan()) return;
        String bestand = map.resolve(pad.getText()).toString();
        String Klasse = Naam.getText().trim();
        String tekst = argumenten.getText();
        achtergrondwerker.submit(() -> {
            try {
                Files.createDirectories(map.resolve("classes"));
                int resultaat = Uitvoeren(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", map.resolve("classes").toString(), bestand));
                if (starten && resultaat == 0) {
                    List<String> opdracht = new ArrayList<>(Arrays.asList("java", "-cp", map.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasse));
                    StreamTokenizer argumentenOntleder = new StreamTokenizer(new StringReader(tekst));
                    argumentenOntleder.resetSyntax(); argumentenOntleder.wordChars(33, 65535); argumentenOntleder.whitespaceChars(0, 32);
                    argumentenOntleder.quoteChar('"'); argumentenOntleder.quoteChar('\'');
                    while (argumentenOntleder.nextToken() != StreamTokenizer.TT_EOF) opdracht.add(argumentenOntleder.sval);
                    Uitvoeren(opdracht);
                }
            } catch (Exception exception) { fout(exception); }
        });
    }

    private void Stoppen() {
        Process huidigProces = Proces;
        if (huidigProces != null) {
            huidigProces.descendants().forEach(ProcessHandle::destroyForcibly);
            huidigProces.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(map.toFile()).start(); }
        catch (Exception exception) { fout(exception); }
    }

    private void kies() {
        JFileChooser chooser = new JFileChooser(map.toFile());
        if (chooser.showOpenDialog(Venster) == JFileChooser.APPROVE_OPTION) {
            pad.setText(chooser.getSelectedFile().getAbsolutePath());
            broncodeLaden();
        }
    }

    private void initialiseren() {
        try (Reader tekstlezer = new InputStreamReader(Werkruimte.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            meldingen.load(tekstlezer);
            Files.createDirectories(map);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Venster.setTitle(Etiket("workspace") + " · WorldOS " + Etiket("identity"));
        Venster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Venster.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Gebeurtenis) {
                Stoppen(); achtergrondwerker.shutdownNow(); System.exit(0);
            }
        });
        broncode.setFont(new Font("Monospaced", Font.PLAIN, 17));
        broncode.setTabSize(4);
        tekstuitvoer.setFont(new Font("Monospaced", Font.PLAIN, 14));
        tekstuitvoer.setEditable(false);
        JPanel Paneel = new JPanel(new GridLayout(0, 1));
        JPanel bestand = new JPanel(new FlowLayout(FlowLayout.LEADING));
        bestand.add(new JLabel(Etiket("file"))); bestand.add(pad);
        Paneel.add(bestand);
        JPanel Werkbalk = new JPanel(new FlowLayout(FlowLayout.LEADING));
        knop(Werkbalk, "open", () -> kies());
        knop(Werkbalk, "save", () -> Opslaan());
        knop(Werkbalk, "compile", () -> compileren(false));
        knop(Werkbalk, "run", () -> compileren(true));
        knop(Werkbalk, "stop", () -> Stoppen());
        knop(Werkbalk, "terminal", () -> terminal());
        Paneel.add(Werkbalk);
        JPanel Instellingen = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Instellingen.add(new JLabel(Etiket("class"))); Instellingen.add(Naam);
        Instellingen.add(new JLabel(Etiket("arguments"))); Instellingen.add(argumenten);
        Paneel.add(Instellingen);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(broncode), new JScrollPane(tekstuitvoer));
        split.setResizeWeight(0.72);
        Venster.add(Paneel, BorderLayout.NORTH);
        Venster.add(split, BorderLayout.CENTER);
        Paneel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiket("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        broncode.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        tekstuitvoer.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Grootte = Toolkit.getDefaultToolkit().getScreenSize();
        Venster.setSize(Math.min(1240, Grootte.width - 40), Math.min(760, Grootte.height - 60));
        Venster.setLocationRelativeTo(null);
        Venster.setVisible(true);
        broncodeLaden();
        split.setDividerLocation(0.72);
        achteraan_toevoegen("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        achteraan_toevoegen(Etiket("help") + "\n");
    }

    public static void main(String[] argumenten) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Werkruimte().initialiseren());
    }
}
