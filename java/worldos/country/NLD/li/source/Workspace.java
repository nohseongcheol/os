// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_li;
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
    private final JTextField Paad = new JTextField("source.java", 26);
    private final JTextField Naam = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Map = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Teks) {
        SwingUtilities.invokeLater(() -> {
            output.append(Teks);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Faeler(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Peniel, String key, Runnable action) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> action.run());
        Peniel.add(button);
    }

    private void load() {
        try {
            source.setText(Files.readString(Map.resolve(Paad.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Faeler(exception); }
    }

    private boolean Opsjlaon() {
        try {
            Path Besjtandj = Map.resolve(Paad.getText()).normalize();
            Files.createDirectories(Besjtandj.getParent());
            Files.writeString(Besjtandj, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Besjtandj + "\n");
            return true;
        } catch (Exception exception) { Faeler(exception); return false; }
    }

    private int execute(List<String> command) throws Exception {
        process = new ProcessBuilder(command).directory(Map.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Oetveure) {
        if (!Opsjlaon()) return;
        String Besjtandj = Map.resolve(Paad.getText()).toString();
        String className = Naam.getText().trim();
        String Teks = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Map.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Map.resolve("classes").toString(), Besjtandj));
                if (Oetveure && result == 0) {
                    List<String> command = new ArrayList<>(Arrays.asList("java", "-cp", Map.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Teks));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) command.add(parser.sval);
                    execute(command);
                }
            } catch (Exception exception) { Faeler(exception); }
        });
    }

    private void Sjtop() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Map.toFile()).start(); }
        catch (Exception exception) { Faeler(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Map.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Paad.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Map);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Sjtop(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Peniel = new JPanel(new GridLayout(0, 1));
        JPanel Besjtandj = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Besjtandj.add(new JLabel(label("file"))); Besjtandj.add(Paad);
        Peniel.add(Besjtandj);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(toolbar, "open", () -> choose());
        button(toolbar, "save", () -> Opsjlaon());
        button(toolbar, "compile", () -> compile(false));
        button(toolbar, "run", () -> compile(true));
        button(toolbar, "stop", () -> Sjtop());
        button(toolbar, "terminal", () -> terminal());
        Peniel.add(toolbar);
        JPanel Insjtèllinge = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Insjtèllinge.add(new JLabel(label("class"))); Insjtèllinge.add(Naam);
        Insjtèllinge.add(new JLabel(label("arguments"))); Insjtèllinge.add(arguments);
        Peniel.add(Insjtèllinge);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Peniel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Peniel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Gruutde = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Gruutde.width - 40), Math.min(760, Gruutde.height - 60));
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
