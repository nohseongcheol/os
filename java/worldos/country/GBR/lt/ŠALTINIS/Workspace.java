// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.GBR.l_lt;
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
    private final JFrame Langas = new JFrame();
    private final JTextArea ŠALTINIS = new JTextArea();
    private final JTextArea Išvestis = new JTextArea();
    private final JTextField KELIAS = new JTextField("ŠALTINIS.java", 26);
    private final JTextField Pavadinimas_2 = new JTextField("ŠALTINIS", 15);
    private final JTextField Argumentai = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Aplankas = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Procesas;

    private String Pavadinimas(String Raktas) {
        return messages.getProperty(Raktas, Raktas);
    }

    private void append(String Tekstas) {
        SwingUtilities.invokeLater(() -> {
            Išvestis.append(Tekstas);
            Išvestis.setCaretPosition(Išvestis.getDocument().getLength());
        });
    }

    private void KLAIDA(Exception exception) {
        append(Pavadinimas("error") + ": " + exception.toString() + "\n");
    }

    private void mygtukas(JPanel Skydelis, String Raktas, Runnable Veiksmas) {
        JButton mygtukas = new JButton(Pavadinimas(Raktas));
        mygtukas.addActionListener(Įvykis -> Veiksmas.run());
        Skydelis.add(mygtukas);
    }

    private void Apkrova() {
        try {
            ŠALTINIS.setText(Files.readString(Aplankas.resolve(KELIAS.getText()), StandardCharsets.UTF_8));
            ŠALTINIS.setCaretPosition(0);
        } catch (Exception exception) { KLAIDA(exception); }
    }

    private boolean Įrašyti() {
        try {
            Path Failas = Aplankas.resolve(KELIAS.getText()).normalize();
            Files.createDirectories(Failas.getParent());
            Files.writeString(Failas, ŠALTINIS.getText(), StandardCharsets.UTF_8);
            append(Pavadinimas("save") + ": " + Failas + "\n");
            return true;
        } catch (Exception exception) { KLAIDA(exception); return false; }
    }

    private int Vykdyti(List<String> Komanda) throws Exception {
        Procesas = new ProcessBuilder(Komanda).directory(Aplankas.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Procesas.getInputStream(), StandardCharsets.UTF_8))) {
            String Eilutė;
            while ((Eilutė = reader.readLine()) != null) append(Eilutė + "\n");
        }
        int REZULTATAS = Procesas.waitFor();
        Procesas = null;
        append(Pavadinimas("result") + ": " + REZULTATAS + "\n");
        return REZULTATAS;
    }

    private void compile(boolean Paleisti) {
        if (!Įrašyti()) return;
        String Failas = Aplankas.resolve(KELIAS.getText()).toString();
        String Klasė = Pavadinimas_2.getText().trim();
        String Tekstas = Argumentai.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Aplankas.resolve("classes"));
                int REZULTATAS = Vykdyti(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Aplankas.resolve("classes").toString(), Failas));
                if (Paleisti && REZULTATAS == 0) {
                    List<String> Komanda = new ArrayList<>(Arrays.asList("java", "-cp", Aplankas.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasė));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Tekstas));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Komanda.add(parser.sval);
                    Vykdyti(Komanda);
                }
            } catch (Exception exception) { KLAIDA(exception); }
        });
    }

    private void Sustabdyti() {
        Process Dabartinis = Procesas;
        if (Dabartinis != null) {
            Dabartinis.descendants().forEach(ProcessHandle::destroyForcibly);
            Dabartinis.destroyForcibly();
        }
    }

    private void Terminalas() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Aplankas.toFile()).start(); }
        catch (Exception exception) { KLAIDA(exception); }
    }

    private void pasirinkite() {
        JFileChooser chooser = new JFileChooser(Aplankas.toFile());
        if (chooser.showOpenDialog(Langas) == JFileChooser.APPROVE_OPTION) {
            KELIAS.setText(chooser.getSelectedFile().getAbsolutePath());
            Apkrova();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Aplankas);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Langas.setTitle(Pavadinimas("workspace") + " · WorldOS " + Pavadinimas("identity"));
        Langas.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Langas.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Įvykis) {
                Sustabdyti(); worker.shutdownNow(); System.exit(0);
            }
        });
        ŠALTINIS.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ŠALTINIS.setTabSize(4);
        Išvestis.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Išvestis.setEditable(false);
        JPanel Skydelis = new JPanel(new GridLayout(0, 1));
        JPanel Failas = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Failas.add(new JLabel(Pavadinimas("file"))); Failas.add(KELIAS);
        Skydelis.add(Failas);
        JPanel Įrankių_juosta = new JPanel(new FlowLayout(FlowLayout.LEADING));
        mygtukas(Įrankių_juosta, "open", () -> pasirinkite());
        mygtukas(Įrankių_juosta, "save", () -> Įrašyti());
        mygtukas(Įrankių_juosta, "compile", () -> compile(false));
        mygtukas(Įrankių_juosta, "run", () -> compile(true));
        mygtukas(Įrankių_juosta, "stop", () -> Sustabdyti());
        mygtukas(Įrankių_juosta, "terminal", () -> Terminalas());
        Skydelis.add(Įrankių_juosta);
        JPanel Nustatymai = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Nustatymai.add(new JLabel(Pavadinimas("class"))); Nustatymai.add(Pavadinimas_2);
        Nustatymai.add(new JLabel(Pavadinimas("arguments"))); Nustatymai.add(Argumentai);
        Skydelis.add(Nustatymai);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ŠALTINIS), new JScrollPane(Išvestis));
        split.setResizeWeight(0.72);
        Langas.add(Skydelis, BorderLayout.NORTH);
        Langas.add(split, BorderLayout.CENTER);
        Skydelis.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Pavadinimas("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ŠALTINIS.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Išvestis.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Dydis = Toolkit.getDefaultToolkit().getScreenSize();
        Langas.setSize(Math.min(1240, Dydis.width - 40), Math.min(760, Dydis.height - 60));
        Langas.setLocationRelativeTo(null);
        Langas.setVisible(true);
        Apkrova();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Pavadinimas("help") + "\n");
    }

    public static void main(String[] Argumentai) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
