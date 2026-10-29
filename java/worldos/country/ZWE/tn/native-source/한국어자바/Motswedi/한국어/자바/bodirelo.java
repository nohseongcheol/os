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

/** modirisi 홈에서 Java 원문을 Tseleganya_Boleng·aga_Motswedi·실행하는 작은 Swing bodirelo. */
public final class bodirelo {
    private final JFrame fensetere = new JFrame("jkoros — 자바 bodirelo");
    private final JTextArea Motswedi = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField faele_tsenyo_leina = new JTextField("인사.java", 20);
    private final JTextField mofuta_tsenyo_leina = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Thulaganyo_Boleng;
    private final String laeborari = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void konopo(JPanel kgaolo_Boleng, String leina, Runnable 행동) {
        JButton konopo = new JButton(leina);
        konopo.addActionListener(tiragalo -> 행동.run());
        kgaolo_Boleng.add(konopo);
    }
    private boolean Store_Boleng() {
        try {
            Path tsela = 작업폴더.resolve(faele_tsenyo_leina.getText());
            Files.createDirectories(tsela.getParent());
            faele.kwala(tsela, Motswedi.getText());
            알림("Store_Boleng: " + tsela);
            return true;
        } catch (Exception phoso) { 알림(phoso.toString()); return false; }
    }
    private void bula() {
        try { Motswedi.setText(faele.읽기(작업폴더.resolve(faele_tsenyo_leina.getText()))); }
        catch (Exception phoso) { 알림(phoso.toString()); }
    }
    private int Taelo(List<String> Taelo) throws Exception {
        Thulaganyo_Boleng = new ProcessBuilder(Taelo).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Mola = new BufferedReader(new InputStreamReader(Thulaganyo_Boleng.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = Mola.readLine()) != null) 알림(SMS);
        }
        int kemo_Boleng = Thulaganyo_Boleng.waitFor(); Thulaganyo_Boleng = null;
        알림("tswaya_Tiriso 코드: " + kemo_Boleng);
        return kemo_Boleng;
    }
    private void Ranola_Motswedi(boolean diragatsa_Taelo, boolean 실행파일) {
        if (!Store_Boleng()) return;
        String 입력 = faele_tsenyo_leina.getText(), tsenyo_ntlha_Boleng = mofuta_tsenyo_leina.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Taelo(Arrays.asList("jclassc", "--target", "openjdk", "--entry", tsenyo_ntlha_Boleng,
                        "--classpath", laeborari, "-o", "실행프로그램", 입력));
                } else if (Taelo(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", laeborari,
                        "-d", "classes", 입력)) == 0 && diragatsa_Taelo) {
                    Taelo(Arrays.asList("java", "-cp", "classes:" + laeborari, tsenyo_ntlha_Boleng));
                }
            } catch (Exception phoso) { 알림(phoso.toString()); }
        });
    }
    private void 멈춤() {
        Process ga_jaana_selwana = Thulaganyo_Boleng;
        if (ga_jaana_selwana != null) { ga_jaana_selwana.descendants().forEach(ProcessHandle::destroy); ga_jaana_selwana.destroy(); }
    }
    private bodirelo() throws IOException {
        Files.createDirectories(작업폴더);
        Font mofutatlhaka_Boleng = new Font("Monospaced", Font.PLAIN, 16);
        Motswedi.setFont(mofutatlhaka_Boleng); 출력.setFont(mofutatlhaka_Boleng); 출력.setEditable(false);
        Motswedi.setTabSize(4);
        Motswedi.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        Motswedi.setBackground(new Color(250, 251, 252));
        Motswedi.setForeground(new Color(32, 43, 58));
        JPanel Taelo_phanele = new JPanel();
        Taelo_phanele.add(new JLabel("faele")); Taelo_phanele.add(faele_tsenyo_leina);
        Taelo_phanele.add(new JLabel("주 mofuta_Boleng")); Taelo_phanele.add(mofuta_tsenyo_leina);
        konopo(Taelo_phanele, "bula", this::bula); konopo(Taelo_phanele, "Store_Boleng", this::Store_Boleng);
        konopo(Taelo_phanele, "aga_Motswedi", () -> Ranola_Motswedi(false, false));
        konopo(Taelo_phanele, "diragatsa_Taelo", () -> Ranola_Motswedi(true, false));
        konopo(Taelo_phanele, "diragatsa_Taelo faele tlhama_tsenyo", () -> Ranola_Motswedi(false, true));
        konopo(Taelo_phanele, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Motswedi), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        fensetere.add(Taelo_phanele, BorderLayout.NORTH); fensetere.add(나눔, BorderLayout.CENTER);
        fensetere.setSize(1200, 750); fensetere.setLocationRelativeTo(null);
        fensetere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fensetere.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent tiragalo) { 멈춤(); 일꾼.shutdownNow(); }
        });
        bula(); fensetere.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource mofutatlhaka_o_o_rulaganyeditsweng_ruri = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object tsenyo_Boleng : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(tsenyo_Boleng) instanceof Font) UIManager.put(tsenyo_Boleng, mofutatlhaka_o_o_rulaganyeditsweng_ruri);
                }
                new bodirelo();
            } catch (Exception phoso) { phoso.printStackTrace(); }
        });
    }
}
