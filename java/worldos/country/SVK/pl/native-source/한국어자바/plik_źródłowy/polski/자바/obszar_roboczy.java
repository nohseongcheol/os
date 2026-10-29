// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.자바;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;

/** przestrzeń_użytkownika 홈에서 Java 원문을 Edytuj_WARTOŚĆ·kompilować_źródło·실행하는 작은 Swing obszar_roboczy. */
public final class obszar_roboczy {
    private final JFrame Okno = new JFrame("jkoros — 자바 obszar_roboczy");
    private final JTextArea plik_źródłowy = new JTextArea();
    private final JTextArea pozycja_wyjścia = new JTextArea(8, 80);
    private final JTextField Plik_wpis_nazwa = new JTextField("인사.java", 20);
    private final JTextField Klasa_wpis_nazwa = new JTextField("인사", 16);
    private final Path katalog_roboczy = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService pracownik_WARTOŚĆ = Executors.newSingleThreadExecutor();
    private volatile Process Proces_WARTOŚĆ;
    private final String biblioteka = "/opt/jkoros/lib/한국어자바.jar";

    private void powiadomienie(String tekst) { SwingUtilities.invokeLater(() -> pozycja_wyjścia.append(tekst + "\n")); }
    private void przycisk(JPanel wersja_WARTOŚĆ, String Nazwa, Runnable 행동) {
        JButton przycisk = new JButton(Nazwa);
        przycisk.addActionListener(Wydarzenie -> 행동.run());
        wersja_WARTOŚĆ.add(przycisk);
    }
    private boolean Store_WARTOŚĆ() {
        try {
            Path ścieżka_2 = katalog_roboczy.resolve(Plik_wpis_nazwa.getText());
            Files.createDirectories(ścieżka_2.getParent());
            nazwa_pliku.Zapis(ścieżka_2, plik_źródłowy.getText());
            powiadomienie("Store_WARTOŚĆ: " + ścieżka_2);
            return true;
        } catch (Exception błąd) { powiadomienie(błąd.toString()); return false; }
    }
    private void Otwórz() {
        try { plik_źródłowy.setText(nazwa_pliku.Odczyt(katalog_roboczy.resolve(Plik_wpis_nazwa.getText()))); }
        catch (Exception błąd) { powiadomienie(błąd.toString()); }
    }
    private int polecenie(List<String> polecenie) throws Exception {
        Proces_WARTOŚĆ = new ProcessBuilder(polecenie).directory(katalog_roboczy.toFile()).redirectErrorStream(true).start();
        try (BufferedReader wiersz_wejścia = new BufferedReader(new InputStreamReader(Proces_WARTOŚĆ.getInputStream(), StandardCharsets.UTF_8))) {
            String tekst;
            while ((tekst = wiersz_wejścia.readLine()) != null) powiadomienie(tekst);
        }
        int Stan_WARTOŚĆ = Proces_WARTOŚĆ.waitFor(); Proces_WARTOŚĆ = null;
        powiadomienie("wyjść_program KOD_WARTOŚĆ: " + Stan_WARTOŚĆ);
        return Stan_WARTOŚĆ;
    }
    private void TŁUMACZ_źródło(boolean Wykonaj_polecenie, boolean plik_wykonywalny) {
        if (!Store_WARTOŚĆ()) return;
        String wejście_WARTOŚĆ = Plik_wpis_nazwa.getText(), punkt_wejścia_WARTOŚĆ = Klasa_wpis_nazwa.getText();
        pracownik_WARTOŚĆ.submit(() -> {
            try {
                Files.createDirectories(katalog_roboczy.resolve("classes"));
                if (plik_wykonywalny) {
                    polecenie(Arrays.asList("jclassc", "--target", "openjdk", "--entry", punkt_wejścia_WARTOŚĆ,
                        "--classpath", biblioteka, "-o", "실행프로그램", wejście_WARTOŚĆ));
                } else if (polecenie(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteka,
                        "-d", "classes", wejście_WARTOŚĆ)) == 0 && Wykonaj_polecenie) {
                    polecenie(Arrays.asList("java", "-cp", "classes:" + biblioteka, punkt_wejścia_WARTOŚĆ));
                }
            } catch (Exception błąd) { powiadomienie(błąd.toString()); }
        });
    }
    private void Wstrzymaj_wykonanie() {
        Process bieżący_towar = Proces_WARTOŚĆ;
        if (bieżący_towar != null) { bieżący_towar.descendants().forEach(ProcessHandle::destroy); bieżący_towar.destroy(); }
    }
    private obszar_roboczy() throws IOException {
        Files.createDirectories(katalog_roboczy);
        Font czcionka_WARTOŚĆ = new Font("Monospaced", Font.PLAIN, 16);
        plik_źródłowy.setFont(czcionka_WARTOŚĆ); pozycja_wyjścia.setFont(czcionka_WARTOŚĆ); pozycja_wyjścia.setEditable(false);
        plik_źródłowy.setTabSize(4);
        plik_źródłowy.setMargin(new Insets(10, 12, 10, 12));
        pozycja_wyjścia.setMargin(new Insets(8, 12, 8, 12));
        plik_źródłowy.setBackground(new Color(250, 251, 252));
        plik_źródłowy.setForeground(new Color(32, 43, 58));
        JPanel polecenie_panel = new JPanel();
        polecenie_panel.add(new JLabel("nazwa_pliku")); polecenie_panel.add(Plik_wpis_nazwa);
        polecenie_panel.add(new JLabel("주 Klasa_WARTOŚĆ")); polecenie_panel.add(Klasa_wpis_nazwa);
        przycisk(polecenie_panel, "Otwórz", this::Otwórz); przycisk(polecenie_panel, "Store_WARTOŚĆ", this::Store_WARTOŚĆ);
        przycisk(polecenie_panel, "kompilować_źródło", () -> TŁUMACZ_źródło(false, false));
        przycisk(polecenie_panel, "Wykonaj_polecenie", () -> TŁUMACZ_źródło(true, false));
        przycisk(polecenie_panel, "Wykonaj_polecenie nazwa_pliku Twórca_wpis", () -> TŁUMACZ_źródło(false, true));
        przycisk(polecenie_panel, "Wstrzymaj_wykonanie", this::Wstrzymaj_wykonanie);
        JSplitPane Dywizja_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(plik_źródłowy), new JScrollPane(pozycja_wyjścia));
        Dywizja_KR.setResizeWeight(0.75);
        Okno.add(polecenie_panel, BorderLayout.NORTH); Okno.add(Dywizja_KR, BorderLayout.CENTER);
        Okno.setSize(1200, 750); Okno.setLocationRelativeTo(null);
        Okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Okno.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Wydarzenie) { Wstrzymaj_wykonanie(); pracownik_WARTOŚĆ.shutdownNow(); }
        });
        Otwórz(); Okno.setVisible(true);
    }
    public static void main(String[] argumenty) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource czcionka_domyślna = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object wpis_WARTOŚĆ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(wpis_WARTOŚĆ) instanceof Font) UIManager.put(wpis_WARTOŚĆ, czcionka_domyślna);
                }
                new obszar_roboczy();
            } catch (Exception błąd) { błąd.printStackTrace(); }
        });
    }
}
