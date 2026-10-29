// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DNK.l_da;
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
    private final JFrame Vindue = new JFrame();
    private final JTextArea KILDE = new JTextArea();
    private final JTextArea Udgang = new JTextArea();
    private final JTextField Sti = new JTextField("KILDE.java", 26);
    private final JTextField Navn = new JTextField("KILDE", 15);
    private final JTextField Argumenter = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Mappe = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Etiket(String Nøgle) {
        return messages.getProperty(Nøgle, Nøgle);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            Udgang.append(Tekst);
            Udgang.setCaretPosition(Udgang.getDocument().getLength());
        });
    }

    private void fejl(Exception exception) {
        append(Etiket("error") + ": " + exception.toString() + "\n");
    }

    private void knap(JPanel panel, String Nøgle, Runnable Handling) {
        JButton knap = new JButton(Etiket(Nøgle));
        knap.addActionListener(event -> Handling.run());
        panel.add(knap);
    }

    private void Belastning() {
        try {
            KILDE.setText(Files.readString(Mappe.resolve(Sti.getText()), StandardCharsets.UTF_8));
            KILDE.setCaretPosition(0);
        } catch (Exception exception) { fejl(exception); }
    }

    private boolean Gem() {
        try {
            Path Fil = Mappe.resolve(Sti.getText()).normalize();
            Files.createDirectories(Fil.getParent());
            Files.writeString(Fil, KILDE.getText(), StandardCharsets.UTF_8);
            append(Etiket("save") + ": " + Fil + "\n");
            return true;
        } catch (Exception exception) { fejl(exception); return false; }
    }

    private int Kør(List<String> Kommando) throws Exception {
        Proces = new ProcessBuilder(Kommando).directory(Mappe.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String Linje;
            while ((Linje = reader.readLine()) != null) append(Linje + "\n");
        }
        int result = Proces.waitFor();
        Proces = null;
        append(Etiket("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Kør_2) {
        if (!Gem()) return;
        String Fil = Mappe.resolve(Sti.getText()).toString();
        String Klasse = Navn.getText().trim();
        String Tekst = Argumenter.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Mappe.resolve("classes"));
                int result = Kør(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Mappe.resolve("classes").toString(), Fil));
                if (Kør_2 && result == 0) {
                    List<String> Kommando = new ArrayList<>(Arrays.asList("java", "-cp", Mappe.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasse));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Kommando.add(parser.sval);
                    Kør(Kommando);
                }
            } catch (Exception exception) { fejl(exception); }
        });
    }

    private void stop() {
        Process Aktive = Proces;
        if (Aktive != null) {
            Aktive.descendants().forEach(ProcessHandle::destroyForcibly);
            Aktive.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Mappe.toFile()).start(); }
        catch (Exception exception) { fejl(exception); }
    }

    private void vælg() {
        JFileChooser chooser = new JFileChooser(Mappe.toFile());
        if (chooser.showOpenDialog(Vindue) == JFileChooser.APPROVE_OPTION) {
            Sti.setText(chooser.getSelectedFile().getAbsolutePath());
            Belastning();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Mappe);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Vindue.setTitle(Etiket("workspace") + " · WorldOS " + Etiket("identity"));
        Vindue.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Vindue.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                stop(); worker.shutdownNow(); System.exit(0);
            }
        });
        KILDE.setFont(new Font("Monospaced", Font.PLAIN, 17));
        KILDE.setTabSize(4);
        Udgang.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Udgang.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fil = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fil.add(new JLabel(Etiket("file"))); Fil.add(Sti);
        panel.add(Fil);
        JPanel Værktøjslinje = new JPanel(new FlowLayout(FlowLayout.LEADING));
        knap(Værktøjslinje, "open", () -> vælg());
        knap(Værktøjslinje, "save", () -> Gem());
        knap(Værktøjslinje, "compile", () -> compile(false));
        knap(Værktøjslinje, "run", () -> compile(true));
        knap(Værktøjslinje, "stop", () -> stop());
        knap(Værktøjslinje, "terminal", () -> terminal());
        panel.add(Værktøjslinje);
        JPanel Indstillinger = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Indstillinger.add(new JLabel(Etiket("class"))); Indstillinger.add(Navn);
        Indstillinger.add(new JLabel(Etiket("arguments"))); Indstillinger.add(Argumenter);
        panel.add(Indstillinger);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(KILDE), new JScrollPane(Udgang));
        split.setResizeWeight(0.72);
        Vindue.add(panel, BorderLayout.NORTH);
        Vindue.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiket("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        KILDE.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Udgang.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Størrelse = Toolkit.getDefaultToolkit().getScreenSize();
        Vindue.setSize(Math.min(1240, Størrelse.width - 40), Math.min(760, Størrelse.height - 60));
        Vindue.setLocationRelativeTo(null);
        Vindue.setVisible(true);
        Belastning();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiket("help") + "\n");
    }

    public static void main(String[] Argumenter) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
