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

/** пайдаланушы 홈에서 Java 원문을 өңдеу_мән·құрастыру_көз·실행하는 작은 Swing жұмыс_кеңістігі. */
public final class жұмыс_кеңістігі {
    private final JFrame Терезе = new JFrame("jkoros — 자바 жұмыс_кеңістігі");
    private final JTextArea Неден = new JTextArea();
    private final JTextArea Шығысы = new JTextArea(8, 80);
    private final JTextField файл_енгізу_аты = new JTextField("인사.java", 20);
    private final JTextField оқу_енгізу_аты = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Процесс_мән;
    private final String кітапхана = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Мәтін) { SwingUtilities.invokeLater(() -> Шығысы.append(Мәтін + "\n")); }
    private void батырма(JPanel нұсқа_мән, String Аты, Runnable 행동) {
        JButton батырма = new JButton(Аты);
        батырма.addActionListener(Оқиға -> 행동.run());
        нұсқа_мән.add(батырма);
    }
    private boolean сақтау_мән() {
        try {
            Path Жол_2 = 작업폴더.resolve(файл_енгізу_аты.getText());
            Files.createDirectories(Жол_2.getParent());
            Файл.Жазу(Жол_2, Неден.getText());
            알림("сақтау_мән: " + Жол_2);
            return true;
        } catch (Exception Қате) { 알림(Қате.toString()); return false; }
    }
    private void Ашу() {
        try { Неден.setText(Файл.Оқу(작업폴더.resolve(файл_енгізу_аты.getText()))); }
        catch (Exception Қате) { 알림(Қате.toString()); }
    }
    private int Команда(List<String> Команда) throws Exception {
        Процесс_мән = new ProcessBuilder(Команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Жол = new BufferedReader(new InputStreamReader(Процесс_мән.getInputStream(), StandardCharsets.UTF_8))) {
            String Мәтін;
            while ((Мәтін = Жол.readLine()) != null) 알림(Мәтін);
        }
        int күй_мән = Процесс_мән.waitFor(); Процесс_мән = null;
        알림("Шығу_бағдарлама код_мән: " + күй_мән);
        return күй_мән;
    }
    private void Аудару_көз(boolean орындау_пәрмен, boolean 실행파일) {
        if (!сақтау_мән()) return;
        String 입력 = файл_енгізу_аты.getText(), енгізу_ұпай_мән = оқу_енгізу_аты.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", енгізу_ұпай_мән,
                        "--classpath", кітапхана, "-o", "실행프로그램", 입력));
                } else if (Команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", кітапхана,
                        "-d", "classes", 입력)) == 0 && орындау_пәрмен) {
                    Команда(Arrays.asList("java", "-cp", "classes:" + кітапхана, енгізу_ұпай_мән));
                }
            } catch (Exception Қате) { 알림(Қате.toString()); }
        });
    }
    private void 멈춤() {
        Process ток_элемент = Процесс_мән;
        if (ток_элемент != null) { ток_элемент.descendants().forEach(ProcessHandle::destroy); ток_элемент.destroy(); }
    }
    private жұмыс_кеңістігі() throws IOException {
        Files.createDirectories(작업폴더);
        Font қаріп_мән = new Font("Monospaced", Font.PLAIN, 16);
        Неден.setFont(қаріп_мән); Шығысы.setFont(қаріп_мән); Шығысы.setEditable(false);
        Неден.setTabSize(4);
        Неден.setMargin(new Insets(10, 12, 10, 12));
        Шығысы.setMargin(new Insets(8, 12, 8, 12));
        Неден.setBackground(new Color(250, 251, 252));
        Неден.setForeground(new Color(32, 43, 58));
        JPanel пәрмен_тақта = new JPanel();
        пәрмен_тақта.add(new JLabel("Файл")); пәрмен_тақта.add(файл_енгізу_аты);
        пәрмен_тақта.add(new JLabel("주 оқу_мән")); пәрмен_тақта.add(оқу_енгізу_аты);
        батырма(пәрмен_тақта, "Ашу", this::Ашу); батырма(пәрмен_тақта, "сақтау_мән", this::сақтау_мән);
        батырма(пәрмен_тақта, "құрастыру_көз", () -> Аудару_көз(false, false));
        батырма(пәрмен_тақта, "орындау_пәрмен", () -> Аудару_көз(true, false));
        батырма(пәрмен_тақта, "орындау_пәрмен Файл жасау_енгізу", () -> Аудару_көз(false, true));
        батырма(пәрмен_тақта, "멈춤", this::멈춤);
        JSplitPane бөлу_өлшем = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(Неден), new JScrollPane(Шығысы));
        бөлу_өлшем.setResizeWeight(0.75);
        Терезе.add(пәрмен_тақта, BorderLayout.NORTH); Терезе.add(бөлу_өлшем, BorderLayout.CENTER);
        Терезе.setSize(1200, 750); Терезе.setLocationRelativeTo(null);
        Терезе.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Терезе.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Оқиға) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Ашу(); Терезе.setVisible(true);
    }
    public static void main(String[] Аргументтер) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource әдепкі_қаріп = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object енгізу_мән : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(енгізу_мән) instanceof Font) UIManager.put(енгізу_мән, әдепкі_қаріп);
                }
                new жұмыс_кеңістігі();
            } catch (Exception Қате) { Қате.printStackTrace(); }
        });
    }
}
