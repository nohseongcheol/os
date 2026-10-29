// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.LVA.l_lv;
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
    private final JFrame Logs = new JFrame();
    private final JTextArea AVOTS = new JTextArea();
    private final JTextArea Izvade = new JTextArea();
    private final JTextField CEĻŠ = new JTextField("AVOTS.java", 26);
    private final JTextField Nosaukums = new JTextField("AVOTS", 15);
    private final JTextField Parametri = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Mape = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process process;

    private String Etiķete(String Atslēga) {
        return messages.getProperty(Atslēga, Atslēga);
    }

    private void append(String Teksts) {
        SwingUtilities.invokeLater(() -> {
            Izvade.append(Teksts);
            Izvade.setCaretPosition(Izvade.getDocument().getLength());
        });
    }

    private void Kļūda(Exception exception) {
        append(Etiķete("error") + ": " + exception.toString() + "\n");
    }

    private void Pogas(JPanel Panelis, String Atslēga, Runnable Darbība) {
        JButton Pogas = new JButton(Etiķete(Atslēga));
        Pogas.addActionListener(Notikums -> Darbība.run());
        Panelis.add(Pogas);
    }

    private void Noslodze() {
        try {
            AVOTS.setText(Files.readString(Mape.resolve(CEĻŠ.getText()), StandardCharsets.UTF_8));
            AVOTS.setCaretPosition(0);
        } catch (Exception exception) { Kļūda(exception); }
    }

    private boolean Saglabāt() {
        try {
            Path Fails = Mape.resolve(CEĻŠ.getText()).normalize();
            Files.createDirectories(Fails.getParent());
            Files.writeString(Fails, AVOTS.getText(), StandardCharsets.UTF_8);
            append(Etiķete("save") + ": " + Fails + "\n");
            return true;
        } catch (Exception exception) { Kļūda(exception); return false; }
    }

    private int Izpildīt(List<String> Komanda) throws Exception {
        process = new ProcessBuilder(Komanda).directory(Mape.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String Līniju;
            while ((Līniju = reader.readLine()) != null) append(Līniju + "\n");
        }
        int result = process.waitFor();
        process = null;
        append(Etiķete("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Palaist) {
        if (!Saglabāt()) return;
        String Fails = Mape.resolve(CEĻŠ.getText()).toString();
        String Klase = Nosaukums.getText().trim();
        String Teksts = Parametri.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Mape.resolve("classes"));
                int result = Izpildīt(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Mape.resolve("classes").toString(), Fails));
                if (Palaist && result == 0) {
                    List<String> Komanda = new ArrayList<>(Arrays.asList("java", "-cp", Mape.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klase));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Teksts));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Komanda.add(parser.sval);
                    Izpildīt(Komanda);
                }
            } catch (Exception exception) { Kļūda(exception); }
        });
    }

    private void Pārtraukt() {
        Process Pašreizējais = process;
        if (Pašreizējais != null) {
            Pašreizējais.descendants().forEach(ProcessHandle::destroyForcibly);
            Pašreizējais.destroyForcibly();
        }
    }

    private void Terminālis() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Mape.toFile()).start(); }
        catch (Exception exception) { Kļūda(exception); }
    }

    private void izvēlēties() {
        JFileChooser chooser = new JFileChooser(Mape.toFile());
        if (chooser.showOpenDialog(Logs) == JFileChooser.APPROVE_OPTION) {
            CEĻŠ.setText(chooser.getSelectedFile().getAbsolutePath());
            Noslodze();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Mape);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Logs.setTitle(Etiķete("workspace") + " · WorldOS " + Etiķete("identity"));
        Logs.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Logs.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Notikums) {
                Pārtraukt(); worker.shutdownNow(); System.exit(0);
            }
        });
        AVOTS.setFont(new Font("Monospaced", Font.PLAIN, 17));
        AVOTS.setTabSize(4);
        Izvade.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Izvade.setEditable(false);
        JPanel Panelis = new JPanel(new GridLayout(0, 1));
        JPanel Fails = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fails.add(new JLabel(Etiķete("file"))); Fails.add(CEĻŠ);
        Panelis.add(Fails);
        JPanel Rīkjosla = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Pogas(Rīkjosla, "open", () -> izvēlēties());
        Pogas(Rīkjosla, "save", () -> Saglabāt());
        Pogas(Rīkjosla, "compile", () -> compile(false));
        Pogas(Rīkjosla, "run", () -> compile(true));
        Pogas(Rīkjosla, "stop", () -> Pārtraukt());
        Pogas(Rīkjosla, "terminal", () -> Terminālis());
        Panelis.add(Rīkjosla);
        JPanel Uzstādījumi = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Uzstādījumi.add(new JLabel(Etiķete("class"))); Uzstādījumi.add(Nosaukums);
        Uzstādījumi.add(new JLabel(Etiķete("arguments"))); Uzstādījumi.add(Parametri);
        Panelis.add(Uzstādījumi);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(AVOTS), new JScrollPane(Izvade));
        split.setResizeWeight(0.72);
        Logs.add(Panelis, BorderLayout.NORTH);
        Logs.add(split, BorderLayout.CENTER);
        Panelis.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiķete("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        AVOTS.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Izvade.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Izmērs = Toolkit.getDefaultToolkit().getScreenSize();
        Logs.setSize(Math.min(1240, Izmērs.width - 40), Math.min(760, Izmērs.height - 60));
        Logs.setLocationRelativeTo(null);
        Logs.setVisible(true);
        Noslodze();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiķete("help") + "\n");
    }

    public static void main(String[] Parametri) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
