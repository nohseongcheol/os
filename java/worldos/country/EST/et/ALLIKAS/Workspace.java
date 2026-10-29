// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.EST.l_et;
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
    private final JTextArea ALLIKAS = new JTextArea();
    private final JTextArea Väljund = new JTextArea();
    private final JTextField RADA = new JTextField("ALLIKAS.java", 26);
    private final JTextField Nimi_2 = new JTextField("ALLIKAS", 15);
    private final JTextField Argumendid = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Kataloog = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Protsess;

    private String Silt(String Võti) {
        return messages.getProperty(Võti, Võti);
    }

    private void append(String Tekst) {
        SwingUtilities.invokeLater(() -> {
            Väljund.append(Tekst);
            Väljund.setCaretPosition(Väljund.getDocument().getLength());
        });
    }

    private void VIGA(Exception exception) {
        append(Silt("error") + ": " + exception.toString() + "\n");
    }

    private void nupp(JPanel Paneel, String Võti, Runnable Nimi) {
        JButton nupp = new JButton(Silt(Võti));
        nupp.addActionListener(Sündmus -> Nimi.run());
        Paneel.add(nupp);
    }

    private void Koormus() {
        try {
            ALLIKAS.setText(Files.readString(Kataloog.resolve(RADA.getText()), StandardCharsets.UTF_8));
            ALLIKAS.setCaretPosition(0);
        } catch (Exception exception) { VIGA(exception); }
    }

    private boolean Salvesta() {
        try {
            Path Fail = Kataloog.resolve(RADA.getText()).normalize();
            Files.createDirectories(Fail.getParent());
            Files.writeString(Fail, ALLIKAS.getText(), StandardCharsets.UTF_8);
            append(Silt("save") + ": " + Fail + "\n");
            return true;
        } catch (Exception exception) { VIGA(exception); return false; }
    }

    private int Käivita(List<String> Käsk) throws Exception {
        Protsess = new ProcessBuilder(Käsk).directory(Kataloog.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Protsess.getInputStream(), StandardCharsets.UTF_8))) {
            String Joon;
            while ((Joon = reader.readLine()) != null) append(Joon + "\n");
        }
        int TULEMUS = Protsess.waitFor();
        Protsess = null;
        append(Silt("result") + ": " + TULEMUS + "\n");
        return TULEMUS;
    }

    private void compile(boolean Käivita_2) {
        if (!Salvesta()) return;
        String Fail = Kataloog.resolve(RADA.getText()).toString();
        String Klass = Nimi_2.getText().trim();
        String Tekst = Argumendid.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Kataloog.resolve("classes"));
                int TULEMUS = Käivita(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Kataloog.resolve("classes").toString(), Fail));
                if (Käivita_2 && TULEMUS == 0) {
                    List<String> Käsk = new ArrayList<>(Arrays.asList("java", "-cp", Kataloog.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klass));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Käsk.add(parser.sval);
                    Käivita(Käsk);
                }
            } catch (Exception exception) { VIGA(exception); }
        });
    }

    private void Peata() {
        Process Käesolev = Protsess;
        if (Käesolev != null) {
            Käesolev.descendants().forEach(ProcessHandle::destroyForcibly);
            Käesolev.destroyForcibly();
        }
    }

    private void terminal() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Kataloog.toFile()).start(); }
        catch (Exception exception) { VIGA(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(Kataloog.toFile());
        if (chooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
            RADA.setText(chooser.getSelectedFile().getAbsolutePath());
            Koormus();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Kataloog);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        window.setTitle(Silt("workspace") + " · WorldOS " + Silt("identity"));
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Sündmus) {
                Peata(); worker.shutdownNow(); System.exit(0);
            }
        });
        ALLIKAS.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ALLIKAS.setTabSize(4);
        Väljund.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Väljund.setEditable(false);
        JPanel Paneel = new JPanel(new GridLayout(0, 1));
        JPanel Fail = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fail.add(new JLabel(Silt("file"))); Fail.add(RADA);
        Paneel.add(Fail);
        JPanel Tööriistariba = new JPanel(new FlowLayout(FlowLayout.LEADING));
        nupp(Tööriistariba, "open", () -> choose());
        nupp(Tööriistariba, "save", () -> Salvesta());
        nupp(Tööriistariba, "compile", () -> compile(false));
        nupp(Tööriistariba, "run", () -> compile(true));
        nupp(Tööriistariba, "stop", () -> Peata());
        nupp(Tööriistariba, "terminal", () -> terminal());
        Paneel.add(Tööriistariba);
        JPanel Seaded = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Seaded.add(new JLabel(Silt("class"))); Seaded.add(Nimi_2);
        Seaded.add(new JLabel(Silt("arguments"))); Seaded.add(Argumendid);
        Paneel.add(Seaded);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ALLIKAS), new JScrollPane(Väljund));
        split.setResizeWeight(0.72);
        window.add(Paneel, BorderLayout.NORTH);
        window.add(split, BorderLayout.CENTER);
        Paneel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Silt("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ALLIKAS.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Väljund.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Suurus = Toolkit.getDefaultToolkit().getScreenSize();
        window.setSize(Math.min(1240, Suurus.width - 40), Math.min(760, Suurus.height - 60));
        window.setLocationRelativeTo(null);
        window.setVisible(true);
        Koormus();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Silt("help") + "\n");
    }

    public static void main(String[] Argumendid) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
