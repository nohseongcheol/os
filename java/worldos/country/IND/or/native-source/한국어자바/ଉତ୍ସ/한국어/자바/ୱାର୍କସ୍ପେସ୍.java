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

/** ଉପଭୋକ୍ତା 홈에서 Java 원문을 ସଂପାଦନା_ମୂଲ୍ୟ·ସଙ୍କଳନ_ଉତ୍ସ·실행하는 작은 Swing ୱାର୍କସ୍ପେସ୍. */
public final class ୱାର୍କସ୍ପେସ୍ {
    private final JFrame ଓ୍ୱିଣ୍ଡୋ = new JFrame("jkoros — 자바 ୱାର୍କସ୍ପେସ୍");
    private final JTextArea ଉତ୍ସ = new JTextArea();
    private final JTextArea ନିର୍ଗମ = new JTextArea(8, 80);
    private final JTextField ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ = new JTextField("인사.java", 20);
    private final JTextField ଶ୍ରେଣୀ_ଏଣ୍ଟ୍ରି_ନାମ = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process ପ୍ରୋସେସ୍_ମୂଲ୍ୟ;
    private final String ଲାଇବ୍ରେରୀ = "/opt/jkoros/lib/한국어자바.jar";

    private void 알림(String ପାଠ୍ଯ) { SwingUtilities.invokeLater(() -> ନିର୍ଗମ.append(ପାଠ୍ଯ + "\n")); }
    private void ବଟନ୍(JPanel ସଂସ୍କରଣ_ମୂଲ୍ୟ, String ନାମ, Runnable 행동) {
        JButton ବଟନ୍ = new JButton(ନାମ);
        ବଟନ୍.addActionListener(ଘଟଣା -> 행동.run());
        ସଂସ୍କରଣ_ମୂଲ୍ୟ.add(ବଟନ୍);
    }
    private boolean ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ() {
        try {
            Path ପଥ = 작업폴더.resolve(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ.getText());
            Files.createDirectories(ପଥ.getParent());
            ଫାଇଲ.ଲେଖନ୍ତୁ(ପଥ, ଉତ୍ସ.getText());
            알림("ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ: " + ପଥ);
            return true;
        } catch (Exception ତ୍ରୁଟି) { 알림(ତ୍ରୁଟି.toString()); return false; }
    }
    private void ଖୋଲନ୍ତୁ() {
        try { ଉତ୍ସ.setText(ଫାଇଲ.ପଢନ୍ତୁ(작업폴더.resolve(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ.getText()))); }
        catch (Exception ତ୍ରୁଟି) { 알림(ତ୍ରୁଟି.toString()); }
    }
    private int ନିର୍ଦ୍ଦେଶ(List<String> ନିର୍ଦ୍ଦେଶ) throws Exception {
        ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = new ProcessBuilder(ନିର୍ଦ୍ଦେଶ).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ରେଖା = new BufferedReader(new InputStreamReader(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.getInputStream(), StandardCharsets.UTF_8))) {
            String ପାଠ୍ଯ;
            while ((ପାଠ୍ଯ = ରେଖା.readLine()) != null) 알림(ପାଠ୍ଯ);
        }
        int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.waitFor(); ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = null;
        알림("ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ 코드: " + ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1);
        return ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1;
    }
    private void ଅନୁବାଦ_ଉତ୍ସ(boolean ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ, boolean 실행파일) {
        if (!ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ()) return;
        String 입력 = ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ.getText(), ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍_ମୂଲ୍ୟ = ଶ୍ରେଣୀ_ଏଣ୍ଟ୍ରି_ନାମ.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    ନିର୍ଦ୍ଦେଶ(Arrays.asList("jclassc", "--target", "openjdk", "--entry", ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍_ମୂଲ୍ୟ,
                        "--classpath", ଲାଇବ୍ରେରୀ, "-o", "실행프로그램", 입력));
                } else if (ନିର୍ଦ୍ଦେଶ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ଲାଇବ୍ରେରୀ,
                        "-d", "classes", 입력)) == 0 && ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ) {
                    ନିର୍ଦ୍ଦେଶ(Arrays.asList("java", "-cp", "classes:" + ଲାଇବ୍ରେରୀ, ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍_ମୂଲ୍ୟ));
                }
            } catch (Exception ତ୍ରୁଟି) { 알림(ତ୍ରୁଟି.toString()); }
        });
    }
    private void 멈춤() {
        Process 현재 = ପ୍ରୋସେସ୍_ମୂଲ୍ୟ;
        if (현재 != null) { 현재.descendants().forEach(ProcessHandle::destroy); 현재.destroy(); }
    }
    private ୱାର୍କସ୍ପେସ୍() throws IOException {
        Files.createDirectories(작업폴더);
        Font ଫଣ୍ଟ_ମୂଲ୍ୟ = new Font("Monospaced", Font.PLAIN, 16);
        ଉତ୍ସ.setFont(ଫଣ୍ଟ_ମୂଲ୍ୟ); ନିର୍ଗମ.setFont(ଫଣ୍ଟ_ମୂଲ୍ୟ); ନିର୍ଗମ.setEditable(false);
        ଉତ୍ସ.setTabSize(4);
        ଉତ୍ସ.setMargin(new Insets(10, 12, 10, 12));
        ନିର୍ଗମ.setMargin(new Insets(8, 12, 8, 12));
        ଉତ୍ସ.setBackground(new Color(250, 251, 252));
        ଉତ୍ସ.setForeground(new Color(32, 43, 58));
        JPanel ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍ = new JPanel();
        ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍.add(new JLabel("ଫାଇଲ")); ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍.add(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ);
        ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍.add(new JLabel("주 ଶ୍ରେଣୀ_ମୂଲ୍ୟ_55654bf1")); ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍.add(ଶ୍ରେଣୀ_ଏଣ୍ଟ୍ରି_ନାମ);
        ବଟନ୍(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, "ଖୋଲନ୍ତୁ", this::ଖୋଲନ୍ତୁ); ବଟନ୍(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, "ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ", this::ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ);
        ବଟନ୍(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, "ସଙ୍କଳନ_ଉତ୍ସ", () -> ଅନୁବାଦ_ଉତ୍ସ(false, false));
        ବଟନ୍(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, "ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ", () -> ଅନୁବାଦ_ଉତ୍ସ(true, false));
        ବଟନ୍(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, "ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ ଫାଇଲ ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି", () -> ଅନୁବାଦ_ଉତ୍ସ(false, true));
        ବଟନ୍(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, "멈춤", this::멈춤);
        JSplitPane ହରଣ_ମାପ = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ଉତ୍ସ), new JScrollPane(ନିର୍ଗମ));
        ହରଣ_ମାପ.setResizeWeight(0.75);
        ଓ୍ୱିଣ୍ଡୋ.add(ନିର୍ଦ୍ଦେଶ_ପ୍ୟାନେଲ୍, BorderLayout.NORTH); ଓ୍ୱିଣ୍ଡୋ.add(ହରଣ_ମାପ, BorderLayout.CENTER);
        ଓ୍ୱିଣ୍ଡୋ.setSize(1200, 750); ଓ୍ୱିଣ୍ଡୋ.setLocationRelativeTo(null);
        ଓ୍ୱିଣ୍ଡୋ.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ଓ୍ୱିଣ୍ଡୋ.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent ଘଟଣା) { 멈춤(); 일꾼.shutdownNow(); }
        });
        ଖୋଲନ୍ତୁ(); ଓ୍ୱିଣ୍ଡୋ.setVisible(true);
    }
    public static void main(String[] 인수) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource ଡିଫଲ୍ଟ_ଫଣ୍ଟ୍ = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ) instanceof Font) UIManager.put(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, ଡିଫଲ୍ଟ_ଫଣ୍ଟ୍);
                }
                new ୱାର୍କସ୍ପେସ୍();
            } catch (Exception ତ୍ରୁଟି) { ତ୍ରୁଟି.printStackTrace(); }
        });
    }
}
