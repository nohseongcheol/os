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

/** ئىشلەتكۈچى 홈에서 Java 원문을 تەھرىرلەش_قىممىتى·قۇرماق_مەنبە·실행하는 작은 Swing ئىش_سۇپىسى. */
public final class ئىش_سۇپىسى {
    private final JFrame كۆزنەك = new JFrame("jkoros — 자바 ئىش_سۇپىسى");
    private final JTextArea مەنبە = new JTextArea();
    private final JTextArea چىقار = new JTextArea(8, 80);
    private final JTextField ھۆججەت_كىرگۈزۈش_نامى = new JTextField("인사.java", 20);
    private final JTextField تۈركۈم_كىرگۈزۈش_نامى = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process جەريان_قىممىتى;
    private final String ئامبار = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String تېكىست) { SwingUtilities.invokeLater(() -> چىقار.append(تېكىست + "\n")); }
    private void كۇنۇپكا(JPanel نەشىر_نومۇرى_قىممىتى, String ئاتى, Runnable 행동) {
        JButton كۇنۇپكا = new JButton(ئاتى);
        كۇنۇپكا.addActionListener(ھادىسە -> 행동.run());
        نەشىر_نومۇرى_قىممىتى.add(كۇنۇپكا);
    }
    private boolean ساقلىماق_قىممىتى() {
        try {
            Path يول = 작업폴더.resolve(ھۆججەت_كىرگۈزۈش_نامى.getText());
            Files.createDirectories(يول.getParent());
            ھۆججەت.ياز(يول, مەنبە.getText());
            알림("ساقلىماق_قىممىتى: " + يول);
            return true;
        } catch (Exception خاتالىق) { 알림(خاتالىق.toString()); return false; }
    }
    private void ئاچ() {
        try { مەنبە.setText(ھۆججەت.ئوقۇ(작업폴더.resolve(ھۆججەت_كىرگۈزۈش_نامى.getText()))); }
        catch (Exception خاتالىق) { 알림(خاتالىق.toString()); }
    }
    private int بۇيرۇق(List<String> بۇيرۇق) throws Exception {
        جەريان_قىممىتى = new ProcessBuilder(بۇيرۇق).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader قۇر = new BufferedReader(new InputStreamReader(جەريان_قىممىتى.getInputStream(), StandardCharsets.UTF_8))) {
            String تېكىست;
            while ((تېكىست = قۇر.readLine()) != null) 알림(تېكىست);
        }
        int ھالەت_قىممىتى = جەريان_قىممىتى.waitFor(); جەريان_قىممىتى = null;
        알림("چىقىش_ئەپ 코드: " + ھالەت_قىممىتى);
        return ھالەت_قىممىتى;
    }
    private void تەرجىمە_مەنبە(boolean ئىجرا_قىلىش_بۇيرۇق, boolean 실행파일) {
        if (!ساقلىماق_قىممىتى()) return;
        String 입력 = ھۆججەت_كىرگۈزۈش_نامى.getText(), كىرگۈزۈش_نوقتا_قىممىتى = تۈركۈم_كىرگۈزۈش_نامى.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    بۇيرۇق(Arrays.asList("jclassc", "--target", "openjdk", "--entry", كىرگۈزۈش_نوقتا_قىممىتى,
                        "--classpath", ئامبار, "-o", "실행프로그램", 입력));
                } else if (بۇيرۇق(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ئامبار,
                        "-d", "classes", 입력)) == 0 && ئىجرا_قىلىش_بۇيرۇق) {
                    بۇيرۇق(Arrays.asList("java", "-cp", "classes:" + ئامبار, كىرگۈزۈش_نوقتا_قىممىتى));
                }
            } catch (Exception خاتالىق) { 알림(خاتالىق.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = جەريان_قىممىتى;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ئىش_سۇپىسى() throws IOException {
        Files.createDirectories(작업폴더);
        Font خەت_نۇسخا_قىممىتى = new Font("Monospaced", Font.PLAIN, 16);
        مەنبە.setFont(خەت_نۇسخا_قىممىتى); چىقار.setFont(خەت_نۇسخا_قىممىتى); چىقار.setEditable(false);
        مەنبە.setTabSize(4);
        مەنبە.setMargin(new Insets(10, 12, 10, 12));
        چىقار.setMargin(new Insets(8, 12, 8, 12));
        مەنبە.setBackground(new Color(250, 251, 252));
        مەنبە.setForeground(new Color(32, 43, 58));
        JPanel بۇيرۇق_سۇپا = new JPanel();
        بۇيرۇق_سۇپا.add(new JLabel("ھۆججەت")); بۇيرۇق_سۇپا.add(ھۆججەت_كىرگۈزۈش_نامى);
        بۇيرۇق_سۇپا.add(new JLabel("주 تۈركۈم_قىممىتى")); بۇيرۇق_سۇپا.add(تۈركۈم_كىرگۈزۈش_نامى);
        كۇنۇپكا(بۇيرۇق_سۇپا, "ئاچ", this::ئاچ); كۇنۇپكا(بۇيرۇق_سۇپا, "ساقلىماق_قىممىتى", this::ساقلىماق_قىممىتى);
        كۇنۇپكا(بۇيرۇق_سۇپا, "قۇرماق_مەنبە", () -> تەرجىمە_مەنبە(false, false));
        كۇنۇپكا(بۇيرۇق_سۇپا, "ئىجرا_قىلىش_بۇيرۇق", () -> تەرجىمە_مەنبە(true, false));
        كۇنۇپكا(بۇيرۇق_سۇپا, "ئىجرا_قىلىش_بۇيرۇق ھۆججەت قۇرۇش_كىرگۈزۈش", () -> تەرجىمە_مەنبە(false, true));
        كۇنۇپكا(بۇيرۇق_سۇپا, "멈춤", this::멈춤);
        JSplitPane بۆلۈش_ئۆلچەم = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(مەنبە), new JScrollPane(چىقار));
        بۆلۈش_ئۆلچەم.setResizeWeight(0.75);
        كۆزنەك.add(بۇيرۇق_سۇپا, BorderLayout.NORTH); كۆزنەك.add(بۆلۈش_ئۆلچەم, BorderLayout.CENTER);
        كۆزنەك.setSize(1200, 750); كۆزنەك.setLocationRelativeTo(null);
        كۆزنەك.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        كۆزنەك.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ھادىسە) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ئاچ(); كۆزنەك.setVisible(true);
    }
    public static void main(String[] ئۆزگەرگۈچىلەر) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource باش_خەت_نۇسخىسى = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object كىرگۈزۈش_قىممىتى : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(كىرگۈزۈش_قىممىتى) instanceof Font) UIManager.put(كىرگۈزۈش_قىممىتى, باش_خەت_نۇسخىسى);
                }
                new ئىش_سۇپىسى();
            } catch (Exception خاتالىق) { خاتالىق.printStackTrace(); }
        });
    }
}
