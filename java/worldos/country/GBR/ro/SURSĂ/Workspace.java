// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_ro;
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
    private final JFrame Fereastră = new JFrame();
    private final JTextArea SURSĂ = new JTextArea();
    private final JTextArea Rezultat = new JTextArea();
    private final JTextField Cale = new JTextField("SURSĂ.java", 26);
    private final JTextField Nume = new JTextField("SURSĂ", 15);
    private final JTextField Argumente = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Director = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Etichetă(String Cheie) {
        return messages.getProperty(Cheie, Cheie);
    }

    private void append(String text) {
        SwingUtilities.invokeLater(() -> {
            Rezultat.append(text);
            Rezultat.setCaretPosition(Rezultat.getDocument().getLength());
        });
    }

    private void eroare(Exception exception) {
        append(Etichetă("error") + ": " + exception.toString() + "\n");
    }

    private void buton(JPanel Panou, String Cheie, Runnable Acțiuni) {
        JButton buton = new JButton(Etichetă(Cheie));
        buton.addActionListener(Eveniment -> Acțiuni.run());
        Panou.add(buton);
    }

    private void Încărcare() {
        try {
            SURSĂ.setText(Files.readString(Director.resolve(Cale.getText()), StandardCharsets.UTF_8));
            SURSĂ.setCaretPosition(0);
        } catch (Exception exception) { eroare(exception); }
    }

    private boolean Salvează() {
        try {
            Path Fișier = Director.resolve(Cale.getText()).normalize();
            Files.createDirectories(Fișier.getParent());
            Files.writeString(Fișier, SURSĂ.getText(), StandardCharsets.UTF_8);
            append(Etichetă("save") + ": " + Fișier + "\n");
            return true;
        } catch (Exception exception) { eroare(exception); return false; }
    }

    private int Execută(List<String> Comandă) throws Exception {
        Proces = new ProcessBuilder(Comandă).directory(Director.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String Linie;
            while ((Linie = reader.readLine()) != null) append(Linie + "\n");
        }
        int result = Proces.waitFor();
        Proces = null;
        append(Etichetă("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Pornește) {
        if (!Salvează()) return;
        String Fișier = Director.resolve(Cale.getText()).toString();
        String Clasa = Nume.getText().trim();
        String text = Argumente.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Director.resolve("classes"));
                int result = Execută(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Director.resolve("classes").toString(), Fișier));
                if (Pornește && result == 0) {
                    List<String> Comandă = new ArrayList<>(Arrays.asList("java", "-cp", Director.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Clasa));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Comandă.add(parser.sval);
                    Execută(Comandă);
                }
            } catch (Exception exception) { eroare(exception); }
        });
    }

    private void Oprește() {
        Process Curentă = Proces;
        if (Curentă != null) {
            Curentă.descendants().forEach(ProcessHandle::destroyForcibly);
            Curentă.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Director.toFile()).start(); }
        catch (Exception exception) { eroare(exception); }
    }

    private void alegeți() {
        JFileChooser chooser = new JFileChooser(Director.toFile());
        if (chooser.showOpenDialog(Fereastră) == JFileChooser.APPROVE_OPTION) {
            Cale.setText(chooser.getSelectedFile().getAbsolutePath());
            Încărcare();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Director);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Fereastră.setTitle(Etichetă("workspace") + " · WorldOS " + Etichetă("identity"));
        Fereastră.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fereastră.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Eveniment) {
                Oprește(); worker.shutdownNow(); System.exit(0);
            }
        });
        SURSĂ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        SURSĂ.setTabSize(4);
        Rezultat.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Rezultat.setEditable(false);
        JPanel Panou = new JPanel(new GridLayout(0, 1));
        JPanel Fișier = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fișier.add(new JLabel(Etichetă("file"))); Fișier.add(Cale);
        Panou.add(Fișier);
        JPanel Bară_cu_unelte = new JPanel(new FlowLayout(FlowLayout.LEADING));
        buton(Bară_cu_unelte, "open", () -> alegeți());
        buton(Bară_cu_unelte, "save", () -> Salvează());
        buton(Bară_cu_unelte, "compile", () -> compile(false));
        buton(Bară_cu_unelte, "run", () -> compile(true));
        buton(Bară_cu_unelte, "stop", () -> Oprește());
        buton(Bară_cu_unelte, "terminal", () -> terminal());
        Panou.add(Bară_cu_unelte);
        JPanel Setări = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Setări.add(new JLabel(Etichetă("class"))); Setări.add(Nume);
        Setări.add(new JLabel(Etichetă("arguments"))); Setări.add(Argumente);
        Panou.add(Setări);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(SURSĂ), new JScrollPane(Rezultat));
        split.setResizeWeight(0.72);
        Fereastră.add(Panou, BorderLayout.NORTH);
        Fereastră.add(split, BorderLayout.CENTER);
        Panou.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etichetă("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        SURSĂ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Rezultat.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Mărime = Toolkit.getDefaultToolkit().getScreenSize();
        Fereastră.setSize(Math.min(1240, Mărime.width - 40), Math.min(760, Mărime.height - 60));
        Fereastră.setLocationRelativeTo(null);
        Fereastră.setVisible(true);
        Încărcare();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etichetă("help") + "\n");
    }

    public static void main(String[] Argumente) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
