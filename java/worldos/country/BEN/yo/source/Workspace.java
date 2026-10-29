// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BEN.l_yo;
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
    private final JTextField Orúkọ = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path directory = Paths.get(System.getProperty("user.home"), "workspace");
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

    private void error(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable action) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> action.run());
        panel.add(button);
    }

    private void load() {
        try {
            source.setText(Files.readString(directory.resolve(path.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { error(exception); }
    }

    private boolean save() {
        try {
            Path Fáìlì = directory.resolve(path.getText()).normalize();
            Files.createDirectories(Fáìlì.getParent());
            Files.writeString(Fáìlì, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Fáìlì + "\n");
            return true;
        } catch (Exception exception) { error(exception); return false; }
    }

    private int execute(List<String> Àṣẹ) throws Exception {
        process = new ProcessBuilder(Àṣẹ).directory(directory.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Rọ́ọ̀nù) {
        if (!save()) return;
        String Fáìlì = directory.resolve(path.getText()).toString();
        String kíláàsì = Orúkọ.getText().trim();
        String text = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(directory.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", directory.resolve("classes").toString(), Fáìlì));
                if (Rọ́ọ̀nù && result == 0) {
                    List<String> Àṣẹ = new ArrayList<>(Arrays.asList("java", "-cp", directory.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", kíláàsì));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Àṣẹ.add(parser.sval);
                    execute(Àṣẹ);
                }
            } catch (Exception exception) { error(exception); }
        });
    }

    private void Dúró() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(directory.toFile()).start(); }
        catch (Exception exception) { error(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(directory.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
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
                Dúró(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fáìlì = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fáìlì.add(new JLabel(label("file"))); Fáìlì.add(path);
        panel.add(Fáìlì);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(toolbar, "open", () -> choose());
        button(toolbar, "save", () -> save());
        button(toolbar, "compile", () -> compile(false));
        button(toolbar, "run", () -> compile(true));
        button(toolbar, "stop", () -> Dúró());
        button(toolbar, "terminal", () -> terminal());
        panel.add(toolbar);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(Orúkọ);
        settings.add(new JLabel(label("arguments"))); settings.add(arguments);
        panel.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ìwọ̀n = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Ìwọ̀n.width - 40), Math.min(760, Ìwọ̀n.height - 60));
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
