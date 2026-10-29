// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PRK.l_ko;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import javax.swing.*;

/** WorldOS project-owned source. Standard Java API names are preserved. */
public final class 작업마당 {
    private final JFrame 창 = new JFrame();
    private final JTextArea 원문 = new JTextArea();
    private final JTextArea 출력 = new JTextArea();
    private final JTextField 경로 = new JTextField("원문.java", 26);
    private final JTextField 이름 = new JTextField("원문", 15);
    private final JTextField 인수 = new JTextField(25);
    private final Properties 안내말 = new Properties();
    private final Path 자료목록 = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService 작업가닥 = Executors.newSingleThreadExecutor();
    private volatile Process 실행과정;

    private String 표시말(String 열쇠) {
        return 안내말.getProperty(열쇠, 열쇠);
    }

    private void 덧붙이기(String 글) {
        SwingUtilities.invokeLater(() -> {
            출력.append(글);
            출력.setCaretPosition(출력.getDocument().getLength());
        });
    }

    private void 오류(Exception 예외) {
        덧붙이기(표시말("error") + ": " + 예외.toString() + "\n");
    }

    private void 단추(JPanel 판, String 열쇠, Runnable 동작) {
        JButton 단추 = new JButton(표시말(열쇠));
        단추.addActionListener(사건 -> 동작.run());
        판.add(단추);
    }

    private void 불러오기() {
        try {
            원문.setText(Files.readString(자료목록.resolve(경로.getText()), StandardCharsets.UTF_8));
            원문.setCaretPosition(0);
        } catch (Exception 예외) { 오류(예외); }
    }

    private boolean 저장하기() {
        try {
            Path 자료파일 = 자료목록.resolve(경로.getText()).normalize();
            Files.createDirectories(자료파일.getParent());
            Files.writeString(자료파일, 원문.getText(), StandardCharsets.UTF_8);
            덧붙이기(표시말("save") + ": " + 자료파일 + "\n");
            return true;
        } catch (Exception 예외) { 오류(예외); return false; }
    }

    private int 실행하기(List<String> 명령) throws Exception {
        실행과정 = new ProcessBuilder(명령).directory(자료목록.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 읽는이 = new BufferedReader(new InputStreamReader(실행과정.getInputStream(), StandardCharsets.UTF_8))) {
            String 줄;
            while ((줄 = 읽는이.readLine()) != null) 덧붙이기(줄 + "\n");
        }
        int 결과 = 실행과정.waitFor();
        실행과정 = null;
        덧붙이기(표시말("result") + ": " + 결과 + "\n");
        return 결과;
    }

    private void 번역하기(boolean 가동하기) {
        if (!저장하기()) return;
        String 자료파일 = 자료목록.resolve(경로.getText()).toString();
        String 자료형이름 = 이름.getText().trim();
        String 글 = 인수.getText();
        작업가닥.submit(() -> {
            try {
                Files.createDirectories(자료목록.resolve("classes"));
                int 결과 = 실행하기(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", 자료목록.resolve("classes").toString(), 자료파일));
                if (가동하기 && 결과 == 0) {
                    List<String> 명령 = new ArrayList<>(Arrays.asList("java", "-cp", 자료목록.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", 자료형이름));
                    StreamTokenizer 문장해석기 = new StreamTokenizer(new StringReader(글));
                    문장해석기.resetSyntax(); 문장해석기.wordChars(33, 65535); 문장해석기.whitespaceChars(0, 32);
                    문장해석기.quoteChar('"'); 문장해석기.quoteChar('\'');
                    while (문장해석기.nextToken() != StreamTokenizer.TT_EOF) 명령.add(문장해석기.sval);
                    실행하기(명령);
                }
            } catch (Exception 예외) { 오류(예외); }
        });
    }

    private void 멈추기() {
        Process 현재실행과정 = 실행과정;
        if (현재실행과정 != null) {
            현재실행과정.descendants().forEach(ProcessHandle::destroyForcibly);
            현재실행과정.destroyForcibly();
        }
    }

    private void 명령창() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(자료목록.toFile()).start(); }
        catch (Exception 예외) { 오류(예외); }
    }

    private void 고르기() {
        JFileChooser 고름창 = new JFileChooser(자료목록.toFile());
        if (고름창.showOpenDialog(창) == JFileChooser.APPROVE_OPTION) {
            경로.setText(고름창.getSelectedFile().getAbsolutePath());
            불러오기();
        }
    }

    private void 초기화하기() {
        try (Reader 읽는이 = new InputStreamReader(작업마당.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            안내말.load(읽는이);
            Files.createDirectories(자료목록);
        } catch (Exception 예외) { throw new IllegalStateException(예외); }
        창.setTitle(표시말("workspace") + " · WorldOS " + 표시말("identity"));
        창.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        창.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent 사건) {
                멈추기(); 작업가닥.shutdownNow(); System.exit(0);
            }
        });
        원문.setFont(new Font("Monospaced", Font.PLAIN, 17));
        원문.setTabSize(4);
        출력.setFont(new Font("Monospaced", Font.PLAIN, 14));
        출력.setEditable(false);
        JPanel 판 = new JPanel(new GridLayout(0, 1));
        JPanel 자료파일 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        자료파일.add(new JLabel(표시말("file"))); 자료파일.add(경로);
        판.add(자료파일);
        JPanel 도구막대 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        단추(도구막대, "open", () -> 고르기());
        단추(도구막대, "save", () -> 저장하기());
        단추(도구막대, "compile", () -> 번역하기(false));
        단추(도구막대, "run", () -> 번역하기(true));
        단추(도구막대, "stop", () -> 멈추기());
        단추(도구막대, "terminal", () -> 명령창());
        판.add(도구막대);
        JPanel 설정 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        설정.add(new JLabel(표시말("class"))); 설정.add(이름);
        설정.add(new JLabel(표시말("arguments"))); 설정.add(인수);
        판.add(설정);
        JSplitPane 나누기 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(원문), new JScrollPane(출력));
        나누기.setResizeWeight(0.72);
        창.add(판, BorderLayout.NORTH);
        창.add(나누기, BorderLayout.CENTER);
        판.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(표시말("locale"))));
        나누기.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        원문.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        출력.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension 크기 = Toolkit.getDefaultToolkit().getScreenSize();
        창.setSize(Math.min(1240, 크기.width - 40), Math.min(760, 크기.height - 60));
        창.setLocationRelativeTo(null);
        창.setVisible(true);
        불러오기();
        나누기.setDividerLocation(0.72);
        덧붙이기("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        덧붙이기(표시말("help") + "\n");
    }

    public static void main(String[] 인수) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new 작업마당().초기화하기());
    }
}
