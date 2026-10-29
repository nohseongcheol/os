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

/** корбар 홈에서 Java 원문을 таҳрир_қимат·сохтан_манбаъ·실행하는 작은 Swing фазои_корӣ. */
public final class фазои_корӣ {
    private final JFrame равзана = new JFrame("jkoros — 자바 фазои_корӣ");
    private final JTextArea манбаъ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField файл_ворида_ном = new JTextField("인사.java", 20);
    private final JTextField синф_ворида_ном = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Раванд_қимат;
    private final String китобхона = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Матн) { SwingUtilities.invokeLater(() -> 출력.append(Матн + "\n")); }
    private void тугма(JPanel версия_қимат, String Ном, Runnable 행동) {
        JButton тугма = new JButton(Ном);
        тугма.addActionListener(рӯйдод -> 행동.run());
        версия_қимат.add(тугма);
    }
    private boolean ҳифз_кардан_қимат() {
        try {
            Path масир = 작업폴더.resolve(файл_ворида_ном.getText());
            Files.createDirectories(масир.getParent());
            Файл.Навиштан(масир, манбаъ.getText());
            알림("ҳифз_кардан_қимат: " + масир);
            return true;
        } catch (Exception Хато) { 알림(Хато.toString()); return false; }
    }
    private void кушодан() {
        try { манбаъ.setText(Файл.Хондан(작업폴더.resolve(файл_ворида_ном.getText()))); }
        catch (Exception Хато) { 알림(Хато.toString()); }
    }
    private int фармон(List<String> фармон) throws Exception {
        Раванд_қимат = new ProcessBuilder(фармон).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader хат = new BufferedReader(new InputStreamReader(Раванд_қимат.getInputStream(), StandardCharsets.UTF_8))) {
            String Матн;
            while ((Матн = хат.readLine()) != null) 알림(Матн);
        }
        int вазъият_қимат = Раванд_қимат.waitFor(); Раванд_қимат = null;
        알림("Баромад_барнома 코드: " + вазъият_қимат);
        return вазъият_қимат;
    }
    private void Тарҷума_манбаъ(boolean иҷро_кардан_фармон, boolean 실행파일) {
        if (!ҳифз_кардан_қимат()) return;
        String 입력 = файл_ворида_ном.getText(), ворида_нуқта_қимат = синф_ворида_ном.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    фармон(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ворида_нуқта_қимат,
                        "--classpath", китобхона, "-o", "실행프로그램", 입력));
                } else if (фармон(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", китобхона,
                        "-d", "classes", 입력)) == 0 && иҷро_кардан_фармон) {
                    фармон(Arrays.asList("java", "-cp", "classes:" + китобхона, ворида_нуқта_қимат));
                }
            } catch (Exception Хато) { 알림(Хато.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Раванд_қимат;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private фазои_корӣ() throws IOException {
        Files.createDirectories(작업폴더);
        Font шрифт_қимат = new Font("Monospaced", Font.PLAIN, 16);
        манбаъ.setFont(шрифт_қимат); 출력.setFont(шрифт_қимат); 출력.setEditable(false);
        манбаъ.setTabSize(4);
        манбаъ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        манбаъ.setBackground(new Color(250, 251, 252));
        манбаъ.setForeground(new Color(32, 43, 58));
        JPanel фармон_панел = new JPanel();
        фармон_панел.add(new JLabel("Файл")); фармон_панел.add(файл_ворида_ном);
        фармон_панел.add(new JLabel("주 синф_қимат")); фармон_панел.add(синф_ворида_ном);
        тугма(фармон_панел, "кушодан", this::кушодан); тугма(фармон_панел, "ҳифз_кардан_қимат", this::ҳифз_кардан_қимат);
        тугма(фармон_панел, "сохтан_манбаъ", () -> Тарҷума_манбаъ(false, false));
        тугма(фармон_панел, "иҷро_кардан_фармон", () -> Тарҷума_манбаъ(true, false));
        тугма(фармон_панел, "иҷро_кардан_фармон Файл эҷод_кардан_ворида", () -> Тарҷума_манбаъ(false, true));
        тугма(фармон_панел, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(манбаъ), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        равзана.add(фармон_панел, BorderLayout.NORTH); равзана.add(나눔, BorderLayout.CENTER);
        равзана.setSize(1200, 750); равзана.setLocationRelativeTo(null);
        равзана.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        равзана.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent рӯйдод) { 멈춤(); 일꾼.shutdownNow(); }
        });
        кушодан(); равзана.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource шрифти_пешфарз = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ворида_қимат : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ворида_қимат) instanceof Font) UIManager.put(ворида_қимат, шрифти_пешфарз);
                }
                new фазои_корӣ();
            } catch (Exception Хато) { Хато.printStackTrace(); }
        });
    }
}
