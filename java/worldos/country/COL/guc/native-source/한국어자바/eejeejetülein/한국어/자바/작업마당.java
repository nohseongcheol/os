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

/** ka_yataayakalü 홈에서 Java 원문을 anaataa_ajutuu·akompiraajaa_eejeejetülein·실행하는 작은 Swing 작업마당. */
public final class 작업마당 {
    private final JFrame analaaya = new JFrame("jkoros — 자바 작업마당");
    private final JTextArea eejeejetülein = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField 파일이름 = new JTextField("인사.java", 20);
    private final JTextField 클래스이름 = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process 과정;
    private final String anaajaalee = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String 글) { SwingUtilities.invokeLater(() -> 출력.append(글 + "\n")); }
    private void ajüttülee(JPanel 판, String 이름, Runnable 행동) {
        JButton ajüttülee = new JButton(이름);
        ajüttülee.addActionListener(kasachiki -> 행동.run());
        판.add(ajüttülee);
    }
    private boolean 저장() {
        try {
            Path wopu_a_ttaaleemüin = 작업폴더.resolve(파일이름.getText());
            Files.createDirectories(wopu_a_ttaaleemüin.getParent());
            anaajaalaa.ashajaa(wopu_a_ttaaleemüin, eejeejetülein.getText());
            알림("저장: " + wopu_a_ttaaleemüin);
            return true;
        } catch (Exception ajachitia) { 알림(ajachitia.toString()); return false; }
    }
    private void 열기() {
        try { eejeejetülein.setText(anaajaalaa.읽기(작업폴더.resolve(파일이름.getText()))); }
        catch (Exception ajachitia) { 알림(ajachitia.toString()); }
    }
    private int aluwataaya(List<String> aluwataaya) throws Exception {
        과정 = new ProcessBuilder(aluwataaya).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader liinia = new BufferedReader(new InputStreamReader(과정.getInputStream(), StandardCharsets.UTF_8))) {
            String 글;
            while ((글 = liinia.readLine()) != null) 알림(글);
        }
        int jamakua_iparülein_ajutuu = 과정.waitFor(); 과정 = null;
        알림("aju_itaa_akumajiaa 코드: " + jamakua_iparülein_ajutuu);
        return jamakua_iparülein_ajutuu;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!저장()) return;
        String 입력 = 파일이름.getText(), ekeroliaa_o_uchikanain_ajutuu = 클래스이름.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    aluwataaya(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ekeroliaa_o_uchikanain_ajutuu,
                        "--classpath", anaajaalee, "-o", "실행프로그램", 입력));
                } else if (aluwataaya(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", anaajaalee,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    aluwataaya(Arrays.asList("java", "-cp", "classes:" + anaajaalee, ekeroliaa_o_uchikanain_ajutuu));
                }
            } catch (Exception ajachitia) { 알림(ajachitia.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = 과정;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private 작업마당() throws IOException {
        Files.createDirectories(작업폴더);
        Font ashajiaakua_ipa_ajutuu = new Font("Monospaced", Font.PLAIN, 16);
        eejeejetülein.setFont(ashajiaakua_ipa_ajutuu); 출력.setFont(ashajiaakua_ipa_ajutuu); 출력.setEditable(false);
        eejeejetülein.setTabSize(4);
        eejeejetülein.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        eejeejetülein.setBackground(new Color(250, 251, 252));
        eejeejetülein.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("anaajaalaa")); 명령판.add(파일이름);
        명령판.add(new JLabel("주 akotchijuushi_ajutuu_55654bf1")); 명령판.add(클래스이름);
        ajüttülee(명령판, "열기", this::열기); ajüttülee(명령판, "저장", this::저장);
        ajüttülee(명령판, "akompiraajaa_eejeejetülein", () -> 번역(false, false));
        ajüttülee(명령판, "실행", () -> 번역(true, false));
        ajüttülee(명령판, "실행 anaajaalaa 만들기", () -> 번역(false, true));
        ajüttülee(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(eejeejetülein), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        analaaya.add(명령판, BorderLayout.NORTH); analaaya.add(나눔, BorderLayout.CENTER);
        analaaya.setSize(1200, 750); analaaya.setLocationRelativeTo(null);
        analaaya.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        analaaya.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent kasachiki) { 멈춤(); 일꾼.shutdownNow(); }
        });
        열기(); analaaya.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource aneekuushitüjülia_ashajiaakua_ipa = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ekeroliaa_ajutuu : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ekeroliaa_ajutuu) instanceof Font) UIManager.put(ekeroliaa_ajutuu, aneekuushitüjülia_ashajiaakua_ipa);
                }
                new 작업마당();
            } catch (Exception ajachitia) { ajachitia.printStackTrace(); }
        });
    }
}
