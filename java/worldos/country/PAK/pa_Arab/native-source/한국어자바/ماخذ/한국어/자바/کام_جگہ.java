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

/** صارف 홈에서 Java 원문을 تدوین_قدر·تیار_کرو_ماخذ·실행하는 작은 Swing کام_جگہ. */
public final class کام_جگہ {
    private final JFrame کھڑکی = new JFrame("jkoros — 자바 کام_جگہ");
    private final JTextArea ماخذ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField فائل_داخلہ_ناں = new JTextField("인사.java", 20);
    private final JTextField درجہ_داخلہ_ناں = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process عمل_قدر;
    private final String لائبریری = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String متن) { SwingUtilities.invokeLater(() -> 출력.append(متن + "\n")); }
    private void بٹن(JPanel ورژن_قدر, String ناں, Runnable 행동) {
        JButton بٹن = new JButton(ناں);
        بٹن.addActionListener(واقعہ -> 행동.run());
        ورژن_قدر.add(بٹن);
    }
    private boolean ذخیرہ_کرو_قدر() {
        try {
            Path راہ = 작업폴더.resolve(فائل_داخلہ_ناں.getText());
            Files.createDirectories(راہ.getParent());
            فائل.لکھو(راہ, ماخذ.getText());
            알림("ذخیرہ_کرو_قدر: " + راہ);
            return true;
        } catch (Exception نقص) { 알림(نقص.toString()); return false; }
    }
    private void بنڑاؤ() {
        try { ماخذ.setText(فائل.읽기(작업폴더.resolve(فائل_داخلہ_ناں.getText()))); }
        catch (Exception نقص) { 알림(نقص.toString()); }
    }
    private int حکم(List<String> حکم) throws Exception {
        عمل_قدر = new ProcessBuilder(حکم).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader لائن = new BufferedReader(new InputStreamReader(عمل_قدر.getInputStream(), StandardCharsets.UTF_8))) {
            String متن;
            while ((متن = لائن.readLine()) != null) 알림(متن);
        }
        int حالت_قدر = عمل_قدر.waitFor(); عمل_قدر = null;
        알림("خارج_کرو_ایپ 코드: " + حالت_قدر);
        return حالت_قدر;
    }
    private void ترجمہ_کرو_ماخذ(boolean نفاذ_کرو_حکم, boolean 실행파일) {
        if (!ذخیرہ_کرو_قدر()) return;
        String 입력 = فائل_داخلہ_ناں.getText(), داخلہ_مقام_قدر = درجہ_داخلہ_ناں.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    حکم(Arrays.asList("jclassc", "--target", "openjdk", "--entry", داخلہ_مقام_قدر,
                        "--classpath", لائبریری, "-o", "실행프로그램", 입력));
                } else if (حکم(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", لائبریری,
                        "-d", "classes", 입력)) == 0 && نفاذ_کرو_حکم) {
                    حکم(Arrays.asList("java", "-cp", "classes:" + لائبریری, داخلہ_مقام_قدر));
                }
            } catch (Exception نقص) { 알림(نقص.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = عمل_قدر;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private کام_جگہ() throws IOException {
        Files.createDirectories(작업폴더);
        Font فانٹ_قدر = new Font("Monospaced", Font.PLAIN, 16);
        ماخذ.setFont(فانٹ_قدر); 출력.setFont(فانٹ_قدر); 출력.setEditable(false);
        ماخذ.setTabSize(4);
        ماخذ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ماخذ.setBackground(new Color(250, 251, 252));
        ماخذ.setForeground(new Color(32, 43, 58));
        JPanel حکم_پینل = new JPanel();
        حکم_پینل.add(new JLabel("فائل")); حکم_پینل.add(فائل_داخلہ_ناں);
        حکم_پینل.add(new JLabel("주 درجہ_قدر")); حکم_پینل.add(درجہ_داخلہ_ناں);
        بٹن(حکم_پینل, "بنڑاؤ", this::بنڑاؤ); بٹن(حکم_پینل, "ذخیرہ_کرو_قدر", this::ذخیرہ_کرو_قدر);
        بٹن(حکم_پینل, "تیار_کرو_ماخذ", () -> ترجمہ_کرو_ماخذ(false, false));
        بٹن(حکم_پینل, "نفاذ_کرو_حکم", () -> ترجمہ_کرو_ماخذ(true, false));
        بٹن(حکم_پینل, "نفاذ_کرو_حکم فائل بنڑاؤ_داخلہ", () -> ترجمہ_کرو_ماخذ(false, true));
        بٹن(حکم_پینل, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ماخذ), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        کھڑکی.add(حکم_پینل, BorderLayout.NORTH); کھڑکی.add(나눔, BorderLayout.CENTER);
        کھڑکی.setSize(1200, 750); کھڑکی.setLocationRelativeTo(null);
        کھڑکی.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        کھڑکی.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent واقعہ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        بنڑاؤ(); کھڑکی.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource طے_شدہ_فونٹ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object داخلہ_قدر : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(داخلہ_قدر) instanceof Font) UIManager.put(داخلہ_قدر, طے_شدہ_فونٹ);
                }
                new کام_جگہ();
            } catch (Exception نقص) { نقص.printStackTrace(); }
        });
    }
}
