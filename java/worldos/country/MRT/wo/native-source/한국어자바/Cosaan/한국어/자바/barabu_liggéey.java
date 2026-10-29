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

/** kiy_jariñoo_internet 홈에서 Java 원문을 soppi_xëyma·tabax_Cosaan·실행하는 작은 Swing barabu_liggéey. */
public final class barabu_liggéey {
    private final JFrame palanteer = new JFrame("jkoros — 자바 barabu_liggéey");
    private final JTextArea Cosaan = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField bara_denc_dugal_xabaar_tur = new JTextField("인사.java", 20);
    private final JTextField maas_dugal_xabaar_tur = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process yokkute_xëyma;
    private final String daaray_téere = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Tekst) { SwingUtilities.invokeLater(() -> 출력.append(Tekst + "\n")); }
    private void butoñ(JPanel taalif_xëyma, String tur_253d1510, Runnable 행동) {
        JButton butoñ = new JButton(tur_253d1510);
        butoñ.addActionListener(xewxew -> 행동.run());
        taalif_xëyma.add(butoñ);
    }
    private boolean Store_xëyma() {
        try {
            Path Yoonu_jëmale = 작업폴더.resolve(bara_denc_dugal_xabaar_tur.getText());
            Files.createDirectories(Yoonu_jëmale.getParent());
            bara_denc.biir(Yoonu_jëmale, Cosaan.getText());
            알림("Store_xëyma: " + Yoonu_jëmale);
            return true;
        } catch (Exception njumte) { 알림(njumte.toString()); return false; }
    }
    private void sos() {
        try { Cosaan.setText(bara_denc.읽기(작업폴더.resolve(bara_denc_dugal_xabaar_tur.getText()))); }
        catch (Exception njumte) { 알림(njumte.toString()); }
    }
    private int ndigel(List<String> ndigel) throws Exception {
        yokkute_xëyma = new ProcessBuilder(ndigel).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader buum = new BufferedReader(new InputStreamReader(yokkute_xëyma.getInputStream(), StandardCharsets.UTF_8))) {
            String Tekst;
            while ((Tekst = buum.readLine()) != null) 알림(Tekst);
        }
        int nekkin_xëyma = yokkute_xëyma.waitFor(); yokkute_xëyma = null;
        알림("Génn_jëfekaay 코드: " + nekkin_xëyma);
        return nekkin_xëyma;
    }
    private void Tekki_Cosaan(boolean def_ndigel, boolean 실행파일) {
        if (!Store_xëyma()) return;
        String 입력 = bara_denc_dugal_xabaar_tur.getText(), dugal_xabaar_Tomb_xëyma = maas_dugal_xabaar_tur.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ndigel(Arrays.asList("jclassc", "--target", "openjdk", "--entry", dugal_xabaar_Tomb_xëyma,
                        "--classpath", daaray_téere, "-o", "실행프로그램", 입력));
                } else if (ndigel(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", daaray_téere,
                        "-d", "classes", 입력)) == 0 && def_ndigel) {
                    ndigel(Arrays.asList("java", "-cp", "classes:" + daaray_téere, dugal_xabaar_Tomb_xëyma));
                }
            } catch (Exception njumte) { 알림(njumte.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = yokkute_xëyma;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private barabu_liggéey() throws IOException {
        Files.createDirectories(작업폴더);
        Font mbindin_xëyma = new Font("Monospaced", Font.PLAIN, 16);
        Cosaan.setFont(mbindin_xëyma); 출력.setFont(mbindin_xëyma); 출력.setEditable(false);
        Cosaan.setTabSize(4);
        Cosaan.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        Cosaan.setBackground(new Color(250, 251, 252));
        Cosaan.setForeground(new Color(32, 43, 58));
        JPanel ndigel_pano = new JPanel();
        ndigel_pano.add(new JLabel("bara_denc")); ndigel_pano.add(bara_denc_dugal_xabaar_tur);
        ndigel_pano.add(new JLabel("주 maas_xëyma")); ndigel_pano.add(maas_dugal_xabaar_tur);
        butoñ(ndigel_pano, "sos", this::sos); butoñ(ndigel_pano, "Store_xëyma", this::Store_xëyma);
        butoñ(ndigel_pano, "tabax_Cosaan", () -> Tekki_Cosaan(false, false));
        butoñ(ndigel_pano, "def_ndigel", () -> Tekki_Cosaan(true, false));
        butoñ(ndigel_pano, "def_ndigel bara_denc sos_dugal_xabaar", () -> Tekki_Cosaan(false, true));
        butoñ(ndigel_pano, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Cosaan), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        palanteer.add(ndigel_pano, BorderLayout.NORTH); palanteer.add(나눔, BorderLayout.CENTER);
        palanteer.setSize(1200, 750); palanteer.setLocationRelativeTo(null);
        palanteer.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        palanteer.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent xewxew) { 멈춤(); 일꾼.shutdownNow(); }
        });
        sos(); palanteer.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource arafu_wàccaale = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object dugal_xabaar_xëyma : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(dugal_xabaar_xëyma) instanceof Font) UIManager.put(dugal_xabaar_xëyma, arafu_wàccaale);
                }
                new barabu_liggéey();
            } catch (Exception njumte) { njumte.printStackTrace(); }
        });
    }
}
