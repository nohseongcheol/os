// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NOR.l_se;
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
    private final JTextArea Gáldu = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField path = new JTextField("Gáldu.java", 26);
    private final JTextField Namma = new JTextField("Gáldu", 15);
    private final JTextField Argumeanttat = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Máhppa = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String teaksta) {
        SwingUtilities.invokeLater(() -> {
            output.append(teaksta);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Meattáhus(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Doaibma) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Doaibma.run());
        panel.add(button);
    }

    private void load() {
        try {
            Gáldu.setText(Files.readString(Máhppa.resolve(path.getText()), StandardCharsets.UTF_8));
            Gáldu.setCaretPosition(0);
        } catch (Exception exception) { Meattáhus(exception); }
    }

    private boolean save() {
        try {
            Path Fiila = Máhppa.resolve(path.getText()).normalize();
            Files.createDirectories(Fiila.getParent());
            Files.writeString(Fiila, Gáldu.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Fiila + "\n");
            return true;
        } catch (Exception exception) { Meattáhus(exception); return false; }
    }

    private int Vuoje(List<String> Gohččun) throws Exception {
        process = new ProcessBuilder(Gohččun).directory(Máhppa.toFile()).redirectErrorStream(true).start();
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
        String Fiila = Máhppa.resolve(path.getText()).toString();
        String Luohkká = Namma.getText().trim();
        String teaksta = Argumeanttat.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Máhppa.resolve("classes"));
                int result = Vuoje(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Máhppa.resolve("classes").toString(), Fiila));
                if (run && result == 0) {
                    List<String> Gohččun = new ArrayList<>(Arrays.asList("java", "-cp", Máhppa.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Luohkká));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(teaksta));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Gohččun.add(parser.sval);
                    Vuoje(Gohččun);
                }
            } catch (Exception exception) { Meattáhus(exception); }
        });
    }

    private void Bisset() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Máhppa.toFile()).start(); }
        catch (Exception exception) { Meattáhus(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Máhppa.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Máhppa);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Bisset(); worker.shutdownNow(); System.exit(0);
            }
        });
        Gáldu.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Gáldu.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fiila = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fiila.add(new JLabel(label("file"))); Fiila.add(path);
        panel.add(Fiila);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(toolbar, "open", () -> choose());
        button(toolbar, "save", () -> save());
        button(toolbar, "compile", () -> compile(false));
        button(toolbar, "run", () -> compile(true));
        button(toolbar, "stop", () -> Bisset());
        button(toolbar, "terminal", () -> terminal());
        panel.add(toolbar);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(Namma);
        settings.add(new JLabel(label("arguments"))); settings.add(Argumeanttat);
        panel.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Gáldu), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Gáldu.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension size = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, size.width - 40), Math.min(760, size.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] Argumeanttat) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
