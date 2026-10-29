// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.AFG.l_tk;
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
    private final JTextArea Çeşme = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField Ýol = new JTextField("Çeşme.java", 26);
    private final JTextField Ad = new JTextField("Çeşme", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path directory = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Metin) {
        SwingUtilities.invokeLater(() -> {
            output.append(Metin);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Hata(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable action) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> action.run());
        panel.add(button);
    }

    private void load() {
        try {
            Çeşme.setText(Files.readString(directory.resolve(Ýol.getText()), StandardCharsets.UTF_8));
            Çeşme.setCaretPosition(0);
        } catch (Exception exception) { Hata(exception); }
    }

    private boolean Gaýd_Et() {
        try {
            Path Faýl = directory.resolve(Ýol.getText()).normalize();
            Files.createDirectories(Faýl.getParent());
            Files.writeString(Faýl, Çeşme.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Faýl + "\n");
            return true;
        } catch (Exception exception) { Hata(exception); return false; }
    }

    private int execute(List<String> command) throws Exception {
        process = new ProcessBuilder(command).directory(directory.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Bitir) {
        if (!Gaýd_Et()) return;
        String Faýl = directory.resolve(Ýol.getText()).toString();
        String className = Ad.getText().trim();
        String Metin = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(directory.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", directory.resolve("classes").toString(), Faýl));
                if (Bitir && result == 0) {
                    List<String> command = new ArrayList<>(Arrays.asList("java", "-cp", directory.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Metin));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) command.add(parser.sval);
                    execute(command);
                }
            } catch (Exception exception) { Hata(exception); }
        });
    }

    private void Dur() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(directory.toFile()).start(); }
        catch (Exception exception) { Hata(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(directory.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Ýol.setText(chooser.getSelectedFile().getAbsolutePath());
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
                Dur(); worker.shutdownNow(); System.exit(0);
            }
        });
        Çeşme.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Çeşme.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Faýl = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Faýl.add(new JLabel(label("file"))); Faýl.add(Ýol);
        panel.add(Faýl);
        JPanel Esbap_zolaky = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Esbap_zolaky, "open", () -> choose());
        button(Esbap_zolaky, "save", () -> Gaýd_Et());
        button(Esbap_zolaky, "compile", () -> compile(false));
        button(Esbap_zolaky, "run", () -> compile(true));
        button(Esbap_zolaky, "stop", () -> Dur());
        button(Esbap_zolaky, "terminal", () -> terminal());
        panel.add(Esbap_zolaky);
        JPanel Düzümler = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Düzümler.add(new JLabel(label("class"))); Düzümler.add(Ad);
        Düzümler.add(new JLabel(label("arguments"))); Düzümler.add(arguments);
        panel.add(Düzümler);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Çeşme), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Çeşme.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ululyk = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Ululyk.width - 40), Math.min(760, Ululyk.height - 60));
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
