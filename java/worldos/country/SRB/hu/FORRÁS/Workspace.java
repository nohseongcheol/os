// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SRB.l_hu;
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
    private final JFrame Ablak = new JFrame();
    private final JTextArea FORRÁS = new JTextArea();
    private final JTextArea Kimenet = new JTextArea();
    private final JTextField ÚTVONAL = new JTextField("FORRÁS.java", 26);
    private final JTextField Név = new JTextField("FORRÁS", 15);
    private final JTextField Argumentumok = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Könyvtár = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Folyamat;

    private String Címke(String Billentyű) {
        return messages.getProperty(Billentyű, Billentyű);
    }

    private void append(String Szöveg) {
        SwingUtilities.invokeLater(() -> {
            Kimenet.append(Szöveg);
            Kimenet.setCaretPosition(Kimenet.getDocument().getLength());
        });
    }

    private void HIBA(Exception exception) {
        append(Címke("error") + ": " + exception.toString() + "\n");
    }

    private void gomb(JPanel panel, String Billentyű, Runnable Művelet) {
        JButton gomb = new JButton(Címke(Billentyű));
        gomb.addActionListener(Esemény -> Művelet.run());
        panel.add(gomb);
    }

    private void Terhelés() {
        try {
            FORRÁS.setText(Files.readString(Könyvtár.resolve(ÚTVONAL.getText()), StandardCharsets.UTF_8));
            FORRÁS.setCaretPosition(0);
        } catch (Exception exception) { HIBA(exception); }
    }

    private boolean Mentés() {
        try {
            Path Fájl = Könyvtár.resolve(ÚTVONAL.getText()).normalize();
            Files.createDirectories(Fájl.getParent());
            Files.writeString(Fájl, FORRÁS.getText(), StandardCharsets.UTF_8);
            append(Címke("save") + ": " + Fájl + "\n");
            return true;
        } catch (Exception exception) { HIBA(exception); return false; }
    }

    private int Végrehajtás(List<String> Parancs) throws Exception {
        Folyamat = new ProcessBuilder(Parancs).directory(Könyvtár.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Folyamat.getInputStream(), StandardCharsets.UTF_8))) {
            String Vonal;
            while ((Vonal = reader.readLine()) != null) append(Vonal + "\n");
        }
        int result = Folyamat.waitFor();
        Folyamat = null;
        append(Címke("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Futtatás) {
        if (!Mentés()) return;
        String Fájl = Könyvtár.resolve(ÚTVONAL.getText()).toString();
        String Osztály = Név.getText().trim();
        String Szöveg = Argumentumok.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Könyvtár.resolve("classes"));
                int result = Végrehajtás(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Könyvtár.resolve("classes").toString(), Fájl));
                if (Futtatás && result == 0) {
                    List<String> Parancs = new ArrayList<>(Arrays.asList("java", "-cp", Könyvtár.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Osztály));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Szöveg));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Parancs.add(parser.sval);
                    Végrehajtás(Parancs);
                }
            } catch (Exception exception) { HIBA(exception); }
        });
    }

    private void Leállítás() {
        Process Jelenlegi = Folyamat;
        if (Jelenlegi != null) {
            Jelenlegi.descendants().forEach(ProcessHandle::destroyForcibly);
            Jelenlegi.destroyForcibly();
        }
    }

    private void Terminál() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Könyvtár.toFile()).start(); }
        catch (Exception exception) { HIBA(exception); }
    }

    private void Válasszon() {
        JFileChooser chooser = new JFileChooser(Könyvtár.toFile());
        if (chooser.showOpenDialog(Ablak) == JFileChooser.APPROVE_OPTION) {
            ÚTVONAL.setText(chooser.getSelectedFile().getAbsolutePath());
            Terhelés();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Könyvtár);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Ablak.setTitle(Címke("workspace") + " · WorldOS " + Címke("identity"));
        Ablak.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ablak.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Esemény) {
                Leállítás(); worker.shutdownNow(); System.exit(0);
            }
        });
        FORRÁS.setFont(new Font("Monospaced", Font.PLAIN, 17));
        FORRÁS.setTabSize(4);
        Kimenet.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Kimenet.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Fájl = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fájl.add(new JLabel(Címke("file"))); Fájl.add(ÚTVONAL);
        panel.add(Fájl);
        JPanel Eszköztár = new JPanel(new FlowLayout(FlowLayout.LEADING));
        gomb(Eszköztár, "open", () -> Válasszon());
        gomb(Eszköztár, "save", () -> Mentés());
        gomb(Eszköztár, "compile", () -> compile(false));
        gomb(Eszköztár, "run", () -> compile(true));
        gomb(Eszköztár, "stop", () -> Leállítás());
        gomb(Eszköztár, "terminal", () -> Terminál());
        panel.add(Eszköztár);
        JPanel Beállítások = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Beállítások.add(new JLabel(Címke("class"))); Beállítások.add(Név);
        Beállítások.add(new JLabel(Címke("arguments"))); Beállítások.add(Argumentumok);
        panel.add(Beállítások);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(FORRÁS), new JScrollPane(Kimenet));
        split.setResizeWeight(0.72);
        Ablak.add(panel, BorderLayout.NORTH);
        Ablak.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Címke("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        FORRÁS.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Kimenet.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Méret = Toolkit.getDefaultToolkit().getScreenSize();
        Ablak.setSize(Math.min(1240, Méret.width - 40), Math.min(760, Méret.height - 60));
        Ablak.setLocationRelativeTo(null);
        Ablak.setVisible(true);
        Terhelés();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Címke("help") + "\n");
    }

    public static void main(String[] Argumentumok) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
