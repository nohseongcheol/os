// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UGA.l_lg;
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
    private final JTextArea NNONO = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField path = new JTextField("NNONO.java", 26);
    private final JTextField Linnya = new JTextField("NNONO", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Tterekero = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Bulambe(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Bigambo) {
        SwingUtilities.invokeLater(() -> {
            output.append(Bigambo);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Kiremya(Exception exception) {
        append(Bulambe("error") + ": " + exception.toString() + "\n");
    }

    private void ppeesa(JPanel Lubaawo, String key, Runnable action) {
        JButton ppeesa = new JButton(Bulambe(key));
        ppeesa.addActionListener(event -> action.run());
        Lubaawo.add(ppeesa);
    }

    private void load() {
        try {
            NNONO.setText(Files.readString(Tterekero.resolve(path.getText()), StandardCharsets.UTF_8));
            NNONO.setCaretPosition(0);
        } catch (Exception exception) { Kiremya(exception); }
    }

    private boolean Kazza() {
        try {
            Path Fayiro = Tterekero.resolve(path.getText()).normalize();
            Files.createDirectories(Fayiro.getParent());
            Files.writeString(Fayiro, NNONO.getText(), StandardCharsets.UTF_8);
            append(Bulambe("save") + ": " + Fayiro + "\n");
            return true;
        } catch (Exception exception) { Kiremya(exception); return false; }
    }

    private int execute(List<String> Mulimu) throws Exception {
        process = new ProcessBuilder(Mulimu).directory(Tterekero.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int KIGENDERWA = process.waitFor();
        process = null;
        append(Bulambe("result") + ": " + KIGENDERWA + "\n");
        return KIGENDERWA;
    }

    private void compile(boolean Tandika) {
        if (!Kazza()) return;
        String Fayiro = Tterekero.resolve(path.getText()).toString();
        String className = Linnya.getText().trim();
        String Bigambo = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Tterekero.resolve("classes"));
                int KIGENDERWA = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Tterekero.resolve("classes").toString(), Fayiro));
                if (Tandika && KIGENDERWA == 0) {
                    List<String> Mulimu = new ArrayList<>(Arrays.asList("java", "-cp", Tterekero.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", className));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Bigambo));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Mulimu.add(parser.sval);
                    execute(Mulimu);
                }
            } catch (Exception exception) { Kiremya(exception); }
        });
    }

    private void Gyako() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Kiwandikiro() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Tterekero.toFile()).start(); }
        catch (Exception exception) { Kiremya(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Tterekero.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            path.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Tterekero);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Bulambe("workspace") + " · WorldOS " + Bulambe("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Gyako(); worker.shutdownNow(); System.exit(0);
            }
        });
        NNONO.setFont(new Font("Monospaced", Font.PLAIN, 17));
        NNONO.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Lubaawo = new JPanel(new GridLayout(0, 1));
        JPanel Fayiro = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fayiro.add(new JLabel(Bulambe("file"))); Fayiro.add(path);
        Lubaawo.add(Fayiro);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ppeesa(toolbar, "open", () -> choose());
        ppeesa(toolbar, "save", () -> Kazza());
        ppeesa(toolbar, "compile", () -> compile(false));
        ppeesa(toolbar, "run", () -> compile(true));
        ppeesa(toolbar, "stop", () -> Gyako());
        ppeesa(toolbar, "terminal", () -> Kiwandikiro());
        Lubaawo.add(toolbar);
        JPanel Enteekateeka = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Enteekateeka.add(new JLabel(Bulambe("class"))); Enteekateeka.add(Linnya);
        Enteekateeka.add(new JLabel(Bulambe("arguments"))); Enteekateeka.add(arguments);
        Lubaawo.add(Enteekateeka);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(NNONO), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Lubaawo, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Lubaawo.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Bulambe("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        NNONO.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Bunene = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Bunene.width - 40), Math.min(760, Bunene.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Bulambe("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
