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

/** atuqtuq 홈에서 Java 원문을 aaqqigiarli_atuutilik·sanali_pivviujuq·실행하는 작은 Swing pilirivvik. */
public final class pilirivvik {
    private final JFrame igalaangujaq = new JFrame("jkoros — 자바 pilirivvik");
    private final JTextArea pivviujuq = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ini_Iliniku_atiq = new JTextField("인사.java", 20);
    private final JTextField naliannuungavik_Iliniku_atiq = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Pivallianiq_atuutilik;
    private final String tukisiurvik = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String titiqqaq) { SwingUtilities.invokeLater(() -> 출력.append(titiqqaq + "\n")); }
    private void tikkuagaq(JPanel imaittuuninga_atuutilik, String atiq, Runnable 행동) {
        JButton tikkuagaq = new JButton(atiq);
        tikkuagaq.addActionListener(piniku -> 행동.run());
        imaittuuninga_atuutilik.add(tikkuagaq);
    }
    private boolean tuqqurli_atuutilik() {
        try {
            Path aqqut = 작업폴더.resolve(ini_Iliniku_atiq.getText());
            Files.createDirectories(aqqut.getParent());
            ini.titiraq(aqqut, pivviujuq.getText());
            알림("tuqqurli_atuutilik: " + aqqut);
            return true;
        } catch (Exception tammarniq) { 알림(tammarniq.toString()); return false; }
    }
    private void matuirli() {
        try { pivviujuq.setText(ini.읽기(작업폴더.resolve(ini_Iliniku_atiq.getText()))); }
        catch (Exception tammarniq) { 알림(tammarniq.toString()); }
    }
    private int piqujijjut(List<String> piqujijjut) throws Exception {
        Pivallianiq_atuutilik = new ProcessBuilder(piqujijjut).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader titikutaak = new BufferedReader(new InputStreamReader(Pivallianiq_atuutilik.getInputStream(), StandardCharsets.UTF_8))) {
            String titiqqaq;
            while ((titiqqaq = titikutaak.readLine()) != null) 알림(titiqqaq);
        }
        int qanuilinganiq_atuutilik = Pivallianiq_atuutilik.waitFor(); Pivallianiq_atuutilik = null;
        알림("taima_pilirijjut 코드: " + qanuilinganiq_atuutilik);
        return qanuilinganiq_atuutilik;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!tuqqurli_atuutilik()) return;
        String 입력 = ini_Iliniku_atiq.getText(), Iliniku_puinti_atuutilik = naliannuungavik_Iliniku_atiq.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    piqujijjut(Arrays.asList("jclassc", "--target", "openjdk", "--entry", Iliniku_puinti_atuutilik,
                        "--classpath", tukisiurvik, "-o", "실행프로그램", 입력));
                } else if (piqujijjut(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", tukisiurvik,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    piqujijjut(Arrays.asList("java", "-cp", "classes:" + tukisiurvik, Iliniku_puinti_atuutilik));
                }
            } catch (Exception tammarniq) { 알림(tammarniq.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Pivallianiq_atuutilik;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private pilirivvik() throws IOException {
        Files.createDirectories(작업폴더);
        Font titirausiq_atuutilik = new Font("Monospaced", Font.PLAIN, 16);
        pivviujuq.setFont(titirausiq_atuutilik); 출력.setFont(titirausiq_atuutilik); 출력.setEditable(false);
        pivviujuq.setTabSize(4);
        pivviujuq.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        pivviujuq.setBackground(new Color(250, 251, 252));
        pivviujuq.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("ini")); 명령판.add(ini_Iliniku_atiq);
        명령판.add(new JLabel("주 naliannuungavik_atuutilik")); 명령판.add(naliannuungavik_Iliniku_atiq);
        tikkuagaq(명령판, "matuirli", this::matuirli); tikkuagaq(명령판, "tuqqurli_atuutilik", this::tuqqurli_atuutilik);
        tikkuagaq(명령판, "sanali_pivviujuq", () -> 번역(false, false));
        tikkuagaq(명령판, "실행", () -> 번역(true, false));
        tikkuagaq(명령판, "실행 ini 만들기", () -> 번역(false, true));
        tikkuagaq(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(pivviujuq), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        igalaangujaq.add(명령판, BorderLayout.NORTH); igalaangujaq.add(나눔, BorderLayout.CENTER);
        igalaangujaq.setSize(1200, 750); igalaangujaq.setLocationRelativeTo(null);
        igalaangujaq.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        igalaangujaq.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent piniku) { 멈춤(); 일꾼.shutdownNow(); }
        });
        matuirli(); igalaangujaq.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource titirausiuttautigijuq = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object Iliniku_atuutilik : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(Iliniku_atuutilik) instanceof Font) UIManager.put(Iliniku_atuutilik, titirausiuttautigijuq);
                }
                new pilirivvik();
            } catch (Exception tammarniq) { tammarniq.printStackTrace(); }
        });
    }
}
