// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.TUR.l_el;
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
    private final JFrame Παράθυρο = new JFrame();
    private final JTextArea ΠΗΓΗ = new JTextArea();
    private final JTextArea Έξοδος = new JTextArea();
    private final JTextField ΔΙΑΔΡΟΜΗ = new JTextField("ΠΗΓΗ.java", 26);
    private final JTextField Όνομα = new JTextField("ΠΗΓΗ", 15);
    private final JTextField Παράμετροι = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Κατάλογος = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Διεργασία;

    private String Ετικέτα(String Κλειδί) {
        return messages.getProperty(Κλειδί, Κλειδί);
    }

    private void append(String Κείμενο) {
        SwingUtilities.invokeLater(() -> {
            Έξοδος.append(Κείμενο);
            Έξοδος.setCaretPosition(Έξοδος.getDocument().getLength());
        });
    }

    private void ΣΦΑΛΜΑ(Exception exception) {
        append(Ετικέτα("error") + ": " + exception.toString() + "\n");
    }

    private void κουμπί(JPanel Πίνακας_εφαρμογών, String Κλειδί, Runnable Ενέργεια) {
        JButton κουμπί = new JButton(Ετικέτα(Κλειδί));
        κουμπί.addActionListener(Συμβάν -> Ενέργεια.run());
        Πίνακας_εφαρμογών.add(κουμπί);
    }

    private void Φόρτος() {
        try {
            ΠΗΓΗ.setText(Files.readString(Κατάλογος.resolve(ΔΙΑΔΡΟΜΗ.getText()), StandardCharsets.UTF_8));
            ΠΗΓΗ.setCaretPosition(0);
        } catch (Exception exception) { ΣΦΑΛΜΑ(exception); }
    }

    private boolean Αποθήκευση() {
        try {
            Path Αρχείο = Κατάλογος.resolve(ΔΙΑΔΡΟΜΗ.getText()).normalize();
            Files.createDirectories(Αρχείο.getParent());
            Files.writeString(Αρχείο, ΠΗΓΗ.getText(), StandardCharsets.UTF_8);
            append(Ετικέτα("save") + ": " + Αρχείο + "\n");
            return true;
        } catch (Exception exception) { ΣΦΑΛΜΑ(exception); return false; }
    }

    private int Εκτέλεση(List<String> Εντολή) throws Exception {
        Διεργασία = new ProcessBuilder(Εντολή).directory(Κατάλογος.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Διεργασία.getInputStream(), StandardCharsets.UTF_8))) {
            String Γραμμή;
            while ((Γραμμή = reader.readLine()) != null) append(Γραμμή + "\n");
        }
        int result = Διεργασία.waitFor();
        Διεργασία = null;
        append(Ετικέτα("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Εκτέλεση_2) {
        if (!Αποθήκευση()) return;
        String Αρχείο = Κατάλογος.resolve(ΔΙΑΔΡΟΜΗ.getText()).toString();
        String Κλάση = Όνομα.getText().trim();
        String Κείμενο = Παράμετροι.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Κατάλογος.resolve("classes"));
                int result = Εκτέλεση(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Κατάλογος.resolve("classes").toString(), Αρχείο));
                if (Εκτέλεση_2 && result == 0) {
                    List<String> Εντολή = new ArrayList<>(Arrays.asList("java", "-cp", Κατάλογος.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Κλάση));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Κείμενο));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Εντολή.add(parser.sval);
                    Εκτέλεση(Εντολή);
                }
            } catch (Exception exception) { ΣΦΑΛΜΑ(exception); }
        });
    }

    private void Στοπ() {
        Process Τρέχον = Διεργασία;
        if (Τρέχον != null) {
            Τρέχον.descendants().forEach(ProcessHandle::destroyForcibly);
            Τρέχον.destroyForcibly();
        }
    }

    private void Τερματικό() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Κατάλογος.toFile()).start(); }
        catch (Exception exception) { ΣΦΑΛΜΑ(exception); }
    }

    private void επιλογή() {
        JFileChooser chooser = new JFileChooser(Κατάλογος.toFile());
        if (chooser.showOpenDialog(Παράθυρο) == JFileChooser.APPROVE_OPTION) {
            ΔΙΑΔΡΟΜΗ.setText(chooser.getSelectedFile().getAbsolutePath());
            Φόρτος();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Κατάλογος);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Παράθυρο.setTitle(Ετικέτα("workspace") + " · WorldOS " + Ετικέτα("identity"));
        Παράθυρο.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Παράθυρο.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Συμβάν) {
                Στοπ(); worker.shutdownNow(); System.exit(0);
            }
        });
        ΠΗΓΗ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ΠΗΓΗ.setTabSize(4);
        Έξοδος.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Έξοδος.setEditable(false);
        JPanel Πίνακας_εφαρμογών = new JPanel(new GridLayout(0, 1));
        JPanel Αρχείο = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Αρχείο.add(new JLabel(Ετικέτα("file"))); Αρχείο.add(ΔΙΑΔΡΟΜΗ);
        Πίνακας_εφαρμογών.add(Αρχείο);
        JPanel Εργαλειοθήκη = new JPanel(new FlowLayout(FlowLayout.LEADING));
        κουμπί(Εργαλειοθήκη, "open", () -> επιλογή());
        κουμπί(Εργαλειοθήκη, "save", () -> Αποθήκευση());
        κουμπί(Εργαλειοθήκη, "compile", () -> compile(false));
        κουμπί(Εργαλειοθήκη, "run", () -> compile(true));
        κουμπί(Εργαλειοθήκη, "stop", () -> Στοπ());
        κουμπί(Εργαλειοθήκη, "terminal", () -> Τερματικό());
        Πίνακας_εφαρμογών.add(Εργαλειοθήκη);
        JPanel Ρυθμίσεις = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ρυθμίσεις.add(new JLabel(Ετικέτα("class"))); Ρυθμίσεις.add(Όνομα);
        Ρυθμίσεις.add(new JLabel(Ετικέτα("arguments"))); Ρυθμίσεις.add(Παράμετροι);
        Πίνακας_εφαρμογών.add(Ρυθμίσεις);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ΠΗΓΗ), new JScrollPane(Έξοδος));
        split.setResizeWeight(0.72);
        Παράθυρο.add(Πίνακας_εφαρμογών, BorderLayout.NORTH);
        Παράθυρο.add(split, BorderLayout.CENTER);
        Πίνακας_εφαρμογών.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Ετικέτα("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ΠΗΓΗ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Έξοδος.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Μέγεθος = Toolkit.getDefaultToolkit().getScreenSize();
        Παράθυρο.setSize(Math.min(1240, Μέγεθος.width - 40), Math.min(760, Μέγεθος.height - 60));
        Παράθυρο.setLocationRelativeTo(null);
        Παράθυρο.setVisible(true);
        Φόρτος();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Ετικέτα("help") + "\n");
    }

    public static void main(String[] Παράμετροι) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
