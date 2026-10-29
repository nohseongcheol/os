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

/** përdorues 홈에서 Java 원문을 redaktim_VALUE·ndërtoj_burim·실행하는 작은 Swing hapësirë_pune. */
public final class hapësirë_pune {
    private final JFrame Dritare = new JFrame("jkoros — 자바 hapësirë_pune");
    private final JTextArea BURIMI = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField skedar_futje_emër = new JTextField("인사.java", 20);
    private final JTextField klasë_futje_emër = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proces_VALUE;
    private final String bibliotekë = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Teksti) { SwingUtilities.invokeLater(() -> 출력.append(Teksti + "\n")); }
    private void Buton(JPanel version_VALUE, String Emër, Runnable 행동) {
        JButton Buton = new JButton(Emër);
        Buton.addActionListener(Ngjarje -> 행동.run());
        version_VALUE.add(Buton);
    }
    private boolean Store_VALUE() {
        try {
            Path POZICIONI = 작업폴더.resolve(skedar_futje_emër.getText());
            Files.createDirectories(POZICIONI.getParent());
            Kartelë.Shkrimi(POZICIONI, BURIMI.getText());
            알림("Store_VALUE: " + POZICIONI);
            return true;
        } catch (Exception GABIM) { 알림(GABIM.toString()); return false; }
    }
    private void Hap() {
        try { BURIMI.setText(Kartelë.Leximi(작업폴더.resolve(skedar_futje_emër.getText()))); }
        catch (Exception GABIM) { 알림(GABIM.toString()); }
    }
    private int Komanda(List<String> Komanda) throws Exception {
        Proces_VALUE = new ProcessBuilder(Komanda).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader linjë = new BufferedReader(new InputStreamReader(Proces_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Teksti;
            while ((Teksti = linjë.readLine()) != null) 알림(Teksti);
        }
        int status_VALUE = Proces_VALUE.waitFor(); Proces_VALUE = null;
        알림("dal_program kod_VALUE: " + status_VALUE);
        return status_VALUE;
    }
    private void Përkthe_burim(boolean zbatoj_komandë, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = skedar_futje_emër.getText(), futje_p_VALUE = klasë_futje_emër.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Komanda(Arrays.asList("jclassc", "--target", "openjdk", "--entry", futje_p_VALUE,
                        "--classpath", bibliotekë, "-o", "실행프로그램", 입력));
                } else if (Komanda(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", bibliotekë,
                        "-d", "classes", 입력)) == 0 && zbatoj_komandë) {
                    Komanda(Arrays.asList("java", "-cp", "classes:" + bibliotekë, futje_p_VALUE));
                }
            } catch (Exception GABIM) { 알림(GABIM.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proces_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private hapësirë_pune() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        BURIMI.setFont(font_VALUE); 출력.setFont(font_VALUE); 출력.setEditable(false);
        BURIMI.setTabSize(4);
        BURIMI.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        BURIMI.setBackground(new Color(250, 251, 252));
        BURIMI.setForeground(new Color(32, 43, 58));
        JPanel komandë_panel = new JPanel();
        komandë_panel.add(new JLabel("Kartelë")); komandë_panel.add(skedar_futje_emër);
        komandë_panel.add(new JLabel("주 klasë_VALUE")); komandë_panel.add(klasë_futje_emër);
        Buton(komandë_panel, "Hap", this::Hap); Buton(komandë_panel, "Store_VALUE", this::Store_VALUE);
        Buton(komandë_panel, "ndërtoj_burim", () -> Përkthe_burim(false, false));
        Buton(komandë_panel, "zbatoj_komandë", () -> Përkthe_burim(true, false));
        Buton(komandë_panel, "zbatoj_komandë Kartelë Krijo_futje", () -> Përkthe_burim(false, true));
        Buton(komandë_panel, "멈춤", this::멈춤);
        JSplitPane pjesëtim_llogaritje = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(BURIMI), new JScrollPane(출력));
        pjesëtim_llogaritje.setResizeWeight(0.75);
        Dritare.add(komandë_panel, BorderLayout.NORTH); Dritare.add(pjesëtim_llogaritje, BorderLayout.CENTER);
        Dritare.setSize(1200, 750); Dritare.setLocationRelativeTo(null);
        Dritare.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Dritare.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Ngjarje) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Hap(); Dritare.setVisible(true);
    }
    public static void main(String[] Argumente) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource font_i_parazgjedhur = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object futje_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(futje_VALUE) instanceof Font) UIManager.put(futje_VALUE, font_i_parazgjedhur);
                }
                new hapësirë_pune();
            } catch (Exception GABIM) { GABIM.printStackTrace(); }
        });
    }
}
