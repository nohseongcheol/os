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

/** بەکارهێنەر 홈에서 Java 원문을 بژار_نرخ·دروست_کردن_ژێدەر·실행하는 작은 Swing شوێنکار. */
public final class شوێنکار {
    private final JFrame پەنجەرە = new JFrame("jkoros — 자바 شوێنکار");
    private final JTextArea ژێدەر = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField فایل_تێنووسین_ناو = new JTextField("인사.java", 20);
    private final JTextField کلاس_تێنووسین_ناو = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process پرۆسە_نرخ;
    private final String کتێبخانە = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String دەق) { SwingUtilities.invokeLater(() -> 출력.append(دەق + "\n")); }
    private void دوگمه(JPanel وەشان_نرخ, String ناو, Runnable 행동) {
        JButton دوگمه = new JButton(ناو);
        دوگمه.addActionListener(پێشهات -> 행동.run());
        وەشان_نرخ.add(دوگمه);
    }
    private boolean Store_نرخ() {
        try {
            Path گوزەر = 작업폴더.resolve(فایل_تێنووسین_ناو.getText());
            Files.createDirectories(گوزەر.getParent());
            فایل.ڕایت_کردن(گوزەر, ژێدەر.getText());
            알림("Store_نرخ: " + گوزەر);
            return true;
        } catch (Exception هەڵە) { 알림(هەڵە.toString()); return false; }
    }
    private void کردنەوە() {
        try { ژێدەر.setText(فایل.읽기(작업폴더.resolve(فایل_تێنووسین_ناو.getText()))); }
        catch (Exception هەڵە) { 알림(هەڵە.toString()); }
    }
    private int فەرمان(List<String> فەرمان) throws Exception {
        پرۆسە_نرخ = new ProcessBuilder(فەرمان).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader دێڕ = new BufferedReader(new InputStreamReader(پرۆسە_نرخ.getInputStream(), StandardCharsets.UTF_8))) {
            String دەق;
            while ((دەق = دێڕ.readLine()) != null) 알림(دەق);
        }
        int دۆخ_نرخ = پرۆسە_نرخ.waitFor(); پرۆسە_نرخ = null;
        알림("بزربوون_بەرنامە 코드: " + دۆخ_نرخ);
        return دۆخ_نرخ;
    }
    private void وەرگێڕان_ژێدەر(boolean جێبەجێکردن_فەرمان, boolean 실행파일) {
        if (!Store_نرخ()) return;
        String 입력 = فایل_تێنووسین_ناو.getText(), تێنووسین_خاڵ_نرخ = کلاس_تێنووسین_ناو.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    فەرمان(Arrays.asList("jclassc", "--target", "openjdk", "--entry", تێنووسین_خاڵ_نرخ,
                        "--classpath", کتێبخانە, "-o", "실행프로그램", 입력));
                } else if (فەرمان(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", کتێبخانە,
                        "-d", "classes", 입력)) == 0 && جێبەجێکردن_فەرمان) {
                    فەرمان(Arrays.asList("java", "-cp", "classes:" + کتێبخانە, تێنووسین_خاڵ_نرخ));
                }
            } catch (Exception هەڵە) { 알림(هەڵە.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = پرۆسە_نرخ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private شوێنکار() throws IOException {
        Files.createDirectories(작업폴더);
        Font جۆرەپیت_نرخ = new Font("Monospaced", Font.PLAIN, 16);
        ژێدەر.setFont(جۆرەپیت_نرخ); 출력.setFont(جۆرەپیت_نرخ); 출력.setEditable(false);
        ژێدەر.setTabSize(4);
        ژێدەر.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ژێدەر.setBackground(new Color(250, 251, 252));
        ژێدەر.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("فایل")); 명령판.add(فایل_تێنووسین_ناو);
        명령판.add(new JLabel("주 کلاس_نرخ")); 명령판.add(کلاس_تێنووسین_ناو);
        دوگمه(명령판, "کردنەوە", this::کردنەوە); دوگمه(명령판, "Store_نرخ", this::Store_نرخ);
        دوگمه(명령판, "دروست_کردن_ژێدەر", () -> وەرگێڕان_ژێدەر(false, false));
        دوگمه(명령판, "جێبەجێکردن_فەرمان", () -> وەرگێڕان_ژێدەر(true, false));
        دوگمه(명령판, "جێبەجێکردن_فەرمان فایل دروستکردن_تێنووسین", () -> وەرگێڕان_ژێدەر(false, true));
        دوگمه(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ژێدەر), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        پەنجەرە.add(명령판, BorderLayout.NORTH); پەنجەرە.add(나눔, BorderLayout.CENTER);
        پەنجەرە.setSize(1200, 750); پەنجەرە.setLocationRelativeTo(null);
        پەنجەرە.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        پەنجەرە.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent پێشهات) { 멈춤(); 일꾼.shutdownNow(); }
        });
        کردنەوە(); پەنجەرە.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource دەستوخەتی_سەرەکیی = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object تێنووسین_نرخ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(تێنووسین_نرخ) instanceof Font) UIManager.put(تێنووسین_نرخ, دەستوخەتی_سەرەکیی);
                }
                new شوێنکار();
            } catch (Exception هەڵە) { هەڵە.printStackTrace(); }
        });
    }
}
