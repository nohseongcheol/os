// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.NOR.l_nb;
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
    private final JFrame Vindu = new JFrame();
    private final JTextArea KILDE = new JTextArea();
    private final JTextArea Utgang = new JTextArea();
    private final JTextField Sti = new JTextField("KILDE.java", 26);
    private final JTextField Navn = new JTextField("KILDE", 15);
    private final JTextField Argumenter = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Mappe = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Prosess;

    private String Etikett(String Nøkkel) {
        return messages.getProperty(Nøkkel, Nøkkel);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            Utgang.append(Tekst);
            Utgang.setCaretPosition(Utgang.getDocument().getLength());
        });
    }

    private void feil(Exception exception) {
        append(Etikett("error") + ": " + exception.toString() + "\n");
    }

    private void Knapp(JPanel panel, String Nøkkel, Runnable Handling) {
        JButton Knapp = new JButton(Etikett(Nøkkel));
        Knapp.addActionListener(Hendelse -> Handling.run());
        panel.add(Knapp);
    }

    private void Belastning() {
        try {
            KILDE.setText(Files.readString(Mappe.resolve(Sti.getText()), StandardCharsets.UTF_8));
            KILDE.setCaretPosition(0);
        } catch (Exception exception) { feil(exception); }
    }

    private boolean Lagre() {
        try {
            Path Fil = Mappe.resolve(Sti.getText()).normalize();
            Files.createDirectories(Fil.getParent());
            Files.writeString(Fil, KILDE.getText(), StandardCharsets.UTF_8);
            append(Etikett("save") + ": " + Fil + "\n");
            return true;
        } catch (Exception exception) { feil(exception); return false; }
    }

    private int Kjør(List<String> Kommando) throws Exception {
        Prosess = new ProcessBuilder(Kommando).directory(Mappe.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Prosess.getInputStream(), StandardCharsets.UTF_8))) {
            String Linje;
            while ((Linje = reader.readLine()) != null) append(Linje + "\n");
        }
        int result = Prosess.waitFor();
        Prosess = null;
        append(Etikett("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Kjør_2) {
        if (!Lagre()) return;
        String Fil = Mappe.resolve(Sti.getText()).toString();
        String Klasse = Navn.getText().trim();
        String Tekst = Argumenter.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Mappe.resolve("classes"));
                int result = Kjør(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Mappe.resolve("classes").toString(), Fil));
                if (Kjør_2 && result == 0) {
                    List<String> Kommando = new ArrayList<>(Arrays.asList("java", "-cp", Mappe.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasse));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Kommando.add(parser.sval);
                    Kjør(Kommando);
                }
            } catch (Exception exception) { feil(exception); }
        });
    }

    private void Stopp() {
        Process Gjeldende = Prosess;
        if (Gjeldende != null) {
            Gjeldende.descendants().forEach(ProcessHandle::destroyForcibly);
            Gjeldende.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Mappe.toFile()).start(); }
        catch (Exception exception) { feil(exception); }
    }

    private void Velg() {
        JFileChooser chooser = new JFileChooser(Mappe.toFile());
        if (chooser.showOpenDialog(Vindu) == JFileChooser.APPROVE_OPTION) {
            Sti.setText(chooser.getSelectedFile().getAbsolutePath());
            Belastning();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Mappe);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Vindu.setTitle(Etikett("workspace") + " · WorldOS " + Etikett("identity"));
        Vindu.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Vindu.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Hendelse) {
                Stopp(); worker.shutdownNow(); System.exit(0);
            }
        });
        KILDE.setFont(new Font("Monospaced", Font.PLAIN, 17));
        KILDE.setTabSize(4);
        Utgang.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Utgang.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fil = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fil.add(new JLabel(Etikett("file"))); Fil.add(Sti);
        panel.add(Fil);
        JPanel Verktøylinje = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Knapp(Verktøylinje, "open", () -> Velg());
        Knapp(Verktøylinje, "save", () -> Lagre());
        Knapp(Verktøylinje, "compile", () -> compile(false));
        Knapp(Verktøylinje, "run", () -> compile(true));
        Knapp(Verktøylinje, "stop", () -> Stopp());
        Knapp(Verktøylinje, "terminal", () -> terminal());
        panel.add(Verktøylinje);
        JPanel Innstillinger = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Innstillinger.add(new JLabel(Etikett("class"))); Innstillinger.add(Navn);
        Innstillinger.add(new JLabel(Etikett("arguments"))); Innstillinger.add(Argumenter);
        panel.add(Innstillinger);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(KILDE), new JScrollPane(Utgang));
        split.setResizeWeight(0.72);
        Vindu.add(panel, BorderLayout.NORTH);
        Vindu.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etikett("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        KILDE.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Utgang.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Størrelse = Toolkit.getDefaultToolkit().getScreenSize();
        Vindu.setSize(Math.min(1240, Størrelse.width - 40), Math.min(760, Størrelse.height - 60));
        Vindu.setLocationRelativeTo(null);
        Vindu.setVisible(true);
        Belastning();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etikett("help") + "\n");
    }

    public static void main(String[] Argumenter) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
