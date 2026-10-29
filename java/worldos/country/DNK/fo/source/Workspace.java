// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DNK.l_fo;
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
    private final JTextField Navn = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Fíluskrá = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Spjaldur(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String text) {
        SwingUtilities.invokeLater(() -> {
            output.append(text);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Brek(Exception exception) {
        append(Spjaldur("error") + ": " + exception.toString() + "\n");
    }

    private void knappur(JPanel panel, String key, Runnable action) {
        JButton knappur = new JButton(Spjaldur(key));
        knappur.addActionListener(event -> action.run());
        panel.add(knappur);
    }

    private void load() {
        try {
            source.setText(Files.readString(Fíluskrá.resolve(path.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Brek(exception); }
    }

    private boolean save() {
        try {
            Path Fíla = Fíluskrá.resolve(path.getText()).normalize();
            Files.createDirectories(Fíla.getParent());
            Files.writeString(Fíla, source.getText(), StandardCharsets.UTF_8);
            append(Spjaldur("save") + ": " + Fíla + "\n");
            return true;
        } catch (Exception exception) { Brek(exception); return false; }
    }

    private int execute(List<String> Stýriboð) throws Exception {
        process = new ProcessBuilder(Stýriboð).directory(Fíluskrá.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Spjaldur("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Koyr) {
        if (!save()) return;
        String Fíla = Fíluskrá.resolve(path.getText()).toString();
        String className = Navn.getText().trim();
        String text = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Fíluskrá.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Fíluskrá.resolve("classes").toString(), Fíla));
                if (Koyr && result == 0) {
                    List<String> Stýriboð = new ArrayList<>(Arrays.asList("java", "-cp", Fíluskrá.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Stýriboð.add(parser.sval);
                    execute(Stýriboð);
                }
            } catch (Exception exception) { Brek(exception); }
        });
    }

    private void Steðga() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Útstøð() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Fíluskrá.toFile()).start(); }
        catch (Exception exception) { Brek(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Fíluskrá.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Fíluskrá);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Spjaldur("workspace") + " · WorldOS " + Spjaldur("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Steðga(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fíla = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fíla.add(new JLabel(Spjaldur("file"))); Fíla.add(path);
        panel.add(Fíla);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        knappur(toolbar, "open", () -> choose());
        knappur(toolbar, "save", () -> save());
        knappur(toolbar, "compile", () -> compile(false));
        knappur(toolbar, "run", () -> compile(true));
        knappur(toolbar, "stop", () -> Steðga());
        knappur(toolbar, "terminal", () -> Útstøð());
        panel.add(toolbar);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(Spjaldur("class"))); settings.add(Navn);
        settings.add(new JLabel(Spjaldur("arguments"))); settings.add(arguments);
        panel.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Spjaldur("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Stødd = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Stødd.width - 40), Math.min(760, Stødd.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Spjaldur("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
