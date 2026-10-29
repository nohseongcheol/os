// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SWZ.l_zu;
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
    private final JTextField Indlela_2 = new JTextField("source.java", 26);
    private final JTextField Igama = new JTextField("source", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path directory = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Itekisi) {
        SwingUtilities.invokeLater(() -> {
            output.append(Itekisi);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Iphutha(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Isenzo) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Isenzo.run());
        panel.add(button);
    }

    private void load() {
        try {
            source.setText(Files.readString(directory.resolve(Indlela_2.getText()), StandardCharsets.UTF_8));
            source.setCaretPosition(0);
        } catch (Exception exception) { Iphutha(exception); }
    }

    private boolean Hlenga() {
        try {
            Path Ihele = directory.resolve(Indlela_2.getText()).normalize();
            Files.createDirectories(Ihele.getParent());
            Files.writeString(Ihele, source.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Ihele + "\n");
            return true;
        } catch (Exception exception) { Iphutha(exception); return false; }
    }

    private int execute(List<String> Umlayelo) throws Exception {
        process = new ProcessBuilder(Umlayelo).directory(directory.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Sebenzisa) {
        if (!Hlenga()) return;
        String Ihele = directory.resolve(Indlela_2.getText()).toString();
        String className = Igama.getText().trim();
        String Itekisi = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(directory.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", directory.resolve("classes").toString(), Ihele));
                if (Sebenzisa && result == 0) {
                    List<String> Umlayelo = new ArrayList<>(Arrays.asList("java", "-cp", directory.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Itekisi));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Umlayelo.add(parser.sval);
                    execute(Umlayelo);
                }
            } catch (Exception exception) { Iphutha(exception); }
        });
    }

    private void Ima() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(directory.toFile()).start(); }
        catch (Exception exception) { Iphutha(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(directory.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Indlela_2.setText(chooser.getSelectedFile().getAbsolutePath());
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
                Ima(); worker.shutdownNow(); System.exit(0);
            }
        });
        source.setFont(new Font("Monospaced", Font.PLAIN, 17));
        source.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Ihele = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ihele.add(new JLabel(label("file"))); Ihele.add(Indlela_2);
        panel.add(Ihele);
        JPanel Ithuluzi_kokumele = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Ithuluzi_kokumele, "open", () -> choose());
        button(Ithuluzi_kokumele, "save", () -> Hlenga());
        button(Ithuluzi_kokumele, "compile", () -> compile(false));
        button(Ithuluzi_kokumele, "run", () -> compile(true));
        button(Ithuluzi_kokumele, "stop", () -> Ima());
        button(Ithuluzi_kokumele, "terminal", () -> terminal());
        panel.add(Ithuluzi_kokumele);
        JPanel Izinhlelo = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Izinhlelo.add(new JLabel(label("class"))); Izinhlelo.add(Igama);
        Izinhlelo.add(new JLabel(label("arguments"))); Izinhlelo.add(arguments);
        panel.add(Izinhlelo);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        source.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ubungako = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Ubungako.width - 40), Math.min(760, Ubungako.height - 60));
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
