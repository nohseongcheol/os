// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ITA.l_fur;
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
    private final JTextArea Jessude = new JTextArea();
    private final JTextField Percors = new JTextField("source.java", 26);
    private final JTextField Nom = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path directory = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Test) {
        SwingUtilities.invokeLater(() -> {
            Jessude.append(Test);
            Jessude.setCaretPosition(Jessude.getDocument().getLength());
        });
    }

    private void Erôr(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Azion) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Azion.run());
        panel.add(button);
    }

    private void load() {
        try {
            source.setText(Files.readString(directory.resolve(Percors.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Erôr(exception); }
    }

    private boolean Salve() {
        try {
            Path file = directory.resolve(Percors.getText()).normalize();
            Files.createDirectories(file.getParent());
            Files.writeString(file, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + file + "\n");
            return true;
        } catch (Exception exception) { Erôr(exception); return false; }
    }

    private int execute(List<String> Comant) throws Exception {
        process = new ProcessBuilder(Comant).directory(directory.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Eseguis) {
        if (!Salve()) return;
        String file = directory.resolve(Percors.getText()).toString();
        String className = Nom.getText().trim();
        String Test = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(directory.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", directory.resolve("classes").toString(), file));
                if (Eseguis && result == 0) {
                    List<String> Comant = new ArrayList<>(Arrays.asList("java", "-cp", directory.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Test));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Comant.add(parser.sval);
                    execute(Comant);
                }
            } catch (Exception exception) { Erôr(exception); }
        });
    }

    private void Ferme() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Terminâl() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(directory.toFile()).start(); }
        catch (Exception exception) { Erôr(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(directory.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Percors.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(directory);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Ferme(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        Jessude.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Jessude.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel file = new JPanel(new FlowLayout(FlowLayout.LEADING));
        file.add(new JLabel(label("file"))); file.add(Percors);
        panel.add(file);
        JPanel Bare_dai_imprescj = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Bare_dai_imprescj, "open", () -> choose());
        button(Bare_dai_imprescj, "save", () -> Salve());
        button(Bare_dai_imprescj, "compile", () -> compile(false));
        button(Bare_dai_imprescj, "run", () -> compile(true));
        button(Bare_dai_imprescj, "stop", () -> Ferme());
        button(Bare_dai_imprescj, "terminal", () -> Terminâl());
        panel.add(Bare_dai_imprescj);
        JPanel Impostazions = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Impostazions.add(new JLabel(label("class"))); Impostazions.add(Nom);
        Impostazions.add(new JLabel(label("arguments"))); Impostazions.add(arguments);
        panel.add(Impostazions);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(Jessude));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Jessude.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Dimension = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Dimension.width - 40), Math.min(760, Dimension.height - 60));
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
