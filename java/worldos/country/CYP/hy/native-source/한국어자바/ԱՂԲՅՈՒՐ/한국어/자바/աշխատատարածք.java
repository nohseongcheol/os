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

/** օգտվող 홈에서 Java 원문을 խմբագրել_արժեք·կառուցել_աղբյուր·실행하는 작은 Swing աշխատատարածք. */
public final class աշխատատարածք {
    private final JFrame պատուհան = new JFrame("jkoros — 자바 աշխատատարածք");
    private final JTextArea ԱՂԲՅՈՒՐ = new JTextArea();
    private final JTextArea Ելք = new JTextArea(8, 80);
    private final JTextField նիշք_մուտքագրում_անուն = new JTextField("인사.java", 20);
    private final JTextField դաս_մուտքագրում_անուն = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Ընթացք_արժեք;
    private final String դարան = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String Տեքստ) { SwingUtilities.invokeLater(() -> Ելք.append(Տեքստ + "\n")); }
    private void կոճակ(JPanel տարբերակ_արժեք, String Անուն, Runnable 행동) {
        JButton կոճակ = new JButton(Անուն);
        կոճակ.addActionListener(միջոցառում -> 행동.run());
        տարբերակ_արժեք.add(կոճակ);
    }
    private boolean պահեստավորել_արժեք() {
        try {
            Path Ճանապարհ = 작업폴더.resolve(նիշք_մուտքագրում_անուն.getText());
            Files.createDirectories(Ճանապարհ.getParent());
            Ֆայլ.Գրել(Ճանապարհ, ԱՂԲՅՈՒՐ.getText());
            알림("պահեստավորել_արժեք: " + Ճանապարհ);
            return true;
        } catch (Exception Սխալ) { 알림(Սխալ.toString()); return false; }
    }
    private void Բաց() {
        try { ԱՂԲՅՈՒՐ.setText(Ֆայլ.Ընթերցում(작업폴더.resolve(նիշք_մուտքագրում_անուն.getText()))); }
        catch (Exception Սխալ) { 알림(Սխալ.toString()); }
    }
    private int Հրահանգ(List<String> Հրահանգ) throws Exception {
        Ընթացք_արժեք = new ProcessBuilder(Հրահանգ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader կապ = new BufferedReader(new InputStreamReader(Ընթացք_արժեք.getInputStream(), StandardCharsets.UTF_8))) {
            String Տեքստ;
            while ((Տեքստ = կապ.readLine()) != null) 알림(Տեքստ);
        }
        int վիճակ_արժեք = Ընթացք_արժեք.waitFor(); Ընթացք_արժեք = null;
        알림("Ելք_ծրագիր կոդ_արժեք: " + վիճակ_արժեք);
        return վիճակ_արժեք;
    }
    private void Թարգմանել_աղբյուր(boolean կատարել_հրաման, boolean 실행파일) {
        if (!պահեստավորել_արժեք()) return;
        String 입력 = նիշք_մուտքագրում_անուն.getText(), մուտքագրում_կետ_արժեք = դաս_մուտքագրում_անուն.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Հրահանգ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", մուտքագրում_կետ_արժեք,
                        "--classpath", դարան, "-o", "실행프로그램", 입력));
                } else if (Հրահանգ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", դարան,
                        "-d", "classes", 입력)) == 0 && կատարել_հրաման) {
                    Հրահանգ(Arrays.asList("java", "-cp", "classes:" + դարան, մուտքագրում_կետ_արժեք));
                }
            } catch (Exception Սխալ) { 알림(Սխալ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = Ընթացք_արժեք;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private աշխատատարածք() throws IOException {
        Files.createDirectories(작업폴더);
        Font տառատեսակ_արժեք = new Font("Monospaced", Font.PLAIN, 16);
        ԱՂԲՅՈՒՐ.setFont(տառատեսակ_արժեք); Ելք.setFont(տառատեսակ_արժեք); Ելք.setEditable(false);
        ԱՂԲՅՈՒՐ.setTabSize(4);
        ԱՂԲՅՈՒՐ.setMargin(new Insets(10, 12, 10, 12));
        Ելք.setMargin(new Insets(8, 12, 8, 12));
        ԱՂԲՅՈՒՐ.setBackground(new Color(250, 251, 252));
        ԱՂԲՅՈՒՐ.setForeground(new Color(32, 43, 58));
        JPanel հրաման_վահանակ = new JPanel();
        հրաման_վահանակ.add(new JLabel("Ֆայլ")); հրաման_վահանակ.add(նիշք_մուտքագրում_անուն);
        հրաման_վահանակ.add(new JLabel("주 դաս_արժեք")); հրաման_վահանակ.add(դաս_մուտքագրում_անուն);
        կոճակ(հրաման_վահանակ, "Բաց", this::Բաց); կոճակ(հրաման_վահանակ, "պահեստավորել_արժեք", this::պահեստավորել_արժեք);
        կոճակ(հրաման_վահանակ, "կառուցել_աղբյուր", () -> Թարգմանել_աղբյուր(false, false));
        կոճակ(հրաման_վահանակ, "կատարել_հրաման", () -> Թարգմանել_աղբյուր(true, false));
        կոճակ(հրաման_վահանակ, "կատարել_հրաման Ֆայլ Կերտի_ր_մուտքագրում", () -> Թարգմանել_աղբյուր(false, true));
        կոճակ(հրաման_վահանակ, "멈춤", this::멈춤);
        JSplitPane բաժանում_չափ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ԱՂԲՅՈՒՐ), new JScrollPane(Ելք));
        բաժանում_չափ.setResizeWeight(0.75);
        պատուհան.add(հրաման_վահանակ, BorderLayout.NORTH); պատուհան.add(բաժանում_չափ, BorderLayout.CENTER);
        պատուհան.setSize(1200, 750); պատուհան.setLocationRelativeTo(null);
        պատուհան.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        պատուհան.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent միջոցառում) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Բաց(); պատուհան.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource սկզբնադիր_տառատեսակ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object մուտքագրում_արժեք : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(մուտքագրում_արժեք) instanceof Font) UIManager.put(մուտքագրում_արժեք, սկզբնադիր_տառատեսակ);
                }
                new աշխատատարածք();
            } catch (Exception Սխալ) { Սխալ.printStackTrace(); }
        });
    }
}
