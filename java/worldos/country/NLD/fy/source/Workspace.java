// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NLD.l_fy;
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
    private final JTextField Namme = new JTextField("source", 15);
    private final JTextField Arguminten = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Triemtafel = Paths.get(System.getProperty("user.home"), "workspace");
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

    private void Flater(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Paniel, String key, Runnable Aksje) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Aksje.run());
        Paniel.add(button);
    }

    private void load() {
        try {
            source.setText(Files.readString(Triemtafel.resolve(path.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Flater(exception); }
    }

    private boolean save() {
        try {
            Path Bestân = Triemtafel.resolve(path.getText()).normalize();
            Files.createDirectories(Bestân.getParent());
            Files.writeString(Bestân, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Bestân + "\n");
            return true;
        } catch (Exception exception) { Flater(exception); return false; }
    }

    private int Utfiere(List<String> Kommando) throws Exception {
        process = new ProcessBuilder(Kommando).directory(Triemtafel.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Start) {
        if (!save()) return;
        String Bestân = Triemtafel.resolve(path.getText()).toString();
        String Klasse = Namme.getText().trim();
        String Tekst = Arguminten.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Triemtafel.resolve("classes"));
                int result = Utfiere(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Triemtafel.resolve("classes").toString(), Bestân));
                if (Start && result == 0) {
                    List<String> Kommando = new ArrayList<>(Arrays.asList("java", "-cp", Triemtafel.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasse));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Kommando.add(parser.sval);
                    Utfiere(Kommando);
                }
            } catch (Exception exception) { Flater(exception); }
        });
    }

    private void Hâld_op() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Triemtafel.toFile()).start(); }
        catch (Exception exception) { Flater(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Triemtafel.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Triemtafel);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Hâld_op(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Paniel = new JPanel(new GridLayout(0, 1));
        JPanel Bestân = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Bestân.add(new JLabel(label("file"))); Bestân.add(path);
        Paniel.add(Bestân);
        JPanel Arkbalke = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Arkbalke, "open", () -> choose());
        button(Arkbalke, "save", () -> save());
        button(Arkbalke, "compile", () -> compile(false));
        button(Arkbalke, "run", () -> compile(true));
        button(Arkbalke, "stop", () -> Hâld_op());
        button(Arkbalke, "terminal", () -> terminal());
        Paniel.add(Arkbalke);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(label("class"))); settings.add(Namme);
        settings.add(new JLabel(label("arguments"))); settings.add(Arguminten);
        Paniel.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Paniel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Paniel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Grutte = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Grutte.width - 40), Math.min(760, Grutte.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] Arguminten) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
