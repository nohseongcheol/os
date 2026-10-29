// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BIH.l_bs;
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
public final class Workspace {
    private final JFrame window = new JFrame();
    private final JTextArea IZVOR = new JTextArea();
    private final JTextArea Ispis = new JTextArea();
    private final JTextField Putanja = new JTextField("IZVOR.java", 26);
    private final JTextField Naziv = new JTextField("IZVOR", 15);
    private final JTextField Argumenti = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Direktorij = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Oznaka(String Ključ) {
        return messages.getProperty(Ključ, Ključ);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            Ispis.append(Tekst);
            Ispis.setCaretPosition(Ispis.getDocument().getLength());
        });
    }

    private void GRESKA(Exception exception) {
        append(Oznaka("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Ploča, String Ključ, Runnable radnja) {
        JButton button = new JButton(Oznaka(Ključ));
        button.addActionListener(event -> radnja.run());
        Ploča.add(button);
    }

    private void Opterećenje() {
        try {
            IZVOR.setText(Files.readString(Direktorij.resolve(Putanja.getText()), StandardCharsets.UTF_8));
            IZVOR.setCaretPosition(0);
        } catch (Exception exception) { GRESKA(exception); }
    }

    private boolean Snimi() {
        try {
            Path Fajl = Direktorij.resolve(Putanja.getText()).normalize();
            Files.createDirectories(Fajl.getParent());
            Files.writeString(Fajl, IZVOR.getText(), StandardCharsets.UTF_8);
            append(Oznaka("save") + ": " + Fajl + "\n");
            return true;
        } catch (Exception exception) { GRESKA(exception); return false; }
    }

    private int Izvrši(List<String> Naredba) throws Exception {
        process = new ProcessBuilder(Naredba).directory(Direktorij.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String Linija;
            while ((Linija = reader.readLine()) != null) append(Linija + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Oznaka("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Pokreni) {
        if (!Snimi()) return;
        String Fajl = Direktorij.resolve(Putanja.getText()).toString();
        String klasa = Naziv.getText().trim();
        String Tekst = Argumenti.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Direktorij.resolve("classes"));
                int result = Izvrši(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Direktorij.resolve("classes").toString(), Fajl));
                if (Pokreni && result == 0) {
                    List<String> Naredba = new ArrayList<>(Arrays.asList("java", "-cp", Direktorij.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", klasa));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Naredba.add(parser.sval);
                    Izvrši(Naredba);
                }
            } catch (Exception exception) { GRESKA(exception); }
        });
    }

    private void Zaustavi() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Direktorij.toFile()).start(); }
        catch (Exception exception) { GRESKA(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Direktorij.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Putanja.setText(chooser.getSelectedFile().getAbsolutePath());
            Opterećenje();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Direktorij);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Oznaka("workspace") + " · WorldOS " + Oznaka("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Zaustavi(); worker.shutdownNow(); System.exit(0);
            }
        });
        IZVOR.setFont(new Font("Monospaced", Font.PLAIN, 17));
        IZVOR.setTabSize(4);
        Ispis.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Ispis.setEditable(false);
        JPanel Ploča = new JPanel(new GridLayout(0, 1));
        JPanel Fajl = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fajl.add(new JLabel(Oznaka("file"))); Fajl.add(Putanja);
        Ploča.add(Fajl);
        JPanel Alatna_traka = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Alatna_traka, "open", () -> choose());
        button(Alatna_traka, "save", () -> Snimi());
        button(Alatna_traka, "compile", () -> compile(false));
        button(Alatna_traka, "run", () -> compile(true));
        button(Alatna_traka, "stop", () -> Zaustavi());
        button(Alatna_traka, "terminal", () -> terminal());
        Ploča.add(Alatna_traka);
        JPanel Postavke = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Postavke.add(new JLabel(Oznaka("class"))); Postavke.add(Naziv);
        Postavke.add(new JLabel(Oznaka("arguments"))); Postavke.add(Argumenti);
        Ploča.add(Postavke);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(IZVOR), new JScrollPane(Ispis));
        split.setResizeWeight(0.72);
        window.add(Ploča, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Ploča.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Oznaka("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        IZVOR.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Ispis.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Veličina = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Veličina.width - 40), Math.min(760, Veličina.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Opterećenje();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Oznaka("help") + "\n");
    }

    public static void main(String[] Argumenti) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
