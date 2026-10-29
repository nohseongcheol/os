// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자바;

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

/** erabiltzaile 홈에서 Java 원문을 edizio_balio·eraiki_iturburu·실행하는 작은 Swing laneko_area. */
public final class laneko_area {
    private final JFrame Leihoa = new JFrame("jkoros — 자바 laneko_area");
    private final JTextArea ITURBURUA = new JTextArea();
    private final JTextArea Irteera = new JTextArea(8, 80);
    private final JTextField fitxategi_sarrera_izen = new JTextField("인사.java", 20);
    private final JTextField Gela_sarrera_izen = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process prozesu_balio;
    private final String liburutegi = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Testua) { SwingUtilities.invokeLater(() -> Irteera.append(Testua + "\n")); }
    private void botoia(JPanel bertsio_balio, String Izena, Runnable 행동) {
        JButton botoia = new JButton(Izena);
        botoia.addActionListener(Gertaera -> 행동.run());
        bertsio_balio.add(botoia);
    }
    private boolean Store_balio() {
        try {
            Path Bide_izena = 작업폴더.resolve(fitxategi_sarrera_izen.getText());
            Files.createDirectories(Bide_izena.getParent());
            Fitxategia.Idatzi(Bide_izena, ITURBURUA.getText());
            알림("Store_balio: " + Bide_izena);
            return true;
        } catch (Exception errorea) { 알림(errorea.toString()); return false; }
    }
    private void Ireki() {
        try { ITURBURUA.setText(Fitxategia.Irakurri(작업폴더.resolve(fitxategi_sarrera_izen.getText()))); }
        catch (Exception errorea) { 알림(errorea.toString()); }
    }
    private int Komandoa(List<String> Komandoa) throws Exception {
        prozesu_balio = new ProcessBuilder(Komandoa).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Marra = new BufferedReader(new InputStreamReader(prozesu_balio.getInputStream(), StandardCharsets.UTF_8))) {
            String Testua;
            while ((Testua = Marra.readLine()) != null) 알림(Testua);
        }
        int Egoera_balio = prozesu_balio.waitFor(); prozesu_balio = null;
        알림("irten_aplik KODE_balio: " + Egoera_balio);
        return Egoera_balio;
    }
    private void ITZULI_iturburu(boolean exekutatu_komando, boolean 실행파일) {
        if (!Store_balio()) return;
        String 입력 = fitxategi_sarrera_izen.getText(), sarrera_p_balio = Gela_sarrera_izen.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Komandoa(Arrays.asList("jclassc", "--target", "openjdk", "--entry", sarrera_p_balio,
                        "--classpath", liburutegi, "-o", "실행프로그램", 입력));
                } else if (Komandoa(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", liburutegi,
                        "-d", "classes", 입력)) == 0 && exekutatu_komando) {
                    Komandoa(Arrays.asList("java", "-cp", "classes:" + liburutegi, sarrera_p_balio));
                }
            } catch (Exception errorea) { 알림(errorea.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = prozesu_balio;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private laneko_area() throws IOException {
        Files.createDirectories(작업폴더);
        Font letra_tipo_balio = new Font("Monospaced", Font.PLAIN, 16);
        ITURBURUA.setFont(letra_tipo_balio); Irteera.setFont(letra_tipo_balio); Irteera.setEditable(false);
        ITURBURUA.setTabSize(4);
        ITURBURUA.setMargin(new Insets(10, 12, 10, 12));
        Irteera.setMargin(new Insets(8, 12, 8, 12));
        ITURBURUA.setBackground(new Color(250, 251, 252));
        ITURBURUA.setForeground(new Color(32, 43, 58));
        JPanel komando_panel = new JPanel();
        komando_panel.add(new JLabel("Fitxategia")); komando_panel.add(fitxategi_sarrera_izen);
        komando_panel.add(new JLabel("주 Gela_balio")); komando_panel.add(Gela_sarrera_izen);
        botoia(komando_panel, "Ireki", this::Ireki); botoia(komando_panel, "Store_balio", this::Store_balio);
        botoia(komando_panel, "eraiki_iturburu", () -> ITZULI_iturburu(false, false));
        botoia(komando_panel, "exekutatu_komando", () -> ITZULI_iturburu(true, false));
        botoia(komando_panel, "exekutatu_komando Fitxategia sortu_sarrera", () -> ITZULI_iturburu(false, true));
        botoia(komando_panel, "멈춤", this::멈춤);
        JSplitPane zatiketa_neurria = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ITURBURUA), new JScrollPane(Irteera));
        zatiketa_neurria.setResizeWeight(0.75);
        Leihoa.add(komando_panel, BorderLayout.NORTH); Leihoa.add(zatiketa_neurria, BorderLayout.CENTER);
        Leihoa.setSize(1200, 750); Leihoa.setLocationRelativeTo(null);
        Leihoa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Leihoa.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Gertaera) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Ireki(); Leihoa.setVisible(true);
    }
    public static void main(String[] Argumentuak) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource letra_tipo_lehenetsi = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object sarrera_balio : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(sarrera_balio) instanceof Font) UIManager.put(sarrera_balio, letra_tipo_lehenetsi);
                }
                new laneko_area();
            } catch (Exception errorea) { errorea.printStackTrace(); }
        });
    }
}
