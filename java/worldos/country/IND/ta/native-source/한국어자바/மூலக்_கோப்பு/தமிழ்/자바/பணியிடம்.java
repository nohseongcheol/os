// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자바;

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

/** பயனர் 홈에서 Java 원문을 திருத்து_மதிப்பு·தொகு_மூலம்·실행하는 작은 Swing பணியிடம். */
public final class பணியிடம் {
    private final JFrame சாளரம் = new JFrame("jkoros — 자바 பணியிடம்");
    private final JTextArea மூலக்_கோப்பு = new JTextArea();
    private final JTextArea வெளியீட்டு_இடம் = new JTextArea(8, 80);
    private final JTextField கோப்பு_உள்ளீடு_பெயர் = new JTextField("인사.java", 20);
    private final JTextField பிரிவு_உள்ளீடு_பெயர் = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process செயலகம்_மதிப்பு;
    private final String நூலகம் = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String உரை) { SwingUtilities.invokeLater(() -> வெளியீட்டு_இடம்.append(உரை + "\n")); }
    private void பொத்தான்(JPanel பதிப்பு_மதிப்பு, String பெயர், Runnable 행동) {
        JButton பொத்தான் = new JButton(பெயர்);
        பொத்தான்.addActionListener(நிகழ்வு -> 행동.run());
        பதிப்பு_மதிப்பு.add(பொத்தான்);
    }
    private boolean சேகரி_மதிப்பு() {
        try {
            Path பாதை_2 = 작업폴더.resolve(கோப்பு_உள்ளீடு_பெயர்.getText());
            Files.createDirectories(பாதை_2.getParent());
            கோப்பின்_பெயர்.எழுது(பாதை_2, மூலக்_கோப்பு.getText());
            알림("சேகரி_மதிப்பு: " + பாதை_2);
            return true;
        } catch (Exception பிழை) { 알림(பிழை.toString()); return false; }
    }
    private void திற() {
        try { மூலக்_கோப்பு.setText(கோப்பின்_பெயர்.படி(작업폴더.resolve(கோப்பு_உள்ளீடு_பெயர்.getText()))); }
        catch (Exception பிழை) { 알림(பிழை.toString()); }
    }
    private int கட்டளை(List<String> கட்டளை) throws Exception {
        செயலகம்_மதிப்பு = new ProcessBuilder(கட்டளை).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader உள்ளீட்டு_வரி = new BufferedReader(new InputStreamReader(செயலகம்_மதிப்பு.getInputStream(), StandardCharsets.UTF_8))) {
            String உரை;
            while ((உரை = உள்ளீட்டு_வரி.readLine()) != null) 알림(உரை);
        }
        int நிலை_மதிப்பு_e10195a1 = செயலகம்_மதிப்பு.waitFor(); செயலகம்_மதிப்பு = null;
        알림("முடிவு_நிரல் குறியீடு_மதிப்பு: " + நிலை_மதிப்பு_e10195a1);
        return நிலை_மதிப்பு_e10195a1;
    }
    private void மொழியாக்கம்_மூலம்(boolean இயக்கு_கட்டளை, boolean செயல்படுத்தக்கூடிய_கோப்பு) {
        if (!சேகரி_மதிப்பு()) return;
        String 입력 = கோப்பு_உள்ளீடு_பெயர்.getText(), நுழைவுப்_புள்ளி_மதிப்பு = பிரிவு_உள்ளீடு_பெயர்.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (செயல்படுத்தக்கூடிய_கோப்பு) {
                    கட்டளை(Arrays.asList("jclassc", "--target", "openjdk", "--entry", நுழைவுப்_புள்ளி_மதிப்பு,
                        "--classpath", நூலகம், "-o", "실행프로그램", 입력));
                } else if (கட்டளை(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", நூலகம்,
                        "-d", "classes", 입력)) == 0 && இயக்கு_கட்டளை) {
                    கட்டளை(Arrays.asList("java", "-cp", "classes:" + நூலகம், நுழைவுப்_புள்ளி_மதிப்பு));
                }
            } catch (Exception பிழை) { 알림(பிழை.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = செயலகம்_மதிப்பு;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private பணியிடம்() throws IOException {
        Files.createDirectories(작업폴더);
        Font எழுத்துரு_மதிப்பு = new Font("Monospaced", Font.PLAIN, 16);
        மூலக்_கோப்பு.setFont(எழுத்துரு_மதிப்பு); வெளியீட்டு_இடம்.setFont(எழுத்துரு_மதிப்பு); வெளியீட்டு_இடம்.setEditable(false);
        மூலக்_கோப்பு.setTabSize(4);
        மூலக்_கோப்பு.setMargin(new Insets(10, 12, 10, 12));
        வெளியீட்டு_இடம்.setMargin(new Insets(8, 12, 8, 12));
        மூலக்_கோப்பு.setBackground(new Color(250, 251, 252));
        மூலக்_கோப்பு.setForeground(new Color(32, 43, 58));
        JPanel கட்டளை_பலகம் = new JPanel();
        கட்டளை_பலகம்.add(new JLabel("கோப்பின்_பெயர்")); கட்டளை_பலகம்.add(கோப்பு_உள்ளீடு_பெயர்);
        கட்டளை_பலகம்.add(new JLabel("주 பிரிவு_மதிப்பு_55654bf1")); கட்டளை_பலகம்.add(பிரிவு_உள்ளீடு_பெயர்);
        பொத்தான்(கட்டளை_பலகம், "திற", this::திற); பொத்தான்(கட்டளை_பலகம், "சேகரி_மதிப்பு", this::சேகரி_மதிப்பு);
        பொத்தான்(கட்டளை_பலகம், "தொகு_மூலம்", () -> மொழியாக்கம்_மூலம்(false, false));
        பொத்தான்(கட்டளை_பலகம், "இயக்கு_கட்டளை", () -> மொழியாக்கம்_மூலம்(true, false));
        பொத்தான்(கட்டளை_பலகம், "இயக்கு_கட்டளை கோப்பின்_பெயர் உருவாக்கு_உள்ளீடு", () -> மொழியாக்கம்_மூலம்(false, true));
        பொத்தான்(கட்டளை_பலகம், "멈춤", this::멈춤);
        JSplitPane வகுத்தல்_அளவிடக்கூடியது = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(மூலக்_கோப்பு), new JScrollPane(வெளியீட்டு_இடம்));
        வகுத்தல்_அளவிடக்கூடியது.setResizeWeight(0.75);
        சாளரம்.add(கட்டளை_பலகம், BorderLayout.NORTH); சாளரம்.add(வகுத்தல்_அளவிடக்கூடியது, BorderLayout.CENTER);
        சாளரம்.setSize(1200, 750); சாளரம்.setLocationRelativeTo(null);
        சாளரம்.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        சாளரம்.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent நிகழ்வு) { 멈춤(); 일꾼.shutdownNow(); }
        });
        திற(); சாளரம்.setVisible(true);
    }
    public static void main(String[] செயலுருபுகள்) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource இயல்புநிலை_எழுத்துரு = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object உள்ளீடு_மதிப்பு : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(உள்ளீடு_மதிப்பு) instanceof Font) UIManager.put(உள்ளீடு_மதிப்பு, இயல்புநிலை_எழுத்துரு);
                }
                new பணியிடம்();
            } catch (Exception பிழை) { பிழை.printStackTrace(); }
        });
    }
}
