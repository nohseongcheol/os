// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자바;

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

/** umsebenzisi 홈에서 Java 원문을 hlela_inani·akha_umthombo·실행하는 작은 Swing indawo_yokusebenzela. */
public final class indawo_yokusebenzela {
    private final JFrame ifasitela = new JFrame("jkoros — 자바 indawo_yokusebenzela");
    private final JTextArea umthombo = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ifayela_okufakwayo_igama = new JTextField("인사.java", 20);
    private final JTextField uhlobo_okufakwayo_igama = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Inqubo_inani;
    private final String umtapo = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Itekisi) { SwingUtilities.invokeLater(() -> 출력.append(Itekisi + "\n")); }
    private void inkinobho(JPanel isibuyekezo_inani, String Igama, Runnable 행동) {
        JButton inkinobho = new JButton(Igama);
        inkinobho.addActionListener(isigameko -> 행동.run());
        isibuyekezo_inani.add(inkinobho);
    }
    private boolean Store_inani() {
        try {
            Path Indlela_2 = 작업폴더.resolve(ifayela_okufakwayo_igama.getText());
            Files.createDirectories(Indlela_2.getParent());
            Ihele.Bhala(Indlela_2, umthombo.getText());
            알림("Store_inani: " + Indlela_2);
            return true;
        } catch (Exception Iphutha) { 알림(Iphutha.toString()); return false; }
    }
    private void Vula() {
        try { umthombo.setText(Ihele.Funda(작업폴더.resolve(ifayela_okufakwayo_igama.getText()))); }
        catch (Exception Iphutha) { 알림(Iphutha.toString()); }
    }
    private int Umlayelo(List<String> Umlayelo) throws Exception {
        Inqubo_inani = new ProcessBuilder(Umlayelo).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader umugqa = new BufferedReader(new InputStreamReader(Inqubo_inani.getInputStream(), StandardCharsets.UTF_8))) {
            String Itekisi;
            while ((Itekisi = umugqa.readLine()) != null) 알림(Itekisi);
        }
        int isimo_inani = Inqubo_inani.waitFor(); Inqubo_inani = null;
        알림("phuma_i_app 코드: " + isimo_inani);
        return isimo_inani;
    }
    private void Ukuhumusha_umthombo(boolean yenza_umyalo, boolean 실행파일) {
        if (!Store_inani()) return;
        String 입력 = ifayela_okufakwayo_igama.getText(), okufakwayo_iphoyinti_inani = uhlobo_okufakwayo_igama.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Umlayelo(Arrays.asList("jclassc", "--target", "openjdk", "--entry", okufakwayo_iphoyinti_inani,
                        "--classpath", umtapo, "-o", "실행프로그램", 입력));
                } else if (Umlayelo(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", umtapo,
                        "-d", "classes", 입력)) == 0 && yenza_umyalo) {
                    Umlayelo(Arrays.asList("java", "-cp", "classes:" + umtapo, okufakwayo_iphoyinti_inani));
                }
            } catch (Exception Iphutha) { 알림(Iphutha.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Inqubo_inani;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private indawo_yokusebenzela() throws IOException {
        Files.createDirectories(작업폴더);
        Font ubuso_bohlamvu_ifonti_inani = new Font("Monospaced", Font.PLAIN, 16);
        umthombo.setFont(ubuso_bohlamvu_ifonti_inani); 출력.setFont(ubuso_bohlamvu_ifonti_inani); 출력.setEditable(false);
        umthombo.setTabSize(4);
        umthombo.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        umthombo.setBackground(new Color(250, 251, 252));
        umthombo.setForeground(new Color(32, 43, 58));
        JPanel umyalo_iphaneli = new JPanel();
        umyalo_iphaneli.add(new JLabel("Ihele")); umyalo_iphaneli.add(ifayela_okufakwayo_igama);
        umyalo_iphaneli.add(new JLabel("주 uhlobo_inani")); umyalo_iphaneli.add(uhlobo_okufakwayo_igama);
        inkinobho(umyalo_iphaneli, "Vula", this::Vula); inkinobho(umyalo_iphaneli, "Store_inani", this::Store_inani);
        inkinobho(umyalo_iphaneli, "akha_umthombo", () -> Ukuhumusha_umthombo(false, false));
        inkinobho(umyalo_iphaneli, "yenza_umyalo", () -> Ukuhumusha_umthombo(true, false));
        inkinobho(umyalo_iphaneli, "yenza_umyalo Ihele yakha_okufakwayo", () -> Ukuhumusha_umthombo(false, true));
        inkinobho(umyalo_iphaneli, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(umthombo), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        ifasitela.add(umyalo_iphaneli, BorderLayout.NORTH); ifasitela.add(나눔, BorderLayout.CENTER);
        ifasitela.setSize(1200, 750); ifasitela.setLocationRelativeTo(null);
        ifasitela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ifasitela.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent isigameko) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Vula(); ifasitela.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ifonti_emisiwe = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object okufakwayo_inani : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(okufakwayo_inani) instanceof Font) UIManager.put(okufakwayo_inani, ifonti_emisiwe);
                }
                new indawo_yokusebenzela();
            } catch (Exception Iphutha) { Iphutha.printStackTrace(); }
        });
    }
}
