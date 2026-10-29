// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.BEL.l_wa;
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
    private final JTextArea Sourdant = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField Tchimin = new JTextField("Sourdant.java", 26);
    private final JTextField No = new JTextField("Sourdant", 15);
    private final JTextField Årgumints = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Ridant = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Etikete(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Tecse) {
        SwingUtilities.invokeLater(() -> {
            output.append(Tecse);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void AROKE(Exception exception) {
        append(Etikete("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Scriftôr, String key, Runnable Accion) {
        JButton button = new JButton(Etikete(key));
        button.addActionListener(event -> Accion.run());
        Scriftôr.add(button);
    }

    private void load() {
        try {
            Sourdant.setText(Files.readString(Ridant.resolve(Tchimin.getText()), StandardCharsets.UTF_8));
            Sourdant.setCaretPosition(0);
        } catch (Exception exception) { AROKE(exception); }
    }

    private boolean Schaper() {
        try {
            Path Fitchî = Ridant.resolve(Tchimin.getText()).normalize();
            Files.createDirectories(Fitchî.getParent());
            Files.writeString(Fitchî, Sourdant.getText(), StandardCharsets.UTF_8);
            append(Etikete("save") + ": " + Fitchî + "\n");
            return true;
        } catch (Exception exception) { AROKE(exception); return false; }
    }

    private int Enonder(List<String> Comande) throws Exception {
        process = new ProcessBuilder(Comande).directory(Ridant.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Etikete("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Enonder_2) {
        if (!Schaper()) return;
        String Fitchî = Ridant.resolve(Tchimin.getText()).toString();
        String Classe = No.getText().trim();
        String Tecse = Årgumints.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Ridant.resolve("classes"));
                int result = Enonder(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Ridant.resolve("classes").toString(), Fitchî));
                if (Enonder_2 && result == 0) {
                    List<String> Comande = new ArrayList<>(Arrays.asList("java", "-cp", Ridant.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Classe));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tecse));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Comande.add(parser.sval);
                    Enonder(Comande);
                }
            } catch (Exception exception) { AROKE(exception); }
        });
    }

    private void Åwe() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Terminå() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Ridant.toFile()).start(); }
        catch (Exception exception) { AROKE(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Ridant.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Tchimin.setText(chooser.getSelectedFile().getAbsolutePath());
            load();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Ridant);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Etikete("workspace") + " · WorldOS " + Etikete("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Åwe(); worker.shutdownNow(); System.exit(0);
            }
        });
        Sourdant.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Sourdant.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Scriftôr = new JPanel(new GridLayout(0, 1));
        JPanel Fitchî = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fitchî.add(new JLabel(Etikete("file"))); Fitchî.add(Tchimin);
        Scriftôr.add(Fitchî);
        JPanel Bår_ås_usteyes = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Bår_ås_usteyes, "open", () -> choose());
        button(Bår_ås_usteyes, "save", () -> Schaper());
        button(Bår_ås_usteyes, "compile", () -> compile(false));
        button(Bår_ås_usteyes, "run", () -> compile(true));
        button(Bår_ås_usteyes, "stop", () -> Åwe());
        button(Bår_ås_usteyes, "terminal", () -> Terminå());
        Scriftôr.add(Bår_ås_usteyes);
        JPanel Apontiaedjes = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Apontiaedjes.add(new JLabel(Etikete("class"))); Apontiaedjes.add(No);
        Apontiaedjes.add(new JLabel(Etikete("arguments"))); Apontiaedjes.add(Årgumints);
        Scriftôr.add(Apontiaedjes);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Sourdant), new JScrollPane(output));
        split.setResizeWeight(0.72);
        window.add(Scriftôr, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Scriftôr.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etikete("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Sourdant.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Grandeu = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Grandeu.width - 40), Math.min(760, Grandeu.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        load();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etikete("help") + "\n");
    }

    public static void main(String[] Årgumints) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
