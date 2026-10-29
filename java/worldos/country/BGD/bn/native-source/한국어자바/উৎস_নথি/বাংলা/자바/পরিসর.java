// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.자바;

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

/** ব্যবহারকারী 홈에서 Java 원문을 সম্পাদন_মান·গঠন_উত্স·실행하는 작은 Swing পরিসর. */
public final class পরিসর {
    private final JFrame উইন্ডো = new JFrame("jkoros — 자바 পরিসর");
    private final JTextArea উৎস_নথি = new JTextArea();
    private final JTextArea নির্গম = new JTextArea(8, 80);
    private final JTextField ফাইল_ভুক্তি_নাম = new JTextField("인사.java", 20);
    private final JTextField শ্রেণী_ভুক্তি_নাম = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process প্রসেসর_মান;
    private final String লাইব্রেরি = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String পাঠ) { SwingUtilities.invokeLater(() -> নির্গম.append(পাঠ + "\n")); }
    private void বোতাম(JPanel সংস্করণ_মান, String নাম, Runnable 행동) {
        JButton বোতাম = new JButton(নাম);
        বোতাম.addActionListener(ঘটনা -> 행동.run());
        সংস্করণ_মান.add(বোতাম);
    }
    private boolean ভাণ্ডার_মান() {
        try {
            Path পথ_2 = 작업폴더.resolve(ফাইল_ভুক্তি_নাম.getText());
            Files.createDirectories(পথ_2.getParent());
            নথির_নাম.লেখা(পথ_2, উৎস_নথি.getText());
            알림("ভাণ্ডার_মান: " + পথ_2);
            return true;
        } catch (Exception ত্রুটি) { 알림(ত্রুটি.toString()); return false; }
    }
    private void খুলুন() {
        try { উৎস_নথি.setText(নথির_নাম.পড়া(작업폴더.resolve(ফাইল_ভুক্তি_নাম.getText()))); }
        catch (Exception ত্রুটি) { 알림(ত্রুটি.toString()); }
    }
    private int আদেশ(List<String> আদেশ) throws Exception {
        প্রসেসর_মান = new ProcessBuilder(আদেশ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader নিবেশের_পঙ্_ক্তি = new BufferedReader(new InputStreamReader(প্রসেসর_মান.getInputStream(), StandardCharsets.UTF_8))) {
            String পাঠ;
            while ((পাঠ = নিবেশের_পঙ্_ক্তি.readLine()) != null) 알림(পাঠ);
        }
        int অবস্হা_মান = প্রসেসর_মান.waitFor(); প্রসেসর_মান = null;
        알림("প্রস্থান_অ্যাপ কোড_মান: " + অবস্হা_মান);
        return অবস্হা_মান;
    }
    private void অনুবাদ_করুন_উত্স(boolean কার্যকর_করুন_আদেশ, boolean 실행파일) {
        if (!ভাণ্ডার_মান()) return;
        String 입력 = ফাইল_ভুক্তি_নাম.getText(), ভুক্তি_বিন্দু_মান = শ্রেণী_ভুক্তি_নাম.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    আদেশ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ভুক্তি_বিন্দু_মান,
                        "--classpath", লাইব্রেরি, "-o", "실행프로그램", 입력));
                } else if (আদেশ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", লাইব্রেরি,
                        "-d", "classes", 입력)) == 0 && কার্যকর_করুন_আদেশ) {
                    আদেশ(Arrays.asList("java", "-cp", "classes:" + লাইব্রেরি, ভুক্তি_বিন্দু_মান));
                }
            } catch (Exception ত্রুটি) { 알림(ত্রুটি.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = প্রসেসর_মান;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private পরিসর() throws IOException {
        Files.createDirectories(작업폴더);
        Font হরফ_মান = new Font("Monospaced", Font.PLAIN, 16);
        উৎস_নথি.setFont(হরফ_মান); নির্গম.setFont(হরফ_মান); নির্গম.setEditable(false);
        উৎস_নথি.setTabSize(4);
        উৎস_নথি.setMargin(new Insets(10, 12, 10, 12));
        নির্গম.setMargin(new Insets(8, 12, 8, 12));
        উৎস_নথি.setBackground(new Color(250, 251, 252));
        উৎস_নথি.setForeground(new Color(32, 43, 58));
        JPanel আদেশ_প্যানেল = new JPanel();
        আদেশ_প্যানেল.add(new JLabel("নথির_নাম")); আদেশ_প্যানেল.add(ফাইল_ভুক্তি_নাম);
        আদেশ_প্যানেল.add(new JLabel("주 শ্রেণী_মান")); আদেশ_প্যানেল.add(শ্রেণী_ভুক্তি_নাম);
        বোতাম(আদেশ_প্যানেল, "খুলুন", this::খুলুন); বোতাম(আদেশ_প্যানেল, "ভাণ্ডার_মান", this::ভাণ্ডার_মান);
        বোতাম(আদেশ_প্যানেল, "গঠন_উত্স", () -> অনুবাদ_করুন_উত্স(false, false));
        বোতাম(আদেশ_প্যানেল, "কার্যকর_করুন_আদেশ", () -> অনুবাদ_করুন_উত্স(true, false));
        বোতাম(আদেশ_প্যানেল, "কার্যকর_করুন_আদেশ নথির_নাম ক্রিয়েট_ভুক্তি", () -> অনুবাদ_করুন_উত্স(false, true));
        বোতাম(আদেশ_প্যানেল, "멈춤", this::멈춤);
        JSplitPane ভাগ_পরিমাপ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(উৎস_নথি), new JScrollPane(নির্গম));
        ভাগ_পরিমাপ.setResizeWeight(0.75);
        উইন্ডো.add(আদেশ_প্যানেল, BorderLayout.NORTH); উইন্ডো.add(ভাগ_পরিমাপ, BorderLayout.CENTER);
        উইন্ডো.setSize(1200, 750); উইন্ডো.setLocationRelativeTo(null);
        উইন্ডো.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        উইন্ডো.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ঘটনা) { 멈춤(); 일꾼.shutdownNow(); }
        });
        খুলুন(); উইন্ডো.setVisible(true);
    }
    public static void main(String[] আর্গুমেন্ট_তালিকা) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource অমনোনীত_হরফ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ভুক্তি_মান : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ভুক্তি_মান) instanceof Font) UIManager.put(ভুক্তি_মান, অমনোনীত_হরফ);
                }
                new পরিসর();
            } catch (Exception ত্রুটি) { ত্রুটি.printStackTrace(); }
        });
    }
}
