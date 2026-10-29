// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.RUS.l_fi;
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
    private final JFrame Ikkuna = new JFrame();
    private final JTextArea lähdetiedosto = new JTextArea();
    private final JTextArea tulostuspaikka = new JTextArea();
    private final JTextField polku_2 = new JTextField("lähdetiedosto.java", 26);
    private final JTextField Nimi = new JTextField("lähdetiedosto", 15);
    private final JTextField argumentit = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path polku = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Prosessi;

    private String Nimike(String Avain) {
        return messages.getProperty(Avain, Avain);
    }

    private void lisää_listan_loppuun(String teksti) {
        SwingUtilities.invokeLater(() -> {
            tulostuspaikka.append(teksti);
            tulostuspaikka.setCaretPosition(tulostuspaikka.getDocument().getLength());
        });
    }

    private void VIRHE(Exception exception) {
        lisää_listan_loppuun(Nimike("error") + ": " + exception.toString() + "\n");
    }

    private void painike(JPanel Paneeli, String Avain, Runnable Toiminto) {
        JButton painike = new JButton(Nimike(Avain));
        painike.addActionListener(Tapahtuma -> Toiminto.run());
        Paneeli.add(painike);
    }

    private void Verkkokuorma() {
        try {
            lähdetiedosto.setText(Files.readString(polku.resolve(polku_2.getText()), StandardCharsets.UTF_8));
            lähdetiedosto.setCaretPosition(0);
        } catch (Exception exception) { VIRHE(exception); }
    }

    private boolean Tallenna() {
        try {
            Path tiedoston_nimi = polku.resolve(polku_2.getText()).normalize();
            Files.createDirectories(tiedoston_nimi.getParent());
            Files.writeString(tiedoston_nimi, lähdetiedosto.getText(), StandardCharsets.UTF_8);
            lisää_listan_loppuun(Nimike("save") + ": " + tiedoston_nimi + "\n");
            return true;
        } catch (Exception exception) { VIRHE(exception); return false; }
    }

    private int Suorita(List<String> komento) throws Exception {
        Prosessi = new ProcessBuilder(komento).directory(polku.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Prosessi.getInputStream(), StandardCharsets.UTF_8))) {
            String syöterivi;
            while ((syöterivi = reader.readLine()) != null) lisää_listan_loppuun(syöterivi + "\n");
        }
        int TULOS = Prosessi.waitFor();
        Prosessi = null;
        lisää_listan_loppuun(Nimike("result") + ": " + TULOS + "\n");
        return TULOS;
    }

    private void compile(boolean Suorita_2) {
        if (!Tallenna()) return;
        String tiedoston_nimi = polku.resolve(polku_2.getText()).toString();
        String Luokka = Nimi.getText().trim();
        String teksti = argumentit.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(polku.resolve("classes"));
                int TULOS = Suorita(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", polku.resolve("classes").toString(), tiedoston_nimi));
                if (Suorita_2 && TULOS == 0) {
                    List<String> komento = new ArrayList<>(Arrays.asList("java", "-cp", polku.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Luokka));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(teksti));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) komento.add(parser.sval);
                    Suorita(komento);
                }
            } catch (Exception exception) { VIRHE(exception); }
        });
    }

    private void Pysäytä() {
        Process nykyinen_paikka = Prosessi;
        if (nykyinen_paikka != null) {
            nykyinen_paikka.descendants().forEach(ProcessHandle::destroyForcibly);
            nykyinen_paikka.destroyForcibly();
        }
    }

    private void komentotulkki() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(polku.toFile()).start(); }
        catch (Exception exception) { VIRHE(exception); }
    }

    private void valitse() {
        JFileChooser chooser = new JFileChooser(polku.toFile());
        if (chooser.showOpenDialog(Ikkuna) == JFileChooser.APPROVE_OPTION) {
            polku_2.setText(chooser.getSelectedFile().getAbsolutePath());
            Verkkokuorma();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(polku);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Ikkuna.setTitle(Nimike("workspace") + " · WorldOS " + Nimike("identity"));
        Ikkuna.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Ikkuna.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Tapahtuma) {
                Pysäytä(); worker.shutdownNow(); System.exit(0);
            }
        });
        lähdetiedosto.setFont(new Font("Monospaced", Font.PLAIN, 17));
        lähdetiedosto.setTabSize(4);
        tulostuspaikka.setFont(new Font("Monospaced", Font.PLAIN, 14));
        tulostuspaikka.setEditable(false);
        JPanel Paneeli = new JPanel(new GridLayout(0, 1));
        JPanel tiedoston_nimi = new JPanel(new FlowLayout(FlowLayout.LEADING));
        tiedoston_nimi.add(new JLabel(Nimike("file"))); tiedoston_nimi.add(polku_2);
        Paneeli.add(tiedoston_nimi);
        JPanel Työkalupalkki = new JPanel(new FlowLayout(FlowLayout.LEADING));
        painike(Työkalupalkki, "open", () -> valitse());
        painike(Työkalupalkki, "save", () -> Tallenna());
        painike(Työkalupalkki, "compile", () -> compile(false));
        painike(Työkalupalkki, "run", () -> compile(true));
        painike(Työkalupalkki, "stop", () -> Pysäytä());
        painike(Työkalupalkki, "terminal", () -> komentotulkki());
        Paneeli.add(Työkalupalkki);
        JPanel Asetukset = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Asetukset.add(new JLabel(Nimike("class"))); Asetukset.add(Nimi);
        Asetukset.add(new JLabel(Nimike("arguments"))); Asetukset.add(argumentit);
        Paneeli.add(Asetukset);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(lähdetiedosto), new JScrollPane(tulostuspaikka));
        split.setResizeWeight(0.72);
        Ikkuna.add(Paneeli, BorderLayout.NORTH);
        Ikkuna.add(split, BorderLayout.CENTER);
        Paneeli.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Nimike("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        lähdetiedosto.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        tulostuspaikka.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Koko = Toolkit.getDefaultToolkit().getScreenSize();
        Ikkuna.setSize(Math.min(1240, Koko.width - 40), Math.min(760, Koko.height - 60));
        Ikkuna.setLocationRelativeTo(null);
        Ikkuna.setVisible(true);
        Verkkokuorma();
        split.setDividerLocation(0.72);
        lisää_listan_loppuun("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        lisää_listan_loppuun(Nimike("help") + "\n");
    }

    public static void main(String[] argumentit) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
