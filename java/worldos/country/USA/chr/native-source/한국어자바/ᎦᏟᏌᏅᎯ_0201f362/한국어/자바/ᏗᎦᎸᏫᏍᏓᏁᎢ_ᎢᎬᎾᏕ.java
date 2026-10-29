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

/** ᎬᏗᏍᎩ 홈에서 Java 원문을 ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ·ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ·실행하는 작은 Swing ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ. */
public final class ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ {
    private final JFrame ᏦᎳᏂ = new JFrame("jkoros — 자바 ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ");
    private final JTextArea ᎦᏟᏌᏅᎯ_0201f362 = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ = new JTextField("인사.java", 20);
    private final JTextField ᏄᏍᏛᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ;
    private final String ᏧᏂᎪᎵᏰᏗᎢ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ᎠᎪᎵᏰᏗ) { SwingUtilities.invokeLater(() -> 출력.append(ᎠᎪᎵᏰᏗ + "\n")); }
    private void ᎠᏐᏅᏍᏙᏗ(JPanel ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ, String ᏚᏙᎥᎢ, Runnable 행동) {
        JButton ᎠᏐᏅᏍᏙᏗ = new JButton(ᏚᏙᎥᎢ);
        ᎠᏐᏅᏍᏙᏗ.addActionListener(ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ -> 행동.run());
        ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ.add(ᎠᏐᏅᏍᏙᏗ);
    }
    private boolean Store_ᏧᎬᏩᎶᏗᏯ() {
        try {
            Path ᎠᏍᏓᏩᏛᏍᏗ = 작업폴더.resolve(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.getText());
            Files.createDirectories(ᎠᏍᏓᏩᏛᏍᏗ.getParent());
            ᎠᏍᏆᏂᎪᏙᏗ.ᎪᏪᎶᏗ(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ_0201f362.getText());
            알림("Store_ᏧᎬᏩᎶᏗᏯ: " + ᎠᏍᏓᏩᏛᏍᏗ);
            return true;
        } catch (Exception ᎦᎵᏓᏍᏔᏅ) { 알림(ᎦᎵᏓᏍᏔᏅ.toString()); return false; }
    }
    private void ᎯᏍᏚᎢ() {
        try { ᎦᏟᏌᏅᎯ_0201f362.setText(ᎠᏍᏆᏂᎪᏙᏗ.읽기(작업폴더.resolve(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.getText()))); }
        catch (Exception ᎦᎵᏓᏍᏔᏅ) { 알림(ᎦᎵᏓᏍᏔᏅ.toString()); }
    }
    private int ᎤᏁᏤᎸᎩ(List<String> ᎤᏁᏤᎸᎩ) throws Exception {
        ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = new ProcessBuilder(ᎤᏁᏤᎸᎩ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ᏚᏓᏅᏅᎢ = new BufferedReader(new InputStreamReader(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.getInputStream(), StandardCharsets.UTF_8))) {
            String ᎠᎪᎵᏰᏗ;
            while ((ᎠᎪᎵᏰᏗ = ᏚᏓᏅᏅᎢ.readLine()) != null) 알림(ᎠᎪᎵᏰᏗ);
        }
        int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.waitFor(); ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = null;
        알림("ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ 코드: " + ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ);
        return ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ;
    }
    private void 번역(boolean ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ, boolean 실행파일) {
        if (!Store_ᏧᎬᏩᎶᏗᏯ()) return;
        String 입력 = ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.getText(), Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ_ᏧᎬᏩᎶᏗᏯ = ᏄᏍᏛᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ᎤᏁᏤᎸᎩ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ_ᏧᎬᏩᎶᏗᏯ,
                        "--classpath", ᏧᏂᎪᎵᏰᏗᎢ, "-o", "실행프로그램", 입력));
                } else if (ᎤᏁᏤᎸᎩ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ᏧᏂᎪᎵᏰᏗᎢ,
                        "-d", "classes", 입력)) == 0 && ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ) {
                    ᎤᏁᏤᎸᎩ(Arrays.asList("java", "-cp", "classes:" + ᏧᏂᎪᎵᏰᏗᎢ, Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ_ᏧᎬᏩᎶᏗᏯ));
                }
            } catch (Exception ᎦᎵᏓᏍᏔᏅ) { 알림(ᎦᎵᏓᏍᏔᏅ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ = new Font("Monospaced", Font.PLAIN, 16);
        ᎦᏟᏌᏅᎯ_0201f362.setFont(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ); 출력.setFont(ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ_ᏧᎬᏩᎶᏗᏯ); 출력.setEditable(false);
        ᎦᏟᏌᏅᎯ_0201f362.setTabSize(4);
        ᎦᏟᏌᏅᎯ_0201f362.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ᎦᏟᏌᏅᎯ_0201f362.setBackground(new Color(250, 251, 252));
        ᎦᏟᏌᏅᎯ_0201f362.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("ᎠᏍᏆᏂᎪᏙᏗ")); 명령판.add(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ);
        명령판.add(new JLabel("주 ᏄᏍᏛᎢ_ᏧᎬᏩᎶᏗᏯ")); 명령판.add(ᏄᏍᏛᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ);
        ᎠᏐᏅᏍᏙᏗ(명령판, "ᎯᏍᏚᎢ", this::ᎯᏍᏚᎢ); ᎠᏐᏅᏍᏙᏗ(명령판, "Store_ᏧᎬᏩᎶᏗᏯ", this::Store_ᏧᎬᏩᎶᏗᏯ);
        ᎠᏐᏅᏍᏙᏗ(명령판, "ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ", () -> 번역(false, false));
        ᎠᏐᏅᏍᏙᏗ(명령판, "ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ", () -> 번역(true, false));
        ᎠᏐᏅᏍᏙᏗ(명령판, "ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ ᎠᏍᏆᏂᎪᏙᏗ 만들기", () -> 번역(false, true));
        ᎠᏐᏅᏍᏙᏗ(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ᎦᏟᏌᏅᎯ_0201f362), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        ᏦᎳᏂ.add(명령판, BorderLayout.NORTH); ᏦᎳᏂ.add(나눔, BorderLayout.CENTER);
        ᏦᎳᏂ.setSize(1200, 750); ᏦᎳᏂ.setLocationRelativeTo(null);
        ᏦᎳᏂ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ᏦᎳᏂ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ᎯᏍᏚᎢ(); ᏦᎳᏂ.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ) instanceof Font) UIManager.put(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏄᏍᏛ_ᎠᏙᏪᎵᏍᎩ);
                }
                new ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ();
            } catch (Exception ᎦᎵᏓᏍᏔᏅ) { ᎦᎵᏓᏍᏔᏅ.printStackTrace(); }
        });
    }
}
