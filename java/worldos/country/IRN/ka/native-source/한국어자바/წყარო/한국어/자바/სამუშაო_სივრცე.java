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

/** მომხმარებელი 홈에서 Java 원문을 რედაქტირება_მნიშვნელობა·აწყობა_წყარო·실행하는 작은 Swing სამუშაო_სივრცე. */
public final class სამუშაო_სივრცე {
    private final JFrame ფანჯარა = new JFrame("jkoros — 자바 სამუშაო_სივრცე");
    private final JTextArea წყარო = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ფაილი_შენატანი_სახელი = new JTextField("인사.java", 20);
    private final JTextField კლასი_შენატანი_სახელი = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process პროცესი_მნიშვნელობა;
    private final String ბიბლიოთეკა = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ტექსტი) { SwingUtilities.invokeLater(() -> 출력.append(ტექსტი + "\n")); }
    private void ღილაკი(JPanel ვერსია_მნიშვნელობა, String სახელი, Runnable 행동) {
        JButton ღილაკი = new JButton(სახელი);
        ღილაკი.addActionListener(მოვლენა -> 행동.run());
        ვერსია_მნიშვნელობა.add(ღილაკი);
    }
    private boolean შენახვა_მნიშვნელობა() {
        try {
            Path გეზი = 작업폴더.resolve(ფაილი_შენატანი_სახელი.getText());
            Files.createDirectories(გეზი.getParent());
            ფაილი.ჩაწერა(გეზი, წყარო.getText());
            알림("შენახვა_მნიშვნელობა: " + გეზი);
            return true;
        } catch (Exception შეცდომა) { 알림(შეცდომა.toString()); return false; }
    }
    private void გახსნა() {
        try { წყარო.setText(ფაილი.კითხვა(작업폴더.resolve(ფაილი_შენატანი_სახელი.getText()))); }
        catch (Exception შეცდომა) { 알림(შეცდომა.toString()); }
    }
    private int ბრძანება(List<String> ბრძანება) throws Exception {
        პროცესი_მნიშვნელობა = new ProcessBuilder(ბრძანება).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ხაზი = new BufferedReader(new InputStreamReader(პროცესი_მნიშვნელობა.getInputStream(), StandardCharsets.UTF_8))) {
            String ტექსტი;
            while ((ტექსტი = ხაზი.readLine()) != null) 알림(ტექსტი);
        }
        int სტატუსი_მნიშვნელობა = პროცესი_მნიშვნელობა.waitFor(); პროცესი_მნიშვნელობა = null;
        알림("გასვლა_აპი კოდექსი_მნიშვნელობა: " + სტატუსი_მნიშვნელობა);
        return სტატუსი_მნიშვნელობა;
    }
    private void თარგმნა_წყარო(boolean შესრულება_ბრძანება, boolean 실행파일) {
        if (!შენახვა_მნიშვნელობა()) return;
        String 입력 = ფაილი_შენატანი_სახელი.getText(), შენატანი_პტ_მნიშვნელობა = კლასი_შენატანი_სახელი.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ბრძანება(Arrays.asList("jclassc", "--target", "openjdk", "--entry", შენატანი_პტ_მნიშვნელობა,
                        "--classpath", ბიბლიოთეკა, "-o", "실행프로그램", 입력));
                } else if (ბრძანება(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ბიბლიოთეკა,
                        "-d", "classes", 입력)) == 0 && შესრულება_ბრძანება) {
                    ბრძანება(Arrays.asList("java", "-cp", "classes:" + ბიბლიოთეკა, შენატანი_პტ_მნიშვნელობა));
                }
            } catch (Exception შეცდომა) { 알림(შეცდომა.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = პროცესი_მნიშვნელობა;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private სამუშაო_სივრცე() throws IOException {
        Files.createDirectories(작업폴더);
        Font შრიფტი_მნიშვნელობა = new Font("Monospaced", Font.PLAIN, 16);
        წყარო.setFont(შრიფტი_მნიშვნელობა); 출력.setFont(შრიფტი_მნიშვნელობა); 출력.setEditable(false);
        წყარო.setTabSize(4);
        წყარო.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        წყარო.setBackground(new Color(250, 251, 252));
        წყარო.setForeground(new Color(32, 43, 58));
        JPanel ბრძანება_პანელი = new JPanel();
        ბრძანება_პანელი.add(new JLabel("ფაილი")); ბრძანება_პანელი.add(ფაილი_შენატანი_სახელი);
        ბრძანება_პანელი.add(new JLabel("주 კლასი_მნიშვნელობა")); ბრძანება_პანელი.add(კლასი_შენატანი_სახელი);
        ღილაკი(ბრძანება_პანელი, "გახსნა", this::გახსნა); ღილაკი(ბრძანება_პანელი, "შენახვა_მნიშვნელობა", this::შენახვა_მნიშვნელობა);
        ღილაკი(ბრძანება_პანელი, "აწყობა_წყარო", () -> თარგმნა_წყარო(false, false));
        ღილაკი(ბრძანება_პანელი, "შესრულება_ბრძანება", () -> თარგმნა_წყარო(true, false));
        ღილაკი(ბრძანება_პანელი, "შესრულება_ბრძანება ფაილი შექმნა_შენატანი", () -> თარგმნა_წყარო(false, true));
        ღილაკი(ბრძანება_პანელი, "멈춤", this::멈춤);
        JSplitPane გაყოფა_გაზომვა = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(წყარო), new JScrollPane(출력));
        გაყოფა_გაზომვა.setResizeWeight(0.75);
        ფანჯარა.add(ბრძანება_პანელი, BorderLayout.NORTH); ფანჯარა.add(გაყოფა_გაზომვა, BorderLayout.CENTER);
        ფანჯარა.setSize(1200, 750); ფანჯარა.setLocationRelativeTo(null);
        ფანჯარა.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ფანჯარა.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent მოვლენა) { 멈춤(); 일꾼.shutdownNow(); }
        });
        გახსნა(); ფანჯარა.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ნაგულისხმევი_შრიფტი = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object შენატანი_მნიშვნელობა : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(შენატანი_მნიშვნელობა) instanceof Font) UIManager.put(შენატანი_მნიშვნელობა, ნაგულისხმევი_შრიფტი);
                }
                new სამუშაო_სივრცე();
            } catch (Exception შეცდომა) { შეცდომა.printStackTrace(); }
        });
    }
}
