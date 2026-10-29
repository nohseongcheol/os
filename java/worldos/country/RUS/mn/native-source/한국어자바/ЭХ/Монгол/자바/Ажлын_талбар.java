// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.자바;

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

/** хэрэглэгч 홈에서 Java 원문을 засварлах_утга·хөрвүүлэх_эх·실행하는 작은 Swing Ажлын_талбар. */
public final class Ажлын_талбар {
    private final JFrame цонх = new JFrame("jkoros — 자바 Ажлын_талбар");
    private final JTextArea ЭХ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField файл_оролт_нэр = new JTextField("인사.java", 20);
    private final JTextField класс_оролт_нэр = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process үйл_явц_утга;
    private final String сан = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Бичвэр) { SwingUtilities.invokeLater(() -> 출력.append(Бичвэр + "\n")); }
    private void товч(JPanel хувилбар_утга, String Нэр, Runnable 행동) {
        JButton товч = new JButton(Нэр);
        товч.addActionListener(үйлдэл -> 행동.run());
        хувилбар_утга.add(товч);
    }
    private boolean хадгалах_утга() {
        try {
            Path ЗАМ = 작업폴더.resolve(файл_оролт_нэр.getText());
            Files.createDirectories(ЗАМ.getParent());
            Файл.Бичих(ЗАМ, ЭХ.getText());
            알림("хадгалах_утга: " + ЗАМ);
            return true;
        } catch (Exception Алдаа) { 알림(Алдаа.toString()); return false; }
    }
    private void Нээх() {
        try { ЭХ.setText(Файл.Унших(작업폴더.resolve(файл_оролт_нэр.getText()))); }
        catch (Exception Алдаа) { 알림(Алдаа.toString()); }
    }
    private int Тушаал(List<String> Тушаал) throws Exception {
        үйл_явц_утга = new ProcessBuilder(Тушаал).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Шугам = new BufferedReader(new InputStreamReader(үйл_явц_утга.getInputStream(), StandardCharsets.UTF_8))) {
            String Бичвэр;
            while ((Бичвэр = Шугам.readLine()) != null) 알림(Бичвэр);
        }
        int төлөв_утга = үйл_явц_утга.waitFor(); үйл_явц_утга = null;
        알림("Гарах_програм 코드: " + төлөв_утга);
        return төлөв_утга;
    }
    private void Орчуулах_эх(boolean Гүйцэтгэх_команд, boolean 실행파일) {
        if (!хадгалах_утга()) return;
        String 입력 = файл_оролт_нэр.getText(), оролт_цэг_утга = класс_оролт_нэр.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Тушаал(Arrays.asList("jclassc", "--target", "openjdk", "--entry", оролт_цэг_утга,
                        "--classpath", сан, "-o", "실행프로그램", 입력));
                } else if (Тушаал(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", сан,
                        "-d", "classes", 입력)) == 0 && Гүйцэтгэх_команд) {
                    Тушаал(Arrays.asList("java", "-cp", "classes:" + сан, оролт_цэг_утга));
                }
            } catch (Exception Алдаа) { 알림(Алдаа.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = үйл_явц_утга;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private Ажлын_талбар() throws IOException {
        Files.createDirectories(작업폴더);
        Font үсгийн_хэв_утга = new Font("Monospaced", Font.PLAIN, 16);
        ЭХ.setFont(үсгийн_хэв_утга); 출력.setFont(үсгийн_хэв_утга); 출력.setEditable(false);
        ЭХ.setTabSize(4);
        ЭХ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ЭХ.setBackground(new Color(250, 251, 252));
        ЭХ.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("Файл")); 명령판.add(файл_оролт_нэр);
        명령판.add(new JLabel("주 класс_утга")); 명령판.add(класс_оролт_нэр);
        товч(명령판, "Нээх", this::Нээх); товч(명령판, "хадгалах_утга", this::хадгалах_утга);
        товч(명령판, "хөрвүүлэх_эх", () -> Орчуулах_эх(false, false));
        товч(명령판, "Гүйцэтгэх_команд", () -> Орчуулах_эх(true, false));
        товч(명령판, "Гүйцэтгэх_команд Файл үүсгэх_оролт", () -> Орчуулах_эх(false, true));
        товч(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ЭХ), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        цонх.add(명령판, BorderLayout.NORTH); цонх.add(나눔, BorderLayout.CENTER);
        цонх.setSize(1200, 750); цонх.setLocationRelativeTo(null);
        цонх.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        цонх.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent үйлдэл) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Нээх(); цонх.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource өгөгдмөл_үсгийн_хэв = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object оролт_утга : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(оролт_утга) instanceof Font) UIManager.put(оролт_утга, өгөгдмөл_үсгийн_хэв);
                }
                new Ажлын_талбар();
            } catch (Exception Алдаа) { Алдаа.printStackTrace(); }
        });
    }
}
