// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.자바;

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

/** korisnik 홈에서 Java 원문을 Uredi_VALUE·programski_prevesti_izvor·실행하는 작은 Swing radni_prostor. */
public final class radni_prostor {
    private final JFrame Prozor = new JFrame("jkoros — 자바 radni_prostor");
    private final JTextArea IZVOR = new JTextArea();
    private final JTextArea Izlaz = new JTextArea(8, 80);
    private final JTextField Datoteka_unos_naziv = new JTextField("인사.java", 20);
    private final JTextField poduka_unos_naziv = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VALUE;
    private final String biblioteka = "/opt/jkoros/lib/한국어자바.jar";

    private void obavijest(String Tekst) { SwingUtilities.invokeLater(() -> Izlaz.append(Tekst + "\n")); }
    private void gumb(JPanel verzija_VALUE, String Ime, Runnable 행동) {
        JButton gumb = new JButton(Ime);
        gumb.addActionListener(Događaj -> 행동.run());
        verzija_VALUE.add(gumb);
    }
    private boolean Store_VALUE() {
        try {
            Path PUTANJA = 작업폴더.resolve(Datoteka_unos_naziv.getText());
            Files.createDirectories(PUTANJA.getParent());
            Datoteka.Zapisuj(PUTANJA, IZVOR.getText());
            obavijest("Store_VALUE: " + PUTANJA);
            return true;
        } catch (Exception GREŠKA) { obavijest(GREŠKA.toString()); return false; }
    }
    private void Otvori() {
        try { IZVOR.setText(Datoteka.Čitaj(작업폴더.resolve(Datoteka_unos_naziv.getText()))); }
        catch (Exception GREŠKA) { obavijest(GREŠKA.toString()); }
    }
    private int Naredba(List<String> Naredba) throws Exception {
        Proces_VALUE = new ProcessBuilder(Naredba).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader red = new BufferedReader(new InputStreamReader(Proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = red.readLine()) != null) obavijest(Tekst);
        }
        int Stanje_VALUE = Proces_VALUE.waitFor(); Proces_VALUE = null;
        obavijest("Izlaz_program kod_VALUE: " + Stanje_VALUE);
        return Stanje_VALUE;
    }
    private void prevesti_izvor(boolean Izvrši_naredba, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = Datoteka_unos_naziv.getText(), unos_p_VALUE = poduka_unos_naziv.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Naredba(Arrays.asList("jclassc", "--target", "openjdk", "--entry", unos_p_VALUE,
                        "--classpath", biblioteka, "-o", "실행프로그램", 입력));
                } else if (Naredba(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteka,
                        "-d", "classes", 입력)) == 0 && Izvrši_naredba) {
                    Naredba(Arrays.asList("java", "-cp", "classes:" + biblioteka, unos_p_VALUE));
                }
            } catch (Exception GREŠKA) { obavijest(GREŠKA.toString()); }
        });
    }
    private void 멈춤() {
        Process redovno_artikl = Proces_VALUE;
        if (redovno_artikl != null) { redovno_artikl.descendants().forEach(ProcessHandle::destroy); redovno_artikl.destroy(); }
    }
    private radni_prostor() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        IZVOR.setFont(font_VALUE); Izlaz.setFont(font_VALUE); Izlaz.setEditable(false);
        IZVOR.setTabSize(4);
        IZVOR.setMargin(new Insets(10, 12, 10, 12));
        Izlaz.setMargin(new Insets(8, 12, 8, 12));
        IZVOR.setBackground(new Color(250, 251, 252));
        IZVOR.setForeground(new Color(32, 43, 58));
        JPanel naredba_panel = new JPanel();
        naredba_panel.add(new JLabel("Datoteka")); naredba_panel.add(Datoteka_unos_naziv);
        naredba_panel.add(new JLabel("주 poduka_VALUE")); naredba_panel.add(poduka_unos_naziv);
        gumb(naredba_panel, "Otvori", this::Otvori); gumb(naredba_panel, "Store_VALUE", this::Store_VALUE);
        gumb(naredba_panel, "programski_prevesti_izvor", () -> prevesti_izvor(false, false));
        gumb(naredba_panel, "Izvrši_naredba", () -> prevesti_izvor(true, false));
        gumb(naredba_panel, "Izvrši_naredba Datoteka Create_unos", () -> prevesti_izvor(false, true));
        gumb(naredba_panel, "멈춤", this::멈춤);
        JSplitPane odjel_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(IZVOR), new JScrollPane(Izlaz));
        odjel_KR.setResizeWeight(0.75);
        Prozor.add(naredba_panel, BorderLayout.NORTH); Prozor.add(odjel_KR, BorderLayout.CENTER);
        Prozor.setSize(1200, 750); Prozor.setLocationRelativeTo(null);
        Prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Prozor.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Događaj) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Otvori(); Prozor.setVisible(true);
    }
    public static void main(String[] Argumenti) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource zadani_font = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object unos_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(unos_VALUE) instanceof Font) UIManager.put(unos_VALUE, zadani_font);
                }
                new radni_prostor();
            } catch (Exception GREŠKA) { GREŠKA.printStackTrace(); }
        });
    }
}
