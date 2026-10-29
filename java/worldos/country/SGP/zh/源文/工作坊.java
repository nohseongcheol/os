// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SGP.l_zh;
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
    private final JFrame 窗口 = new JFrame();
    private final JTextArea 源文 = new JTextArea();
    private final JTextArea 输出 = new JTextArea();
    private final JTextField 路径 = new JTextField("源文.java", 26);
    private final JTextField 名称 = new JTextField("源文", 15);
    private final JTextField 参数 = new JTextField(25);
    private final Properties 消息 = new Properties();
    private final Path 目录 = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService 工作线程 = Executors.newSingleThreadExecutor();
    private volatile Process 进程;

    private String 标签(String 键) {
        return 消息.getProperty(键, 键);
    }

    private void 追加(String 文本) {
        SwingUtilities.invokeLater(() -> {
            输出.append(文本);
            输出.setCaretPosition(输出.getDocument().getLength());
        });
    }

    private void 错误(Exception 异常) {
        追加(标签("error") + ": " + 异常.toString() + "\n");
    }

    private void 按钮(JPanel 面板, String 键, Runnable 动作) {
        JButton 按钮 = new JButton(标签(键));
        按钮.addActionListener(事件 -> 动作.run());
        面板.add(按钮);
    }

    private void 加载() {
        try {
            源文.setText(Files.readString(目录.resolve(路径.getText()), StandardCharsets.UTF_8));
            源文.setCaretPosition(0);
        } catch (Exception 异常) { 错误(异常); }
    }

    private boolean 保存() {
        try {
            Path 文件 = 目录.resolve(路径.getText()).normalize();
            Files.createDirectories(文件.getParent());
            Files.writeString(文件, 源文.getText(), StandardCharsets.UTF_8);
            追加(标签("save") + ": " + 文件 + "\n");
            return true;
        } catch (Exception 异常) { 错误(异常); return false; }
    }

    private int 执行(List<String> 命令) throws Exception {
        进程 = new ProcessBuilder(命令).directory(目录.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 读取器 = new BufferedReader(new InputStreamReader(进程.getInputStream(), StandardCharsets.UTF_8))) {
            String 行;
            while ((行 = 读取器.readLine()) != null) 追加(行 + "\n");
        }
        int 结果 = 进程.waitFor();
        进程 = null;
        追加(标签("result") + ": " + 结果 + "\n");
        return 结果;
    }

    private void 编译(boolean 运行) {
        if (!保存()) return;
        String 文件 = 目录.resolve(路径.getText()).toString();
        String 类名 = 名称.getText().trim();
        String 文本 = 参数.getText();
        工作线程.submit(() -> {
            try {
                Files.createDirectories(目录.resolve("classes"));
                int 结果 = 执行(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", 目录.resolve("classes").toString(), 文件));
                if (运行 && 结果 == 0) {
                    List<String> 命令 = new ArrayList<>(Arrays.asList("java", "-cp", 目录.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", 类名));
                    StreamTokenizer 解析器 = new StreamTokenizer(new StringReader(文本));
                    解析器.resetSyntax(); 解析器.wordChars(33, 65535); 解析器.whitespaceChars(0, 32);
                    解析器.quoteChar('"'); 解析器.quoteChar('\'');
                    while (解析器.nextToken() != StreamTokenizer.TT_EOF) 命令.add(解析器.sval);
                    执行(命令);
                }
            } catch (Exception 异常) { 错误(异常); }
        });
    }

    private void 停止() {
        Process 当前进程 = 进程;
        if (当前进程 != null) {
            当前进程.descendants().forEach(ProcessHandle::destroyForcibly);
            当前进程.destroyForcibly();
        }
    }

    private void 终端() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(目录.toFile()).start(); }
        catch (Exception 异常) { 错误(异常); }
    }

    private void 选择() {
        JFileChooser 选择器 = new JFileChooser(目录.toFile());
        if (选择器.showOpenDialog(窗口) == JFileChooser.APPROVE_OPTION) {
            路径.setText(选择器.getSelectedFile().getAbsolutePath());
            加载();
        }
    }

    private void 初始化() {
        try (Reader 读取器 = new InputStreamReader(工作坊.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            消息.load(读取器);
            Files.createDirectories(目录);
        } catch (Exception 异常) { throw new IllegalStateException(异常); }
        窗口.setTitle(标签("workspace") + " · WorldOS " + 标签("identity"));
        窗口.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窗口.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent 事件) {
                停止(); 工作线程.shutdownNow(); System.exit(0);
            }
        });
        源文.setFont(new Font("Monospaced", Font.PLAIN, 17));
        源文.setTabSize(4);
        输出.setFont(new Font("Monospaced", Font.PLAIN, 14));
        输出.setEditable(false);
        JPanel 面板 = new JPanel(new GridLayout(0, 1));
        JPanel 文件 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        文件.add(new JLabel(标签("file"))); 文件.add(路径);
        面板.add(文件);
        JPanel 工具栏 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        按钮(工具栏, "open", () -> 选择());
        按钮(工具栏, "save", () -> 保存());
        按钮(工具栏, "compile", () -> 编译(false));
        按钮(工具栏, "run", () -> 编译(true));
        按钮(工具栏, "stop", () -> 停止());
        按钮(工具栏, "terminal", () -> 终端());
        面板.add(工具栏);
        JPanel 设置 = new JPanel(new FlowLayout(FlowLayout.LEADING));
        设置.add(new JLabel(标签("class"))); 设置.add(名称);
        设置.add(new JLabel(标签("arguments"))); 设置.add(参数);
        面板.add(设置);
        JSplitPane 分割 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(源文), new JScrollPane(输出));
        分割.setResizeWeight(0.72);
        窗口.add(面板, BorderLayout.NORTH);
        窗口.add(分割, BorderLayout.CENTER);
        面板.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(标签("locale"))));
        分割.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        源文.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        输出.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension 大小 = Toolkit.getDefaultToolkit().getScreenSize();
        窗口.setSize(Math.min(1240, 大小.width - 40), Math.min(760, 大小.height - 60));
        窗口.setLocationRelativeTo(null);
        窗口.setVisible(true);
        加载();
        分割.setDividerLocation(0.72);
        追加("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        追加(标签("help") + "\n");
    }

    public static void main(String[] 参数) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new 工作坊().初始化());
    }
}
