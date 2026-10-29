// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_frp;
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
    private final JTextArea source = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField path = new JTextField("source.java", 26);
    private final JTextField Nom = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Menû_dos_repetères = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String text) {
        SwingUtilities.invokeLater(() -> {
            output.append(text);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Erròr(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Pancarta, String key, Runnable action) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> action.run());
        Pancarta.add(button);
    }

    private void load() {
        try {
            source.setText(Files.readString(Menû_dos_repetères.resolve(path.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Erròr(exception); }
    }

    private boolean save() {
        try {
            Path FICHIÉR = Menû_dos_repetères.resolve(path.getText()).normalize();
            Files.createDirectories(FICHIÉR.getParent());
            Files.writeString(FICHIÉR, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + FICHIÉR + "\n");
            return true;
        } catch (Exception exception) { Erròr(exception); return false; }
    }

    private int execute(List<String> Comanda) throws Exception {
        process = new ProcessBuilder(Comanda).directory(Menû_dos_repetères.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Emprendre) {
        if (!save()) return;
        String FICHIÉR = Menû_dos_repetères.resolve(path.getText()).toString();
        String className = Nom.getText().trim();
        String text = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Menû_dos_repetères.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Menû_dos_repetères.resolve("classes").toString(), FICHIÉR));
                if (Emprendre && result == 0) {
                    List<String> Comanda = new ArrayList<>(Arrays.asList("java", "-cp", Menû_dos_repetères.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Comanda.add(parser.sval);
                    execute(Comanda);
                }
            } catch (Exception exception) { Erròr(exception); }
        });
    }

    private void Arretar() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Tèrminâl() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Menû_dos_repetères.toFile()).start(); }
        catch (Exception exception) { Erròr(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Menû_dos_repetères.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Menû_dos_repetères);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Arretar(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Pancarta = new JPanel(new GridLayout(0, 1));
        JPanel FICHIÉR = new JPanel(new FlowLayout(FlowLayout.LEADING));
        FICHIÉR.add(new JLabel(label("file"))); FICHIÉR.add(path);
        Pancarta.add(FICHIÉR);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(toolbar, "open", () -> choose());
        button(toolbar, "save", () -> save());
        button(toolbar, "compile", () -> compile(false));
        button(toolbar, "run", () -> compile(true));
        button(toolbar, "stop", () -> Arretar());
        button(toolbar, "terminal", () -> Tèrminâl());
        Pancarta.add(toolbar);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(Nom);
        settings.add(new JLabel(label("arguments"))); settings.add(arguments);
        Pancarta.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Pancarta, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Pancarta.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Talyi = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Talyi.width - 40), Math.min(760, Talyi.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
