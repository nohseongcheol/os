// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ARM.l_ku;
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
    private final JTextArea ÇAVKANÎ = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField RÊ = new JTextField("ÇAVKANÎ.java", 26);
    private final JTextField Nav = new JTextField("ÇAVKANÎ", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Pelrêç = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String label(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Nivîs) {
        SwingUtilities.invokeLater(() -> {
            output.append(Nivîs);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Çewtî(Exception exception) {
        append(label("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Çalakî) {
        JButton button = new JButton(label(key));
        button.addActionListener(event -> Çalakî.run());
        panel.add(button);
    }

    private void Lê_bar_bike() {
        try {
            ÇAVKANÎ.setText(Files.readString(Pelrêç.resolve(RÊ.getText()), StandardCharsets.UTF_8));
            ÇAVKANÎ.setCaretPosition(0);
        } catch (Exception exception) { Çewtî(exception); }
    }

    private boolean Tomar_bike() {
        try {
            Path Pel = Pelrêç.resolve(RÊ.getText()).normalize();
            Files.createDirectories(Pel.getParent());
            Files.writeString(Pel, ÇAVKANÎ.getText(), StandardCharsets.UTF_8);
            append(label("save") + ": " + Pel + "\n");
            return true;
        } catch (Exception exception) { Çewtî(exception); return false; }
    }

    private int Bixebitîne(List<String> Ferman) throws Exception {
        process = new ProcessBuilder(Ferman).directory(Pelrêç.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(label("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Bimeşîne) {
        if (!Tomar_bike()) return;
        String Pel = Pelrêç.resolve(RÊ.getText()).toString();
        String className = Nav.getText().trim();
        String Nivîs = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Pelrêç.resolve("classes"));
                int result = Bixebitîne(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Pelrêç.resolve("classes").toString(), Pel));
                if (Bimeşîne && result == 0) {
                    List<String> Ferman = new ArrayList<>(Arrays.asList("java", "-cp", Pelrêç.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Nivîs));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Ferman.add(parser.sval);
                    Bixebitîne(Ferman);
                }
            } catch (Exception exception) { Çewtî(exception); }
        });
    }

    private void Bisekine() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Termînal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Pelrêç.toFile()).start(); }
        catch (Exception exception) { Çewtî(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Pelrêç.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            RÊ.setText(chooser.getSelectedFile().getAbsolutePath());
            Lê_bar_bike();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Pelrêç);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(label("workspace") + " · WorldOS " + label("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Bisekine(); worker.shutdownNow(); System.exit(0);
            }
        });
        ÇAVKANÎ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ÇAVKANÎ.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Pel = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Pel.add(new JLabel(label("file"))); Pel.add(RÊ);
        panel.add(Pel);
        JPanel Darikê_Amûran = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Darikê_Amûran, "open", () -> choose());
        button(Darikê_Amûran, "save", () -> Tomar_bike());
        button(Darikê_Amûran, "compile", () -> compile(false));
        button(Darikê_Amûran, "run", () -> compile(true));
        button(Darikê_Amûran, "stop", () -> Bisekine());
        button(Darikê_Amûran, "terminal", () -> Termînal());
        panel.add(Darikê_Amûran);
        JPanel Vebijêrk = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Vebijêrk.add(new JLabel(label("class"))); Vebijêrk.add(Nav);
        Vebijêrk.add(new JLabel(label("arguments"))); Vebijêrk.add(arguments);
        panel.add(Vebijêrk);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ÇAVKANÎ), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(label("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ÇAVKANÎ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Mezinahî = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Mezinahî.width - 40), Math.min(760, Mezinahî.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Lê_bar_bike();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(label("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
