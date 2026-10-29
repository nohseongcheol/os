// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SVK.l_pl;
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
    private final JTextArea plik_źródłowy = new JTextArea();
    private final JTextArea pozycja_wyjścia = new JTextArea();
    private final JTextField ścieżka_2 = new JTextField("plik_źródłowy.java", 26);
    private final JTextField Nazwa = new JTextField("plik_źródłowy", 15);
    private final JTextField argumenty = new JTextField(25);
    private final Properties messages = new Properties();
    private final Path ścieżka = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private volatile Process Proces;

    private String Etykieta(String Klucz) {
        return messages.getProperty(Klucz, Klucz);
    }

    private void dodaj_na_końcu_listy(String tekst) {
        SwingUtilities.invokeLater(() -> {
            pozycja_wyjścia.append(tekst);
            pozycja_wyjścia.setCaretPosition(pozycja_wyjścia.getDocument().getLength());
        });
    }

    private void błąd(Exception exception) {
        dodaj_na_końcu_listy(Etykieta("error") + ": " + exception.toString() + "\n");
    }

    private void przycisk(JPanel panel, String Klucz, Runnable Akcja) {
        JButton przycisk = new JButton(Etykieta(Klucz));
        przycisk.addActionListener(Wydarzenie -> Akcja.run());
        panel.add(przycisk);
    }

    private void Obciążenie() {
        try {
            plik_źródłowy.setText(Files.readString(ścieżka.resolve(ścieżka_2.getText()), StandardCharsets.UTF_8));
            plik_źródłowy.setCaretPosition(0);
        } catch (Exception exception) { błąd(exception); }
    }

    private boolean Zapisz() {
        try {
            Path nazwa_pliku = ścieżka.resolve(ścieżka_2.getText()).normalize();
            Files.createDirectories(nazwa_pliku.getParent());
            Files.writeString(nazwa_pliku, plik_źródłowy.getText(), StandardCharsets.UTF_8);
            dodaj_na_końcu_listy(Etykieta("save") + ": " + nazwa_pliku + "\n");
            return true;
        } catch (Exception exception) { błąd(exception); return false; }
    }

    private int Uruchom(List<String> polecenie) throws Exception {
        Proces = new ProcessBuilder(polecenie).directory(ścieżka.toFile()).redirectErrorStream(true).start();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(Proces.getInputStream(), StandardCharsets.UTF_8))) {
            String wiersz_wejścia;
            while ((wiersz_wejścia = reader.readLine()) != null) dodaj_na_końcu_listy(wiersz_wejścia + "\n");
        }
        int WYNIK = Proces.waitFor();
        Proces = null;
        dodaj_na_końcu_listy(Etykieta("result") + ": " + WYNIK + "\n");
        return WYNIK;
    }

    private void compile(boolean Uruchom_2) {
        if (!Zapisz()) return;
        String nazwa_pliku = ścieżka.resolve(ścieżka_2.getText()).toString();
        String Klasa = Nazwa.getText().trim();
        String tekst = argumenty.getText();
        worker.submit(() -> {
            try {
                Files.createDirectories(ścieżka.resolve("classes"));
                int WYNIK = Uruchom(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ścieżka.resolve("classes").toString(), nazwa_pliku));
                if (Uruchom_2 && WYNIK == 0) {
                    List<String> polecenie = new ArrayList<>(Arrays.asList("java", "-cp", ścieżka.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Klasa));
                    StreamTokenizer parser = new StreamTokenizer(new StringReader(tekst));
                    parser.resetSyntax(); parser.wordChars(33, 65535); parser.whitespaceChars(0, 32);
                    parser.quoteChar('"'); parser.quoteChar('\'');
                    while (parser.nextToken() != StreamTokenizer.TT_EOF) polecenie.add(parser.sval);
                    Uruchom(polecenie);
                }
            } catch (Exception exception) { błąd(exception); }
        });
    }

    private void Zatrzymaj() {
        Process bieżąca_pozycja = Proces;
        if (bieżąca_pozycja != null) {
            bieżąca_pozycja.descendants().forEach(ProcessHandle::destroyForcibly);
            bieżąca_pozycja.destroyForcibly();
        }
    }

    private void interpretator_poleceń() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ścieżka.toFile()).start(); }
        catch (Exception exception) { błąd(exception); }
    }

    private void wybierz() {
        JFileChooser chooser = new JFileChooser(ścieżka.toFile());
        if (chooser.showOpenDialog(Okno) == JFileChooser.APPROVE_OPTION) {
            ścieżka_2.setText(chooser.getSelectedFile().getAbsolutePath());
            Obciążenie();
        }
    }

    private void initialize() {
        try (Reader reader = new InputStreamReader(Workspace.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            messages.load(reader);
            Files.createDirectories(ścieżka);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Okno.setTitle(Etykieta("workspace") + " · WorldOS " + Etykieta("identity"));
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Wydarzenie) {
                Zatrzymaj(); worker.shutdownNow(); System.exit(0);
            }
        });
        plik_źródłowy.setFont(new Font("Monospaced", Font.PLAIN, 17));
        plik_źródłowy.setTabSize(4);
        pozycja_wyjścia.setFont(new Font("Monospaced", Font.PLAIN, 14));
        pozycja_wyjścia.setEditable(false);
        JPanel panel = new JPanel(new GridLayout(0, 1));
        JPanel nazwa_pliku = new JPanel(new FlowLayout(FlowLayout.LEADING));
        nazwa_pliku.add(new JLabel(Etykieta("file"))); nazwa_pliku.add(ścieżka_2);
        panel.add(nazwa_pliku);
        JPanel Pasek_narzędziowy = new JPanel(new FlowLayout(FlowLayout.LEADING));
        przycisk(Pasek_narzędziowy, "open", () -> wybierz());
        przycisk(Pasek_narzędziowy, "save", () -> Zapisz());
        przycisk(Pasek_narzędziowy, "compile", () -> compile(false));
        przycisk(Pasek_narzędziowy, "run", () -> compile(true));
        przycisk(Pasek_narzędziowy, "stop", () -> Zatrzymaj());
        przycisk(Pasek_narzędziowy, "terminal", () -> interpretator_poleceń());
        panel.add(Pasek_narzędziowy);
        JPanel Ustawienia = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Ustawienia.add(new JLabel(Etykieta("class"))); Ustawienia.add(Nazwa);
        Ustawienia.add(new JLabel(Etykieta("arguments"))); Ustawienia.add(argumenty);
        panel.add(Ustawienia);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(plik_źródłowy), new JScrollPane(pozycja_wyjścia));
        split.setResizeWeight(0.72);
        Okno.add(panel, BorderLayout.NORTH);
        Okno.add(split, BorderLayout.CENTER);
        panel.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Etykieta("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        plik_źródłowy.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        pozycja_wyjścia.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Rozmiar = Toolkit.getDefaultToolkit().getScreenSize();
        Okno.setSize(Math.min(1240, Rozmiar.width - 40), Math.min(760, Rozmiar.height - 60));
        Okno.setLocationRelativeTo(null);
        Okno.setVisible(true);
        Obciążenie();
        split.setDividerLocation(0.72);
        dodaj_na_końcu_listy("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        dodaj_na_końcu_listy(Etykieta("help") + "\n");
    }

    public static void main(String[] argumenty) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new Workspace().initialize());
    }
}
