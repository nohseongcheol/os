// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자바;

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

/** кулланучы 홈에서 Java 원문을 төзәтү_VALUE·төзү_чыганак·실행하는 작은 Swing эш_өлкәсе. */
public final class эш_өлкәсе {
    private final JFrame тәрәз = new JFrame("jkoros — 자바 эш_өлкәсе");
    private final JTextArea чыганак = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField файл_кертү_исем = new JTextField("인사.java", 20);
    private final JTextField класс_кертү_исем = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Процесс_VALUE;
    private final String библиотека = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Mäten) { SwingUtilities.invokeLater(() -> 출력.append(Mäten + "\n")); }
    private void төймә(JPanel версия_VALUE, String исем, Runnable 행동) {
        JButton төймә = new JButton(исем);
        төймә.addActionListener(вакыйга -> 행동.run());
        версия_VALUE.add(төймә);
    }
    private boolean Store_VALUE() {
        try {
            Path Yul = 작업폴더.resolve(файл_кертү_исем.getText());
            Files.createDirectories(Yul.getParent());
            Birem.язу(Yul, чыганак.getText());
            알림("Store_VALUE: " + Yul);
            return true;
        } catch (Exception Хата) { 알림(Хата.toString()); return false; }
    }
    private void ачу() {
        try { чыганак.setText(Birem.읽기(작업폴더.resolve(файл_кертү_исем.getText()))); }
        catch (Exception Хата) { 알림(Хата.toString()); }
    }
    private int команда(List<String> команда) throws Exception {
        Процесс_VALUE = new ProcessBuilder(команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader юл = new BufferedReader(new InputStreamReader(Процесс_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Mäten;
            while ((Mäten = юл.readLine()) != null) 알림(Mäten);
        }
        int халәт_VALUE = Процесс_VALUE.waitFor(); Процесс_VALUE = null;
        알림("Чыгу_кушымта CODE_VALUE: " + халәт_VALUE);
        return халәт_VALUE;
    }
    private void TRANSLATE_чыганак(boolean үтәргә_команда, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = файл_кертү_исем.getText(), кертү_балл_VALUE = класс_кертү_исем.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", кертү_балл_VALUE,
                        "--classpath", библиотека, "-o", "실행프로그램", 입력));
                } else if (команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", библиотека,
                        "-d", "classes", 입력)) == 0 && үтәргә_команда) {
                    команда(Arrays.asList("java", "-cp", "classes:" + библиотека, кертү_балл_VALUE));
                }
            } catch (Exception Хата) { 알림(Хата.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Процесс_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private эш_өлкәсе() throws IOException {
        Files.createDirectories(작업폴더);
        Font шрифт_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        чыганак.setFont(шрифт_VALUE); 출력.setFont(шрифт_VALUE); 출력.setEditable(false);
        чыганак.setTabSize(4);
        чыганак.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        чыганак.setBackground(new Color(250, 251, 252));
        чыганак.setForeground(new Color(32, 43, 58));
        JPanel команда_панель = new JPanel();
        команда_панель.add(new JLabel("Birem")); команда_панель.add(файл_кертү_исем);
        команда_панель.add(new JLabel("주 класс_VALUE")); команда_панель.add(класс_кертү_исем);
        төймә(команда_панель, "ачу", this::ачу); төймә(команда_панель, "Store_VALUE", this::Store_VALUE);
        төймә(команда_панель, "төзү_чыганак", () -> TRANSLATE_чыганак(false, false));
        төймә(команда_панель, "үтәргә_команда", () -> TRANSLATE_чыганак(true, false));
        төймә(команда_панель, "үтәргә_команда Birem Төзү_кертү", () -> TRANSLATE_чыганак(false, true));
        төймә(команда_панель, "멈춤", this::멈춤);
        JSplitPane бүлү_үлчәм = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(чыганак), new JScrollPane(출력));
        бүлү_үлчәм.setResizeWeight(0.75);
        тәрәз.add(команда_панель, BorderLayout.NORTH); тәрәз.add(бүлү_үлчәм, BorderLayout.CENTER);
        тәрәз.setSize(1200, 750); тәрәз.setLocationRelativeTo(null);
        тәрәз.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        тәрәз.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent вакыйга) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ачу(); тәрәз.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource килешенгән_шрифт = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object кертү_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(кертү_VALUE) instanceof Font) UIManager.put(кертү_VALUE, килешенгән_шрифт);
                }
                new эш_өлкәсе();
            } catch (Exception Хата) { Хата.printStackTrace(); }
        });
    }
}
