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

/** korisnik 홈에서 Java 원문을 Uredi_VALUE·kompajlirati_izvor·실행하는 작은 Swing radni_prostor. */
public final class radni_prostor {
    private final JFrame prozor = new JFrame("jkoros — 자바 radni_prostor");
    private final JTextArea izvor = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField Datoteka_stavka_ime = new JTextField("인사.java", 20);
    private final JTextField Razred_stavka_ime = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VALUE;
    private final String biblioteka = "/opt/jkoros/lib/한국어자바.jar";

    private void obaveštavanje(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void taster(JPanel verzija_VALUE, String ime, Runnable 행동) {
        JButton taster = new JButton(ime);
        taster.addActionListener(događaj -> 행동.run());
        verzija_VALUE.add(taster);
    }
    private boolean Store_VALUE() {
        try {
            Path putanja = 작업폴더.resolve(Datoteka_stavka_ime.getText());
            Files.createDirectories(putanja.getParent());
            Datoteka.쓰기(putanja, izvor.getText());
            obaveštavanje("Store_VALUE: " + putanja);
            return true;
        } catch (Exception greška) { obaveštavanje(greška.toString()); return false; }
    }
    private void otvoren() {
        try { izvor.setText(Datoteka.읽기(작업폴더.resolve(Datoteka_stavka_ime.getText()))); }
        catch (Exception greška) { obaveštavanje(greška.toString()); }
    }
    private int komanda(List<String> komanda) throws Exception {
        Proces_VALUE = new ProcessBuilder(komanda).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader red = new BufferedReader(new InputStreamReader(Proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = red.readLine()) != null) obaveštavanje(SMS);
        }
        int Status_VALUE = Proces_VALUE.waitFor(); Proces_VALUE = null;
        obaveštavanje("Izađi_program kôd_VALUE: " + Status_VALUE);
        return Status_VALUE;
    }
    private void prevesti_izvor(boolean Izvrši_komanda, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = Datoteka_stavka_ime.getText(), stavka_p_VALUE = Razred_stavka_ime.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    komanda(Arrays.asList("jclassc", "--target", "openjdk", "--entry", stavka_p_VALUE,
                        "--classpath", biblioteka, "-o", "실행프로그램", 입력));
                } else if (komanda(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", biblioteka,
                        "-d", "classes", 입력)) == 0 && Izvrši_komanda) {
                    komanda(Arrays.asList("java", "-cp", "classes:" + biblioteka, stavka_p_VALUE));
                }
            } catch (Exception greška) { obaveštavanje(greška.toString()); }
        });
    }
    private void 멈춤() {
        Process aktuelno_stavka = Proces_VALUE;
        if (aktuelno_stavka != null) { aktuelno_stavka.descendants().forEach(ProcessHandle::destroy); aktuelno_stavka.destroy(); }
    }
    private radni_prostor() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        izvor.setFont(font_VALUE); 출력.setFont(font_VALUE); 출력.setEditable(false);
        izvor.setTabSize(4);
        izvor.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        izvor.setBackground(new Color(250, 251, 252));
        izvor.setForeground(new Color(32, 43, 58));
        JPanel komanda_tabla = new JPanel();
        komanda_tabla.add(new JLabel("Datoteka")); komanda_tabla.add(Datoteka_stavka_ime);
        komanda_tabla.add(new JLabel("주 Razred_VALUE")); komanda_tabla.add(Razred_stavka_ime);
        taster(komanda_tabla, "otvoren", this::otvoren); taster(komanda_tabla, "Store_VALUE", this::Store_VALUE);
        taster(komanda_tabla, "kompajlirati_izvor", () -> prevesti_izvor(false, false));
        taster(komanda_tabla, "Izvrši_komanda", () -> prevesti_izvor(true, false));
        taster(komanda_tabla, "Izvrši_komanda Datoteka Create_stavka", () -> prevesti_izvor(false, true));
        taster(komanda_tabla, "멈춤", this::멈춤);
        JSplitPane deljenje_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(izvor), new JScrollPane(출력));
        deljenje_KR.setResizeWeight(0.75);
        prozor.add(komanda_tabla, BorderLayout.NORTH); prozor.add(deljenje_KR, BorderLayout.CENTER);
        prozor.setSize(1200, 750); prozor.setLocationRelativeTo(null);
        prozor.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        prozor.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent događaj) { 멈춤(); 일꾼.shutdownNow(); }
        });
        otvoren(); prozor.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource podrazumevani_font = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object stavka_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(stavka_VALUE) instanceof Font) UIManager.put(stavka_VALUE, podrazumevani_font);
                }
                new radni_prostor();
            } catch (Exception greška) { greška.printStackTrace(); }
        });
    }
}
