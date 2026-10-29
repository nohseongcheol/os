// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.Java;

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

/** 利用者のホームで Java ソースを編集・コンパイル・実行する小さな Swing 作業場。 */
public final class 作業場 {
    private final JFrame 窓 = new JFrame("jkoros — Java 作業場");
    private final JTextArea ソース = new JTextArea();
    private final JTextArea 出力 = new JTextArea(8, 80);
    private final JTextField ファイル入口名前 = new JTextField("挨拶例.java", 20);
    private final JTextField クラス入口名前 = new JTextField("挨拶例", 16);
    private final Path 作業中ディレクトリ = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 作業担当値 = Executors.newSingleThreadExecutor();
    private volatile Process プロセス値;
    private final String ライブラリ = "/opt/jkoros/lib/日本語Java.jar";

    private void 通知(String 文) { SwingUtilities.invokeLater(() -> 出力.append(文 + "\n")); }
    private void ボタン(JPanel 版値, String 名前, Runnable 挙動値) {
        JButton ボタン = new JButton(名前);
        ボタン.addActionListener(イベント -> 挙動値.run());
        版値.add(ボタン);
    }
    private boolean 格納値() {
        try {
            Path 経路 = 作業中ディレクトリ.resolve(ファイル入口名前.getText());
            Files.createDirectories(経路.getParent());
            ファイル.書込(経路, ソース.getText());
            通知("格納値: " + 経路);
            return true;
        } catch (Exception エラー) { 通知(エラー.toString()); return false; }
    }
    private void 開放() {
        try { ソース.setText(ファイル.読取(作業中ディレクトリ.resolve(ファイル入口名前.getText()))); }
        catch (Exception エラー) { 通知(エラー.toString()); }
    }
    private int 命令(List<String> 命令) throws Exception {
        プロセス値 = new ProcessBuilder(命令).directory(作業中ディレクトリ.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 行 = new BufferedReader(new InputStreamReader(プロセス値.getInputStream(), StandardCharsets.UTF_8))) {
            String 文;
            while ((文 = 行.readLine()) != null) 通知(文);
        }
        int 状況値 = プロセス値.waitFor(); プロセス値 = null;
        通知("終了点プログラム コード値: " + 状況値);
        return 状況値;
    }
    private void ソース翻訳処理(boolean 命令実行, boolean 実行形式ファイル) {
        if (!格納値()) return;
        String 入力値 = ファイル入口名前.getText(), 入口点値 = クラス入口名前.getText();
        作業担当値.submit(() -> {
            try {
                Files.createDirectories(作業中ディレクトリ.resolve("classes"));
                if (実行形式ファイル) {
                    命令(Arrays.asList("jclassc", "--target", "openjdk", "--entry", 入口点値,
                        "--classpath", ライブラリ, "-o", "실행프로그램", 入力値));
                } else if (命令(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ライブラリ,
                        "-d", "classes", 入力値)) == 0 && 命令実行) {
                    命令(Arrays.asList("java", "-cp", "classes:" + ライブラリ, 入口点値));
                }
            } catch (Exception エラー) { 通知(エラー.toString()); }
        });
    }
    private void 一時停止実行状態() {
        Process 現在項目 = プロセス値;
        if (現在項目 != null) { 現在項目.descendants().forEach(ProcessHandle::destroy); 現在項目.destroy(); }
    }
    private 作業場() throws IOException {
        Files.createDirectories(作業中ディレクトリ);
        Font 書体値 = new Font("Monospaced", Font.PLAIN, 16);
        ソース.setFont(書体値); 出力.setFont(書体値); 出力.setEditable(false);
        ソース.setTabSize(4);
        ソース.setMargin(new Insets(10, 12, 10, 12));
        出力.setMargin(new Insets(8, 12, 8, 12));
        ソース.setBackground(new Color(250, 251, 252));
        ソース.setForeground(new Color(32, 43, 58));
        JPanel 命令操作面 = new JPanel();
        命令操作面.add(new JLabel("ファイル")); 命令操作面.add(ファイル入口名前);
        命令操作面.add(new JLabel("주 クラス値")); 命令操作面.add(クラス入口名前);
        ボタン(命令操作面, "開放", this::開放); ボタン(命令操作面, "格納値", this::格納値);
        ボタン(命令操作面, "ソースコンパイル", () -> ソース翻訳処理(false, false));
        ボタン(命令操作面, "命令実行", () -> ソース翻訳処理(true, false));
        ボタン(命令操作面, "命令実行 ファイル 入口作成", () -> ソース翻訳処理(false, true));
        ボタン(命令操作面, "一時停止実行状態", this::一時停止実行状態);
        JSplitPane 除算結果 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ソース), new JScrollPane(出力));
        除算結果.setResizeWeight(0.75);
        窓.add(命令操作面, BorderLayout.NORTH); 窓.add(除算結果, BorderLayout.CENTER);
        窓.setSize(1200, 750); 窓.setLocationRelativeTo(null);
        窓.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窓.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent イベント) { 一時停止実行状態(); 作業担当値.shutdownNow(); }
        });
        開放(); 窓.setVisible(true);
    }
    public static void main(String[] 引数) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource 既定書体 = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object 入口値 : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(入口値) instanceof Font) UIManager.put(入口値, 既定書体);
                }
                new 作業場();
            } catch (Exception エラー) { エラー.printStackTrace(); }
        });
    }
}
