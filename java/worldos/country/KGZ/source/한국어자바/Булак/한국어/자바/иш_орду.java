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

/** колдонуучу 홈에서 Java 원문을 түзөтүү_маани·тургузуу_башат·실행하는 작은 Swing иш_орду. */
public final class иш_орду {
    private final JFrame терезе = new JFrame("jkoros — 자바 иш_орду");
    private final JTextArea Булак = new JTextArea();
    private final JTextArea Чыгыш = new JTextArea(8, 80);
    private final JTextField файл_киргизме_жазуу_аты = new JTextField("인사.java", 20);
    private final JTextField класс_киргизме_жазуу_аты = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Процесс_маани;
    private final String жыйнак = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Текст) { SwingUtilities.invokeLater(() -> Чыгыш.append(Текст + "\n")); }
    private void баскыч(JPanel нуска_маани, String Аты, Runnable 행동) {
        JButton баскыч = new JButton(Аты);
        баскыч.addActionListener(окуя -> 행동.run());
        нуска_маани.add(баскыч);
    }
    private boolean сактагыч_маани() {
        try {
            Path ЖОЛ = 작업폴더.resolve(файл_киргизме_жазуу_аты.getText());
            Files.createDirectories(ЖОЛ.getParent());
            Файл.Жазуу(ЖОЛ, Булак.getText());
            알림("сактагыч_маани: " + ЖОЛ);
            return true;
        } catch (Exception Ката) { 알림(Ката.toString()); return false; }
    }
    private void Ачуу() {
        try { Булак.setText(Файл.Окуу(작업폴더.resolve(файл_киргизме_жазуу_аты.getText()))); }
        catch (Exception Ката) { 알림(Ката.toString()); }
    }
    private int Команда(List<String> Команда) throws Exception {
        Процесс_маани = new ProcessBuilder(Команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader сап = new BufferedReader(new InputStreamReader(Процесс_маани.getInputStream(), StandardCharsets.UTF_8))) {
            String Текст;
            while ((Текст = сап.readLine()) != null) 알림(Текст);
        }
        int абал_маани = Процесс_маани.waitFor(); Процесс_маани = null;
        알림("Чыгуу_програм 코드: " + абал_маани);
        return абал_маани;
    }
    private void Которуу_башат(boolean аткаруу_буйрук, boolean 실행파일) {
        if (!сактагыч_маани()) return;
        String 입력 = файл_киргизме_жазуу_аты.getText(), киргизме_жазуу_упай_маани = класс_киргизме_жазуу_аты.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", киргизме_жазуу_упай_маани,
                        "--classpath", жыйнак, "-o", "실행프로그램", 입력));
                } else if (Команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", жыйнак,
                        "-d", "classes", 입력)) == 0 && аткаруу_буйрук) {
                    Команда(Arrays.asList("java", "-cp", "classes:" + жыйнак, киргизме_жазуу_упай_маани));
                }
            } catch (Exception Ката) { 알림(Ката.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Процесс_маани;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private иш_орду() throws IOException {
        Files.createDirectories(작업폴더);
        Font арип_маани = new Font("Monospaced", Font.PLAIN, 16);
        Булак.setFont(арип_маани); Чыгыш.setFont(арип_маани); Чыгыш.setEditable(false);
        Булак.setTabSize(4);
        Булак.setMargin(new Insets(10, 12, 10, 12));
        Чыгыш.setMargin(new Insets(8, 12, 8, 12));
        Булак.setBackground(new Color(250, 251, 252));
        Булак.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("Файл")); 명령판.add(файл_киргизме_жазуу_аты);
        명령판.add(new JLabel("주 класс_маани")); 명령판.add(класс_киргизме_жазуу_аты);
        баскыч(명령판, "Ачуу", this::Ачуу); баскыч(명령판, "сактагыч_маани", this::сактагыч_маани);
        баскыч(명령판, "тургузуу_башат", () -> Которуу_башат(false, false));
        баскыч(명령판, "аткаруу_буйрук", () -> Которуу_башат(true, false));
        баскыч(명령판, "аткаруу_буйрук Файл түзүү_киргизме_жазуу", () -> Которуу_башат(false, true));
        баскыч(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Булак), new JScrollPane(Чыгыш));
        나눔.setResizeWeight(0.75);
        терезе.add(명령판, BorderLayout.NORTH); терезе.add(나눔, BorderLayout.CENTER);
        терезе.setSize(1200, 750); терезе.setLocationRelativeTo(null);
        терезе.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        терезе.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent окуя) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Ачуу(); терезе.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource жарыяланбаган_арип = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object киргизме_жазуу_маани : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(киргизме_жазуу_маани) instanceof Font) UIManager.put(киргизме_жазуу_маани, жарыяланбаган_арип);
                }
                new иш_орду();
            } catch (Exception Ката) { Ката.printStackTrace(); }
        });
    }
}
