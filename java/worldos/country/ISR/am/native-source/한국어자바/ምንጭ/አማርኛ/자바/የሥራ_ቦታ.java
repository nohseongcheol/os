// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자바;

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

/** ተጠቃሚ 홈에서 Java 원문을 አርትዕ_እሴት·መገንባት_ምንጭ·실행하는 작은 Swing የሥራ_ቦታ. */
public final class የሥራ_ቦታ {
    private final JFrame መስኮት = new JFrame("jkoros — 자바 የሥራ_ቦታ");
    private final JTextArea ምንጭ = new JTextArea();
    private final JTextArea ውጤት = new JTextArea(8, 80);
    private final JTextField ፋይል_ምዝግብ_ስም = new JTextField("인사.java", 20);
    private final JTextField መደብ_ምዝግብ_ስም = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ሂደት_እሴት;
    private final String ማከማቻ_ስፍራ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ጽሁፍ) { SwingUtilities.invokeLater(() -> ውጤት.append(ጽሁፍ + "\n")); }
    private void አዝራር(JPanel ስሪት_እሴት, String ስም, Runnable 행동) {
        JButton አዝራር = new JButton(ስም);
        አዝራር.addActionListener(ፍጻሜ -> 행동.run());
        ስሪት_እሴት.add(አዝራር);
    }
    private boolean ማከማቻ_እሴት() {
        try {
            Path መተላለፊያ = 작업폴더.resolve(ፋይል_ምዝግብ_ስም.getText());
            Files.createDirectories(መተላለፊያ.getParent());
            ፋይል.መጻፊያ(መተላለፊያ, ምንጭ.getText());
            알림("ማከማቻ_እሴት: " + መተላለፊያ);
            return true;
        } catch (Exception ስህተት) { 알림(ስህተት.toString()); return false; }
    }
    private void መክፈቻ() {
        try { ምንጭ.setText(ፋይል.ማንበቢያ(작업폴더.resolve(ፋይል_ምዝግብ_ስም.getText()))); }
        catch (Exception ስህተት) { 알림(ስህተት.toString()); }
    }
    private int ትእዛዝ(List<String> ትእዛዝ) throws Exception {
        ሂደት_እሴት = new ProcessBuilder(ትእዛዝ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader መስመር = new BufferedReader(new InputStreamReader(ሂደት_እሴት.getInputStream(), StandardCharsets.UTF_8))) {
            String ጽሁፍ;
            while ((ጽሁፍ = መስመር.readLine()) != null) 알림(ጽሁፍ);
        }
        int ዞን_እሴት = ሂደት_እሴት.waitFor(); ሂደት_እሴት = null;
        알림("ውጣ_ፕሮግራም 코드: " + ዞን_እሴት);
        return ዞን_እሴት;
    }
    private void ተርጉም_ምንጭ(boolean ፈጽም_ትእዛዝ, boolean 실행파일) {
        if (!ማከማቻ_እሴት()) return;
        String 입력 = ፋይል_ምዝግብ_ስም.getText(), ምዝግብ_ቦታ_እሴት = መደብ_ምዝግብ_ስም.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ትእዛዝ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ምዝግብ_ቦታ_እሴት,
                        "--classpath", ማከማቻ_ስፍራ, "-o", "실행프로그램", 입력));
                } else if (ትእዛዝ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ማከማቻ_ስፍራ,
                        "-d", "classes", 입력)) == 0 && ፈጽም_ትእዛዝ) {
                    ትእዛዝ(Arrays.asList("java", "-cp", "classes:" + ማከማቻ_ስፍራ, ምዝግብ_ቦታ_እሴት));
                }
            } catch (Exception ስህተት) { 알림(ስህተት.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ሂደት_እሴት;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private የሥራ_ቦታ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ቅርጸ_ቁምፊ_እሴት = new Font("Monospaced", Font.PLAIN, 16);
        ምንጭ.setFont(ቅርጸ_ቁምፊ_እሴት); ውጤት.setFont(ቅርጸ_ቁምፊ_እሴት); ውጤት.setEditable(false);
        ምንጭ.setTabSize(4);
        ምንጭ.setMargin(new Insets(10, 12, 10, 12));
        ውጤት.setMargin(new Insets(8, 12, 8, 12));
        ምንጭ.setBackground(new Color(250, 251, 252));
        ምንጭ.setForeground(new Color(32, 43, 58));
        JPanel ትእዛዝ_መቃን = new JPanel();
        ትእዛዝ_መቃን.add(new JLabel("ፋይል")); ትእዛዝ_መቃን.add(ፋይል_ምዝግብ_ስም);
        ትእዛዝ_መቃን.add(new JLabel("주 መደብ_እሴት")); ትእዛዝ_መቃን.add(መደብ_ምዝግብ_ስም);
        አዝራር(ትእዛዝ_መቃን, "መክፈቻ", this::መክፈቻ); አዝራር(ትእዛዝ_መቃን, "ማከማቻ_እሴት", this::ማከማቻ_እሴት);
        አዝራር(ትእዛዝ_መቃን, "መገንባት_ምንጭ", () -> ተርጉም_ምንጭ(false, false));
        አዝራር(ትእዛዝ_መቃን, "ፈጽም_ትእዛዝ", () -> ተርጉም_ምንጭ(true, false));
        አዝራር(ትእዛዝ_መቃን, "ፈጽም_ትእዛዝ ፋይል ፍጠር_ምዝግብ", () -> ተርጉም_ምንጭ(false, true));
        አዝራር(ትእዛዝ_መቃን, "멈춤", this::멈춤);
        JSplitPane ማካፈል_ልኬት = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ምንጭ), new JScrollPane(ውጤት));
        ማካፈል_ልኬት.setResizeWeight(0.75);
        መስኮት.add(ትእዛዝ_መቃን, BorderLayout.NORTH); መስኮት.add(ማካፈል_ልኬት, BorderLayout.CENTER);
        መስኮት.setSize(1200, 750); መስኮት.setLocationRelativeTo(null);
        መስኮት.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        መስኮት.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ፍጻሜ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        መክፈቻ(); መስኮት.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ነባሪ_ቅርጸ_ቁምፊ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ምዝግብ_እሴት : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ምዝግብ_እሴት) instanceof Font) UIManager.put(ምዝግብ_እሴት, ነባሪ_ቅርጸ_ቁምፊ);
                }
                new የሥራ_ቦታ();
            } catch (Exception ስህተት) { ስህተት.printStackTrace(); }
        });
    }
}
