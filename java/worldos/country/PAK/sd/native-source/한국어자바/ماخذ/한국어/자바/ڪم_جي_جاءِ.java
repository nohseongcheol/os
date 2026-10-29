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

/** صارف 홈에서 Java 원문을 تدوين_قدر·گڏ_ڪريو_ماخذ·실행하는 작은 Swing ڪم_جي_جاءِ. */
public final class ڪم_جي_جاءِ {
    private final JFrame دري = new JFrame("jkoros — 자바 ڪم_جي_جاءِ");
    private final JTextArea ماخذ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField فائل_داخلا_نالو = new JTextField("인사.java", 20);
    private final JTextField درجو_داخلا_نالو = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process عمل_قدر;
    private final String لائبريري = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String متن) { SwingUtilities.invokeLater(() -> 출력.append(متن + "\n")); }
    private void بٽن(JPanel ورزين_قدر, String نالو, Runnable 행동) {
        JButton بٽن = new JButton(نالو);
        بٽن.addActionListener(واقعو -> 행동.run());
        ورزين_قدر.add(بٽن);
    }
    private boolean روڪيو_قدر() {
        try {
            Path راههه = 작업폴더.resolve(فائل_داخلا_نالو.getText());
            Files.createDirectories(راههه.getParent());
            فائل.لکو(راههه, ماخذ.getText());
            알림("روڪيو_قدر: " + راههه);
            return true;
        } catch (Exception نقص) { 알림(نقص.toString()); return false; }
    }
    private void ٺاھيو() {
        try { ماخذ.setText(فائل.읽기(작업폴더.resolve(فائل_داخلا_نالو.getText()))); }
        catch (Exception نقص) { 알림(نقص.toString()); }
    }
    private int حڪم(List<String> حڪم) throws Exception {
        عمل_قدر = new ProcessBuilder(حڪم).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader لڪير = new BufferedReader(new InputStreamReader(عمل_قدر.getInputStream(), StandardCharsets.UTF_8))) {
            String متن;
            while ((متن = لڪير.readLine()) != null) 알림(متن);
        }
        int حالت_قدر = عمل_قدر.waitFor(); عمل_قدر = null;
        알림("خارج_ڪريو_ائپ 코드: " + حالت_قدر);
        return حالت_قدر;
    }
    private void ترجمو_ماخذ(boolean تعميل_ڪرڻ_حڪم, boolean 실행파일) {
        if (!روڪيو_قدر()) return;
        String 입력 = فائل_داخلا_نالو.getText(), داخلا_هنڌ_قدر = درجو_داخلا_نالو.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    حڪم(Arrays.asList("jclassc", "--target", "openjdk", "--entry", داخلا_هنڌ_قدر,
                        "--classpath", لائبريري, "-o", "실행프로그램", 입력));
                } else if (حڪم(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", لائبريري,
                        "-d", "classes", 입력)) == 0 && تعميل_ڪرڻ_حڪم) {
                    حڪم(Arrays.asList("java", "-cp", "classes:" + لائبريري, داخلا_هنڌ_قدر));
                }
            } catch (Exception نقص) { 알림(نقص.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = عمل_قدر;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ڪم_جي_جاءِ() throws IOException {
        Files.createDirectories(작업폴더);
        Font فانٽ_قدر = new Font("Monospaced", Font.PLAIN, 16);
        ماخذ.setFont(فانٽ_قدر); 출력.setFont(فانٽ_قدر); 출력.setEditable(false);
        ماخذ.setTabSize(4);
        ماخذ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ماخذ.setBackground(new Color(250, 251, 252));
        ماخذ.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("فائل")); 명령판.add(فائل_داخلا_نالو);
        명령판.add(new JLabel("주 درجو_قدر")); 명령판.add(درجو_داخلا_نالو);
        بٽن(명령판, "ٺاھيو", this::ٺاھيو); بٽن(명령판, "روڪيو_قدر", this::روڪيو_قدر);
        بٽن(명령판, "گڏ_ڪريو_ماخذ", () -> ترجمو_ماخذ(false, false));
        بٽن(명령판, "تعميل_ڪرڻ_حڪم", () -> ترجمو_ماخذ(true, false));
        بٽن(명령판, "تعميل_ڪرڻ_حڪم فائل ٺاھيو_داخلا", () -> ترجمو_ماخذ(false, true));
        بٽن(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ماخذ), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        دري.add(명령판, BorderLayout.NORTH); دري.add(나눔, BorderLayout.CENTER);
        دري.setSize(1200, 750); دري.setLocationRelativeTo(null);
        دري.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        دري.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent واقعو) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ٺاھيو(); دري.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ڊفالٽ_فونٽ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object داخلا_قدر : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(داخلا_قدر) instanceof Font) UIManager.put(داخلا_قدر, ڊفالٽ_فونٽ);
                }
                new ڪم_جي_جاءِ();
            } catch (Exception نقص) { نقص.printStackTrace(); }
        });
    }
}
