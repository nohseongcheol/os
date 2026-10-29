// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.JPN.l_ja;
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
public final class 作業場 {
    private final JFrame 窓 = new JFrame();
    private final JTextArea 原文 = new JTextArea();
    private final JTextArea 出力 = new JTextArea();
    private final JTextField 経路 = new JTextField("原文.java", 26);
    private final JTextField 名前 = new JTextField("原文", 15);
    private final JTextField 引数 = new JTextField(25);
    private final Properties 案内文 = new Properties();
    private final Path 資料目録 = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService 作業の糸 = Executors.newSingleThreadExecutor();
    private volatile Process 実行過程;

    private String 表示語(String 鍵) {
        return 案内文.getProperty(鍵, 鍵);
    }

    private void 追記する(String 文字列) {
        SwingUtilities.invokeLater(() -> {
            出力.append(文字列);
            出力.setCaretPosition(出力.getDocument().getLength());
        });
    }

    private void 誤り(Exception 例外) {
        追記する(表示語("error") + ": " + 例外.toString() + "\n");
    }

    private void 押し釦(JPanel 区画, String 鍵, Runnable 動作) {
        JButton 押し釦 = new JButton(表示語(鍵));
        押し釦.addActionListener(出来事 -> 動作.run());
        区画.add(押し釦);
    }

    private void 読み込む() {
        try {
            原文.setText(Files.readString(資料目録.resolve(経路.getText()), StandardCharsets.UTF_8));
            原文.setCaretPosition(0);
        } catch (Exception 例外) { 誤り(例外); }
    }

    private boolean 保存する() {
        try {
            Path 文書 = 資料目録.resolve(経路.getText()).normalize();
            Files.createDirectories(文書.getParent());
            Files.writeString(文書, 原文.getText(), StandardCharsets.UTF_8);
            追記する(表示語("save") + ": " + 文書 + "\n");
            return true;
        } catch (Exception 例外) { 誤り(例外); return false; }
    }

    private int 実行する(List<String> 命令) throws Exception {
        実行過程 = new ProcessBuilder(命令).directory(資料目録.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 読取り器 = new BufferedReader(new InputStreamReader(実行過程.getInputStream(), StandardCharsets.UTF_8))) {
            String 行;
            while ((行 = 読取り器.readLine()) != null) 追記する(行 + "\n");
        }
        int 結果 = 実行過程.waitFor();
        実行過程 = null;
        追記する(表示語("result") + ": " + 結果 + "\n");
        return 結果;
    }

    private void 翻訳する(boolean 起動する) {
        if (!保存する()) return;
        String 文書 = 資料目録.resolve(経路.getText()).toString();
        String 型名 = 名前.getText().trim();
        String 文字列 = 引数.getText();
        作業の糸.submit(() -> {
            try {
                Files.createDirectories(資料目録.resolve("classes"));
                int 結果 = 実行する(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", 資料目録.resolve("classes").toString(), 文書));
                if (起動する && 結果 == 0) {
                    List<String> 命令 = new ArrayList<>(Arrays.asList("java", "-cp", 資料目録.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", 型名));
                    StreamTokenizer 構文解析器 = new StreamTokenizer(new StringReader(文字列));
                    構文解析器.resetSyntax(); 構文解析器.wordChars(33, 65535); 構文解析器.whitespaceChars(0, 32);
                    構文解析器.quoteChar('"'); 構文解析器.quoteChar('\'');
                    while (構文解析器.nextToken() != StreamTokenizer.TT_EOF) 命令.add(構文解析器.sval);
                    実行する(命令);
                }
            } catch (Exception 例外) { 誤り(例外); }
        });
    }

    private void 止める() {
        Process 実行中のプロセス = 実行過程;
        if (実行中のプロセス != null) {
            実行中のプロセス.descendants().forEach(ProcessHandle::destroyForcibly);
            実行中のプロセス.destroyForcibly();
        }
    }

    private void 命令窓() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(資料目録.toFile()).start(); }
        catch (Exception 例外) { 誤り(例外); }
    }

    private void 選ぶ() {
        JFileChooser 選択窓 = new JFileChooser(資料目録.toFile());
        if (選択窓.showOpenDialog(窓) == JFileChooser.APPROVE_OPTION) {
            経路.setText(選択窓.getSelectedFile().getAbsolutePath());
            読み込む();
        }
    }

    private void 初期化する() {
        try (Reader 読取り器 = new InputStreamReader(作業場.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            案内文.load(読取り器);
            Files.createDirectories(資料目録);
        } catch (Exception 例外) { throw new IllegalStateException(例外); }
        窓.setTitle(表示語("workspace") + " · WorldOS " + 表示語("identity"));
        窓.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窓.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent 出来事) {
                止める(); 作業の糸.shutdownNow(); System.exit(0);
            }
        });
        原文.setFont(new Font("Monospaced", Font.PLAIN, 17));
        原文.setTabSize(4);
        出力.setFont(new Font("Monospaced", Font.PLAIN, 14));
        出力.setEditable(false);
        JPanel 区画 = new JPanel(new GridLayout(0, 1));
        JPanel 文書 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        文書.add(new JLabel(表示語("file"))); 文書.add(経路);
        区画.add(文書);
        JPanel 道具欄 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        押し釦(道具欄, "open", () -> 選ぶ());
        押し釦(道具欄, "save", () -> 保存する());
        押し釦(道具欄, "compile", () -> 翻訳する(false));
        押し釦(道具欄, "run", () -> 翻訳する(true));
        押し釦(道具欄, "stop", () -> 止める());
        押し釦(道具欄, "terminal", () -> 命令窓());
        区画.add(道具欄);
        JPanel 設定 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        設定.add(new JLabel(表示語("class"))); 設定.add(名前);
        設定.add(new JLabel(表示語("arguments"))); 設定.add(引数);
        区画.add(設定);
        JSplitPane 分ける = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(原文), new JScrollPane(出力));
        分ける.setResizeWeight(0.72);
        窓.add(区画, BorderLayout.NORTH);
        窓.add(分ける, BorderLayout.CENTER);
        区画.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(表示語("locale"))));
        分ける.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        原文.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        出力.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension 大きさ = Toolkit.getDefaultToolkit().getScreenSize();
        窓.setSize(Math.min(1240, 大きさ.width - 40), Math.min(760, 大きさ.height - 60));
        窓.setLocationRelativeTo(null);
        窓.setVisible(true);
        読み込む();
        分ける.setDividerLocation(0.72);
        追記する("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        追記する(表示語("help") + "\n");
    }

    public static void main(String[] 引数) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new 作業場().初期化する());
    }
}
