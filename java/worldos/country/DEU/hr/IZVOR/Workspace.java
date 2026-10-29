// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.DEU.l_hr;
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
    private final JFrame Prozor = new JFrame();
    private final JTextArea IZVOR = new JTextArea();
    private final JTextArea Izlaz = new JTextArea();
    private final JTextField PUTANJA = new JTextField("IZVOR.java", 26);
    private final JTextField Ime = new JTextField("IZVOR", 15);
    private final JTextField Argumenti = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Direktorij = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Natpis(String Ključ) {
        return messages.getProperty(Ključ, Ključ);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            Izlaz.append(Tekst);
            Izlaz.setCaretPosition(Izlaz.getDocument().getLength());
        });
    }

    private void GREŠKA(Exception exception) {
        append(Natpis("error") + ": " + exception.toString() + "\n");
    }

    private void gumb(JPanel Ploča, String Ključ, Runnable Aktivnost) {
        JButton gumb = new JButton(Natpis(Ključ));
        gumb.addActionListener(Događaj -> Aktivnost.run());
        Ploča.add(gumb);
    }

    private void Opterečenje() {
        try {
            IZVOR.setText(Files.readString(Direktorij.resolve(PUTANJA.getText()), StandardCharsets.UTF_8));
            IZVOR.setCaretPosition(0);
        } catch (Exception exception) { GREŠKA(exception); }
    }

    private boolean Spremi() {
        try {
            Path Datoteka = Direktorij.resolve(PUTANJA.getText()).normalize();
            Files.createDirectories(Datoteka.getParent());
            Files.writeString(Datoteka, IZVOR.getText(), StandardCharsets.UTF_8);
            append(Natpis("save") + ": " + Datoteka + "\n");
            return true;
        } catch (Exception exception) { GREŠKA(exception); return false; }
    }

    private int Izvrši(List<String> Naredba) throws Exception {
        Proces = new ProcessBuilder(Naredba).directory(Direktorij.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int REZULTAT = Proces.waitFor();
        Proces = null;
        append(Natpis("result") + ": " + REZULTAT + "\n");
        return REZULTAT;
    }

    private void compile(boolean Pokreni) {
        if (!Spremi()) return;
        String Datoteka = Direktorij.resolve(PUTANJA.getText()).toString();
        String Razred = Ime.getText().trim();
        String Tekst = Argumenti.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Direktorij.resolve("classes"));
                int REZULTAT = Izvrši(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Direktorij.resolve("classes").toString(), Datoteka));
                if (Pokreni && REZULTAT == 0) {
                    List<String> Naredba = new ArrayList<>(Arrays.asList("java", "-cp", Direktorij.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Razred));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Naredba.add(parser.sval);
                    Izvrši(Naredba);
                }
            } catch (Exception exception) { GREŠKA(exception); }
        });
    }

    private void Zaustavi() {
        Process Trenutno = Proces;
        if (Trenutno != null) {
            Trenutno.descendants().forEach(ProcessHandle::destroyForcibly);
            Trenutno.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Direktorij.toFile()).start(); }
        catch (Exception exception) { GREŠKA(exception); }
    }

    private void izaberi() {
        JFileChooser chooser = new JFileChooser(Direktorij.toFile());
        if (chooser.showOpenDialog(Prozor) == JFileChooser.APPROVE_OPTION) {
            PUTANJA.setText(chooser.getSelectedFile().getAbsolutePath());
            Opterečenje();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Direktorij);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Prozor.setTitle(Natpis("workspace") + " · WorldOS " + Natpis("identity"));
        Prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Prozor.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Događaj) {
                Zaustavi(); worker.shutdownNow(); System.exit(0);
            }
        });
        IZVOR.setFont(new Font("Monospaced", Font.PLAIN, 17));
        IZVOR.setTabSize(4);
        Izlaz.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Izlaz.setEditable(false);
        JPanel Ploča = new JPanel(new GridLayout(0, 1));
        JPanel Datoteka = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Datoteka.add(new JLabel(Natpis("file"))); Datoteka.add(PUTANJA);
        Ploča.add(Datoteka);
        JPanel Alatna_traka = new JPanel(new FlowLayout(FlowLayout.LEADING));
        gumb(Alatna_traka, "open", () -> izaberi());
        gumb(Alatna_traka, "save", () -> Spremi());
        gumb(Alatna_traka, "compile", () -> compile(false));
        gumb(Alatna_traka, "run", () -> compile(true));
        gumb(Alatna_traka, "stop", () -> Zaustavi());
        gumb(Alatna_traka, "terminal", () -> terminal());
        Ploča.add(Alatna_traka);
        JPanel Postavke = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Postavke.add(new JLabel(Natpis("class"))); Postavke.add(Ime);
        Postavke.add(new JLabel(Natpis("arguments"))); Postavke.add(Argumenti);
        Ploča.add(Postavke);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(IZVOR), new JScrollPane(Izlaz));
        split.setResizeWeight(0.72);
        Prozor.add(Ploča, BorderLayout.NORTH);
        Prozor.add(split, BorderLayout.CENTER);
        Ploča.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Natpis("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        IZVOR.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Izlaz.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Veličina = Toolkit.getDefaultToolkit().getScreenSize();
        Prozor.setSize(Math.min(1240, Veličina.width - 40), Math.min(760, Veličina.height - 60));
        Prozor.setLocationRelativeTo(null);
        Prozor.setVisible(true);
        Opterečenje();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Natpis("help") + "\n");
    }

    public static void main(String[] Argumenti) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
