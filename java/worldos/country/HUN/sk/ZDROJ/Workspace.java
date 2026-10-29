// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.HUN.l_sk;
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
    private final JFrame Okno = new JFrame();
    private final JTextArea ZDROJ = new JTextArea();
    private final JTextArea Výstup = new JTextArea();
    private final JTextField Cesta = new JTextField("ZDROJ.java", 26);
    private final JTextField Názov = new JTextField("ZDROJ", 15);
    private final JTextField Argumenty = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path Adresár = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Nápis(String Kľúč) {
        return messages.getProperty(Kľúč, Kľúč);
    }

    private void append(String Spracovanie_textu) {
        SwingUtilities.invokeLater(() -> {
            Výstup.append(Spracovanie_textu);
            Výstup.setCaretPosition(Výstup.getDocument().getLength());
        });
    }

    private void chyba(Exception exception) {
        append(Nápis("error") + ": " + exception.toString() + "\n");
    }

    private void Tlačidlo(JPanel panel, String Kľúč, Runnable Akcia) {
        JButton Tlačidlo = new JButton(Nápis(Kľúč));
        Tlačidlo.addActionListener(Udalosť -> Akcia.run());
        panel.add(Tlačidlo);
    }

    private void Zaťaženie() {
        try {
            ZDROJ.setText(Files.readString(Adresár.resolve(Cesta.getText()), StandardCharsets.UTF_8));
            ZDROJ.setCaretPosition(0);
        } catch (Exception exception) { chyba(exception); }
    }

    private boolean Uložiť() {
        try {
            Path Súbor = Adresár.resolve(Cesta.getText()).normalize();
            Files.createDirectories(Súbor.getParent());
            Files.writeString(Súbor, ZDROJ.getText(), StandardCharsets.UTF_8);
            append(Nápis("save") + ": " + Súbor + "\n");
            return true;
        } catch (Exception exception) { chyba(exception); return false; }
    }

    private int Spustiť(List<String> Príkaz) throws Exception {
        Proces = new ProcessBuilder(Príkaz).directory(Adresár.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String riadok;
            while ((riadok = reader.readLine()) != null) append(riadok + "\n");
        }
        int result = Proces.waitFor();
        Proces = null;
        append(Nápis("result") + ": " + result + "\n");
        return result;
    }

    private void compile(boolean Spustiť_2) {
        if (!Uložiť()) return;
        String Súbor = Adresár.resolve(Cesta.getText()).toString();
        String Trieda = Názov.getText().trim();
        String Spracovanie_textu = Argumenty.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(Adresár.resolve("classes"));
                int result = Spustiť(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", Adresár.resolve("classes").toString(), Súbor));
                if (Spustiť_2 && result == 0) {
                    List<String> Príkaz = new ArrayList<>(Arrays.asList("java", "-cp", Adresár.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Trieda));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(Spracovanie_textu));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) Príkaz.add(parser.sval);
                    Spustiť(Príkaz);
                }
            } catch (Exception exception) { chyba(exception); }
        });
    }

    private void Zastaviť() {
        Process Aktuálny = Proces;
        if (Aktuálny != null) {
            Aktuálny.descendants().forEach(ProcessHandle::destroyForcibly);
            Aktuálny.destroyForcibly();
        }
    }

    private void Terminál() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(Adresár.toFile()).start(); }
        catch (Exception exception) { chyba(exception); }
    }

    private void vybrať() {
        JFileChooser chooser = new JFileChooser(Adresár.toFile());
        if (chooser.showOpenDialog(Okno) == JFileChooser.APPROVE_OPTION) {
            Cesta.setText(chooser.getSelectedFile().getAbsolutePath());
            Zaťaženie();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(Adresár);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Okno.setTitle(Nápis("workspace") + " · WorldOS " + Nápis("identity"));
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Udalosť) {
                Zastaviť(); worker.shutdownNow(); System.exit(0);
            }
        });
        ZDROJ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        ZDROJ.setTabSize(4);
        Výstup.setFont(new Font("Monospaced", Font.PLAIN, 14));
        Výstup.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel Súbor = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Súbor.add(new JLabel(Nápis("file"))); Súbor.add(Cesta);
        panel.add(Súbor);
        JPanel Panel_nástrojov = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Tlačidlo(Panel_nástrojov, "open", () -> vybrať());
        Tlačidlo(Panel_nástrojov, "save", () -> Uložiť());
        Tlačidlo(Panel_nástrojov, "compile", () -> compile(false));
        Tlačidlo(Panel_nástrojov, "run", () -> compile(true));
        Tlačidlo(Panel_nástrojov, "stop", () -> Zastaviť());
        Tlačidlo(Panel_nástrojov, "terminal", () -> Terminál());
        panel.add(Panel_nástrojov);
        JPanel Nastavenia = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Nastavenia.add(new JLabel(Nápis("class"))); Nastavenia.add(Názov);
        Nastavenia.add(new JLabel(Nápis("arguments"))); Nastavenia.add(Argumenty);
        panel.add(Nastavenia);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ZDROJ), new JScrollPane(Výstup));
        split.setResizeWeight(0.72);
        Okno.add(panel, BorderLayout.NORTH);
        Okno.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Nápis("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        ZDROJ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Výstup.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Veľkosť = Toolkit.getDefaultToolkit().getScreenSize();
        Okno.setSize(Math.min(1240, Veľkosť.width - 40), Math.min(760, Veľkosť.height - 60));
        Okno.setLocationRelativeTo(null);
        Okno.setVisible(true);
        Zaťaženie();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(Nápis("help") + "\n");
    }

    public static void main(String[] Argumenty) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
