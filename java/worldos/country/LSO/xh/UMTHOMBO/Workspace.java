// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LSO.l_xh;
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
    private final JTextArea UMTHOMBO = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField INDLELA = new JTextField("UMTHOMBO.java", 26);
    private final JTextField Igama = new JTextField("UMTHOMBO", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path directory = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Ilebhile(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Umbhalo) {
        SwingUtilities.invokeLater(() -> {
            output.append(Umbhalo);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Impazamo(Exception exception) {
        append(Ilebhile("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Intshukumo) {
        JButton button = new JButton(Ilebhile(key));
        button.addActionListener(event -> Intshukumo.run());
        panel.add(button);
    }

    private void Faka() {
        try {
            UMTHOMBO.setText(Files.readString(directory.resolve(INDLELA.getText()), StandardCharsets.UTF_8));
            UMTHOMBO.setCaretPosition(0);
        } catch (Exception exception) { Impazamo(exception); }
    }

    private boolean Gcina() {
        try {
            Path iFayili = directory.resolve(INDLELA.getText()).normalize();
            Files.createDirectories(iFayili.getParent());
            Files.writeString(iFayili, UMTHOMBO.getText(), StandardCharsets.UTF_8);
            append(Ilebhile("save") + ": " + iFayili + "\n");
            return true;
        } catch (Exception exception) { Impazamo(exception); return false; }
    }

    private int execute(List<String> Umyalelo) throws Exception {
        process = new ProcessBuilder(Umyalelo).directory(directory.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Ilebhile("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Phumeza) {
        if (!Gcina()) return;
        String iFayili = directory.resolve(INDLELA.getText()).toString();
        String Udidi = Igama.getText().trim();
        String Umbhalo = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(directory.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", directory.resolve("classes").toString(), iFayili));
                if (Phumeza && result == 0) {
                    List<String> Umyalelo = new ArrayList<>(Arrays.asList("java", "-cp", directory.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Udidi));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Umbhalo));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Umyalelo.add(parser.sval);
                    execute(Umyalelo);
                }
            } catch (Exception exception) { Impazamo(exception); }
        });
    }

    private void Yima() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void i_Terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(directory.toFile()).start(); }
        catch (Exception exception) { Impazamo(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(directory.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            INDLELA.setText(chooser.getSelectedFile().getAbsolutePath());
            Faka();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(directory);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Ilebhile("workspace") + " · WorldOS " + Ilebhile("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Yima(); worker.shutdownNow(); System.exit(0);
            }
        });
        UMTHOMBO.setFont(new Font("Monospaced", Font.PLAIN, 17));
        UMTHOMBO.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel iFayili = new JPanel(new FlowLayout(FlowLayout.LEADING));
        iFayili.add(new JLabel(Ilebhile("file"))); iFayili.add(INDLELA);
        panel.add(iFayili);
        JPanel I_Toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(I_Toolbar, "open", () -> choose());
        button(I_Toolbar, "save", () -> Gcina());
        button(I_Toolbar, "compile", () -> compile(false));
        button(I_Toolbar, "run", () -> compile(true));
        button(I_Toolbar, "stop", () -> Yima());
        button(I_Toolbar, "terminal", () -> i_Terminal());
        panel.add(I_Toolbar);
        JPanel Imimiselo = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Imimiselo.add(new JLabel(Ilebhile("class"))); Imimiselo.add(Igama);
        Imimiselo.add(new JLabel(Ilebhile("arguments"))); Imimiselo.add(arguments);
        panel.add(Imimiselo);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(UMTHOMBO), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Ilebhile("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        UMTHOMBO.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ubukhulu = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Ubukhulu.width - 40), Math.min(760, Ubukhulu.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Faka();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Ilebhile("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
