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

/** 사용자 홈에서 Java 원문을 편집·컴파일·실행하는 작은 Swing 작업마당. */
public final class 작업마당 {
    private final JFrame 창 = new JFrame("jkoros — 자바 작업마당");
    private final JTextArea 원문 = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField 파일이름 = new JTextField("인사.java", 20);
    private final JTextField 클래스이름 = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process 과정;
    private final String 라이브러리 = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String 글) { SwingUtilities.invokeLater(() -> 출력.append(글 + "\n")); }
    private void 단추(JPanel 판, String मुं, Runnable 행동) {
        JButton 단추 = new JButton(मुं);
        단추.addActionListener(사건 -> 행동.run());
        판.add(단추);
    }
    private boolean 저장() {
        try {
            Path 경로 = 작업폴더.resolve(파일이름.getText());
            Files.createDirectories(경로.getParent());
            파일.쓰기(경로, 원문.getText());
            알림("저장: " + 경로);
            return true;
        } catch (Exception 오류) { 알림(오류.toString()); return false; }
    }
    private void 열기() {
        try { 원문.setText(파일.읽기(작업폴더.resolve(파일이름.getText()))); }
        catch (Exception 오류) { 알림(오류.toString()); }
    }
    private int 명령(List<String> 명령) throws Exception {
        과정 = new ProcessBuilder(명령).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 줄 = new BufferedReader(new InputStreamReader(과정.getInputStream(), StandardCharsets.UTF_8))) {
            String 글;
            while ((글 = 줄.readLine()) != null) 알림(글);
        }
        int 상태 = 과정.waitFor(); 과정 = null;
        알림("종료 코드: " + 상태);
        return 상태;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!저장()) return;
        String 입력 = 파일이름.getText(), 진입 = 클래스이름.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    명령(Arrays.asList("jclassc", "--target", "openjdk", "--entry", 진입,
                        "--classpath", 라이브러리, "-o", "실행프로그램", 입력));
                } else if (명령(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", 라이브러리,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    명령(Arrays.asList("java", "-cp", "classes:" + 라이브러리, 진입));
                }
            } catch (Exception 오류) { 알림(오류.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = 과정;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private 작업마당() throws IOException {
        Files.createDirectories(작업폴더);
        Font 글꼴 = new Font("Monospaced", Font.PLAIN, 16);
        원문.setFont(글꼴); 출력.setFont(글꼴); 출력.setEditable(false);
        원문.setTabSize(4);
        원문.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        원문.setBackground(new Color(250, 251, 252));
        원문.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("파일")); 명령판.add(파일이름);
        명령판.add(new JLabel("주 클래스")); 명령판.add(클래스이름);
        단추(명령판, "열기", this::열기); 단추(명령판, "저장", this::저장);
        단추(명령판, "컴파일", () -> 번역(false, false));
        단추(명령판, "실행", () -> 번역(true, false));
        단추(명령판, "실행 파일 만들기", () -> 번역(false, true));
        단추(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(원문), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        창.add(명령판, BorderLayout.NORTH); 창.add(나눔, BorderLayout.CENTER);
        창.setSize(1200, 750); 창.setLocationRelativeTo(null);
        창.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        창.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent 사건) { 멈춤(); 일꾼.shutdownNow(); }
        });
        열기(); 창.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource 기본글꼴 = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object 항목 : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(항목) instanceof Font) UIManager.put(항목, 기본글꼴);
                }
                new 작업마당();
            } catch (Exception 오류) { 오류.printStackTrace(); }
        });
    }
}
