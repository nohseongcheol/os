// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NOR.l_nn;
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
    private final JTextArea KJELDE = new JTextArea();
    private final JTextArea Utdata = new JTextArea();
    private final JTextField STIGE = new JTextField("KJELDE.java", 26);
    private final JTextField Namn = new JTextField("KJELDE", 15);
    private final JTextField Argument = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Mappe = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Prosess;

    private String Etikett(String Nøkkel) {
        return messages.getProperty(Nøkkel, Nøkkel);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            Utdata.append(Tekst);
            Utdata.setCaretPosition(Utdata.getDocument().getLength());
        });
    }

    private void FEIL(Exception exception) {
        append(Etikett("error") + ": " + exception.toString() + "\n");
    }

    private void button(JPanel panel, String Nøkkel, Runnable Handling) {
        JButton button = new JButton(Etikett(Nøkkel));
        button.addActionListener(Hending -> Handling.run());
        panel.add(button);
    }

    private void Last() {
        try {
            KJELDE.setText(Files.readString(Mappe.resolve(STIGE.getText()), StandardCharsets.UTF_8));
            KJELDE.setCaretPosition(0);
        } catch (Exception exception) { FEIL(exception); }
    }

    private boolean Lagra() {
        try {
            Path Fil = Mappe.resolve(STIGE.getText()).normalize();
            Files.createDirectories(Fil.getParent());
            Files.writeString(Fil, KJELDE.getText(), StandardCharsets.UTF_8);
            append(Etikett("save") + ": " + Fil + "\n");
            return true;
        } catch (Exception exception) { FEIL(exception); return false; }
    }

    private int Køyr(List<String> Kommando) throws Exception {
        Prosess = new ProcessBuilder(Kommando).directory(Mappe.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Prosess.getInputStream(), StandardCharsets.UTF_8))) {
            String linje;
            while ((linje = reader.readLine()) != null) append(linje + "\n");
        }
        int result = Prosess.waitFor();
        Prosess = null;
        append(Etikett("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Køyr_2) {
        if (!Lagra()) return;
        String Fil = Mappe.resolve(STIGE.getText()).toString();
        String Klasse = Namn.getText().trim();
        String Tekst = Argument.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Mappe.resolve("classes"));
                int result = Køyr(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Mappe.resolve("classes").toString(), Fil));
                if (Køyr_2 && result == 0) {
                    List<String> Kommando = new ArrayList<>(Arrays.asList("java", "-cp", Mappe.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasse));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Kommando.add(parser.sval);
                    Køyr(Kommando);
                }
            } catch (Exception exception) { FEIL(exception); }
        });
    }

    private void Stopp() {
        Process Gjeldande = Prosess;
        if (Gjeldande != null) {
            Gjeldande.descendants().forEach(ProcessHandle::destroyForcibly);
            Gjeldande.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Mappe.toFile()).start(); }
        catch (Exception exception) { FEIL(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Mappe.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            STIGE.setText(chooser.getSelectedFile().getAbsolutePath());
            Last();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Mappe);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Etikett("workspace") + " · WorldOS " + Etikett("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Hending) {
                Stopp(); worker.shutdownNow(); System.exit(0);
            }
        });
        KJELDE.setFont(new Font("Monospaced", Font.PLAIN, 17));
        KJELDE.setTabSize(4);
        Utdata.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Utdata.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fil = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fil.add(new JLabel(Etikett("file"))); Fil.add(STIGE);
        panel.add(Fil);
        JPanel Verktøylinje = new JPanel(new FlowLayout(FlowLayout.LEADING));
        button(Verktøylinje, "open", () -> choose());
        button(Verktøylinje, "save", () -> Lagra());
        button(Verktøylinje, "compile", () -> compile(false));
        button(Verktøylinje, "run", () -> compile(true));
        button(Verktøylinje, "stop", () -> Stopp());
        button(Verktøylinje, "terminal", () -> terminal());
        panel.add(Verktøylinje);
        JPanel Innstillingar = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Innstillingar.add(new JLabel(Etikett("class"))); Innstillingar.add(Namn);
        Innstillingar.add(new JLabel(Etikett("arguments"))); Innstillingar.add(Argument);
        panel.add(Innstillingar);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(KJELDE), new JScrollPane(Utdata));
        split.setResizeWeight(0.72);
        window.add(panel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etikett("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        KJELDE.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Utdata.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Storleik = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Storleik.width - 40), Math.min(760, Storleik.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Last();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etikett("help") + "\n");
    }

    public static void main(String[] Argument) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
