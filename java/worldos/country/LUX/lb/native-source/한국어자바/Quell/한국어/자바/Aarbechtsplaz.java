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

/** Benotzer 홈에서 Java 원문을 Editéieren_VALUE·erstellen_Quell·실행하는 작은 Swing Aarbechtsplaz. */
public final class Aarbechtsplaz {
    private final JFrame Fënster = new JFrame("jkoros — 자바 Aarbechtsplaz");
    private final JTextArea Quell = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField Fichier_Agab_Numm = new JTextField("인사.java", 20);
    private final JTextField Klass_Agab_Numm = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Prozess_VALUE;
    private final String Bibliothéik = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String SMS) { SwingUtilities.invokeLater(() -> 출력.append(SMS + "\n")); }
    private void Tast(JPanel Versioun_VALUE, String Numm, Runnable 행동) {
        JButton Tast = new JButton(Numm);
        Tast.addActionListener(Evenement -> 행동.run());
        Versioun_VALUE.add(Tast);
    }
    private boolean Store_VALUE() {
        try {
            Path Wee = 작업폴더.resolve(Fichier_Agab_Numm.getText());
            Files.createDirectories(Wee.getParent());
            Fichier.schreiwen(Wee, Quell.getText());
            알림("Store_VALUE: " + Wee);
            return true;
        } catch (Exception Feeler) { 알림(Feeler.toString()); return false; }
    }
    private void ariichten() {
        try { Quell.setText(Fichier.읽기(작업폴더.resolve(Fichier_Agab_Numm.getText()))); }
        catch (Exception Feeler) { 알림(Feeler.toString()); }
    }
    private int Befeel(List<String> Befeel) throws Exception {
        Prozess_VALUE = new ProcessBuilder(Befeel).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Zeil = new BufferedReader(new InputStreamReader(Prozess_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String SMS;
            while ((SMS = Zeil.readLine()) != null) 알림(SMS);
        }
        int Status_VALUE = Prozess_VALUE.waitFor(); Prozess_VALUE = null;
        알림("Schluss_App CODE_VALUE: " + Status_VALUE);
        return Status_VALUE;
    }
    private void TRANSLATE_Quell(boolean ausféieren_Befeel, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = Fichier_Agab_Numm.getText(), Agab_Punkt_VALUE = Klass_Agab_Numm.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Befeel(Arrays.asList("jclassc", "--target", "openjdk", "--entry", Agab_Punkt_VALUE,
                        "--classpath", Bibliothéik, "-o", "실행프로그램", 입력));
                } else if (Befeel(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", Bibliothéik,
                        "-d", "classes", 입력)) == 0 && ausféieren_Befeel) {
                    Befeel(Arrays.asList("java", "-cp", "classes:" + Bibliothéik, Agab_Punkt_VALUE));
                }
            } catch (Exception Feeler) { 알림(Feeler.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Prozess_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private Aarbechtsplaz() throws IOException {
        Files.createDirectories(작업폴더);
        Font Schrëftaart_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        Quell.setFont(Schrëftaart_VALUE); 출력.setFont(Schrëftaart_VALUE); 출력.setEditable(false);
        Quell.setTabSize(4);
        Quell.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        Quell.setBackground(new Color(250, 251, 252));
        Quell.setForeground(new Color(32, 43, 58));
        JPanel Befeel_Panel = new JPanel();
        Befeel_Panel.add(new JLabel("Fichier")); Befeel_Panel.add(Fichier_Agab_Numm);
        Befeel_Panel.add(new JLabel("주 Klass_VALUE")); Befeel_Panel.add(Klass_Agab_Numm);
        Tast(Befeel_Panel, "ariichten", this::ariichten); Tast(Befeel_Panel, "Store_VALUE", this::Store_VALUE);
        Tast(Befeel_Panel, "erstellen_Quell", () -> TRANSLATE_Quell(false, false));
        Tast(Befeel_Panel, "ausféieren_Befeel", () -> TRANSLATE_Quell(true, false));
        Tast(Befeel_Panel, "ausféieren_Befeel Fichier Create_Agab", () -> TRANSLATE_Quell(false, true));
        Tast(Befeel_Panel, "멈춤", this::멈춤);
        JSplitPane Divisioun_Mooss = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Quell), new JScrollPane(출력));
        Divisioun_Mooss.setResizeWeight(0.75);
        Fënster.add(Befeel_Panel, BorderLayout.NORTH); Fënster.add(Divisioun_Mooss, BorderLayout.CENTER);
        Fënster.setSize(1200, 750); Fënster.setLocationRelativeTo(null);
        Fënster.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Fënster.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Evenement) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ariichten(); Fënster.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource Standardschrëftaart = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object Agab_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(Agab_VALUE) instanceof Font) UIManager.put(Agab_VALUE, Standardschrëftaart);
                }
                new Aarbechtsplaz();
            } catch (Exception Feeler) { Feeler.printStackTrace(); }
        });
    }
}
