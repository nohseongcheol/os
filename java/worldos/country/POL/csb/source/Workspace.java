// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.POL.l_csb;
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
    private final JTextField name = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Katalog = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            output.append(Tekst);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Fela(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Dzejanié) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Dzejanié.run());
        panel.add(button);
    }

    private void Zladëjë() {
        try {
            source.setText(Files.readString(Katalog.resolve(path.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Fela(exception); }
    }

    private boolean save() {
        try {
            Path Lopk = Katalog.resolve(path.getText()).normalize();
            Files.createDirectories(Lopk.getParent());
            Files.writeString(Lopk, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Lopk + "\n");
            return true;
        } catch (Exception exception) { Fela(exception); return false; }
    }

    private int Zrëszë(List<String> Pòlét) throws Exception {
        process = new ProcessBuilder(Pòlét).directory(Katalog.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean run) {
        if (!save()) return;
        String Lopk = Katalog.resolve(path.getText()).toString();
        String className = name.getText().trim();
        String Tekst = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Katalog.resolve("classes"));
                int result = Zrëszë(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Katalog.resolve("classes").toString(), Lopk));
                if (run && result == 0) {
                    List<String> Pòlét = new ArrayList<>(Arrays.asList("java", "-cp", Katalog.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Pòlét.add(parser.sval);
                    Zrëszë(Pòlét);
                }
            } catch (Exception exception) { Fela(exception); }
        });
    }

    private void stop() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Katalog.toFile()).start(); }
        catch (Exception exception) { Fela(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Katalog.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            Zladëjë();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Katalog);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                stop(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Lopk = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Lopk.add(new JLabel(label("file"))); Lopk.add(path);
        panel.add(Lopk);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(toolbar, "open", () -> choose());
        button(toolbar, "save", () -> save());
        button(toolbar, "compile", () -> compile(false));
        button(toolbar, "run", () -> compile(true));
        button(toolbar, "stop", () -> stop());
        button(toolbar, "terminal", () -> terminal());
        panel.add(toolbar);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(name);
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
        Dimension size = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, size.width - 40), Math.min(760, size.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Zladëjë();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
