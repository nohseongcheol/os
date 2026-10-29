// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.자바;

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

/** فضاء_المستخدم 홈에서 Java 원문을 يحرر_قيمة·يحول_برمجياً_مصدر·실행하는 작은 Swing مساحة_عمل. */
public final class مساحة_عمل {
    private final JFrame نافذة = new JFrame("jkoros — 자바 مساحة_عمل");
    private final JTextArea مصدر = new JTextArea();
    private final JTextArea مخرجات = new JTextArea(8, 80);
    private final JTextField ملف_إدخال_اسم = new JTextField("인사.java", 20);
    private final JTextField فئة_إدخال_اسم = new JTextField("인사", 16);
    private final Path الدليل_المشغَّل = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService عامل_قيمة = Executors.newSingleThreadExecutor();
    private volatile Process عملية_قيمة;
    private final String مكتبة = "/opt/jkoros/lib/한국어자바.jar";

    private void إشعار(String نص) { SwingUtilities.invokeLater(() -> مخرجات.append(نص + "\n")); }
    private void زر(JPanel إصدار_قيمة, String اسم, Runnable 행동) {
        JButton زر = new JButton(اسم);
        زر.addActionListener(حدث -> 행동.run());
        إصدار_قيمة.add(زر);
    }
    private boolean مخزن_قيمة() {
        try {
            Path مسار = الدليل_المشغَّل.resolve(ملف_إدخال_اسم.getText());
            Files.createDirectories(مسار.getParent());
            ملف.كتابة(مسار, مصدر.getText());
            إشعار("مخزن_قيمة: " + مسار);
            return true;
        } catch (Exception خطأ) { إشعار(خطأ.toString()); return false; }
    }
    private void فتح() {
        try { مصدر.setText(ملف.قراءة(الدليل_المشغَّل.resolve(ملف_إدخال_اسم.getText()))); }
        catch (Exception خطأ) { إشعار(خطأ.toString()); }
    }
    private int أمر(List<String> أمر) throws Exception {
        عملية_قيمة = new ProcessBuilder(أمر).directory(الدليل_المشغَّل.toFile()).redirectErrorStream(true).start();
        try (BufferedReader سطر = new BufferedReader(new InputStreamReader(عملية_قيمة.getInputStream(), StandardCharsets.UTF_8))) {
            String نص;
            while ((نص = سطر.readLine()) != null) إشعار(نص);
        }
        int حالة_قيمة = عملية_قيمة.waitFor(); عملية_قيمة = null;
        إشعار("خروج_تطبيق رمز_قيمة_f3cd31ee: " + حالة_قيمة);
        return حالة_قيمة;
    }
    private void تحويل_مصدر(boolean ينفذ_أمر, boolean 실행파일) {
        if (!مخزن_قيمة()) return;
        String إدخال_قيمة = ملف_إدخال_اسم.getText(), نقطة_الإدخال_قيمة = فئة_إدخال_اسم.getText();
        عامل_قيمة.submit(() -> {
            try {
                Files.createDirectories(الدليل_المشغَّل.resolve("classes"));
                if (실행파일) {
                    أمر(Arrays.asList("jclassc", "--target", "openjdk", "--entry", نقطة_الإدخال_قيمة,
                        "--classpath", مكتبة, "-o", "실행프로그램", إدخال_قيمة));
                } else if (أمر(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", مكتبة,
                        "-d", "classes", إدخال_قيمة)) == 0 && ينفذ_أمر) {
                    أمر(Arrays.asList("java", "-cp", "classes:" + مكتبة, نقطة_الإدخال_قيمة));
                }
            } catch (Exception خطأ) { إشعار(خطأ.toString()); }
        });
    }
    private void 멈춤() {
        Process حديث_عنصر = عملية_قيمة;
        if (حديث_عنصر != null) { حديث_عنصر.descendants().forEach(ProcessHandle::destroy); حديث_عنصر.destroy(); }
    }
    private مساحة_عمل() throws IOException {
        Files.createDirectories(الدليل_المشغَّل);
        Font خط_قيمة = new Font("Monospaced", Font.PLAIN, 16);
        مصدر.setFont(خط_قيمة); مخرجات.setFont(خط_قيمة); مخرجات.setEditable(false);
        مصدر.setTabSize(4);
        مصدر.setMargin(new Insets(10, 12, 10, 12));
        مخرجات.setMargin(new Insets(8, 12, 8, 12));
        مصدر.setBackground(new Color(250, 251, 252));
        مصدر.setForeground(new Color(32, 43, 58));
        JPanel أمر_لوحة = new JPanel();
        أمر_لوحة.add(new JLabel("ملف")); أمر_لوحة.add(ملف_إدخال_اسم);
        أمر_لوحة.add(new JLabel("주 فئة_قيمة_55654bf1")); أمر_لوحة.add(فئة_إدخال_اسم);
        زر(أمر_لوحة, "فتح", this::فتح); زر(أمر_لوحة, "مخزن_قيمة", this::مخزن_قيمة);
        زر(أمر_لوحة, "يحول_برمجياً_مصدر", () -> تحويل_مصدر(false, false));
        زر(أمر_لوحة, "ينفذ_أمر", () -> تحويل_مصدر(true, false));
        زر(أمر_لوحة, "ينفذ_أمر ملف فتح_إدخال", () -> تحويل_مصدر(false, true));
        زر(أمر_لوحة, "멈춤", this::멈춤);
        JSplitPane قسم_مقياس = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(مصدر), new JScrollPane(مخرجات));
        قسم_مقياس.setResizeWeight(0.75);
        نافذة.add(أمر_لوحة, BorderLayout.NORTH); نافذة.add(قسم_مقياس, BorderLayout.CENTER);
        نافذة.setSize(1200, 750); نافذة.setLocationRelativeTo(null);
        نافذة.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        نافذة.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent حدث) { 멈춤(); عامل_قيمة.shutdownNow(); }
        });
        فتح(); نافذة.setVisible(true);
    }
    public static void main(String[] وسائط) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource خط_افتراضي = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object إدخال_قيمة_962f286b : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(إدخال_قيمة_962f286b) instanceof Font) UIManager.put(إدخال_قيمة_962f286b, خط_افتراضي);
                }
                new مساحة_عمل();
            } catch (Exception خطأ) { خطأ.printStackTrace(); }
        });
    }
}
