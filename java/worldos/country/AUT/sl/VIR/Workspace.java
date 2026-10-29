// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.AUT.l_sl;
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
    private final JTextArea VIR = new JTextArea();
    private final JTextArea Izpis = new JTextArea();
    private final JTextField POT = new JTextField("VIR.java", 26);
    private final JTextField Ime = new JTextField("VIR", 15);
    private final JTextField Argumenti = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Mapa = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Opravilo;

    private String Oznaka(String Ključ) {
        return messages.getProperty(Ključ, Ključ);
    }

    private void append(String Besedilo) {
        SwingUtilities.invokeLater(() -> {
            Izpis.append(Besedilo);
            Izpis.setCaretPosition(Izpis.getDocument().getLength());
        });
    }

    private void NAPAKA(Exception exception) {
        append(Oznaka("error") + ": " + exception.toString() + "\n");
    }

    private void Gumb(JPanel Pult, String Ključ, Runnable Dejanje) {
        JButton Gumb = new JButton(Oznaka(Ključ));
        Gumb.addActionListener(event -> Dejanje.run());
        Pult.add(Gumb);
    }

    private void Obremenjenost() {
        try {
            VIR.setText(Files.readString(Mapa.resolve(POT.getText()), StandardCharsets.UTF_8));
            VIR.setCaretPosition(0);
        } catch (Exception exception) { NAPAKA(exception); }
    }

    private boolean Shrani() {
        try {
            Path Datoteka = Mapa.resolve(POT.getText()).normalize();
            Files.createDirectories(Datoteka.getParent());
            Files.writeString(Datoteka, VIR.getText(), StandardCharsets.UTF_8);
            append(Oznaka("save") + ": " + Datoteka + "\n");
            return true;
        } catch (Exception exception) { NAPAKA(exception); return false; }
    }

    private int Izvedi(List<String> Ukaz) throws Exception {
        Opravilo = new ProcessBuilder(Ukaz).directory(Mapa.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Opravilo.getInputStream(), StandardCharsets.UTF_8))) {
            String Črtni;
            while ((Črtni = reader.readLine()) != null) append(Črtni + "\n");
        }
        int REZULTAT = Opravilo.waitFor();
        Opravilo = null;
        append(Oznaka("result") + ": " + REZULTAT + "\n");
        return REZULTAT;
    }

    private void compile(boolean Zaženi) {
        if (!Shrani()) return;
        String Datoteka = Mapa.resolve(POT.getText()).toString();
        String Razred = Ime.getText().trim();
        String Besedilo = Argumenti.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Mapa.resolve("classes"));
                int REZULTAT = Izvedi(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Mapa.resolve("classes").toString(), Datoteka));
                if (Zaženi && REZULTAT == 0) {
                    List<String> Ukaz = new ArrayList<>(Arrays.asList("java", "-cp", Mapa.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Razred));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Besedilo));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Ukaz.add(parser.sval);
                    Izvedi(Ukaz);
                }
            } catch (Exception exception) { NAPAKA(exception); }
        });
    }

    private void Zaustavi() {
        Process current = Opravilo;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Mapa.toFile()).start(); }
        catch (Exception exception) { NAPAKA(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Mapa.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            POT.setText(chooser.getSelectedFile().getAbsolutePath());
            Obremenjenost();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Mapa);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Oznaka("workspace") + " · WorldOS " + Oznaka("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Zaustavi(); worker.shutdownNow(); System.exit(0);
            }
        });
        VIR.setFont(new Font("Monospaced", Font.PLAIN, 17));
        VIR.setTabSize(4);
        Izpis.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Izpis.setEditable(false);
        JPanel Pult = new JPanel(new GridLayout(0, 1));
        JPanel Datoteka = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Datoteka.add(new JLabel(Oznaka("file"))); Datoteka.add(POT);
        Pult.add(Datoteka);
        JPanel Orodna_vrstica = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Gumb(Orodna_vrstica, "open", () -> choose());
        Gumb(Orodna_vrstica, "save", () -> Shrani());
        Gumb(Orodna_vrstica, "compile", () -> compile(false));
        Gumb(Orodna_vrstica, "run", () -> compile(true));
        Gumb(Orodna_vrstica, "stop", () -> Zaustavi());
        Gumb(Orodna_vrstica, "terminal", () -> Terminal());
        Pult.add(Orodna_vrstica);
        JPanel Nastavitve = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Nastavitve.add(new JLabel(Oznaka("class"))); Nastavitve.add(Ime);
        Nastavitve.add(new JLabel(Oznaka("arguments"))); Nastavitve.add(Argumenti);
        Pult.add(Nastavitve);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(VIR), new JScrollPane(Izpis));
        split.setResizeWeight(0.72);
        window.add(Pult, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Pult.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Oznaka("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        VIR.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Izpis.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Velikost = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Velikost.width - 40), Math.min(760, Velikost.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Obremenjenost();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Oznaka("help") + "\n");
    }

    public static void main(String[] Argumenti) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
