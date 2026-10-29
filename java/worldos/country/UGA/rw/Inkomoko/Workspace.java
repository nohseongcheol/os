// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.UGA.l_rw;
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
    private final JTextArea Inkomoko = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField Inzira = new JTextField("Inkomoko.java", 26);
    private final JTextField Izina = new JTextField("Inkomoko", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Ububiko = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Akarango(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Umwandiko) {
        SwingUtilities.invokeLater(() -> {
            output.append(Umwandiko);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void IKOSA(Exception exception) {
        append(Akarango("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String key, Runnable Igikorwa) {
        JButton button = new JButton(Akarango(key));
        button.addActionListener(event -> Igikorwa.run());
        panel.add(button);
    }

    private void Ibirimo() {
        try {
            Inkomoko.setText(Files.readString(Ububiko.resolve(Inzira.getText()), StandardCharsets.UTF_8));
            Inkomoko.setCaretPosition(0);
        } catch (Exception exception) { IKOSA(exception); }
    }

    private boolean Kubika() {
        try {
            Path Idosiye = Ububiko.resolve(Inzira.getText()).normalize();
            Files.createDirectories(Idosiye.getParent());
            Files.writeString(Idosiye, Inkomoko.getText(), StandardCharsets.UTF_8);
            append(Akarango("save") + ": " + Idosiye + "\n");
            return true;
        } catch (Exception exception) { IKOSA(exception); return false; }
    }

    private int execute(List<String> Icyo_wifuza) throws Exception {
        process = new ProcessBuilder(Icyo_wifuza).directory(Ububiko.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Akarango("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean run) {
        if (!Kubika()) return;
        String Idosiye = Ububiko.resolve(Inzira.getText()).toString();
        String ishuri_urwego = Izina.getText().trim();
        String Umwandiko = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Ububiko.resolve("classes"));
                int result = execute(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Ububiko.resolve("classes").toString(), Idosiye));
                if (run && result == 0) {
                    List<String> Icyo_wifuza = new ArrayList<>(Arrays.asList("java", "-cp", Ububiko.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", ishuri_urwego));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Umwandiko));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Icyo_wifuza.add(parser.sval);
                    execute(Icyo_wifuza);
                }
            } catch (Exception exception) { IKOSA(exception); }
        });
    }

    private void Guhagarara() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Ububiko.toFile()).start(); }
        catch (Exception exception) { IKOSA(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Ububiko.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Inzira.setText(chooser.getSelectedFile().getAbsolutePath());
            Ibirimo();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Ububiko);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Akarango("workspace") + " · WorldOS " + Akarango("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Guhagarara(); worker.shutdownNow(); System.exit(0);
            }
        });
        Inkomoko.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Inkomoko.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Idosiye = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Idosiye.add(new JLabel(Akarango("file"))); Idosiye.add(Inzira);
        panel.add(Idosiye);
        JPanel toolbar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(toolbar, "open", () -> choose());
        button(toolbar, "save", () -> Kubika());
        button(toolbar, "compile", () -> compile(false));
        button(toolbar, "run", () -> compile(true));
        button(toolbar, "stop", () -> Guhagarara());
        button(toolbar, "terminal", () -> terminal());
        panel.add(toolbar);
        JPanel settings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        settings.add(new JLabel(Akarango("class"))); settings.add(Izina);
        settings.add(new JLabel(Akarango("arguments"))); settings.add(arguments);
        panel.add(settings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Inkomoko), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Akarango("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Inkomoko.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Ingano = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Ingano.width - 40), Math.min(760, Ingano.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Ibirimo();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Akarango("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
