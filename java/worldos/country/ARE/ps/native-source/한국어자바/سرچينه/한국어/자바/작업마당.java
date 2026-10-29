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

/** کارن 홈에서 Java 원문을 سمون_ارزښت·جوړول_سرچینه·실행하는 작은 Swing 작업마당. */
public final class 작업마당 {
    private final JFrame کړکۍ = new JFrame("jkoros — 자바 작업마당");
    private final JTextArea سرچينه = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField 파일이름 = new JTextField("인사.java", 20);
    private final JTextField 클래스이름 = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process 과정;
    private final String کتابتون = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ليکنه) { SwingUtilities.invokeLater(() -> 출력.append(ليکنه + "\n")); }
    private void تڼۍ(JPanel 판, String نوم, Runnable 행동) {
        JButton تڼۍ = new JButton(نوم);
        تڼۍ.addActionListener(پېښه -> 행동.run());
        판.add(تڼۍ);
    }
    private boolean 저장() {
        try {
            Path يونلور = 작업폴더.resolve(파일이름.getText());
            Files.createDirectories(يونلور.getParent());
            دوتنه.لوستل_2(يونلور, سرچينه.getText());
            알림("저장: " + يونلور);
            return true;
        } catch (Exception تېروتنه) { 알림(تېروتنه.toString()); return false; }
    }
    private void پرانيستل() {
        try { سرچينه.setText(دوتنه.لوستل(작업폴더.resolve(파일이름.getText()))); }
        catch (Exception تېروتنه) { 알림(تېروتنه.toString()); }
    }
    private int بولۍ(List<String> بولۍ) throws Exception {
        과정 = new ProcessBuilder(بولۍ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ليکه = new BufferedReader(new InputStreamReader(과정.getInputStream(), StandardCharsets.UTF_8))) {
            String ليکنه;
            while ((ليکنه = ليکه.readLine()) != null) 알림(ليکنه);
        }
        int انکړ_ارزښت = 과정.waitFor(); 과정 = null;
        알림("وتون_کاريال 코드: " + انکړ_ارزښت);
        return انکړ_ارزښت;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!저장()) return;
        String 입력 = 파일이름.getText(), ننوت_ټکى_ارزښت = 클래스이름.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    بولۍ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ننوت_ټکى_ارزښت,
                        "--classpath", کتابتون, "-o", "실행프로그램", 입력));
                } else if (بولۍ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", کتابتون,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    بولۍ(Arrays.asList("java", "-cp", "classes:" + کتابتون, ننوت_ټکى_ارزښت));
                }
            } catch (Exception تېروتنه) { 알림(تېروتنه.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = 과정;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private 작업마당() throws IOException {
        Files.createDirectories(작업폴더);
        Font ليکبڼه_ارزښت = new Font("Monospaced", Font.PLAIN, 16);
        سرچينه.setFont(ليکبڼه_ارزښت); 출력.setFont(ليکبڼه_ارزښت); 출력.setEditable(false);
        سرچينه.setTabSize(4);
        سرچينه.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        سرچينه.setBackground(new Color(250, 251, 252));
        سرچينه.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("دوتنه")); 명령판.add(파일이름);
        명령판.add(new JLabel("주 پاړکى_ارزښت")); 명령판.add(클래스이름);
        تڼۍ(명령판, "پرانيستل", this::پرانيستل); تڼۍ(명령판, "저장", this::저장);
        تڼۍ(명령판, "جوړول_سرچینه", () -> 번역(false, false));
        تڼۍ(명령판, "실행", () -> 번역(true, false));
        تڼۍ(명령판, "실행 دوتنه 만들기", () -> 번역(false, true));
        تڼۍ(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(سرچينه), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        کړکۍ.add(명령판, BorderLayout.NORTH); کړکۍ.add(나눔, BorderLayout.CENTER);
        کړکۍ.setSize(1200, 750); کړکۍ.setLocationRelativeTo(null);
        کړکۍ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        کړکۍ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent پېښه) { 멈춤(); 일꾼.shutdownNow(); }
        });
        پرانيستل(); کړکۍ.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource تلواله_ليکبڼه = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ننوت_ارزښت : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ننوت_ارزښت) instanceof Font) UIManager.put(ننوت_ارزښت, تلواله_ليکبڼه);
                }
                new 작업마당();
            } catch (Exception تېروتنه) { تېروتنه.printStackTrace(); }
        });
    }
}
