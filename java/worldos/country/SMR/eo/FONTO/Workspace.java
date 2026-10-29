// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SMR.l_eo;
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
    private final JTextArea FONTO = new JTextArea();
    private final JTextArea Eligo = new JTextArea();
    private final JTextField Vojo = new JTextField("FONTO.java", 26);
    private final JTextField Nomo = new JTextField("FONTO", 15);
    private final JTextField Argumentoj = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Dosierujo = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Procezo;

    private String Etikedo(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Teksto) {
        SwingUtilities.invokeLater(() -> {
            Eligo.append(Teksto);
            Eligo.setCaretPosition(Eligo.getDocument().getLength());
        });
    }

    private void eraro(Exception exception) {
        append(Etikedo("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Panelo, String key, Runnable Ago) {
        JButton button = new JButton(Etikedo(key));
        button.addActionListener(event -> Ago.run());
        Panelo.add(button);
    }

    private void Ŝargo() {
        try {
            FONTO.setText(Files.readString(Dosierujo.resolve(Vojo.getText()), StandardCharsets.UTF_8));
            FONTO.setCaretPosition(0);
        } catch (Exception exception) { eraro(exception); }
    }

    private boolean Konservi() {
        try {
            Path Dosiero = Dosierujo.resolve(Vojo.getText()).normalize();
            Files.createDirectories(Dosiero.getParent());
            Files.writeString(Dosiero, FONTO.getText(), StandardCharsets.UTF_8);
            append(Etikedo("save") + ": " + Dosiero + "\n");
            return true;
        } catch (Exception exception) { eraro(exception); return false; }
    }

    private int Lanĉu(List<String> Komando) throws Exception {
        Procezo = new ProcessBuilder(Komando).directory(Dosierujo.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Procezo.getInputStream(), StandardCharsets.UTF_8))) {
            String Linio;
            while ((Linio = reader.readLine()) != null) append(Linio + "\n");
        }
        int result = Procezo.waitFor();
        Procezo = null;
        append(Etikedo("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Ruli) {
        if (!Konservi()) return;
        String Dosiero = Dosierujo.resolve(Vojo.getText()).toString();
        String Klaso = Nomo.getText().trim();
        String Teksto = Argumentoj.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Dosierujo.resolve("classes"));
                int result = Lanĉu(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Dosierujo.resolve("classes").toString(), Dosiero));
                if (Ruli && result == 0) {
                    List<String> Komando = new ArrayList<>(Arrays.asList("java", "-cp", Dosierujo.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klaso));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Teksto));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Komando.add(parser.sval);
                    Lanĉu(Komando);
                }
            } catch (Exception exception) { eraro(exception); }
        });
    }

    private void Halti() {
        Process Nuna = Procezo;
        if (Nuna != null) {
            Nuna.descendants().forEach(ProcessHandle::destroyForcibly);
            Nuna.destroyForcibly();
        }
    }

    private void Terminalo() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Dosierujo.toFile()).start(); }
        catch (Exception exception) { eraro(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Dosierujo.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Vojo.setText(chooser.getSelectedFile().getAbsolutePath());
            Ŝargo();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Dosierujo);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Etikedo("workspace") + " · WorldOS " + Etikedo("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Halti(); worker.shutdownNow(); System.exit(0);
            }
        });
        FONTO.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FONTO.setTabSize(4);
        Eligo.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Eligo.setEditable(false);
        JPanel Panelo = new JPanel(new GridLayout(0, 1));
        JPanel Dosiero = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Dosiero.add(new JLabel(Etikedo("file"))); Dosiero.add(Vojo);
        Panelo.add(Dosiero);
        JPanel Ilobreto = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Ilobreto, "open", () -> choose());
        button(Ilobreto, "save", () -> Konservi());
        button(Ilobreto, "compile", () -> compile(false));
        button(Ilobreto, "run", () -> compile(true));
        button(Ilobreto, "stop", () -> Halti());
        button(Ilobreto, "terminal", () -> Terminalo());
        Panelo.add(Ilobreto);
        JPanel Agordoj = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Agordoj.add(new JLabel(Etikedo("class"))); Agordoj.add(Nomo);
        Agordoj.add(new JLabel(Etikedo("arguments"))); Agordoj.add(Argumentoj);
        Panelo.add(Agordoj);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FONTO), new JScrollPane(Eligo));
        split.setResizeWeight(0.72);
        window.add(Panelo, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Panelo.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etikedo("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FONTO.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Eligo.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Amplekso = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Amplekso.width - 40), Math.min(760, Amplekso.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Ŝargo();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etikedo("help") + "\n");
    }

    public static void main(String[] Argumentoj) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
