// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_nds;
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
    private final JTextArea Born = new JTextArea();
    private final JTextArea Utgaav = new JTextArea();
    private final JTextField PADD = new JTextField("Born.java", 26);
    private final JTextField Naam = new JTextField("Born", 15);
    private final JTextField Argumenten = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Orner = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Prozess;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Text) {
        SwingUtilities.invokeLater(() -> {
            Utgaav.append(Text);
            Utgaav.setCaretPosition(Utgaav.getDocument().getLength());
        });
    }

    private void Fehler(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Balken, String key, Runnable Akschoon) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Akschoon.run());
        Balken.add(button);
    }

    private void load() {
        try {
            Born.setText(Files.readString(Orner.resolve(PADD.getText()), StandardCharsets.UTF_8));
            Born.setCaretPosition(0);
        } catch (Exception exception) { Fehler(exception); }
    }

    private boolean Spiekern() {
        try {
            Path Datei = Orner.resolve(PADD.getText()).normalize();
            Files.createDirectories(Datei.getParent());
            Files.writeString(Datei, Born.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Datei + "\n");
            return true;
        } catch (Exception exception) { Fehler(exception); return false; }
    }

    private int Utföhren(List<String> Order) throws Exception {
        Prozess = new ProcessBuilder(Order).directory(Orner.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Prozess.getInputStream(), StandardCharsets.UTF_8))) {
            String Reeg;
            while ((Reeg = reader.readLine()) != null) append(Reeg + "\n");
        }
        int result = Prozess.waitFor();
        Prozess = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Starte) {
        if (!Spiekern()) return;
        String Datei = Orner.resolve(PADD.getText()).toString();
        String Klass = Naam.getText().trim();
        String Text = Argumenten.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Orner.resolve("classes"));
                int result = Utföhren(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Orner.resolve("classes").toString(), Datei));
                if (Starte && result == 0) {
                    List<String> Order = new ArrayList<>(Arrays.asList("java", "-cp", Orner.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klass));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Order.add(parser.sval);
                    Utföhren(Order);
                }
            } catch (Exception exception) { Fehler(exception); }
        });
    }

    private void Anhollen() {
        Process current = Prozess;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Konsool() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Orner.toFile()).start(); }
        catch (Exception exception) { Fehler(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Orner.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            PADD.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Orner);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Anhollen(); worker.shutdownNow(); System.exit(0);
            }
        });
        Born.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Born.setTabSize(4);
        Utgaav.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Utgaav.setEditable(false);
        JPanel Balken = new JPanel(new GridLayout(0, 1));
        JPanel Datei = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Datei.add(new JLabel(label("file"))); Datei.add(PADD);
        Balken.add(Datei);
        JPanel Warktüügbalken = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Warktüügbalken, "open", () -> choose());
        button(Warktüügbalken, "save", () -> Spiekern());
        button(Warktüügbalken, "compile", () -> compile(false));
        button(Warktüügbalken, "run", () -> compile(true));
        button(Warktüügbalken, "stop", () -> Anhollen());
        button(Warktüügbalken, "terminal", () -> Konsool());
        Balken.add(Warktüügbalken);
        JPanel Instellens = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Instellens.add(new JLabel(label("class"))); Instellens.add(Naam);
        Instellens.add(new JLabel(label("arguments"))); Instellens.add(Argumenten);
        Balken.add(Instellens);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Born), new JScrollPane(Utgaav));
        split.setResizeWeight(0.72);
        window.add(Balken, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Balken.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Born.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Utgaav.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Gröte = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Gröte.width - 40), Math.min(760, Gröte.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] Argumenten) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
