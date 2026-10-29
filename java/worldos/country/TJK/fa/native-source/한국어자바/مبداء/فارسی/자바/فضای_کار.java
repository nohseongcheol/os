// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.자바;

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

/** کاربر 홈에서 Java 원문을 ویرایش_مقدار·ساختن_منبع·실행하는 작은 Swing فضای_کار. */
public final class فضای_کار {
    private final JFrame پنجره = new JFrame("jkoros — 자바 فضای_کار");
    private final JTextArea مبداء = new JTextArea();
    private final JTextArea خروجی = new JTextArea(8, 80);
    private final JTextField فایل_ورودی_نام = new JTextField("인사.java", 20);
    private final JTextField کلاس_ورودی_نام = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process فرآیند_مقدار;
    private final String کتابخانه = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String متن) { SwingUtilities.invokeLater(() -> خروجی.append(متن + "\n")); }
    private void دکمه(JPanel نسخه_مقدار, String نام, Runnable 행동) {
        JButton دکمه = new JButton(نام);
        دکمه.addActionListener(رویداد -> 행동.run());
        نسخه_مقدار.add(دکمه);
    }
    private boolean ذخیره_مقدار() {
        try {
            Path مسیر = 작업폴더.resolve(فایل_ورودی_نام.getText());
            Files.createDirectories(مسیر.getParent());
            پرونده.نوشتن(مسیر, مبداء.getText());
            알림("ذخیره_مقدار: " + مسیر);
            return true;
        } catch (Exception خطا) { 알림(خطا.toString()); return false; }
    }
    private void باز_کردن() {
        try { مبداء.setText(پرونده.خواندن(작업폴더.resolve(فایل_ورودی_نام.getText()))); }
        catch (Exception خطا) { 알림(خطا.toString()); }
    }
    private int فرمان(List<String> فرمان) throws Exception {
        فرآیند_مقدار = new ProcessBuilder(فرمان).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader خط = new BufferedReader(new InputStreamReader(فرآیند_مقدار.getInputStream(), StandardCharsets.UTF_8))) {
            String متن;
            while ((متن = خط.readLine()) != null) 알림(متن);
        }
        int وضعیت_مقدار = فرآیند_مقدار.waitFor(); فرآیند_مقدار = null;
        알림("خروج_برنامه کد_مقدار: " + وضعیت_مقدار);
        return وضعیت_مقدار;
    }
    private void تبدیل_منبع(boolean اجرا_فرمان, boolean 실행파일) {
        if (!ذخیره_مقدار()) return;
        String 입력 = فایل_ورودی_نام.getText(), ورودی_نقطه_مقدار = کلاس_ورودی_نام.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    فرمان(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ورودی_نقطه_مقدار,
                        "--classpath", کتابخانه, "-o", "실행프로그램", 입력));
                } else if (فرمان(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", کتابخانه,
                        "-d", "classes", 입력)) == 0 && اجرا_فرمان) {
                    فرمان(Arrays.asList("java", "-cp", "classes:" + کتابخانه, ورودی_نقطه_مقدار));
                }
            } catch (Exception خطا) { 알림(خطا.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = فرآیند_مقدار;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private فضای_کار() throws IOException {
        Files.createDirectories(작업폴더);
        Font قلم_مقدار = new Font("Monospaced", Font.PLAIN, 16);
        مبداء.setFont(قلم_مقدار); خروجی.setFont(قلم_مقدار); خروجی.setEditable(false);
        مبداء.setTabSize(4);
        مبداء.setMargin(new Insets(10, 12, 10, 12));
        خروجی.setMargin(new Insets(8, 12, 8, 12));
        مبداء.setBackground(new Color(250, 251, 252));
        مبداء.setForeground(new Color(32, 43, 58));
        JPanel فرمان_پنجره = new JPanel();
        فرمان_پنجره.add(new JLabel("پرونده")); فرمان_پنجره.add(فایل_ورودی_نام);
        فرمان_پنجره.add(new JLabel("주 کلاس_مقدار")); فرمان_پنجره.add(کلاس_ورودی_نام);
        دکمه(فرمان_پنجره, "باز_کردن", this::باز_کردن); دکمه(فرمان_پنجره, "ذخیره_مقدار", this::ذخیره_مقدار);
        دکمه(فرمان_پنجره, "ساختن_منبع", () -> تبدیل_منبع(false, false));
        دکمه(فرمان_پنجره, "اجرا_فرمان", () -> تبدیل_منبع(true, false));
        دکمه(فرمان_پنجره, "اجرا_فرمان پرونده ایجاد_ورودی", () -> تبدیل_منبع(false, true));
        دکمه(فرمان_پنجره, "멈춤", this::멈춤);
        JSplitPane تقسیم_سنجش = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(مبداء), new JScrollPane(خروجی));
        تقسیم_سنجش.setResizeWeight(0.75);
        پنجره.add(فرمان_پنجره, BorderLayout.NORTH); پنجره.add(تقسیم_سنجش, BorderLayout.CENTER);
        پنجره.setSize(1200, 750); پنجره.setLocationRelativeTo(null);
        پنجره.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        پنجره.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent رویداد) { 멈춤(); 일꾼.shutdownNow(); }
        });
        باز_کردن(); پنجره.setVisible(true);
    }
    public static void main(String[] نشانوندها) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource قلم_پیش_فرض = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ورودی_مقدار : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ورودی_مقدار) instanceof Font) UIManager.put(ورودی_مقدار, قلم_پیش_فرض);
                }
                new فضای_کار();
            } catch (Exception خطا) { خطا.printStackTrace(); }
        });
    }
}
