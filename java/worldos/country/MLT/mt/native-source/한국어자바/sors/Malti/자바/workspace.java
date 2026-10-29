// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자바;

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

/** utent 홈에서 Java 원문을 editja_VALUE·bena_sors·실행하는 작은 Swing workspace. */
public final class workspace {
    private final JFrame tieqa = new JFrame("jkoros — 자바 workspace");
    private final JTextArea sors = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField fajl_entrata_isem = new JTextField("인사.java", 20);
    private final JTextField klassi_entrata_isem = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Proċess_VALUE;
    private final String librerija = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void buttuna(JPanel verżjoni_VALUE, String isem, Runnable 행동) {
        JButton buttuna = new JButton(isem);
        buttuna.addActionListener(avveniment -> 행동.run());
        verżjoni_VALUE.add(buttuna);
    }
    private boolean Store_VALUE() {
        try {
            Path mogħdija = 작업폴더.resolve(fajl_entrata_isem.getText());
            Files.createDirectories(mogħdija.getParent());
            fajl.kiteb(mogħdija, sors.getText());
            알림("Store_VALUE: " + mogħdija);
            return true;
        } catch (Exception żball) { 알림(żball.toString()); return false; }
    }
    private void fetaħ() {
        try { sors.setText(fajl.읽기(작업폴더.resolve(fajl_entrata_isem.getText()))); }
        catch (Exception żball) { 알림(żball.toString()); }
    }
    private int kmand(List<String> kmand) throws Exception {
        Proċess_VALUE = new ProcessBuilder(kmand).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader linja = new BufferedReader(new InputStreamReader(Proċess_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = linja.readLine()) != null) 알림(SMS);
        }
        int stat_VALUE = Proċess_VALUE.waitFor(); Proċess_VALUE = null;
        알림("Ħruġ_programm CODE_VALUE: " + stat_VALUE);
        return stat_VALUE;
    }
    private void Ittraduċi_sors(boolean eżegwixxa_kmand, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = fajl_entrata_isem.getText(), entrata_punt_VALUE = klassi_entrata_isem.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    kmand(Arrays.asList("jclassc", "--target", "openjdk", "--entry", entrata_punt_VALUE,
                        "--classpath", librerija, "-o", "실행프로그램", 입력));
                } else if (kmand(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", librerija,
                        "-d", "classes", 입력)) == 0 && eżegwixxa_kmand) {
                    kmand(Arrays.asList("java", "-cp", "classes:" + librerija, entrata_punt_VALUE));
                }
            } catch (Exception żball) { 알림(żball.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Proċess_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private workspace() throws IOException {
        Files.createDirectories(작업폴더);
        Font font_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        sors.setFont(font_VALUE); 출력.setFont(font_VALUE); 출력.setEditable(false);
        sors.setTabSize(4);
        sors.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        sors.setBackground(new Color(250, 251, 252));
        sors.setForeground(new Color(32, 43, 58));
        JPanel kmand_panew = new JPanel();
        kmand_panew.add(new JLabel("fajl")); kmand_panew.add(fajl_entrata_isem);
        kmand_panew.add(new JLabel("주 klassi_VALUE")); kmand_panew.add(klassi_entrata_isem);
        buttuna(kmand_panew, "fetaħ", this::fetaħ); buttuna(kmand_panew, "Store_VALUE", this::Store_VALUE);
        buttuna(kmand_panew, "bena_sors", () -> Ittraduċi_sors(false, false));
        buttuna(kmand_panew, "eżegwixxa_kmand", () -> Ittraduċi_sors(true, false));
        buttuna(kmand_panew, "eżegwixxa_kmand fajl ħalaq_entrata", () -> Ittraduċi_sors(false, true));
        buttuna(kmand_panew, "멈춤", this::멈춤);
        JSplitPane diviżjoni_miżura = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(sors), new JScrollPane(출력));
        diviżjoni_miżura.setResizeWeight(0.75);
        tieqa.add(kmand_panew, BorderLayout.NORTH); tieqa.add(diviżjoni_miżura, BorderLayout.CENTER);
        tieqa.setSize(1200, 750); tieqa.setLocationRelativeTo(null);
        tieqa.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        tieqa.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent avveniment) { 멈춤(); 일꾼.shutdownNow(); }
        });
        fetaħ(); tieqa.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource font_default = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object entrata_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(entrata_VALUE) instanceof Font) UIManager.put(entrata_VALUE, font_default);
                }
                new workspace();
            } catch (Exception żball) { żball.printStackTrace(); }
        });
    }
}
