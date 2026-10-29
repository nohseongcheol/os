// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.MNE.l_sq;
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
    private final JFrame Dritare = new JFrame();
    private final JTextArea BURIMI = new JTextArea();
    private final JTextArea output = new JTextArea();
    private final JTextField POZICIONI = new JTextField("BURIMI.java", 26);
    private final JTextField Emër = new JTextField("BURIMI", 15);
    private final JTextField Argumente = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Dosje = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proçes;

    private String Etiketë(String Çeles) {
        return messages.getProperty(Çeles, Çeles);
    }

    private void append(String Teksti) {
        SwingUtilities.invokeLater(() -> {
            output.append(Teksti);
            output.setCaretPosition(output.getDocument().getLength());
        });
    }

    private void GABIM(Exception exception) {
        append(Etiketë("error") + ": " + exception.toString() + "\n");
    }

    private void Buton(JPanel panel, String Çeles, Runnable Veprim) {
        JButton Buton = new JButton(Etiketë(Çeles));
        Buton.addActionListener(Ngjarje -> Veprim.run());
        panel.add(Buton);
    }

    private void Ngarko() {
        try {
            BURIMI.setText(Files.readString(Dosje.resolve(POZICIONI.getText()), StandardCharsets.UTF_8));
            BURIMI.setCaretPosition(0);
        } catch (Exception exception) { GABIM(exception); }
    }

    private boolean Ruaj() {
        try {
            Path Kartelë = Dosje.resolve(POZICIONI.getText()).normalize();
            Files.createDirectories(Kartelë.getParent());
            Files.writeString(Kartelë, BURIMI.getText(), StandardCharsets.UTF_8);
            append(Etiketë("save") + ": " + Kartelë + "\n");
            return true;
        } catch (Exception exception) { GABIM(exception); return false; }
    }

    private int Kryej(List<String> Komanda) throws Exception {
        Proçes = new ProcessBuilder(Komanda).directory(Dosje.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proçes.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) append(line + "\n");
        }
        int result = Proçes.waitFor();
        Proçes = null;
        append(Etiketë("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Ekzekuto) {
        if (!Ruaj()) return;
        String Kartelë = Dosje.resolve(POZICIONI.getText()).toString();
        String Klasa = Emër.getText().trim();
        String Teksti = Argumente.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Dosje.resolve("classes"));
                int result = Kryej(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Dosje.resolve("classes").toString(), Kartelë));
                if (Ekzekuto && result == 0) {
                    List<String> Komanda = new ArrayList<>(Arrays.asList("java", "-cp", Dosje.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasa));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Teksti));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Komanda.add(parser.sval);
                    Kryej(Komanda);
                }
            } catch (Exception exception) { GABIM(exception); }
        });
    }

    private void Ndalo() {
        Process E_tanishme = Proçes;
        if (E_tanishme != null) {
            E_tanishme.descendants().forEach(ProcessHandle::destroyForcibly);
            E_tanishme.destroyForcibly();
        }
    }

    private void Terminali() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Dosje.toFile()).start(); }
        catch (Exception exception) { GABIM(exception); }
    }

    private void zgjidhni() {
        JFileChooser chooser = new JFileChooser(Dosje.toFile());
        if (chooser.showOpenDialog(Dritare) == JFileChooser.APPROVE_OPTION) {
            POZICIONI.setText(chooser.getSelectedFile().getAbsolutePath());
            Ngarko();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Dosje);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Dritare.setTitle(Etiketë("workspace") + " · WorldOS " + Etiketë("identity"));
        Dritare.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Dritare.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Ngjarje) {
                Ndalo(); worker.shutdownNow(); System.exit(0);
            }
        });
        BURIMI.setFont(new Font("Monospaced", Font.PLAIN, 17));
        BURIMI.setTabSize(4);
        output.setFont(new Font("Monospaced", Font.PLAIN, 14));
        output.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Kartelë = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Kartelë.add(new JLabel(Etiketë("file"))); Kartelë.add(POZICIONI);
        panel.add(Kartelë);
        JPanel Paneli_i_instrumentëve = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Buton(Paneli_i_instrumentëve, "open", () -> zgjidhni());
        Buton(Paneli_i_instrumentëve, "save", () -> Ruaj());
        Buton(Paneli_i_instrumentëve, "compile", () -> compile(false));
        Buton(Paneli_i_instrumentëve, "run", () -> compile(true));
        Buton(Paneli_i_instrumentëve, "stop", () -> Ndalo());
        Buton(Paneli_i_instrumentëve, "terminal", () -> Terminali());
        panel.add(Paneli_i_instrumentëve);
        JPanel Rregullime = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Rregullime.add(new JLabel(Etiketë("class"))); Rregullime.add(Emër);
        Rregullime.add(new JLabel(Etiketë("arguments"))); Rregullime.add(Argumente);
        panel.add(Rregullime);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(BURIMI), new JScrollPane(output));
        split.setResizeWeight(0.72);
        Dritare.add(panel, BorderLayout.NORTH);
        Dritare.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiketë("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        BURIMI.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        output.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Madhësi = Toolkit.getDefaultToolkit().getScreenSize();
        Dritare.setSize(Math.min(1240, Madhësi.width - 40), Math.min(760, Madhësi.height - 60));
        Dritare.setLocationRelativeTo(null);
        Dritare.setVisible(true);
        Ngarko();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiketë("help") + "\n");
    }

    public static void main(String[] Argumente) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
