// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

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

/** korisnik 홈에서 Java 원문을 uređivati_VALUE·napraviti_izvor·실행하는 작은 Swing radni_stol. */
public final class radni_stol {
    private final JFrame prozor = new JFrame("jkoros — 자바 radni_stol");
    private final JTextArea IZVOR = new JTextArea();
    private final JTextArea Ispis = new JTextArea(8, 80);
    private final JTextField fajl_unos_naziv = new JTextField("인사.java", 20);
    private final JTextField klasa_unos_naziv = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process proces_VALUE;
    private final String biblioteka = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Tekst) { SwingUtilities.invokeLater(() -> Ispis.append(Tekst + "\n")); }
    private void dugme(JPanel verzija_VALUE, String Naziv, Runnable 행동) {
        JButton dugme = new JButton(Naziv);
        dugme.addActionListener(događaj -> 행동.run());
        verzija_VALUE.add(dugme);
    }
    private boolean Store_VALUE() {
        try {
            Path Putanja = 작업폴더.resolve(fajl_unos_naziv.getText());
            Files.createDirectories(Putanja.getParent());
            Fajl.Piši(Putanja, IZVOR.getText());
            알림("Store_VALUE: " + Putanja);
            return true;
        } catch (Exception GRESKA) { 알림(GRESKA.toString()); return false; }
    }
    private void Otvori() {
        try { IZVOR.setText(Fajl.Čitaj(작업폴더.resolve(fajl_unos_naziv.getText()))); }
        catch (Exception GRESKA) { 알림(GRESKA.toString()); }
    }
    private int Naredba(List<String> Naredba) throws Exception {
        proces_VALUE = new ProcessBuilder(Naredba).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Linija = new BufferedReader(new InputStreamReader(proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = Linija.readLine()) != null) 알림(Tekst);
        }
        int stanje_VALUE = proces_VALUE.waitFor(); proces_VALUE = null;
        알림("izaći_program kod_VALUE: " + stanje_VALUE);
        return stanje_VALUE;
    }
    private void Prevedi_izvor(boolean Izvrši_komanda, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = fajl_unos_naziv.getText(), unos_p_VALUE = klasa_unos_naziv.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Naredba(Arrays.asList("jclassc", "--target", "openjdk", "--entry", unos_p_VALUE,
                        "--classpath", biblioteka, "-o", "실행프로그램", 입력));
                } else if (Naredba(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteka,
                        "-d", "classes", 입력)) == 0 && Izvrši_komanda) {
                    Naredba(Arrays.asList("java", "-cp", "classes:" + biblioteka, unos_p_VALUE));
                }
            } catch (Exception GRESKA) { 알림(GRESKA.toString()); }
        });
    }
    private void 멈춤() {
        Process trenutno_stavka = proces_VALUE;
        if (trenutno_stavka != null) { trenutno_stavka.descendants().forEach(ProcessHandle::destroy); trenutno_stavka.destroy(); }
    }
    private radni_stol() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        IZVOR.setFont(font_VALUE); Ispis.setFont(font_VALUE); Ispis.setEditable(false);
        IZVOR.setTabSize(4);
        IZVOR.setMargin(new Insets(10, 12, 10, 12));
        Ispis.setMargin(new Insets(8, 12, 8, 12));
        IZVOR.setBackground(new Color(250, 251, 252));
        IZVOR.setForeground(new Color(32, 43, 58));
        JPanel komanda_ploča = new JPanel();
        komanda_ploča.add(new JLabel("Fajl")); komanda_ploča.add(fajl_unos_naziv);
        komanda_ploča.add(new JLabel("주 klasa_VALUE")); komanda_ploča.add(klasa_unos_naziv);
        dugme(komanda_ploča, "Otvori", this::Otvori); dugme(komanda_ploča, "Store_VALUE", this::Store_VALUE);
        dugme(komanda_ploča, "napraviti_izvor", () -> Prevedi_izvor(false, false));
        dugme(komanda_ploča, "Izvrši_komanda", () -> Prevedi_izvor(true, false));
        dugme(komanda_ploča, "Izvrši_komanda Fajl Create_unos", () -> Prevedi_izvor(false, true));
        dugme(komanda_ploča, "멈춤", this::멈춤);
        JSplitPane dijeljenje_mjera = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(IZVOR), new JScrollPane(Ispis));
        dijeljenje_mjera.setResizeWeight(0.75);
        prozor.add(komanda_ploča, BorderLayout.NORTH); prozor.add(dijeljenje_mjera, BorderLayout.CENTER);
        prozor.setSize(1200, 750); prozor.setLocationRelativeTo(null);
        prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        prozor.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent događaj) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Otvori(); prozor.setVisible(true);
    }
    public static void main(String[] Argumenti) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standardni_font = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object unos_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(unos_VALUE) instanceof Font) UIManager.put(unos_VALUE, standardni_font);
                }
                new radni_stol();
            } catch (Exception GRESKA) { GRESKA.printStackTrace(); }
        });
    }
}
