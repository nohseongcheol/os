// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.자바;

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

/** uporabnik 홈에서 Java 원문을 Uredi_VALUE·prevajati_vir·실행하는 작은 Swing delovni_prostor. */
public final class delovni_prostor {
    private final JFrame okno = new JFrame("jkoros — 자바 delovni_prostor");
    private final JTextArea VIR = new JTextArea();
    private final JTextArea Izpis = new JTextArea(8, 80);
    private final JTextField Datoteka_vnos_ime = new JTextField("인사.java", 20);
    private final JTextField Razred_vnos_ime = new JTextField("인사", 16);
    private final Path delovni_imenik = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VALUE;
    private final String knjižnica = "/opt/jkoros/lib/한국어자바.jar";

    private void obvestilo(String Besedilo) { SwingUtilities.invokeLater(() -> Izpis.append(Besedilo + "\n")); }
    private void Gumb(JPanel različica_VALUE, String Ime, Runnable 행동) {
        JButton Gumb = new JButton(Ime);
        Gumb.addActionListener(dogodek -> 행동.run());
        različica_VALUE.add(Gumb);
    }
    private boolean Store_VALUE() {
        try {
            Path POT = delovni_imenik.resolve(Datoteka_vnos_ime.getText());
            Files.createDirectories(POT.getParent());
            Datoteka.Pisanje(POT, VIR.getText());
            obvestilo("Store_VALUE: " + POT);
            return true;
        } catch (Exception NAPAKA) { obvestilo(NAPAKA.toString()); return false; }
    }
    private void Odpri() {
        try { VIR.setText(Datoteka.Branje(delovni_imenik.resolve(Datoteka_vnos_ime.getText()))); }
        catch (Exception NAPAKA) { obvestilo(NAPAKA.toString()); }
    }
    private int Ukaz(List<String> Ukaz) throws Exception {
        Proces_VALUE = new ProcessBuilder(Ukaz).directory(delovni_imenik.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Črtni = new BufferedReader(new InputStreamReader(Proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Besedilo;
            while ((Besedilo = Črtni.readLine()) != null) obvestilo(Besedilo);
        }
        int stanje_VALUE = Proces_VALUE.waitFor(); Proces_VALUE = null;
        obvestilo("Izhod_aplikacija CODE_VALUE: " + stanje_VALUE);
        return stanje_VALUE;
    }
    private void prevesti_vir(boolean Izvedi_ukaz, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = Datoteka_vnos_ime.getText(), vnos_p_VALUE = Razred_vnos_ime.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(delovni_imenik.resolve("classes"));
                if (실행파일) {
                    Ukaz(Arrays.asList("jclassc", "--target", "openjdk", "--entry", vnos_p_VALUE,
                        "--classpath", knjižnica, "-o", "실행프로그램", 입력));
                } else if (Ukaz(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", knjižnica,
                        "-d", "classes", 입력)) == 0 && Izvedi_ukaz) {
                    Ukaz(Arrays.asList("java", "-cp", "classes:" + knjižnica, vnos_p_VALUE));
                }
            } catch (Exception NAPAKA) { obvestilo(NAPAKA.toString()); }
        });
    }
    private void 멈춤() {
        Process sprotno_element = Proces_VALUE;
        if (sprotno_element != null) { sprotno_element.descendants().forEach(ProcessHandle::destroy); sprotno_element.destroy(); }
    }
    private delovni_prostor() throws IOException {
        Files.createDirectories(delovni_imenik);
        Font pisava_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        VIR.setFont(pisava_VALUE); Izpis.setFont(pisava_VALUE); Izpis.setEditable(false);
        VIR.setTabSize(4);
        VIR.setMargin(new Insets(10, 12, 10, 12));
        Izpis.setMargin(new Insets(8, 12, 8, 12));
        VIR.setBackground(new Color(250, 251, 252));
        VIR.setForeground(new Color(32, 43, 58));
        JPanel ukaz_plošča = new JPanel();
        ukaz_plošča.add(new JLabel("Datoteka")); ukaz_plošča.add(Datoteka_vnos_ime);
        ukaz_plošča.add(new JLabel("주 Razred_VALUE")); ukaz_plošča.add(Razred_vnos_ime);
        Gumb(ukaz_plošča, "Odpri", this::Odpri); Gumb(ukaz_plošča, "Store_VALUE", this::Store_VALUE);
        Gumb(ukaz_plošča, "prevajati_vir", () -> prevesti_vir(false, false));
        Gumb(ukaz_plošča, "Izvedi_ukaz", () -> prevesti_vir(true, false));
        Gumb(ukaz_plošča, "Izvedi_ukaz Datoteka Ustvari_vnos", () -> prevesti_vir(false, true));
        Gumb(ukaz_plošča, "멈춤", this::멈춤);
        JSplitPane sektor_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(VIR), new JScrollPane(Izpis));
        sektor_KR.setResizeWeight(0.75);
        okno.add(ukaz_plošča, BorderLayout.NORTH); okno.add(sektor_KR, BorderLayout.CENTER);
        okno.setSize(1200, 750); okno.setLocationRelativeTo(null);
        okno.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        okno.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent dogodek) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Odpri(); okno.setVisible(true);
    }
    public static void main(String[] Argumenti) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource privzeta_pisava = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object vnos_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(vnos_VALUE) instanceof Font) UIManager.put(vnos_VALUE, privzeta_pisava);
                }
                new delovni_prostor();
            } catch (Exception NAPAKA) { NAPAKA.printStackTrace(); }
        });
    }
}
