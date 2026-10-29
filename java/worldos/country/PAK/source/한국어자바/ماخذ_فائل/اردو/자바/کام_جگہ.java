// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.자바;

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

/** صارف 홈에서 Java 원문을 تدوین_قدر·مرتب_کریں_ماخذ·실행하는 작은 Swing کام_جگہ. */
public final class کام_جگہ {
    private final JFrame ونڈو = new JFrame("jkoros — 자바 کام_جگہ");
    private final JTextArea ماخذ_فائل = new JTextArea();
    private final JTextArea اخراج_کا_مقام = new JTextArea(8, 80);
    private final JTextField فائل_اندراج_نام = new JTextField("인사.java", 20);
    private final JTextField صنف_اندراج_نام = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process عمل_قدر;
    private final String لائبریری = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String متن) { SwingUtilities.invokeLater(() -> اخراج_کا_مقام.append(متن + "\n")); }
    private void بٹن(JPanel ورژن_قدر, String نام, Runnable 행동) {
        JButton بٹن = new JButton(نام);
        بٹن.addActionListener(واقعہ -> 행동.run());
        ورژن_قدر.add(بٹن);
    }
    private boolean ذخیرہ_کریں_قدر() {
        try {
            Path راستہ_2 = 작업폴더.resolve(فائل_اندراج_نام.getText());
            Files.createDirectories(راستہ_2.getParent());
            فائل_کا_نام.لکھیں(راستہ_2, ماخذ_فائل.getText());
            알림("ذخیرہ_کریں_قدر: " + راستہ_2);
            return true;
        } catch (Exception غلطی) { 알림(غلطی.toString()); return false; }
    }
    private void کھولیں() {
        try { ماخذ_فائل.setText(فائل_کا_نام.پڑھیں(작업폴더.resolve(فائل_اندراج_نام.getText()))); }
        catch (Exception غلطی) { 알림(غلطی.toString()); }
    }
    private int حکم(List<String> حکم) throws Exception {
        عمل_قدر = new ProcessBuilder(حکم).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader اندراج_کی_سطر = new BufferedReader(new InputStreamReader(عمل_قدر.getInputStream(), StandardCharsets.UTF_8))) {
            String متن;
            while ((متن = اندراج_کی_سطر.readLine()) != null) 알림(متن);
        }
        int حالت_قدر = عمل_قدر.waitFor(); عمل_قدر = null;
        알림("خروج_ایپ 코드: " + حالت_قدر);
        return حالت_قدر;
    }
    private void ترجمہ_ماخذ(boolean نفاذ_کریں_حکم, boolean 실행파일) {
        if (!ذخیرہ_کریں_قدر()) return;
        String 입력 = فائل_اندراج_نام.getText(), اندراج_نقطہ_قدر = صنف_اندراج_نام.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    حکم(Arrays.asList("jclassc", "--target", "openjdk", "--entry", اندراج_نقطہ_قدر,
                        "--classpath", لائبریری, "-o", "실행프로그램", 입력));
                } else if (حکم(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", لائبریری,
                        "-d", "classes", 입력)) == 0 && نفاذ_کریں_حکم) {
                    حکم(Arrays.asList("java", "-cp", "classes:" + لائبریری, اندراج_نقطہ_قدر));
                }
            } catch (Exception غلطی) { 알림(غلطی.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = عمل_قدر;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private کام_جگہ() throws IOException {
        Files.createDirectories(작업폴더);
        Font فانٹ_قدر = new Font("Monospaced", Font.PLAIN, 16);
        ماخذ_فائل.setFont(فانٹ_قدر); اخراج_کا_مقام.setFont(فانٹ_قدر); اخراج_کا_مقام.setEditable(false);
        ماخذ_فائل.setTabSize(4);
        ماخذ_فائل.setMargin(new Insets(10, 12, 10, 12));
        اخراج_کا_مقام.setMargin(new Insets(8, 12, 8, 12));
        ماخذ_فائل.setBackground(new Color(250, 251, 252));
        ماخذ_فائل.setForeground(new Color(32, 43, 58));
        JPanel حکم_پینل = new JPanel();
        حکم_پینل.add(new JLabel("فائل_کا_نام")); حکم_پینل.add(فائل_اندراج_نام);
        حکم_پینل.add(new JLabel("주 صنف_قدر")); حکم_پینل.add(صنف_اندراج_نام);
        بٹن(حکم_پینل, "کھولیں", this::کھولیں); بٹن(حکم_پینل, "ذخیرہ_کریں_قدر", this::ذخیرہ_کریں_قدر);
        بٹن(حکم_پینل, "مرتب_کریں_ماخذ", () -> ترجمہ_ماخذ(false, false));
        بٹن(حکم_پینل, "نفاذ_کریں_حکم", () -> ترجمہ_ماخذ(true, false));
        بٹن(حکم_پینل, "نفاذ_کریں_حکم فائل_کا_نام بنائیں_اندراج", () -> ترجمہ_ماخذ(false, true));
        بٹن(حکم_پینل, "멈춤", this::멈춤);
        JSplitPane تقسیم_پیمائش = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ماخذ_فائل), new JScrollPane(اخراج_کا_مقام));
        تقسیم_پیمائش.setResizeWeight(0.75);
        ونڈو.add(حکم_پینل, BorderLayout.NORTH); ونڈو.add(تقسیم_پیمائش, BorderLayout.CENTER);
        ونڈو.setSize(1200, 750); ونڈو.setLocationRelativeTo(null);
        ونڈو.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ونڈو.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent واقعہ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        کھولیں(); ونڈو.setVisible(true);
    }
    public static void main(String[] دلائل) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource طے_شدہ_فانٹ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object اندراج_قدر : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(اندراج_قدر) instanceof Font) UIManager.put(اندراج_قدر, طے_شدہ_فانٹ);
                }
                new کام_جگہ();
            } catch (Exception غلطی) { غلطی.printStackTrace(); }
        });
    }
}
