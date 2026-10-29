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

/** brukar 홈에서 Java 원문을 redigere_VALUE·byggje_kjelde·실행하는 작은 Swing arbeidsområde. */
public final class arbeidsområde {
    private final JFrame vindauge = new JFrame("jkoros — 자바 arbeidsområde");
    private final JTextArea KJELDE = new JTextArea();
    private final JTextArea Utdata = new JTextArea(8, 80);
    private final JTextField fil_oppføring_namn = new JTextField("인사.java", 20);
    private final JTextField time_oppføring_namn = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Prosess_VALUE;
    private final String bibliotek = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Tekst) { SwingUtilities.invokeLater(() -> Utdata.append(Tekst + "\n")); }
    private void knapp(JPanel versjon_VALUE, String Namn, Runnable 행동) {
        JButton knapp = new JButton(Namn);
        knapp.addActionListener(Hending -> 행동.run());
        versjon_VALUE.add(knapp);
    }
    private boolean Store_VALUE() {
        try {
            Path STIGE = 작업폴더.resolve(fil_oppføring_namn.getText());
            Files.createDirectories(STIGE.getParent());
            Fil.Skriv(STIGE, KJELDE.getText());
            알림("Store_VALUE: " + STIGE);
            return true;
        } catch (Exception FEIL) { 알림(FEIL.toString()); return false; }
    }
    private void Opna() {
        try { KJELDE.setText(Fil.Les(작업폴더.resolve(fil_oppføring_namn.getText()))); }
        catch (Exception FEIL) { 알림(FEIL.toString()); }
    }
    private int Kommando(List<String> Kommando) throws Exception {
        Prosess_VALUE = new ProcessBuilder(Kommando).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader linje = new BufferedReader(new InputStreamReader(Prosess_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = linje.readLine()) != null) 알림(Tekst);
        }
        int status_VALUE = Prosess_VALUE.waitFor(); Prosess_VALUE = null;
        알림("Utgang_app CODE_VALUE: " + status_VALUE);
        return status_VALUE;
    }
    private void TRANSLATE_kjelde(boolean Utfør_kommando, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = fil_oppføring_namn.getText(), oppføring_p_VALUE = time_oppføring_namn.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Kommando(Arrays.asList("jclassc", "--target", "openjdk", "--entry", oppføring_p_VALUE,
                        "--classpath", bibliotek, "-o", "실행프로그램", 입력));
                } else if (Kommando(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotek,
                        "-d", "classes", 입력)) == 0 && Utfør_kommando) {
                    Kommando(Arrays.asList("java", "-cp", "classes:" + bibliotek, oppføring_p_VALUE));
                }
            } catch (Exception FEIL) { 알림(FEIL.toString()); }
        });
    }
    private void 멈춤() {
        Process betalt_vare = Prosess_VALUE;
        if (betalt_vare != null) { betalt_vare.descendants().forEach(ProcessHandle::destroy); betalt_vare.destroy(); }
    }
    private arbeidsområde() throws IOException {
        Files.createDirectories(작업폴더);
        Font skrift_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        KJELDE.setFont(skrift_VALUE); Utdata.setFont(skrift_VALUE); Utdata.setEditable(false);
        KJELDE.setTabSize(4);
        KJELDE.setMargin(new Insets(10, 12, 10, 12));
        Utdata.setMargin(new Insets(8, 12, 8, 12));
        KJELDE.setBackground(new Color(250, 251, 252));
        KJELDE.setForeground(new Color(32, 43, 58));
        JPanel kommando_panel = new JPanel();
        kommando_panel.add(new JLabel("Fil")); kommando_panel.add(fil_oppføring_namn);
        kommando_panel.add(new JLabel("주 time_VALUE")); kommando_panel.add(time_oppføring_namn);
        knapp(kommando_panel, "Opna", this::Opna); knapp(kommando_panel, "Store_VALUE", this::Store_VALUE);
        knapp(kommando_panel, "byggje_kjelde", () -> TRANSLATE_kjelde(false, false));
        knapp(kommando_panel, "Utfør_kommando", () -> TRANSLATE_kjelde(true, false));
        knapp(kommando_panel, "Utfør_kommando Fil Opprett_oppføring", () -> TRANSLATE_kjelde(false, true));
        knapp(kommando_panel, "멈춤", this::멈춤);
        JSplitPane divisjon_forretningsmål = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(KJELDE), new JScrollPane(Utdata));
        divisjon_forretningsmål.setResizeWeight(0.75);
        vindauge.add(kommando_panel, BorderLayout.NORTH); vindauge.add(divisjon_forretningsmål, BorderLayout.CENTER);
        vindauge.setSize(1200, 750); vindauge.setLocationRelativeTo(null);
        vindauge.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        vindauge.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Hending) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Opna(); vindauge.setVisible(true);
    }
    public static void main(String[] Argument) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standardskrift = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object oppføring_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(oppføring_VALUE) instanceof Font) UIManager.put(oppføring_VALUE, standardskrift);
                }
                new arbeidsområde();
            } catch (Exception FEIL) { FEIL.printStackTrace(); }
        });
    }
}
