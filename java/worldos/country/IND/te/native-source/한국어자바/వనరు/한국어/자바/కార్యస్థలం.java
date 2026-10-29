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

/** వినియోగదారు 홈에서 Java 원문을 సంకలనంచేయు_మూల్యం·నిర్మించు_మూలం·실행하는 작은 Swing కార్యస్థలం. */
public final class కార్యస్థలం {
    private final JFrame విండో = new JFrame("jkoros — 자바 కార్యస్థలం");
    private final JTextArea వనరు = new JTextArea();
    private final JTextArea అవుట్పుట్ = new JTextArea(8, 80);
    private final JTextField ఫైలు_ప్రవేశం_పేరు = new JTextField("인사.java", 20);
    private final JTextField తరగతి_ప్రవేశం_పేరు = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process విధానం_మూల్యం;
    private final String లైబ్రరీ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String పాఠ్యము) { SwingUtilities.invokeLater(() -> అవుట్పుట్.append(పాఠ్యము + "\n")); }
    private void బటన్(JPanel సంస్కరణ_మూల్యం, String పేరు, Runnable 행동) {
        JButton బటన్ = new JButton(పేరు);
        బటన్.addActionListener(ఈవెంట్ -> 행동.run());
        సంస్కరణ_మూల్యం.add(బటన్);
    }
    private boolean నిల్వ_మూల్యం() {
        try {
            Path పాత్ = 작업폴더.resolve(ఫైలు_ప్రవేశం_పేరు.getText());
            Files.createDirectories(పాత్.getParent());
            దస్త్రం.వ్రాయుము(పాత్, వనరు.getText());
            알림("నిల్వ_మూల్యం: " + పాత్);
            return true;
        } catch (Exception దోషం) { 알림(దోషం.toString()); return false; }
    }
    private void తెరువు() {
        try { వనరు.setText(దస్త్రం.చదువు(작업폴더.resolve(ఫైలు_ప్రవేశం_పేరు.getText()))); }
        catch (Exception దోషం) { 알림(దోషం.toString()); }
    }
    private int ఆదేశము(List<String> ఆదేశము) throws Exception {
        విధానం_మూల్యం = new ProcessBuilder(ఆదేశము).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader పంక్తి = new BufferedReader(new InputStreamReader(విధానం_మూల్యం.getInputStream(), StandardCharsets.UTF_8))) {
            String పాఠ్యము;
            while ((పాఠ్యము = పంక్తి.readLine()) != null) 알림(పాఠ్యము);
        }
        int స్థితి_మూల్యం = విధానం_మూల్యం.waitFor(); విధానం_మూల్యం = null;
        알림("నిష్క్రమణ_అనువర్తనం కోడ్_మూల్యం: " + స్థితి_మూల్యం);
        return స్థితి_మూల్యం;
    }
    private void అనువదించు_మూలం(boolean అమలు_చేయి_ఆదేశం, boolean 실행파일) {
        if (!నిల్వ_మూల్యం()) return;
        String 입력 = ఫైలు_ప్రవేశం_పేరు.getText(), ప్రవేశం_పాయింట్_మూల్యం = తరగతి_ప్రవేశం_పేరు.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ఆదేశము(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ప్రవేశం_పాయింట్_మూల్యం,
                        "--classpath", లైబ్రరీ, "-o", "실행프로그램", 입력));
                } else if (ఆదేశము(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", లైబ్రరీ,
                        "-d", "classes", 입력)) == 0 && అమలు_చేయి_ఆదేశం) {
                    ఆదేశము(Arrays.asList("java", "-cp", "classes:" + లైబ్రరీ, ప్రవేశం_పాయింట్_మూల్యం));
                }
            } catch (Exception దోషం) { 알림(దోషం.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = విధానం_మూల్యం;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private కార్యస్థలం() throws IOException {
        Files.createDirectories(작업폴더);
        Font అక్షరాకృతి_మూల్యం = new Font("Monospaced", Font.PLAIN, 16);
        వనరు.setFont(అక్షరాకృతి_మూల్యం); అవుట్పుట్.setFont(అక్షరాకృతి_మూల్యం); అవుట్పుట్.setEditable(false);
        వనరు.setTabSize(4);
        వనరు.setMargin(new Insets(10, 12, 10, 12));
        అవుట్పుట్.setMargin(new Insets(8, 12, 8, 12));
        వనరు.setBackground(new Color(250, 251, 252));
        వనరు.setForeground(new Color(32, 43, 58));
        JPanel ఆదేశం_ప్యానెల్ = new JPanel();
        ఆదేశం_ప్యానెల్.add(new JLabel("దస్త్రం")); ఆదేశం_ప్యానెల్.add(ఫైలు_ప్రవేశం_పేరు);
        ఆదేశం_ప్యానెల్.add(new JLabel("주 తరగతి_మూల్యం")); ఆదేశం_ప్యానెల్.add(తరగతి_ప్రవేశం_పేరు);
        బటన్(ఆదేశం_ప్యానెల్, "తెరువు", this::తెరువు); బటన్(ఆదేశం_ప్యానెల్, "నిల్వ_మూల్యం", this::నిల్వ_మూల్యం);
        బటన్(ఆదేశం_ప్యానెల్, "నిర్మించు_మూలం", () -> అనువదించు_మూలం(false, false));
        బటన్(ఆదేశం_ప్యానెల్, "అమలు_చేయి_ఆదేశం", () -> అనువదించు_మూలం(true, false));
        బటన్(ఆదేశం_ప్యానెల్, "అమలు_చేయి_ఆదేశం దస్త్రం క్రియేట్_ప్రవేశం", () -> అనువదించు_మూలం(false, true));
        బటన్(ఆదేశం_ప్యానెల్, "멈춤", this::멈춤);
        JSplitPane భాగహారం_ప్రమాణం = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(వనరు), new JScrollPane(అవుట్పుట్));
        భాగహారం_ప్రమాణం.setResizeWeight(0.75);
        విండో.add(ఆదేశం_ప్యానెల్, BorderLayout.NORTH); విండో.add(భాగహారం_ప్రమాణం, BorderLayout.CENTER);
        విండో.setSize(1200, 750); విండో.setLocationRelativeTo(null);
        విండో.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        విండో.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ఈవెంట్) { 멈춤(); 일꾼.shutdownNow(); }
        });
        తెరువు(); విండో.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource స్వయంసిద్ధ_అక్షరాకృతి = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ప్రవేశం_మూల్యం : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ప్రవేశం_మూల్యం) instanceof Font) UIManager.put(ప్రవేశం_మూల్యం, స్వయంసిద్ధ_అక్షరాకృతి);
                }
                new కార్యస్థలం();
            } catch (Exception దోషం) { దోషం.printStackTrace(); }
        });
    }
}
