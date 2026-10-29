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

/** корисник 홈에서 Java 원문을 Уреди_вриједност·направити_извор·실행하는 작은 Swing радни_сто. */
public final class радни_сто {
    private final JFrame Прозор = new JFrame("jkoros — 자바 радни_сто");
    private final JTextArea ИЗВОР = new JTextArea();
    private final JTextArea Излаз = new JTextArea(8, 80);
    private final JTextField фајл_унос_име = new JTextField("인사.java", 20);
    private final JTextField класа_унос_име = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Процес_вриједност;
    private final String библиотека = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Текст) { SwingUtilities.invokeLater(() -> Излаз.append(Текст + "\n")); }
    private void дугме(JPanel верзија_вриједност, String Назив, Runnable 행동) {
        JButton дугме = new JButton(Назив);
        дугме.addActionListener(Догађај -> 행동.run());
        верзија_вриједност.add(дугме);
    }
    private boolean похранити_вриједност() {
        try {
            Path ПУТАЊА = 작업폴더.resolve(фајл_унос_име.getText());
            Files.createDirectories(ПУТАЊА.getParent());
            Датотека.Пише(ПУТАЊА, ИЗВОР.getText());
            알림("похранити_вриједност: " + ПУТАЊА);
            return true;
        } catch (Exception ГРЕШКА) { 알림(ГРЕШКА.toString()); return false; }
    }
    private void Отвори() {
        try { ИЗВОР.setText(Датотека.Чита(작업폴더.resolve(фајл_унос_име.getText()))); }
        catch (Exception ГРЕШКА) { 알림(ГРЕШКА.toString()); }
    }
    private int Наредба(List<String> Наредба) throws Exception {
        Процес_вриједност = new ProcessBuilder(Наредба).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Ред = new BufferedReader(new InputStreamReader(Процес_вриједност.getInputStream(), StandardCharsets.UTF_8))) {
            String Текст;
            while ((Текст = Ред.readLine()) != null) 알림(Текст);
        }
        int стање_вриједност = Процес_вриједност.waitFor(); Процес_вриједност = null;
        알림("Излаз_програм шифра_вриједност: " + стање_вриједност);
        return стање_вриједност;
    }
    private void превести_извор(boolean Изврши_команда, boolean 실행파일) {
        if (!похранити_вриједност()) return;
        String 입력 = фајл_унос_име.getText(), унос_поен_вриједност = класа_унос_име.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Наредба(Arrays.asList("jclassc", "--target", "openjdk", "--entry", унос_поен_вриједност,
                        "--classpath", библиотека, "-o", "실행프로그램", 입력));
                } else if (Наредба(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", библиотека,
                        "-d", "classes", 입력)) == 0 && Изврши_команда) {
                    Наредба(Arrays.asList("java", "-cp", "classes:" + библиотека, унос_поен_вриједност));
                }
            } catch (Exception ГРЕШКА) { 알림(ГРЕШКА.toString()); }
        });
    }
    private void 멈춤() {
        Process актуелно_ставка = Процес_вриједност;
        if (актуелно_ставка != null) { актуелно_ставка.descendants().forEach(ProcessHandle::destroy); актуелно_ставка.destroy(); }
    }
    private радни_сто() throws IOException {
        Files.createDirectories(작업폴더);
        Font фонт_вриједност = new Font("Monospaced", Font.PLAIN, 16);
        ИЗВОР.setFont(фонт_вриједност); Излаз.setFont(фонт_вриједност); Излаз.setEditable(false);
        ИЗВОР.setTabSize(4);
        ИЗВОР.setMargin(new Insets(10, 12, 10, 12));
        Излаз.setMargin(new Insets(8, 12, 8, 12));
        ИЗВОР.setBackground(new Color(250, 251, 252));
        ИЗВОР.setForeground(new Color(32, 43, 58));
        JPanel команда_табла = new JPanel();
        команда_табла.add(new JLabel("Датотека")); команда_табла.add(фајл_унос_име);
        команда_табла.add(new JLabel("주 класа_вриједност")); команда_табла.add(класа_унос_име);
        дугме(команда_табла, "Отвори", this::Отвори); дугме(команда_табла, "похранити_вриједност", this::похранити_вриједност);
        дугме(команда_табла, "направити_извор", () -> превести_извор(false, false));
        дугме(команда_табла, "Изврши_команда", () -> превести_извор(true, false));
        дугме(команда_табла, "Изврши_команда Датотека Направи_унос", () -> превести_извор(false, true));
        дугме(команда_табла, "멈춤", this::멈춤);
        JSplitPane дељење_мера = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ИЗВОР), new JScrollPane(Излаз));
        дељење_мера.setResizeWeight(0.75);
        Прозор.add(команда_табла, BorderLayout.NORTH); Прозор.add(дељење_мера, BorderLayout.CENTER);
        Прозор.setSize(1200, 750); Прозор.setLocationRelativeTo(null);
        Прозор.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Прозор.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Догађај) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Отвори(); Прозор.setVisible(true);
    }
    public static void main(String[] Аргументи) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource стандардни_фонт = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object унос_вриједност : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(унос_вриједност) instanceof Font) UIManager.put(унос_вриједност, стандардни_фонт);
                }
                new радни_сто();
            } catch (Exception ГРЕШКА) { ГРЕШКА.printStackTrace(); }
        });
    }
}
