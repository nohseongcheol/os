// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.FRA.l_eu;
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
    private final JFrame Leihoa = new JFrame();
    private final JTextArea ITURBURUA = new JTextArea();
    private final JTextArea Irteera = new JTextArea();
    private final JTextField Bide_izena = new JTextField("ITURBURUA.java", 26);
    private final JTextField Izena = new JTextField("ITURBURUA", 15);
    private final JTextField Argumentuak = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Direktorioa = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Prozesua;

    private String Etiketa(String Gakoa) {
        return messages.getProperty(Gakoa, Gakoa);
    }

    private void append(String Testua) {
        SwingUtilities.invokeLater(() -> {
            Irteera.append(Testua);
            Irteera.setCaretPosition(Irteera.getDocument().getLength());
        });
    }

    private void errorea(Exception exception) {
        append(Etiketa("error") + ": " + exception.toString() + "\n");
    }

    private void botoia(JPanel Panela, String Gakoa, Runnable Ekintza) {
        JButton botoia = new JButton(Etiketa(Gakoa));
        botoia.addActionListener(Gertaera -> Ekintza.run());
        Panela.add(botoia);
    }

    private void Karga() {
        try {
            ITURBURUA.setText(Files.readString(Direktorioa.resolve(Bide_izena.getText()), StandardCharsets.UTF_8));
            ITURBURUA.setCaretPosition(0);
        } catch (Exception exception) { errorea(exception); }
    }

    private boolean Gorde() {
        try {
            Path Fitxategia = Direktorioa.resolve(Bide_izena.getText()).normalize();
            Files.createDirectories(Fitxategia.getParent());
            Files.writeString(Fitxategia, ITURBURUA.getText(), StandardCharsets.UTF_8);
            append(Etiketa("save") + ": " + Fitxategia + "\n");
            return true;
        } catch (Exception exception) { errorea(exception); return false; }
    }

    private int Exekutatu(List<String> Komandoa) throws Exception {
        Prozesua = new ProcessBuilder(Komandoa).directory(Direktorioa.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Prozesua.getInputStream(), StandardCharsets.UTF_8))) {
            String Marra;
            while ((Marra = reader.readLine()) != null) append(Marra + "\n");
        }
        int EMAITZA = Prozesua.waitFor();
        Prozesua = null;
        append(Etiketa("result") + ": " + EMAITZA + "\n");
        return EMAITZA;
    }

    private void compile(boolean Exekutatu_2) {
        if (!Gorde()) return;
        String Fitxategia = Direktorioa.resolve(Bide_izena.getText()).toString();
        String Klasea = Izena.getText().trim();
        String Testua = Argumentuak.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Direktorioa.resolve("classes"));
                int EMAITZA = Exekutatu(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Direktorioa.resolve("classes").toString(), Fitxategia));
                if (Exekutatu_2 && EMAITZA == 0) {
                    List<String> Komandoa = new ArrayList<>(Arrays.asList("java", "-cp", Direktorioa.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasea));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Testua));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Komandoa.add(parser.sval);
                    Exekutatu(Komandoa);
                }
            } catch (Exception exception) { errorea(exception); }
        });
    }

    private void Gelditu() {
        Process Unekoa = Prozesua;
        if (Unekoa != null) {
            Unekoa.descendants().forEach(ProcessHandle::destroyForcibly);
            Unekoa.destroyForcibly();
        }
    }

    private void Terminala() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Direktorioa.toFile()).start(); }
        catch (Exception exception) { errorea(exception); }
    }

    private void hautatu() {
        JFileChooser chooser = new JFileChooser(Direktorioa.toFile());
        if (chooser.showOpenDialog(Leihoa) == JFileChooser.APPROVE_OPTION) {
            Bide_izena.setText(chooser.getSelectedFile().getAbsolutePath());
            Karga();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Direktorioa);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Leihoa.setTitle(Etiketa("workspace") + " · WorldOS " + Etiketa("identity"));
        Leihoa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Leihoa.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Gertaera) {
                Gelditu(); worker.shutdownNow(); System.exit(0);
            }
        });
        ITURBURUA.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ITURBURUA.setTabSize(4);
        Irteera.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Irteera.setEditable(false);
        JPanel Panela = new JPanel(new GridLayout(0, 1));
        JPanel Fitxategia = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Fitxategia.add(new JLabel(Etiketa("file"))); Fitxategia.add(Bide_izena);
        Panela.add(Fitxategia);
        JPanel Tresna_barra = new JPanel(new FlowLayout(FlowLayout.LEADING));
        botoia(Tresna_barra, "open", () -> hautatu());
        botoia(Tresna_barra, "save", () -> Gorde());
        botoia(Tresna_barra, "compile", () -> compile(false));
        botoia(Tresna_barra, "run", () -> compile(true));
        botoia(Tresna_barra, "stop", () -> Gelditu());
        botoia(Tresna_barra, "terminal", () -> Terminala());
        Panela.add(Tresna_barra);
        JPanel Ezarpenak = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ezarpenak.add(new JLabel(Etiketa("class"))); Ezarpenak.add(Izena);
        Ezarpenak.add(new JLabel(Etiketa("arguments"))); Ezarpenak.add(Argumentuak);
        Panela.add(Ezarpenak);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ITURBURUA), new JScrollPane(Irteera));
        split.setResizeWeight(0.72);
        Leihoa.add(Panela, BorderLayout.NORTH);
        Leihoa.add(split, BorderLayout.CENTER);
        Panela.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etiketa("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ITURBURUA.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Irteera.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Tamaina = Toolkit.getDefaultToolkit().getScreenSize();
        Leihoa.setSize(Math.min(1240, Tamaina.width - 40), Math.min(760, Tamaina.height - 60));
        Leihoa.setLocationRelativeTo(null);
        Leihoa.setVisible(true);
        Karga();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Etiketa("help") + "\n");
    }

    public static void main(String[] Argumentuak) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
