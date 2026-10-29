// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.THA.l_zh_Hant;
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
public final class 工作坊 {
    private final JFrame 視窗 = new JFrame();
    private final JTextArea 原文 = new JTextArea();
    private final JTextArea 輸出 = new JTextArea();
    private final JTextField 路徑 = new JTextField("原文.java", 26);
    private final JTextField 名稱 = new JTextField("原文", 15);
    private final JTextField 引數 = new JTextField(25);
    private final Properties 訊息 = new Properties();
    private final Path 目錄 = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService 工作執行緒 = Executors.newSingleThreadExecutor();
    private volatile Process 行程;

    private String 標籤(String 鍵) {
        return 訊息.getProperty(鍵, 鍵);
    }

    private void 附加(String 文字) {
        SwingUtilities.invokeLater(() -> {
            輸出.append(文字);
            輸出.setCaretPosition(輸出.getDocument().getLength());
        });
    }

    private void 錯誤(Exception 例外) {
        附加(標籤("error") + ": " + 例外.toString() + "\n");
    }

    private void 按鈕(JPanel 面板, String 鍵, Runnable 動作) {
        JButton 按鈕 = new JButton(標籤(鍵));
        按鈕.addActionListener(事件 -> 動作.run());
        面板.add(按鈕);
    }

    private void 載入() {
        try {
            原文.setText(Files.readString(目錄.resolve(路徑.getText()), StandardCharsets.UTF_8));
            原文.setCaretPosition(0);
        } catch (Exception 例外) { 錯誤(例外); }
    }

    private boolean 儲存() {
        try {
            Path 檔案 = 目錄.resolve(路徑.getText()).normalize();
            Files.createDirectories(檔案.getParent());
            Files.writeString(檔案, 原文.getText(), StandardCharsets.UTF_8);
            附加(標籤("save") + ": " + 檔案 + "\n");
            return true;
        } catch (Exception 例外) { 錯誤(例外); return false; }
    }

    private int 執行(List<String> 命令) throws Exception {
        行程 = new ProcessBuilder(命令).directory(目錄.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 讀取器 = new BufferedReader(new InputStreamReader(行程.getInputStream(), StandardCharsets.UTF_8))) {
            String 列;
            while ((列 = 讀取器.readLine()) != null) 附加(列 + "\n");
        }
        int 結果 = 行程.waitFor();
        行程 = null;
        附加(標籤("result") + ": " + 結果 + "\n");
        return 結果;
    }

    private void 編譯(boolean 運行) {
        if (!儲存()) return;
        String 檔案 = 目錄.resolve(路徑.getText()).toString();
        String 類別名稱 = 名稱.getText().trim();
        String 文字 = 引數.getText();
        工作執行緒.submit(() -> {
            try {
                Files.createDirectories(目錄.resolve("classes"));
                int 結果 = 執行(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", 目錄.resolve("classes").toString(), 檔案));
                if (運行 && 結果 == 0) {
                    List<String> 命令 = new ArrayList<>(Arrays.asList("java", "-cp", 目錄.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", 類別名稱));
                    StreamTokenizer 剖析器 = new StreamTokenizer(new StringReader(文字));
                    剖析器.resetSyntax(); 剖析器.wordChars(33, 65535); 剖析器.whitespaceChars(0, 32);
                    剖析器.quoteChar('"'); 剖析器.quoteChar('\'');
                    while (剖析器.nextToken() != StreamTokenizer.TT_EOF) 命令.add(剖析器.sval);
                    執行(命令);
                }
            } catch (Exception 例外) { 錯誤(例外); }
        });
    }

    private void 停止() {
        Process 目前行程 = 行程;
        if (目前行程 != null) {
            目前行程.descendants().forEach(ProcessHandle::destroyForcibly);
            目前行程.destroyForcibly();
        }
    }

    private void 終端() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(目錄.toFile()).start(); }
        catch (Exception 例外) { 錯誤(例外); }
    }

    private void 選擇() {
        JFileChooser 選擇器 = new JFileChooser(目錄.toFile());
        if (選擇器.showOpenDialog(視窗) == JFileChooser.APPROVE_OPTION) {
            路徑.setText(選擇器.getSelectedFile().getAbsolutePath());
            載入();
        }
    }

    private void 初始化() {
        try (Reader 讀取器 = new InputStreamReader(工作坊.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            訊息.load(讀取器);
            Files.createDirectories(目錄);
        } catch (Exception 例外) { throw new IllegalStateException(例外); }
        視窗.setTitle(標籤("workspace") + " · WorldOS " + 標籤("identity"));
        視窗.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        視窗.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent 事件) {
                停止(); 工作執行緒.shutdownNow(); System.exit(0);
            }
        });
        原文.setFont(new Font("Monospaced", Font.PLAIN, 17));
        原文.setTabSize(4);
        輸出.setFont(new Font("Monospaced", Font.PLAIN, 14));
        輸出.setEditable(false);
        JPanel 面板 = new JPanel(new GridLayout(0, 1));
        JPanel 檔案 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        檔案.add(new JLabel(標籤("file"))); 檔案.add(路徑);
        面板.add(檔案);
        JPanel 工具列 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        按鈕(工具列, "open", () -> 選擇());
        按鈕(工具列, "save", () -> 儲存());
        按鈕(工具列, "compile", () -> 編譯(false));
        按鈕(工具列, "run", () -> 編譯(true));
        按鈕(工具列, "stop", () -> 停止());
        按鈕(工具列, "terminal", () -> 終端());
        面板.add(工具列);
        JPanel 設定 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        設定.add(new JLabel(標籤("class"))); 設定.add(名稱);
        設定.add(new JLabel(標籤("arguments"))); 設定.add(引數);
        面板.add(設定);
        JSplitPane 分割 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(原文), new JScrollPane(輸出));
        分割.setResizeWeight(0.72);
        視窗.add(面板, BorderLayout.NORTH);
        視窗.add(分割, BorderLayout.CENTER);
        面板.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(標籤("locale"))));
        分割.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        原文.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        輸出.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension 大小 = Toolkit.getDefaultToolkit().getScreenSize();
        視窗.setSize(Math.min(1240, 大小.width - 40), Math.min(760, 大小.height - 60));
        視窗.setLocationRelativeTo(null);
        視窗.setVisible(true);
        載入();
        分割.setDividerLocation(0.72);
        附加("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        附加(標籤("help") + "\n");
    }

    public static void main(String[] 引數) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new 工作坊().初始化());
    }
}
