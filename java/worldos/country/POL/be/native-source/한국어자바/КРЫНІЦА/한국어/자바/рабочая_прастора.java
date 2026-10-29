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

/** карыстальнік 홈에서 Java 원문을 рэдагаваць_значэнне·будаваць_крыніца·실행하는 작은 Swing рабочая_прастора. */
public final class рабочая_прастора {
    private final JFrame акно = new JFrame("jkoros — 자바 рабочая_прастора");
    private final JTextArea КРЫНІЦА = new JTextArea();
    private final JTextArea Выхад = new JTextArea(8, 80);
    private final JTextField файл_увядзенне_імя = new JTextField("인사.java", 20);
    private final JTextField клас_увядзенне_імя = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Працэс_значэнне;
    private final String бібліятэка = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Тэкст) { SwingUtilities.invokeLater(() -> Выхад.append(Тэкст + "\n")); }
    private void кнопка(JPanel версія_значэнне, String Назва, Runnable 행동) {
        JButton кнопка = new JButton(Назва);
        кнопка.addActionListener(Падзея -> 행동.run());
        версія_значэнне.add(кнопка);
    }
    private boolean сховішча_значэнне() {
        try {
            Path ШЛЯХ = 작업폴더.resolve(файл_увядзенне_імя.getText());
            Files.createDirectories(ШЛЯХ.getParent());
            Файл.Запіс(ШЛЯХ, КРЫНІЦА.getText());
            알림("сховішча_значэнне: " + ШЛЯХ);
            return true;
        } catch (Exception ПАМЫЛКА) { 알림(ПАМЫЛКА.toString()); return false; }
    }
    private void Адкрыць() {
        try { КРЫНІЦА.setText(Файл.Чытанне(작업폴더.resolve(файл_увядзенне_імя.getText()))); }
        catch (Exception ПАМЫЛКА) { 알림(ПАМЫЛКА.toString()); }
    }
    private int Загад(List<String> Загад) throws Exception {
        Працэс_значэнне = new ProcessBuilder(Загад).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader лінія = new BufferedReader(new InputStreamReader(Працэс_значэнне.getInputStream(), StandardCharsets.UTF_8))) {
            String Тэкст;
            while ((Тэкст = лінія.readLine()) != null) 알림(Тэкст);
        }
        int стан_значэнне = Працэс_значэнне.waitFor(); Працэс_значэнне = null;
        알림("Выхад_праграма код_значэнне: " + стан_значэнне);
        return стан_значэнне;
    }
    private void Пераклад_крыніца(boolean выканаць_каманда, boolean 실행파일) {
        if (!сховішча_значэнне()) return;
        String 입력 = файл_увядзенне_імя.getText(), увядзенне_бал_значэнне = клас_увядзенне_імя.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Загад(Arrays.asList("jclassc", "--target", "openjdk", "--entry", увядзенне_бал_значэнне,
                        "--classpath", бібліятэка, "-o", "실행프로그램", 입력));
                } else if (Загад(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", бібліятэка,
                        "-d", "classes", 입력)) == 0 && выканаць_каманда) {
                    Загад(Arrays.asList("java", "-cp", "classes:" + бібліятэка, увядзенне_бал_значэнне));
                }
            } catch (Exception ПАМЫЛКА) { 알림(ПАМЫЛКА.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Працэс_значэнне;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private рабочая_прастора() throws IOException {
        Files.createDirectories(작업폴더);
        Font шрыфт_значэнне = new Font("Monospaced", Font.PLAIN, 16);
        КРЫНІЦА.setFont(шрыфт_значэнне); Выхад.setFont(шрыфт_значэнне); Выхад.setEditable(false);
        КРЫНІЦА.setTabSize(4);
        КРЫНІЦА.setMargin(new Insets(10, 12, 10, 12));
        Выхад.setMargin(new Insets(8, 12, 8, 12));
        КРЫНІЦА.setBackground(new Color(250, 251, 252));
        КРЫНІЦА.setForeground(new Color(32, 43, 58));
        JPanel каманда_панэль = new JPanel();
        каманда_панэль.add(new JLabel("Файл")); каманда_панэль.add(файл_увядзенне_імя);
        каманда_панэль.add(new JLabel("주 клас_значэнне")); каманда_панэль.add(клас_увядзенне_імя);
        кнопка(каманда_панэль, "Адкрыць", this::Адкрыць); кнопка(каманда_панэль, "сховішча_значэнне", this::сховішча_значэнне);
        кнопка(каманда_панэль, "будаваць_крыніца", () -> Пераклад_крыніца(false, false));
        кнопка(каманда_панэль, "выканаць_каманда", () -> Пераклад_крыніца(true, false));
        кнопка(каманда_панэль, "выканаць_каманда Файл стварыць_увядзенне", () -> Пераклад_крыніца(false, true));
        кнопка(каманда_панэль, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(КРЫНІЦА), new JScrollPane(Выхад));
        나눔.setResizeWeight(0.75);
        акно.add(каманда_панэль, BorderLayout.NORTH); акно.add(나눔, BorderLayout.CENTER);
        акно.setSize(1200, 750); акно.setLocationRelativeTo(null);
        акно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        акно.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Падзея) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Адкрыць(); акно.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource шрыфт_па_змаўчанні = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object увядзенне_значэнне : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(увядзенне_значэнне) instanceof Font) UIManager.put(увядзенне_значэнне, шрыфт_па_змаўчанні);
                }
                new рабочая_прастора();
            } catch (Exception ПАМЫЛКА) { ПАМЫЛКА.printStackTrace(); }
        });
    }
}
