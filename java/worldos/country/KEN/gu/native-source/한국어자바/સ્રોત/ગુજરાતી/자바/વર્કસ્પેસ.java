// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자바;

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

/** ઉપયોગકર્તા 홈에서 Java 원문을 સંપાદન_મૂલ્ય·બિલ્ડ_કરો_સ્રોત·실행하는 작은 Swing વર્કસ્પેસ. */
public final class વર્કસ્પેસ {
    private final JFrame વિંડો = new JFrame("jkoros — 자바 વર્કસ્પેસ");
    private final JTextArea સ્રોત = new JTextArea();
    private final JTextArea આઉટપુટ = new JTextArea(8, 80);
    private final JTextField ફાઇલ_પ્રવેશ_નામ = new JTextField("인사.java", 20);
    private final JTextField વર્ગ_પ્રવેશ_નામ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process પ્રક્રિયા_મૂલ્ય;
    private final String લાઇબ્રેરી = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String લખાણ) { SwingUtilities.invokeLater(() -> આઉટપુટ.append(લખાણ + "\n")); }
    private void બટન(JPanel વર્ઝન_મૂલ્ય, String નામ, Runnable 행동) {
        JButton બટન = new JButton(નામ);
        બટન.addActionListener(ઇવેંટ -> 행동.run());
        વર્ઝન_મૂલ્ય.add(બટન);
    }
    private boolean સંગ્રહ_કરવો_મૂલ્ય() {
        try {
            Path પથ = 작업폴더.resolve(ફાઇલ_પ્રવેશ_નામ.getText());
            Files.createDirectories(પથ.getParent());
            ફાઈલ.લખો(પથ, સ્રોત.getText());
            알림("સંગ્રહ_કરવો_મૂલ્ય: " + પથ);
            return true;
        } catch (Exception ભૂલ) { 알림(ભૂલ.toString()); return false; }
    }
    private void ખોલો() {
        try { સ્રોત.setText(ફાઈલ.વાંચો(작업폴더.resolve(ફાઇલ_પ્રવેશ_નામ.getText()))); }
        catch (Exception ભૂલ) { 알림(ભૂલ.toString()); }
    }
    private int આદેશ(List<String> આદેશ) throws Exception {
        પ્રક્રિયા_મૂલ્ય = new ProcessBuilder(આદેશ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader લાઇન = new BufferedReader(new InputStreamReader(પ્રક્રિયા_મૂલ્ય.getInputStream(), StandardCharsets.UTF_8))) {
            String લખાણ;
            while ((લખાણ = લાઇન.readLine()) != null) 알림(લખાણ);
        }
        int સ્થિતિ_મૂલ્ય_e10195a1 = પ્રક્રિયા_મૂલ્ય.waitFor(); પ્રક્રિયા_મૂલ્ય = null;
        알림("પ્રસ્થાન_એપ્લિકેશન 코드: " + સ્થિતિ_મૂલ્ય_e10195a1);
        return સ્થિતિ_મૂલ્ય_e10195a1;
    }
    private void અનુવાદ_કરો_સ્રોત(boolean અમલ_કરો_આદેશ, boolean 실행파일) {
        if (!સંગ્રહ_કરવો_મૂલ્ય()) return;
        String 입력 = ફાઇલ_પ્રવેશ_નામ.getText(), પ્રવેશ_બિંદુ_મૂલ્ય = વર્ગ_પ્રવેશ_નામ.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    આદેશ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", પ્રવેશ_બિંદુ_મૂલ્ય,
                        "--classpath", લાઇબ્રેરી, "-o", "실행프로그램", 입력));
                } else if (આદેશ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", લાઇબ્રેરી,
                        "-d", "classes", 입력)) == 0 && અમલ_કરો_આદેશ) {
                    આદેશ(Arrays.asList("java", "-cp", "classes:" + લાઇબ્રેરી, પ્રવેશ_બિંદુ_મૂલ્ય));
                }
            } catch (Exception ભૂલ) { 알림(ભૂલ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = પ્રક્રિયા_મૂલ્ય;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private વર્કસ્પેસ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ફૉન્ટ_મૂલ્ય = new Font("Monospaced", Font.PLAIN, 16);
        સ્રોત.setFont(ફૉન્ટ_મૂલ્ય); આઉટપુટ.setFont(ફૉન્ટ_મૂલ્ય); આઉટપુટ.setEditable(false);
        સ્રોત.setTabSize(4);
        સ્રોત.setMargin(new Insets(10, 12, 10, 12));
        આઉટપુટ.setMargin(new Insets(8, 12, 8, 12));
        સ્રોત.setBackground(new Color(250, 251, 252));
        સ્રોત.setForeground(new Color(32, 43, 58));
        JPanel આદેશ_પેનલ = new JPanel();
        આદેશ_પેનલ.add(new JLabel("ફાઈલ")); આદેશ_પેનલ.add(ફાઇલ_પ્રવેશ_નામ);
        આદેશ_પેનલ.add(new JLabel("주 વર્ગ_મૂલ્ય")); આદેશ_પેનલ.add(વર્ગ_પ્રવેશ_નામ);
        બટન(આદેશ_પેનલ, "ખોલો", this::ખોલો); બટન(આદેશ_પેનલ, "સંગ્રહ_કરવો_મૂલ્ય", this::સંગ્રહ_કરવો_મૂલ્ય);
        બટન(આદેશ_પેનલ, "બિલ્ડ_કરો_સ્રોત", () -> અનુવાદ_કરો_સ્રોત(false, false));
        બટન(આદેશ_પેનલ, "અમલ_કરો_આદેશ", () -> અનુવાદ_કરો_સ્રોત(true, false));
        બટન(આદેશ_પેનલ, "અમલ_કરો_આદેશ ફાઈલ બનાવો_પ્રવેશ", () -> અનુવાદ_કરો_સ્રોત(false, true));
        બટન(આદેશ_પેનલ, "멈춤", this::멈춤);
        JSplitPane ભાગાકાર_પરિમાણ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(સ્રોત), new JScrollPane(આઉટપુટ));
        ભાગાકાર_પરિમાણ.setResizeWeight(0.75);
        વિંડો.add(આદેશ_પેનલ, BorderLayout.NORTH); વિંડો.add(ભાગાકાર_પરિમાણ, BorderLayout.CENTER);
        વિંડો.setSize(1200, 750); વિંડો.setLocationRelativeTo(null);
        વિંડો.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        વિંડો.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ઇવેંટ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ખોલો(); વિંડો.setVisible(true);
    }
    public static void main(String[] દલીલો) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ડિફૉલ્ટ_ફૉન્ટ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object પ્રવેશ_મૂલ્ય : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(પ્રવેશ_મૂલ્ય) instanceof Font) UIManager.put(પ્રવેશ_મૂલ્ય, ડિફૉલ્ટ_ફૉન્ટ);
                }
                new વર્કસ્પેસ();
            } catch (Exception ભૂલ) { ભૂલ.printStackTrace(); }
        });
    }
}
