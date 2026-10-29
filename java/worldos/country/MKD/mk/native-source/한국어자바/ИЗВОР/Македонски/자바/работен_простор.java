// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자바;

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

/** корисник 홈에서 Java 원문을 уреди_VALUE·изгради_извор·실행하는 작은 Swing работен_простор. */
public final class работен_простор {
    private final JFrame прозорец = new JFrame("jkoros — 자바 работен_простор");
    private final JTextArea ИЗВОР = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField датотека_внес_име = new JTextField("인사.java", 20);
    private final JTextField класа_внес_име = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Процес_VALUE;
    private final String библиотека = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Текст) { SwingUtilities.invokeLater(() -> 출력.append(Текст + "\n")); }
    private void копче(JPanel верзија_VALUE, String Име, Runnable 행동) {
        JButton копче = new JButton(Име);
        копче.addActionListener(настан -> 행동.run());
        верзија_VALUE.add(копче);
    }
    private boolean Store_VALUE() {
        try {
            Path ПАТЕКА = 작업폴더.resolve(датотека_внес_име.getText());
            Files.createDirectories(ПАТЕКА.getParent());
            Датотека.Запиши(ПАТЕКА, ИЗВОР.getText());
            알림("Store_VALUE: " + ПАТЕКА);
            return true;
        } catch (Exception ГРЕШКА) { 알림(ГРЕШКА.toString()); return false; }
    }
    private void Отвори() {
        try { ИЗВОР.setText(Датотека.Читај(작업폴더.resolve(датотека_внес_име.getText()))); }
        catch (Exception ГРЕШКА) { 알림(ГРЕШКА.toString()); }
    }
    private int Команда(List<String> Команда) throws Exception {
        Процес_VALUE = new ProcessBuilder(Команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ред = new BufferedReader(new InputStreamReader(Процес_VALUE.getInputStream(), StandardCharsets.UTF_8))) {
            String Текст;
            while ((Текст = ред.readLine()) != null) 알림(Текст);
        }
        int статус_VALUE = Процес_VALUE.waitFor(); Процес_VALUE = null;
        알림("Излез_програма CODE_VALUE: " + статус_VALUE);
        return статус_VALUE;
    }
    private void Превод_извор(boolean Изврши_наредба, boolean 실행파일) {
        if (!Store_VALUE()) return;
        String 입력 = датотека_внес_име.getText(), внес_поен_VALUE = класа_внес_име.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", внес_поен_VALUE,
                        "--classpath", библиотека, "-o", "실행프로그램", 입력));
                } else if (Команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", библиотека,
                        "-d", "classes", 입력)) == 0 && Изврши_наредба) {
                    Команда(Arrays.asList("java", "-cp", "classes:" + библиотека, внес_поен_VALUE));
                }
            } catch (Exception ГРЕШКА) { 알림(ГРЕШКА.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Процес_VALUE;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private работен_простор() throws IOException {
        Files.createDirectories(작업폴더);
        Font фонт_VALUE = new Font("Monospaced", Font.PLAIN, 16);
        ИЗВОР.setFont(фонт_VALUE); 출력.setFont(фонт_VALUE); 출력.setEditable(false);
        ИЗВОР.setTabSize(4);
        ИЗВОР.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ИЗВОР.setBackground(new Color(250, 251, 252));
        ИЗВОР.setForeground(new Color(32, 43, 58));
        JPanel наредба_панел = new JPanel();
        наредба_панел.add(new JLabel("Датотека")); наредба_панел.add(датотека_внес_име);
        наредба_панел.add(new JLabel("주 класа_VALUE")); наредба_панел.add(класа_внес_име);
        копче(наредба_панел, "Отвори", this::Отвори); копче(наредба_панел, "Store_VALUE", this::Store_VALUE);
        копче(наредба_панел, "изгради_извор", () -> Превод_извор(false, false));
        копче(наредба_панел, "Изврши_наредба", () -> Превод_извор(true, false));
        копче(наредба_панел, "Изврши_наредба Датотека Create_внес", () -> Превод_извор(false, true));
        копче(наредба_панел, "멈춤", this::멈춤);
        JSplitPane делење_мерка = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ИЗВОР), new JScrollPane(출력));
        делење_мерка.setResizeWeight(0.75);
        прозорец.add(наредба_панел, BorderLayout.NORTH); прозорец.add(делење_мерка, BorderLayout.CENTER);
        прозорец.setSize(1200, 750); прозорец.setLocationRelativeTo(null);
        прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        прозорец.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent настан) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Отвори(); прозорец.setVisible(true);
    }
    public static void main(String[] Аргументи) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource стандарден_фонт = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object внес_VALUE : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(внес_VALUE) instanceof Font) UIManager.put(внес_VALUE, стандарден_фонт);
                }
                new работен_простор();
            } catch (Exception ГРЕШКА) { ГРЕШКА.printStackTrace(); }
        });
    }
}
