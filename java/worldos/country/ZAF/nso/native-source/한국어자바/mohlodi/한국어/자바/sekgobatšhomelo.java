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

/** mošomiši 홈에서 Java 원문을 rulaganya_boleng·aga_mohlodi·실행하는 작은 Swing sekgobatšhomelo. */
public final class sekgobatšhomelo {
    private final JFrame lefastere = new JFrame("jkoros — 자바 sekgobatšhomelo");
    private final JTextArea mohlodi = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField faele_go_tsenya_tshedimošo_leina = new JTextField("인사.java", 20);
    private final JTextField legoro_go_tsenya_tshedimošo_leina = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process tiragalo_boleng;
    private final String Bokgobadata = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Sengwalwa) { SwingUtilities.invokeLater(() -> 출력.append(Sengwalwa + "\n")); }
    private void konope(JPanel bešene_boleng, String Leina, Runnable 행동) {
        JButton konope = new JButton(Leina);
        konope.addActionListener(tiragalo -> 행동.run());
        bešene_boleng.add(konope);
    }
    private boolean lota_boleng() {
        try {
            Path Tsejana = 작업폴더.resolve(faele_go_tsenya_tshedimošo_leina.getText());
            Files.createDirectories(Tsejana.getParent());
            Faele.Ngwala(Tsejana, mohlodi.getText());
            알림("lota_boleng: " + Tsejana);
            return true;
        } catch (Exception Phošo) { 알림(Phošo.toString()); return false; }
    }
    private void Bula() {
        try { mohlodi.setText(Faele.Bala(작업폴더.resolve(faele_go_tsenya_tshedimošo_leina.getText()))); }
        catch (Exception Phošo) { 알림(Phošo.toString()); }
    }
    private int Taelo(List<String> Taelo) throws Exception {
        tiragalo_boleng = new ProcessBuilder(Taelo).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader mothaladi = new BufferedReader(new InputStreamReader(tiragalo_boleng.getInputStream(), StandardCharsets.UTF_8))) {
            String Sengwalwa;
            while ((Sengwalwa = mothaladi.readLine()) != null) 알림(Sengwalwa);
        }
        int boemo_boleng = tiragalo_boleng.waitFor(); tiragalo_boleng = null;
        알림("Etšwa_tirišo 코드: " + boemo_boleng);
        return boemo_boleng;
    }
    private void Fetolela_mohlodi(boolean phethagatša_taelo, boolean 실행파일) {
        if (!lota_boleng()) return;
        String 입력 = faele_go_tsenya_tshedimošo_leina.getText(), go_tsenya_tshedimošo_ntlha_boleng = legoro_go_tsenya_tshedimošo_leina.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Taelo(Arrays.asList("jclassc", "--target", "openjdk", "--entry", go_tsenya_tshedimošo_ntlha_boleng,
                        "--classpath", Bokgobadata, "-o", "실행프로그램", 입력));
                } else if (Taelo(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", Bokgobadata,
                        "-d", "classes", 입력)) == 0 && phethagatša_taelo) {
                    Taelo(Arrays.asList("java", "-cp", "classes:" + Bokgobadata, go_tsenya_tshedimošo_ntlha_boleng));
                }
            } catch (Exception Phošo) { 알림(Phošo.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = tiragalo_boleng;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private sekgobatšhomelo() throws IOException {
        Files.createDirectories(작업폴더);
        Font fonte_boleng = new Font("Monospaced", Font.PLAIN, 16);
        mohlodi.setFont(fonte_boleng); 출력.setFont(fonte_boleng); 출력.setEditable(false);
        mohlodi.setTabSize(4);
        mohlodi.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        mohlodi.setBackground(new Color(250, 251, 252));
        mohlodi.setForeground(new Color(32, 43, 58));
        JPanel taelo_phanele = new JPanel();
        taelo_phanele.add(new JLabel("Faele")); taelo_phanele.add(faele_go_tsenya_tshedimošo_leina);
        taelo_phanele.add(new JLabel("주 legoro_boleng_55654bf1")); taelo_phanele.add(legoro_go_tsenya_tshedimošo_leina);
        konope(taelo_phanele, "Bula", this::Bula); konope(taelo_phanele, "lota_boleng", this::lota_boleng);
        konope(taelo_phanele, "aga_mohlodi", () -> Fetolela_mohlodi(false, false));
        konope(taelo_phanele, "phethagatša_taelo", () -> Fetolela_mohlodi(true, false));
        konope(taelo_phanele, "phethagatša_taelo Faele 만들기", () -> Fetolela_mohlodi(false, true));
        konope(taelo_phanele, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(mohlodi), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        lefastere.add(taelo_phanele, BorderLayout.NORTH); lefastere.add(나눔, BorderLayout.CENTER);
        lefastere.setSize(1200, 750); lefastere.setLocationRelativeTo(null);
        lefastere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        lefastere.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent tiragalo) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Bula(); lefastere.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource fonte_ya_maitirišo = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object go_tsenya_tshedimošo_boleng : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(go_tsenya_tshedimošo_boleng) instanceof Font) UIManager.put(go_tsenya_tshedimošo_boleng, fonte_ya_maitirišo);
                }
                new sekgobatšhomelo();
            } catch (Exception Phošo) { Phošo.printStackTrace(); }
        });
    }
}
