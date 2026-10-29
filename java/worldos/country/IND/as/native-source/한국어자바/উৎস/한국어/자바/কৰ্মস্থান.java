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

/** ব্যৱহাৰকৰ্তা 홈에서 Java 원문을 সম্পাদনা_মান·বিল্ড_উৎস·실행하는 작은 Swing কৰ্মস্থান. */
public final class কৰ্মস্থান {
    private final JFrame উইণ্ড = new JFrame("jkoros — 자바 কৰ্মস্থান");
    private final JTextArea উৎস = new JTextArea();
    private final JTextArea নিৰ্গম = new JTextArea(8, 80);
    private final JTextField ফাইল_প্রবিষ্ট_নাম = new JTextField("인사.java", 20);
    private final JTextField শ্ৰেণী_প্রবিষ্ট_নাম = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process প্ৰক্ৰিয়া_মান;
    private final String লাইব্ৰেৰী = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String টেক্সট) { SwingUtilities.invokeLater(() -> নিৰ্গম.append(টেক্সট + "\n")); }
    private void বুটাম(JPanel সংস্কৰণ_মান, String নাম, Runnable 행동) {
        JButton বুটাম = new JButton(নাম);
        বুটাম.addActionListener(ইভেণ্ট -> 행동.run());
        সংস্কৰণ_মান.add(বুটাম);
    }
    private boolean জমা_কৰক_মান() {
        try {
            Path পথ = 작업폴더.resolve(ফাইল_প্রবিষ্ট_নাম.getText());
            Files.createDirectories(পথ.getParent());
            নথিপত্ৰ.লিখা(পথ, উৎস.getText());
            알림("জমা_কৰক_মান: " + পথ);
            return true;
        } catch (Exception ত্ৰুটি) { 알림(ত্ৰুটি.toString()); return false; }
    }
    private void খোলো() {
        try { উৎস.setText(নথিপত্ৰ.পড়া(작업폴더.resolve(ফাইল_প্রবিষ্ট_নাম.getText()))); }
        catch (Exception ত্ৰুটি) { 알림(ত্ৰুটি.toString()); }
    }
    private int কমান্ড(List<String> কমান্ড) throws Exception {
        প্ৰক্ৰিয়া_মান = new ProcessBuilder(কমান্ড).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader লাইন = new BufferedReader(new InputStreamReader(প্ৰক্ৰিয়া_মান.getInputStream(), StandardCharsets.UTF_8))) {
            String টেক্সট;
            while ((টেক্সট = লাইন.readLine()) != null) 알림(টেক্সট);
        }
        int অৱস্থা_মান = প্ৰক্ৰিয়া_মান.waitFor(); প্ৰক্ৰিয়া_মান = null;
        알림("প্ৰস্থান_এপ্প্ 코드: " + অৱস্থা_মান);
        return অৱস্থা_মান;
    }
    private void অনুবাদ_উৎস(boolean নিষ্পাদন_আদেশ, boolean 실행파일) {
        if (!জমা_কৰক_মান()) return;
        String 입력 = ফাইল_প্রবিষ্ট_নাম.getText(), প্রবিষ্ট_পইণ্ট_মান = শ্ৰেণী_প্রবিষ্ট_নাম.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    কমান্ড(Arrays.asList("jclassc", "--target", "openjdk", "--entry", প্রবিষ্ট_পইণ্ট_মান,
                        "--classpath", লাইব্ৰেৰী, "-o", "실행프로그램", 입력));
                } else if (কমান্ড(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", লাইব্ৰেৰী,
                        "-d", "classes", 입력)) == 0 && নিষ্পাদন_আদেশ) {
                    কমান্ড(Arrays.asList("java", "-cp", "classes:" + লাইব্ৰেৰী, প্রবিষ্ট_পইণ্ট_মান));
                }
            } catch (Exception ত্ৰুটি) { 알림(ত্ৰুটি.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = প্ৰক্ৰিয়া_মান;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private কৰ্মস্থান() throws IOException {
        Files.createDirectories(작업폴더);
        Font ফ_ন্ট_মান = new Font("Monospaced", Font.PLAIN, 16);
        উৎস.setFont(ফ_ন্ট_মান); নিৰ্গম.setFont(ফ_ন্ট_মান); নিৰ্গম.setEditable(false);
        উৎস.setTabSize(4);
        উৎস.setMargin(new Insets(10, 12, 10, 12));
        নিৰ্গম.setMargin(new Insets(8, 12, 8, 12));
        উৎস.setBackground(new Color(250, 251, 252));
        উৎস.setForeground(new Color(32, 43, 58));
        JPanel আদেশ_পেনেল = new JPanel();
        আদেশ_পেনেল.add(new JLabel("নথিপত্ৰ")); আদেশ_পেনেল.add(ফাইল_প্রবিষ্ট_নাম);
        আদেশ_পেনেল.add(new JLabel("주 শ্ৰেণী_মান")); আদেশ_পেনেল.add(শ্ৰেণী_প্রবিষ্ট_নাম);
        বুটাম(আদেশ_পেনেল, "খোলো", this::খোলো); বুটাম(আদেশ_পেনেল, "জমা_কৰক_মান", this::জমা_কৰক_মান);
        বুটাম(আদেশ_পেনেল, "বিল্ড_উৎস", () -> অনুবাদ_উৎস(false, false));
        বুটাম(আদেশ_পেনেল, "নিষ্পাদন_আদেশ", () -> অনুবাদ_উৎস(true, false));
        বুটাম(আদেশ_পেনেল, "নিষ্পাদন_আদেশ নথিপত্ৰ ক্ৰিয়েট_প্রবিষ্ট", () -> অনুবাদ_উৎস(false, true));
        বুটাম(আদেশ_পেনেল, "멈춤", this::멈춤);
        JSplitPane হৰণ_পৰিমাপ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(উৎস), new JScrollPane(নিৰ্গম));
        হৰণ_পৰিমাপ.setResizeWeight(0.75);
        উইণ্ড.add(আদেশ_পেনেল, BorderLayout.NORTH); উইণ্ড.add(হৰণ_পৰিমাপ, BorderLayout.CENTER);
        উইণ্ড.setSize(1200, 750); উইণ্ড.setLocationRelativeTo(null);
        উইণ্ড.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        উইণ্ড.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ইভেণ্ট) { 멈춤(); 일꾼.shutdownNow(); }
        });
        খোলো(); উইণ্ড.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ডিফল্ট_ফ_ণ্ট = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object প্রবিষ্ট_মান : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(প্রবিষ্ট_মান) instanceof Font) UIManager.put(প্রবিষ্ট_মান, ডিফল্ট_ফ_ণ্ট);
                }
                new কৰ্মস্থান();
            } catch (Exception ত্ৰুটি) { ত্ৰুটি.printStackTrace(); }
        });
    }
}
