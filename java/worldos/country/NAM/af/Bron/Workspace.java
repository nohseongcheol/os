// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NAM.l_af;
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
    private final JTextArea Bron = new JTextArea();
    private final JTextArea Afvoer = new JTextArea();
    private final JTextField Pad = new JTextField("Bron.java", 26);
    private final JTextField Naam = new JTextField("Bron", 15);
    private final JTextField arguments = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Gids = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String etiket(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Teks) {
        SwingUtilities.invokeLater(() -> {
            Afvoer.append(Teks);
            Afvoer.setCaretPosition(Afvoer.getDocument().getLength());
        });
    }

    private void Fout(Exception exception) {
        append(etiket("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel Paneel, String key, Runnable Aksie) {
        JButton button = new JButton(etiket(key));
        button.addActionListener(event -> Aksie.run());
        Paneel.add(button);
    }

    private void Lading() {
        try {
            Bron.setText(Files.readString(Gids.resolve(Pad.getText()), StandardCharsets.UTF_8));
            Bron.setCaretPosition(0);
        } catch (Exception exception) { Fout(exception); }
    }

    private boolean Stoor() {
        try {
            Path Lêer = Gids.resolve(Pad.getText()).normalize();
            Files.createDirectories(Lêer.getParent());
            Files.writeString(Lêer, Bron.getText(), StandardCharsets.UTF_8);
            append(etiket("save") + ": " + Lêer + "\n");
            return true;
        } catch (Exception exception) { Fout(exception); return false; }
    }

    private int Voer_uit(List<String> Opdrag) throws Exception {
        process = new ProcessBuilder(Opdrag).directory(Gids.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(etiket("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Loop) {
        if (!Stoor()) return;
        String Lêer = Gids.resolve(Pad.getText()).toString();
        String Klas = Naam.getText().trim();
        String Teks = arguments.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Gids.resolve("classes"));
                int result = Voer_uit(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Gids.resolve("classes").toString(), Lêer));
                if (Loop && result == 0) {
                    List<String> Opdrag = new ArrayList<>(Arrays.asList("java", "-cp", Gids.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klas));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Teks));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Opdrag.add(parser.sval);
                    Voer_uit(Opdrag);
                }
            } catch (Exception exception) { Fout(exception); }
        });
    }

    private void stop() {
        Process current = process;
        if (current != null) {
            current.descendants().forEach(ProcessHandle::destroyForcibly);
            current.destroyForcibly();
        }
    }

    private void Terminaal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Gids.toFile()).start(); }
        catch (Exception exception) { Fout(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Gids.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            Pad.setText(chooser.getSelectedFile().getAbsolutePath());
            Lading();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Gids);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(etiket("workspace") + " · WorldOS " + etiket("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                stop(); worker.shutdownNow(); System.exit(0);
            }
        });
        Bron.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Bron.setTabSize(4);
        Afvoer.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Afvoer.setEditable(false);
        JPanel Paneel = new JPanel(new GridLayout(0, 1));
        JPanel Lêer = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Lêer.add(new JLabel(etiket("file"))); Lêer.add(Pad);
        Paneel.add(Lêer);
        JPanel Nutsbalk = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Nutsbalk, "open", () -> choose());
        button(Nutsbalk, "save", () -> Stoor());
        button(Nutsbalk, "compile", () -> compile(false));
        button(Nutsbalk, "run", () -> compile(true));
        button(Nutsbalk, "stop", () -> stop());
        button(Nutsbalk, "terminal", () -> Terminaal());
        Paneel.add(Nutsbalk);
        JPanel Instellings = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Instellings.add(new JLabel(etiket("class"))); Instellings.add(Naam);
        Instellings.add(new JLabel(etiket("arguments"))); Instellings.add(arguments);
        Paneel.add(Instellings);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Bron), new JScrollPane(Afvoer));
        split.setResizeWeight(0.72);
        window.add(Paneel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Paneel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(etiket("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Bron.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Afvoer.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Grootte = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Grootte.width - 40), Math.min(760, Grootte.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Lading();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(etiket("help") + "\n");
    }

    public static void main(String[] arguments) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
