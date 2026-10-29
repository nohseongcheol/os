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

/** kuutoro 홈에서 Java 원문을 feewnditde_njaru·tafde_sewnde·실행하는 작은 Swing gollorde. */
public final class gollorde {
    private final JFrame falanteere = new JFrame("jkoros — 자바 gollorde");
    private final JTextArea sewnde = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField fiilde_naatnugol_innde = new JTextField("인사.java", 20);
    private final JTextField fedde_naatnugol_innde = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Yuɓɓo_golle_njaru;
    private final String defterdu = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String binndi) { SwingUtilities.invokeLater(() -> 출력.append(binndi + "\n")); }
    private void feɗoode(JPanel yamre_njaru, String innde, Runnable 행동) {
        JButton feɗoode = new JButton(innde);
        feɗoode.addActionListener(saɗteende -> 행동.run());
        yamre_njaru.add(feɗoode);
    }
    private boolean resde_njaru() {
        try {
            Path laawol = 작업폴더.resolve(fiilde_naatnugol_innde.getText());
            Files.createDirectories(laawol.getParent());
            fiilde.winndude(laawol, sewnde.getText());
            알림("resde_njaru: " + laawol);
            return true;
        } catch (Exception juumre) { 알림(juumre.toString()); return false; }
    }
    private void udditde() {
        try { sewnde.setText(fiilde.읽기(작업폴더.resolve(fiilde_naatnugol_innde.getText()))); }
        catch (Exception juumre) { 알림(juumre.toString()); }
    }
    private int ginol(List<String> ginol) throws Exception {
        Yuɓɓo_golle_njaru = new ProcessBuilder(ginol).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader diidol = new BufferedReader(new InputStreamReader(Yuɓɓo_golle_njaru.getInputStream(), StandardCharsets.UTF_8))) {
            String binndi;
            while ((binndi = diidol.readLine()) != null) 알림(binndi);
        }
        int ngonka_njaru = Yuɓɓo_golle_njaru.waitFor(); Yuɓɓo_golle_njaru = null;
        알림("yaltude_tafirde 코드: " + ngonka_njaru);
        return ngonka_njaru;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!resde_njaru()) return;
        String 입력 = fiilde_naatnugol_innde.getText(), naatnugol_toɓɓere_njaru = fedde_naatnugol_innde.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ginol(Arrays.asList("jclassc", "--target", "openjdk", "--entry", naatnugol_toɓɓere_njaru,
                        "--classpath", defterdu, "-o", "실행프로그램", 입력));
                } else if (ginol(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", defterdu,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    ginol(Arrays.asList("java", "-cp", "classes:" + defterdu, naatnugol_toɓɓere_njaru));
                }
            } catch (Exception juumre) { 알림(juumre.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Yuɓɓo_golle_njaru;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private gollorde() throws IOException {
        Files.createDirectories(작업폴더);
        Font fontere_njaru = new Font("Monospaced", Font.PLAIN, 16);
        sewnde.setFont(fontere_njaru); 출력.setFont(fontere_njaru); 출력.setEditable(false);
        sewnde.setTabSize(4);
        sewnde.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        sewnde.setBackground(new Color(250, 251, 252));
        sewnde.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("fiilde")); 명령판.add(fiilde_naatnugol_innde);
        명령판.add(new JLabel("주 fedde_njaru")); 명령판.add(fedde_naatnugol_innde);
        feɗoode(명령판, "udditde", this::udditde); feɗoode(명령판, "resde_njaru", this::resde_njaru);
        feɗoode(명령판, "tafde_sewnde", () -> 번역(false, false));
        feɗoode(명령판, "실행", () -> 번역(true, false));
        feɗoode(명령판, "실행 fiilde 만들기", () -> 번역(false, true));
        feɗoode(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(sewnde), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        falanteere.add(명령판, BorderLayout.NORTH); falanteere.add(나눔, BorderLayout.CENTER);
        falanteere.setSize(1200, 750); falanteere.setLocationRelativeTo(null);
        falanteere.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        falanteere.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent saɗteende) { 멈춤(); 일꾼.shutdownNow(); }
        });
        udditde(); falanteere.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource lasli_fontere = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object naatnugol_njaru : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(naatnugol_njaru) instanceof Font) UIManager.put(naatnugol_njaru, lasli_fontere);
                }
                new gollorde();
            } catch (Exception juumre) { juumre.printStackTrace(); }
        });
    }
}
