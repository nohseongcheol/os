// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.CZE.l_cs;
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
    private final JTextArea zdrojový_soubor = new JTextArea();
    private final JTextArea výstupní_pozice = new JTextArea();
    private final JTextField cesta_2 = new JTextField("zdrojový_soubor.java", 26);
    private final JTextField Název = new JTextField("zdrojový_soubor", 15);
    private final JTextField argumenty = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path cesta = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Popisek(String Klíč) {
        return messages.getProperty(Klíč, Klíč);
    }

    private void přidat_na_konec_seznamu(String text) {
        SwingUtilities.invokeLater(() -> {
            výstupní_pozice.append(text);
            výstupní_pozice.setCaretPosition(výstupní_pozice.getDocument().getLength());
        });
    }

    private void chyba(Exception exception) {
        přidat_na_konec_seznamu(Popisek("error") + ": " + exception.toString() + "\n");
    }

    private void tlačítko(JPanel panel, String Klíč, Runnable Akce) {
        JButton tlačítko = new JButton(Popisek(Klíč));
        tlačítko.addActionListener(Události -> Akce.run());
        panel.add(tlačítko);
    }

    private void Zátěž() {
        try {
            zdrojový_soubor.setText(Files.readString(cesta.resolve(cesta_2.getText()), StandardCharsets.UTF_8));
            zdrojový_soubor.setCaretPosition(0);
        } catch (Exception exception) { chyba(exception); }
    }

    private boolean Uložit() {
        try {
            Path název_souboru = cesta.resolve(cesta_2.getText()).normalize();
            Files.createDirectories(název_souboru.getParent());
            Files.writeString(název_souboru, zdrojový_soubor.getText(), StandardCharsets.UTF_8);
            přidat_na_konec_seznamu(Popisek("save") + ": " + název_souboru + "\n");
            return true;
        } catch (Exception exception) { chyba(exception); return false; }
    }

    private int Spustit(List<String> příkaz) throws Exception {
        Proces = new ProcessBuilder(příkaz).directory(cesta.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String vstupní_řádek;
            while ((vstupní_řádek = reader.readLine()) != null) přidat_na_konec_seznamu(vstupní_řádek + "\n");
        }
        int VÝSLEDEK = Proces.waitFor();
        Proces = null;
        přidat_na_konec_seznamu(Popisek("result") + ": " + VÝSLEDEK + "\n");
        return VÝSLEDEK;
    }

    private void compile(boolean Spustit_2) {
        if (!Uložit()) return;
        String název_souboru = cesta.resolve(cesta_2.getText()).toString();
        String Třída = Název.getText().trim();
        String text = argumenty.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(cesta.resolve("classes"));
                int VÝSLEDEK = Spustit(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", cesta.resolve("classes").toString(), název_souboru));
                if (Spustit_2 && VÝSLEDEK == 0) {
                    List<String> příkaz = new ArrayList<>(Arrays.asList("java", "-cp", cesta.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Třída));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(text));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) příkaz.add(parser.sval);
                    Spustit(příkaz);
                }
            } catch (Exception exception) { chyba(exception); }
        });
    }

    private void Zastavit() {
        Process aktuální_pozice = Proces;
        if (aktuální_pozice != null) {
            aktuální_pozice.descendants().forEach(ProcessHandle::destroyForcibly);
            aktuální_pozice.destroyForcibly();
        }
    }

    private void interpret_příkazů() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(cesta.toFile()).start(); }
        catch (Exception exception) { chyba(exception); }
    }

    private void zvolit() {
        JFileChooser chooser = new JFileChooser(cesta.toFile());
        if (chooser.showOpenDialog(Okno) == JFileChooser.APPROVE_OPTION) {
            cesta_2.setText(chooser.getSelectedFile().getAbsolutePath());
            Zátěž();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(cesta);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Okno.setTitle(Popisek("workspace") + " · WorldOS " + Popisek("identity"));
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Události) {
                Zastavit(); worker.shutdownNow(); System.exit(0);
            }
        });
        zdrojový_soubor.setFont(new Font("Monospaced", Font.PLAIN, 17));
        zdrojový_soubor.setTabSize(4);
        výstupní_pozice.setFont(new Font("Monospaced", Font.PLAIN, 14));
        výstupní_pozice.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel název_souboru = new JPanel(new FlowLayout(FlowLayout.LEADING));
        název_souboru.add(new JLabel(Popisek("file"))); název_souboru.add(cesta_2);
        panel.add(název_souboru);
        JPanel Nástrojová_lišta = new JPanel(new FlowLayout(FlowLayout.LEADING));
        tlačítko(Nástrojová_lišta, "open", () -> zvolit());
        tlačítko(Nástrojová_lišta, "save", () -> Uložit());
        tlačítko(Nástrojová_lišta, "compile", () -> compile(false));
        tlačítko(Nástrojová_lišta, "run", () -> compile(true));
        tlačítko(Nástrojová_lišta, "stop", () -> Zastavit());
        tlačítko(Nástrojová_lišta, "terminal", () -> interpret_příkazů());
        panel.add(Nástrojová_lišta);
        JPanel Nastavení = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Nastavení.add(new JLabel(Popisek("class"))); Nastavení.add(Název);
        Nastavení.add(new JLabel(Popisek("arguments"))); Nastavení.add(argumenty);
        panel.add(Nastavení);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(zdrojový_soubor), new JScrollPane(výstupní_pozice));
        split.setResizeWeight(0.72);
        Okno.add(panel, BorderLayout.NORTH);
        Okno.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Popisek("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        zdrojový_soubor.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        výstupní_pozice.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Velikost = Toolkit.getDefaultToolkit().getScreenSize();
        Okno.setSize(Math.min(1240, Velikost.width - 40), Math.min(760, Velikost.height - 60));
        Okno.setLocationRelativeTo(null);
        Okno.setVisible(true);
        Zátěž();
        split.setDividerLocation(0.72);
        přidat_na_konec_seznamu("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        přidat_na_konec_seznamu(Popisek("help") + "\n");
    }

    public static void main(String[] argumenty) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
