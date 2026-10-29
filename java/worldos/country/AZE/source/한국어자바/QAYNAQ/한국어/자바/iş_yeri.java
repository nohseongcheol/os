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

/** istifadəçi 홈에서 Java 원문을 redaktə_VALUE·qurmaq_mənbə·실행하는 작은 Swing iş_yeri. */
public final class iş_yeri {
    private final JFrame pəncərə = new JFrame("jkoros — 자바 iş_yeri");
    private final JTextArea QAYNAQ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField fayl_daxiletmə_ad = new JTextField("인사.java", 20);
    private final JTextField Sinif_daxiletmə_ad = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proses_VALUE;
    private final String kitabxana = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Mətn) { SwingUtilities.invokeLater(() -> 출력.append(Mətn + "\n")); }
    private void düymə(JPanel versiya_VALUE, String Ad, Runnable 행동) {
        JButton düymə = new JButton(Ad);
        düymə.addActionListener(hadisə -> 행동.run());
        versiya_VALUE.add(düymə);
    }
    private boolean Store_VALUE() {
        try {
            Path Cığır = 작업폴더.resolve(fayl_daxiletmə_ad.getText());
            Files.createDirectories(Cığır.getParent());
            FAYL.Yazma(Cığır, QAYNAQ.getText());
            알림("Store_VALUE: " + Cığır);
            return true;
        } catch (Exception XƏTA) { 알림(XƏTA.toString()); return false; }
    }
    private void Aç() {
        try { QAYNAQ.setText(FAYL.Oxuma(작업폴더.resolve(fayl_daxiletmə_ad.getText()))); }
        catch (Exception XƏTA) { 알림(XƏTA.toString()); }
    }
    private int Əmr(List<String> Əmr) throws Exception {
        Proses_VALUE = new ProcessBuilder(Əmr).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Giriş = new BufferedReader(new InputStreamReader(Proses_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Mətn;
            while ((Mətn = Giriş.readLine()) != null) 알림(Mətn);
        }
        int vəziyyət_VALUE = Proses_VALUE.waitFor(); Proses_VALUE = null;
        알림("Çıxış_proqram kod_VALUE: " + vəziyyət_VALUE);
        return vəziyyət_VALUE;
    }
    private void TRANSLATE_mənbə(boolean icra_etmək_əmr, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = fayl_daxiletmə_ad.getText(), daxiletmə_p_VALUE = Sinif_daxiletmə_ad.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Əmr(Arrays.asList("jclassc", "--target", "openjdk", "--entry", daxiletmə_p_VALUE,
                        "--classpath", kitabxana, "-o", "실행프로그램", 입력));
                } else if (Əmr(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", kitabxana,
                        "-d", "classes", 입력)) == 0 && icra_etmək_əmr) {
                    Əmr(Arrays.asList("java", "-cp", "classes:" + kitabxana, daxiletmə_p_VALUE));
                }
            } catch (Exception XƏTA) { 알림(XƏTA.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proses_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private iş_yeri() throws IOException {
        Files.createDirectories(작업폴더);
        Font şrift_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        QAYNAQ.setFont(şrift_VALUE); 출력.setFont(şrift_VALUE); 출력.setEditable(false);
        QAYNAQ.setTabSize(4);
        QAYNAQ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        QAYNAQ.setBackground(new Color(250, 251, 252));
        QAYNAQ.setForeground(new Color(32, 43, 58));
        JPanel əmr_panel = new JPanel();
        əmr_panel.add(new JLabel("FAYL")); əmr_panel.add(fayl_daxiletmə_ad);
        əmr_panel.add(new JLabel("주 Sinif_VALUE")); əmr_panel.add(Sinif_daxiletmə_ad);
        düymə(əmr_panel, "Aç", this::Aç); düymə(əmr_panel, "Store_VALUE", this::Store_VALUE);
        düymə(əmr_panel, "qurmaq_mənbə", () -> TRANSLATE_mənbə(false, false));
        düymə(əmr_panel, "icra_etmək_əmr", () -> TRANSLATE_mənbə(true, false));
        düymə(əmr_panel, "icra_etmək_əmr FAYL yarat_daxiletmə", () -> TRANSLATE_mənbə(false, true));
        düymə(əmr_panel, "멈춤", this::멈춤);
        JSplitPane bölmə_ölçü = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(QAYNAQ), new JScrollPane(출력));
        bölmə_ölçü.setResizeWeight(0.75);
        pəncərə.add(əmr_panel, BorderLayout.NORTH); pəncərə.add(bölmə_ölçü, BorderLayout.CENTER);
        pəncərə.setSize(1200, 750); pəncərə.setLocationRelativeTo(null);
        pəncərə.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        pəncərə.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent hadisə) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Aç(); pəncərə.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource standart_şrift = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object daxiletmə_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(daxiletmə_VALUE) instanceof Font) UIManager.put(daxiletmə_VALUE, standart_şrift);
                }
                new iş_yeri();
            } catch (Exception XƏTA) { XƏTA.printStackTrace(); }
        });
    }
}
