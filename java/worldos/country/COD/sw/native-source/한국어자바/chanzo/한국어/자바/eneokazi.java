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

/** mtumiaji 홈에서 Java 원문을 hariri_thamani·jenga_chanzo·실행하는 작은 Swing eneokazi. */
public final class eneokazi {
    private final JFrame dirisha = new JFrame("jkoros — 자바 eneokazi");
    private final JTextArea chanzo = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField faili_ingizo_jina = new JTextField("인사.java", 20);
    private final JTextField tabaka_ingizo_jina = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Mchakato_thamani;
    private final String maktaba = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void kitufe(JPanel toleo_thamani, String Jina, Runnable 행동) {
        JButton kitufe = new JButton(Jina);
        kitufe.addActionListener(tukio -> 행동.run());
        toleo_thamani.add(kitufe);
    }
    private boolean Store_thamani() {
        try {
            Path njia = 작업폴더.resolve(faili_ingizo_jina.getText());
            Files.createDirectories(njia.getParent());
            faili.andika(njia, chanzo.getText());
            알림("Store_thamani: " + njia);
            return true;
        } catch (Exception kosa) { 알림(kosa.toString()); return false; }
    }
    private void unda() {
        try { chanzo.setText(faili.읽기(작업폴더.resolve(faili_ingizo_jina.getText()))); }
        catch (Exception kosa) { 알림(kosa.toString()); }
    }
    private int amri(List<String> amri) throws Exception {
        Mchakato_thamani = new ProcessBuilder(amri).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader laini = new BufferedReader(new InputStreamReader(Mchakato_thamani.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = laini.readLine()) != null) 알림(SMS);
        }
        int hali_thamani = Mchakato_thamani.waitFor(); Mchakato_thamani = null;
        알림("toka_programu msimbo_thamani: " + hali_thamani);
        return hali_thamani;
    }
    private void Tafsiri_chanzo(boolean tekeleza_amri, boolean 실행파일) {
        if (!Store_thamani()) return;
        String 입력 = faili_ingizo_jina.getText(), ingizo_pointi_thamani = tabaka_ingizo_jina.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    amri(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ingizo_pointi_thamani,
                        "--classpath", maktaba, "-o", "실행프로그램", 입력));
                } else if (amri(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", maktaba,
                        "-d", "classes", 입력)) == 0 && tekeleza_amri) {
                    amri(Arrays.asList("java", "-cp", "classes:" + maktaba, ingizo_pointi_thamani));
                }
            } catch (Exception kosa) { 알림(kosa.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Mchakato_thamani;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private eneokazi() throws IOException {
        Files.createDirectories(작업폴더);
        Font fonti_thamani = new Font("Monospaced", Font.PLAIN, 16);
        chanzo.setFont(fonti_thamani); 출력.setFont(fonti_thamani); 출력.setEditable(false);
        chanzo.setTabSize(4);
        chanzo.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        chanzo.setBackground(new Color(250, 251, 252));
        chanzo.setForeground(new Color(32, 43, 58));
        JPanel amri_paneli = new JPanel();
        amri_paneli.add(new JLabel("faili")); amri_paneli.add(faili_ingizo_jina);
        amri_paneli.add(new JLabel("주 tabaka_thamani_55654bf1")); amri_paneli.add(tabaka_ingizo_jina);
        kitufe(amri_paneli, "unda", this::unda); kitufe(amri_paneli, "Store_thamani", this::Store_thamani);
        kitufe(amri_paneli, "jenga_chanzo", () -> Tafsiri_chanzo(false, false));
        kitufe(amri_paneli, "tekeleza_amri", () -> Tafsiri_chanzo(true, false));
        kitufe(amri_paneli, "tekeleza_amri faili unda_ingizo", () -> Tafsiri_chanzo(false, true));
        kitufe(amri_paneli, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(chanzo), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        dirisha.add(amri_paneli, BorderLayout.NORTH); dirisha.add(나눔, BorderLayout.CENTER);
        dirisha.setSize(1200, 750); dirisha.setLocationRelativeTo(null);
        dirisha.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        dirisha.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent tukio) { 멈춤(); 일꾼.shutdownNow(); }
        });
        unda(); dirisha.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource fonti_ya_chaguo_msingi = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ingizo_thamani : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ingizo_thamani) instanceof Font) UIManager.put(ingizo_thamani, fonti_ya_chaguo_msingi);
                }
                new eneokazi();
            } catch (Exception kosa) { kosa.printStackTrace(); }
        });
    }
}
