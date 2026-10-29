// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

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

/** 在使用者家目錄編輯、編譯與執行 Java 原始碼的小型 Swing 工作區。 */
public final class 工作區 {
    private final JFrame 窗口 = new JFrame("jkoros — Java 工作區");
    private final JTextArea 原始碼 = new JTextArea();
    private final JTextArea 輸出 = new JTextArea(8, 80);
    private final JTextField 檔案條目名稱 = new JTextField("問候例.java", 20);
    private final JTextField 類別條目名稱 = new JTextField("問候例", 16);
    private final Path 工作中目錄 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 後臺任務值 = Executors.newSingleThreadExecutor();
    private volatile Process 程序值;
    private final String 庫 = "/opt/jkoros/lib/中文Java.jar";

    private void 通知(String 文本) { SwingUtilities.invokeLater(() -> 輸出.append(文本 + "\n")); }
    private void 按鈕(JPanel 版本值, String 名稱, Runnable 行爲值) {
        JButton 按鈕 = new JButton(名稱);
        按鈕.addActionListener(事件 -> 行爲值.run());
        版本值.add(按鈕);
    }
    private boolean 存儲值() {
        try {
            Path 路徑 = 工作中目錄.resolve(檔案條目名稱.getText());
            Files.createDirectories(路徑.getParent());
            檔案.寫入(路徑, 原始碼.getText());
            通知("存儲值: " + 路徑);
            return true;
        } catch (Exception 錯誤) { 通知(錯誤.toString()); return false; }
    }
    private void 打開() {
        try { 原始碼.setText(檔案.讀取(工作中目錄.resolve(檔案條目名稱.getText()))); }
        catch (Exception 錯誤) { 通知(錯誤.toString()); }
    }
    private int 命令(List<String> 命令) throws Exception {
        程序值 = new ProcessBuilder(命令).directory(工作中目錄.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 行 = new BufferedReader(new InputStreamReader(程序值.getInputStream(), StandardCharsets.UTF_8))) {
            String 文本;
            while ((文本 = 行.readLine()) != null) 通知(文本);
        }
        int 狀態值 = 程序值.waitFor(); 程序值 = null;
        通知("退出程式 程式碼值: " + 狀態值);
        return 狀態值;
    }
    private void 翻譯原始碼(boolean 執行命令, boolean 可執行文件檔案) {
        if (!存儲值()) return;
        String 輸入值 = 檔案條目名稱.getText(), 條目分值 = 類別條目名稱.getText();
        後臺任務值.submit(() -> {
            try {
                Files.createDirectories(工作中目錄.resolve("classes"));
                if (可執行文件檔案) {
                    命令(Arrays.asList("jclassc", "--target", "openjdk", "--entry", 條目分值,
                        "--classpath", 庫, "-o", "실행프로그램", 輸入值));
                } else if (命令(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", 庫,
                        "-d", "classes", 輸入值)) == 0 && 執行命令) {
                    命令(Arrays.asList("java", "-cp", "classes:" + 庫, 條目分值));
                }
            } catch (Exception 錯誤) { 通知(錯誤.toString()); }
        });
    }
    private void 暫停執行狀態() {
        Process 當前項目 = 程序值;
        if (當前項目 != null) { 當前項目.descendants().forEach(ProcessHandle::destroy); 當前項目.destroy(); }
    }
    private 工作區() throws IOException {
        Files.createDirectories(工作中目錄);
        Font 字體值 = new Font("Monospaced", Font.PLAIN, 16);
        原始碼.setFont(字體值); 輸出.setFont(字體值); 輸出.setEditable(false);
        原始碼.setTabSize(4);
        原始碼.setMargin(new Insets(10, 12, 10, 12));
        輸出.setMargin(new Insets(8, 12, 8, 12));
        原始碼.setBackground(new Color(250, 251, 252));
        原始碼.setForeground(new Color(32, 43, 58));
        JPanel 命令面板 = new JPanel();
        命令面板.add(new JLabel("檔案")); 命令面板.add(檔案條目名稱);
        命令面板.add(new JLabel("주 類別值")); 命令面板.add(類別條目名稱);
        按鈕(命令面板, "打開", this::打開); 按鈕(命令面板, "存儲值", this::存儲值);
        按鈕(命令面板, "編譯原始碼", () -> 翻譯原始碼(false, false));
        按鈕(命令面板, "執行命令", () -> 翻譯原始碼(true, false));
        按鈕(命令面板, "執行命令 檔案 創建條目", () -> 翻譯原始碼(false, true));
        按鈕(命令面板, "暫停執行狀態", this::暫停執行狀態);
        JSplitPane 除法結果 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(原始碼), new JScrollPane(輸出));
        除法結果.setResizeWeight(0.75);
        窗口.add(命令面板, BorderLayout.NORTH); 窗口.add(除法結果, BorderLayout.CENTER);
        窗口.setSize(1200, 750); 窗口.setLocationRelativeTo(null);
        窗口.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窗口.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent 事件) { 暫停執行狀態(); 後臺任務值.shutdownNow(); }
        });
        打開(); 窗口.setVisible(true);
    }
    public static void main(String[] 實參) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource 默認字體 = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object 條目值 : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(條目值) instanceof Font) UIManager.put(條目值, 默認字體);
                }
                new 工作區();
            } catch (Exception 錯誤) { 錯誤.printStackTrace(); }
        });
    }
}
