// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MDG.l_mg;
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
    private final JTextArea LOHARANO = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField LALANA = new JTextField("LOHARANO.java", 26);
    private final JTextField Anarana = new JTextField("LOHARANO", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Lahatahiry = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Mari_tsoratra(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Soratra) {
        SwingUtilities.invokeLater(() -> {
            output.append(Soratra);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Tsy_fetezana(Exception exception) {
        append(Mari_tsoratra("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Tontonana, String key, Runnable Asa) {
        JButton button = new JButton(Mari_tsoratra(key));
        button.addActionListener(event -> Asa.run());
        Tontonana.add(button);
    }

    private void Vesatra() {
        try {
            LOHARANO.setText(Files.readString(Lahatahiry.resolve(LALANA.getText()), StandardCharsets.UTF_8));
            LOHARANO.setCaretPosition(0);
        } catch (Exception exception) { Tsy_fetezana(exception); }
    }

    private boolean Raiketo() {
        try {
            Path Rakitra = Lahatahiry.resolve(LALANA.getText()).normalize();
            Files.createDirectories(Rakitra.getParent());
            Files.writeString(Rakitra, LOHARANO.getText(), StandardCharsets.UTF_8);
            append(Mari_tsoratra("save") + ": " + Rakitra + "\n");
            return true;
        } catch (Exception exception) { Tsy_fetezana(exception); return false; }
    }

    private int execute(List<String> Baiko) throws Exception {
        process = new ProcessBuilder(Baiko).directory(Lahatahiry.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Mari_tsoratra("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Alefaso) {
        if (!Raiketo()) return;
        String Rakitra = Lahatahiry.resolve(LALANA.getText()).toString();
        String Sokajy = Anarana.getText().trim();
        String Soratra = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Lahatahiry.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Lahatahiry.resolve("classes").toString(), Rakitra));
                if (Alefaso && result == 0) {
                    List<String> Baiko = new ArrayList<>(Arrays.asList("java", "-cp", Lahatahiry.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Sokajy));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Soratra));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Baiko.add(parser.sval);
                    execute(Baiko);
                }
            } catch (Exception exception) { Tsy_fetezana(exception); }
        });
    }

    private void Ajanony() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Lahatahiry.toFile()).start(); }
        catch (Exception exception) { Tsy_fetezana(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Lahatahiry.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            LALANA.setText(chooser.getSelectedFile().getAbsolutePath());
            Vesatra();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Lahatahiry);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Mari_tsoratra("workspace") + " · WorldOS " + Mari_tsoratra("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Ajanony(); worker.shutdownNow(); System.exit(0);
            }
        });
        LOHARANO.setFont(new Font("Monospaced", Font.PLAIN, 17));
        LOHARANO.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Tontonana = new JPanel(new GridLayout(0, 1));
        JPanel Rakitra = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Rakitra.add(new JLabel(Mari_tsoratra("file"))); Rakitra.add(LALANA);
        Tontonana.add(Rakitra);
        JPanel Anjam_pitaovana = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Anjam_pitaovana, "open", () -> choose());
        button(Anjam_pitaovana, "save", () -> Raiketo());
        button(Anjam_pitaovana, "compile", () -> compile(false));
        button(Anjam_pitaovana, "run", () -> compile(true));
        button(Anjam_pitaovana, "stop", () -> Ajanony());
        button(Anjam_pitaovana, "terminal", () -> terminal());
        Tontonana.add(Anjam_pitaovana);
        JPanel Fandrindrana = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fandrindrana.add(new JLabel(Mari_tsoratra("class"))); Fandrindrana.add(Anarana);
        Fandrindrana.add(new JLabel(Mari_tsoratra("arguments"))); Fandrindrana.add(arguments);
        Tontonana.add(Fandrindrana);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(LOHARANO), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Tontonana, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Tontonana.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Mari_tsoratra("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        LOHARANO.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Habe = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Habe.width - 40), Math.min(760, Habe.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Vesatra();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Mari_tsoratra("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
