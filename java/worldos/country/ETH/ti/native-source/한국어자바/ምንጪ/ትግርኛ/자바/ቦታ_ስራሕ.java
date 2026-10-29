// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자바;

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

/** ተጠቃሚ 홈에서 Java 원문을 ምዕራይ_ዋጋ·ህነጽ_ምንጪ·실행하는 작은 Swing ቦታ_ስራሕ. */
public final class ቦታ_ስራሕ {
    private final JFrame መስኮት = new JFrame("jkoros — 자바 ቦታ_ስራሕ");
    private final JTextArea ምንጪ = new JTextArea();
    private final JTextArea 출력 = new JTextArea(8, 80);
    private final JTextField ፋይል_ምእታው_ሽም = new JTextField("인사.java", 20);
    private final JTextField ክፍሊ_ምእታው_ሽም = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process መስርሕ_ዋጋ;
    private final String ቤት_ንባብ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ጽሑፍ) { SwingUtilities.invokeLater(() -> 출력.append(ጽሑፍ + "\n")); }
    private void መጠወቒ(JPanel ሕታም_ዋጋ, String ሽም, Runnable 행동) {
        JButton መጠወቒ = new JButton(ሽም);
        መጠወቒ.addActionListener(ፍጻመ -> 행동.run());
        ሕታም_ዋጋ.add(መጠወቒ);
    }
    private boolean ከዝን_ዋጋ() {
        try {
            Path መገዲ = 작업폴더.resolve(ፋይል_ምእታው_ሽም.getText());
            Files.createDirectories(መገዲ.getParent());
            ፋይል.ጸሓፍ(መገዲ, ምንጪ.getText());
            알림("ከዝን_ዋጋ: " + መገዲ);
            return true;
        } catch (Exception ጌጋ) { 알림(ጌጋ.toString()); return false; }
    }
    private void ክፈት() {
        try { ምንጪ.setText(ፋይል.읽기(작업폴더.resolve(ፋይል_ምእታው_ሽም.getText()))); }
        catch (Exception ጌጋ) { 알림(ጌጋ.toString()); }
    }
    private int ትእዛዝ(List<String> ትእዛዝ) throws Exception {
        መስርሕ_ዋጋ = new ProcessBuilder(ትእዛዝ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader መስመር = new BufferedReader(new InputStreamReader(መስርሕ_ዋጋ.getInputStream(), StandardCharsets.UTF_8))) {
            String ጽሑፍ;
            while ((ጽሑፍ = መስመር.readLine()) != null) 알림(ጽሑፍ);
        }
        int ደረጃ_ዋጋ = መስርሕ_ዋጋ.waitFor(); መስርሕ_ዋጋ = null;
        알림("ውጻእ_መተግበሪ 코드: " + ደረጃ_ዋጋ);
        return ደረጃ_ዋጋ;
    }
    private void ተርጉም_ምንጪ(boolean ተግብር_ትእዛዝ, boolean 실행파일) {
        if (!ከዝን_ዋጋ()) return;
        String 입력 = ፋይል_ምእታው_ሽም.getText(), ምእታው_ነጥቢ_ዋጋ = ክፍሊ_ምእታው_ሽም.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ትእዛዝ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ምእታው_ነጥቢ_ዋጋ,
                        "--classpath", ቤት_ንባብ, "-o", "실행프로그램", 입력));
                } else if (ትእዛዝ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ቤት_ንባብ,
                        "-d", "classes", 입력)) == 0 && ተግብር_ትእዛዝ) {
                    ትእዛዝ(Arrays.asList("java", "-cp", "classes:" + ቤት_ንባብ, ምእታው_ነጥቢ_ዋጋ));
                }
            } catch (Exception ጌጋ) { 알림(ጌጋ.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = መስርሕ_ዋጋ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ቦታ_ስራሕ() throws IOException {
        Files.createDirectories(작업폴더);
        Font ቅርጺ_ፊደል_ዋጋ = new Font("Monospaced", Font.PLAIN, 16);
        ምንጪ.setFont(ቅርጺ_ፊደል_ዋጋ); 출력.setFont(ቅርጺ_ፊደል_ዋጋ); 출력.setEditable(false);
        ምንጪ.setTabSize(4);
        ምንጪ.setMargin(new Insets(10, 12, 10, 12));
        출력.setMargin(new Insets(8, 12, 8, 12));
        ምንጪ.setBackground(new Color(250, 251, 252));
        ምንጪ.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("ፋይል")); 명령판.add(ፋይል_ምእታው_ሽም);
        명령판.add(new JLabel("주 ክፍሊ_ዋጋ")); 명령판.add(ክፍሊ_ምእታው_ሽም);
        መጠወቒ(명령판, "ክፈት", this::ክፈት); መጠወቒ(명령판, "ከዝን_ዋጋ", this::ከዝን_ዋጋ);
        መጠወቒ(명령판, "ህነጽ_ምንጪ", () -> ተርጉም_ምንጪ(false, false));
        መጠወቒ(명령판, "ተግብር_ትእዛዝ", () -> ተርጉም_ምንጪ(true, false));
        መጠወቒ(명령판, "ተግብር_ትእዛዝ ፋይል ፍጠር_ምእታው", () -> ተርጉም_ምንጪ(false, true));
        መጠወቒ(명령판, "멈춤", this::멈춤);
        JSplitPane 나눔 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ምንጪ), new JScrollPane(출력));
        나눔.setResizeWeight(0.75);
        መስኮት.add(명령판, BorderLayout.NORTH); መስኮት.add(나눔, BorderLayout.CENTER);
        መስኮት.setSize(1200, 750); መስኮት.setLocationRelativeTo(null);
        መስኮት.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        መስኮት.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ፍጻመ) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ክፈት(); መስኮት.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ልሙድ_ኣጻሓሕፋ_ፊደል = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ምእታው_ዋጋ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ምእታው_ዋጋ) instanceof Font) UIManager.put(ምእታው_ዋጋ, ልሙድ_ኣጻሓሕፋ_ፊደል);
                }
                new ቦታ_ስራሕ();
            } catch (Exception ጌጋ) { ጌጋ.printStackTrace(); }
        });
    }
}
