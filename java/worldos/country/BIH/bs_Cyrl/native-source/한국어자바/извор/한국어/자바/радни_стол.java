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

/** корисник 홈에서 Java 원문을 уређивати_вриједност·направити_извор·실행하는 작은 Swing радни_стол. */
public final class радни_стол {
    private final JFrame прозор = new JFrame("jkoros — 자바 радни_стол");
    private final JTextArea извор = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField фајл_унос_назив = new JTextField("인사.java", 20);
    private final JTextField класа_унос_назив = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process процес_вриједност;
    private final String библиотека = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String текст) { SwingUtilities.invokeLater(() -> 출력.append(текст + "\n")); }
    private void дугме(JPanel верзија_вриједност, String назив, Runnable 행동) {
        JButton дугме = new JButton(назив);
        дугме.addActionListener(догађај -> 행동.run());
        верзија_вриједност.add(дугме);
    }
    private boolean похранити_вриједност() {
        try {
            Path пут = 작업폴더.resolve(фајл_унос_назив.getText());
            Files.createDirectories(пут.getParent());
            фајл.писати(пут, извор.getText());
            알림("похранити_вриједност: " + пут);
            return true;
        } catch (Exception грешка) { 알림(грешка.toString()); return false; }
    }
    private void отворити() {
        try { извор.setText(фајл.읽기(작업폴더.resolve(фајл_унос_назив.getText()))); }
        catch (Exception грешка) { 알림(грешка.toString()); }
    }
    private int команда(List<String> команда) throws Exception {
        процес_вриједност = new ProcessBuilder(команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader редак = new BufferedReader(new InputStreamReader(процес_вриједност.getInputStream(), StandardCharsets.UTF_8))) {
            String текст;
            while ((текст = редак.readLine()) != null) 알림(текст);
        }
        int стање_вриједност = процес_вриједност.waitFor(); процес_вриједност = null;
        알림("изаћи_програм 코드: " + стање_вриједност);
        return стање_вриједност;
    }
    private void 번역(boolean 실행, boolean 실행파일) {
        if (!похранити_вриједност()) return;
        String 입력 = фајл_унос_назив.getText(), унос_тачка_вриједност = класа_унос_назив.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", унос_тачка_вриједност,
                        "--classpath", библиотека, "-o", "실행프로그램", 입력));
                } else if (команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", библиотека,
                        "-d", "classes", 입력)) == 0 && 실행) {
                    команда(Arrays.asList("java", "-cp", "classes:" + библиотека, унос_тачка_вриједност));
                }
            } catch (Exception грешка) { 알림(грешка.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = процес_вриједност;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private радни_стол() throws IOException {
        Files.createDirectories(작업폴더);
        Font фонт_вриједност = new Font("Monospaced", Font.PLAIN, 16);
        извор.setFont(фонт_вриједност); 출력.setFont(фонт_вриједност); 출력.setEditable(false);
        извор.setTabSize(4);
        извор.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        извор.setBackground(new Color(250, 251, 252));
        извор.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("фајл")); 명령판.add(фајл_унос_назив);
        명령판.add(new JLabel("주 класа_вриједност")); 명령판.add(класа_унос_назив);
        дугме(명령판, "отворити", this::отворити); дугме(명령판, "похранити_вриједност", this::похранити_вриједност);
        дугме(명령판, "направити_извор", () -> 번역(false, false));
        дугме(명령판, "실행", () -> 번역(true, false));
        дугме(명령판, "실행 фајл 만들기", () -> 번역(false, true));
        дугме(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(извор), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        прозор.add(명령판, BorderLayout.NORTH); прозор.add(나눔, BorderLayout.CENTER);
        прозор.setSize(1200, 750); прозор.setLocationRelativeTo(null);
        прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        прозор.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent догађај) { 멈춤(); 일꾼.shutdownNow(); }
        });
        отворити(); прозор.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource стандардни_фонт = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object унос_вриједност : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(унос_вриједност) instanceof Font) UIManager.put(унос_вриједност, стандардни_фонт);
                }
                new радни_стол();
            } catch (Exception грешка) { грешка.printStackTrace(); }
        });
    }
}
