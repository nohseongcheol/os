// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ISL.l_is;
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
    private final JFrame Gluggi = new JFrame();
    private final JTextArea Uppruni = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField SLÓÐ = new JTextField("Uppruni.java", 26);
    private final JTextField Heiti = new JTextField("Uppruni", 15);
    private final JTextField Viðföng = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Mappa = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Skýring(String key) {
        return messages.getProperty(key, key);
    }

    private void append(String Texti) {
        SwingUtilities.invokeLater(() -> {
            output.append(Texti);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void Villa(Exception exception) {
        append(Skýring("error") + ": " + exception.toString() + "\n");
    }

    private void hnappur(JPanel Skjástika, String key, Runnable Aðgerð) {
        JButton hnappur = new JButton(Skýring(key));
        hnappur.addActionListener(event -> Aðgerð.run());
        Skjástika.add(hnappur);
    }

    private void Hlaða() {
        try {
            Uppruni.setText(Files.readString(Mappa.resolve(SLÓÐ.getText()), StandardCharsets.UTF_8));
            Uppruni.setCaretPosition(0);
        } catch (Exception exception) { Villa(exception); }
    }

    private boolean Vista() {
        try {
            Path Skrá = Mappa.resolve(SLÓÐ.getText()).normalize();
            Files.createDirectories(Skrá.getParent());
            Files.writeString(Skrá, Uppruni.getText(), StandardCharsets.UTF_8);
            append(Skýring("save") + ": " + Skrá + "\n");
            return true;
        } catch (Exception exception) { Villa(exception); return false; }
    }

    private int Keyra(List<String> Skipun) throws Exception {
        process = new ProcessBuilder(Skipun).directory(Mappa.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String Lína;
            while ((Lína = reader.readLine()) != null) append(Lína + "\n");
        }
        int NIÐURSTAÐA = process.waitFor();
        process = null;
        append(Skýring("result") + ": " + NIÐURSTAÐA + "\n");
        return NIÐURSTAÐA;
    }

    private void compile(boolean Keyra_2) {
        if (!Vista()) return;
        String Skrá = Mappa.resolve(SLÓÐ.getText()).toString();
        String Flokkur = Heiti.getText().trim();
        String Texti = Viðföng.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Mappa.resolve("classes"));
                int NIÐURSTAÐA = Keyra(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Mappa.resolve("classes").toString(), Skrá));
                if (Keyra_2 && NIÐURSTAÐA == 0) {
                    List<String> Skipun = new ArrayList<>(Arrays.asList("java", "-cp", Mappa.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Flokkur));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Texti));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Skipun.add(parser.sval);
                    Keyra(Skipun);
                }
            } catch (Exception exception) { Villa(exception); }
        });
    }

    private void Stopp() {
        Process Núverandi = process;
        if (Núverandi != null) {
            Núverandi.descendants().forEach(ProcessHandle::destroyForcibly);
            Núverandi.destroyForcibly();
        }
    }

    private void Skjáhermir() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Mappa.toFile()).start(); }
        catch (Exception exception) { Villa(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Mappa.toFile());
        if (chooser.showOpenDialog(Gluggi) == JFileChooser.APPROVE_OPTION) {
            SLÓÐ.setText(chooser.getSelectedFile().getAbsolutePath());
            Hlaða();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Mappa);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Gluggi.setTitle(Skýring("workspace") + " · WorldOS " + Skýring("identity"));
        Gluggi.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Gluggi.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                Stopp(); worker.shutdownNow(); System.exit(0);
            }
        });
        Uppruni.setFont(new Font("Monospaced", Font.PLAIN, 17));
        Uppruni.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel Skjástika = new JPanel(new GridLayout(0, 1));
        JPanel Skrá = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Skrá.add(new JLabel(Skýring("file"))); Skrá.add(SLÓÐ);
        Skjástika.add(Skrá);
        JPanel Verkfærastika = new JPanel(new FlowLayout(FlowLayout.LEADING));
        hnappur(Verkfærastika, "open", () -> choose());
        hnappur(Verkfærastika, "save", () -> Vista());
        hnappur(Verkfærastika, "compile", () -> compile(false));
        hnappur(Verkfærastika, "run", () -> compile(true));
        hnappur(Verkfærastika, "stop", () -> Stopp());
        hnappur(Verkfærastika, "terminal", () -> Skjáhermir());
        Skjástika.add(Verkfærastika);
        JPanel Stillingar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Stillingar.add(new JLabel(Skýring("class"))); Stillingar.add(Heiti);
        Stillingar.add(new JLabel(Skýring("arguments"))); Stillingar.add(Viðföng);
        Skjástika.add(Stillingar);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Uppruni), new JScrollPane(output));
        split.setResizeWeight(0.72);
        Gluggi.add(Skjástika, BorderLayout.NORTH);
        Gluggi.add(split, BorderLayout.CENTER);
        Skjástika.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Skýring("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        Uppruni.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Stærð = Toolkit.getDefaultToolkit().getScreenSize();
        Gluggi.setSize(Math.min(1240, Stærð.width - 40), Math.min(760, Stærð.height - 60));
        Gluggi.setLocationRelativeTo(null);
        Gluggi.setVisible(true);
        Hlaða();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Skýring("help") + "\n");
    }

    public static void main(String[] Viðföng) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
