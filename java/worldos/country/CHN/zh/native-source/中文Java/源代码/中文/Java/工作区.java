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

/** 在用户主目录编辑、编译和运行 Java 源码的小型 Swing 工作区。 */
public final class 工作区 {
    private final JFrame 窗口 = new JFrame("jkoros — Java 工作区");
    private final JTextArea 源代码 = new JTextArea();
    private final JTextArea 输出 = new JTextArea(8, 80);
    private final JTextField 文件条目名称 = new JTextField("问候例.java", 20);
    private final JTextField 类条目名称 = new JTextField("问候例", 16);
    private final Path 工作中目录 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 后台任务值 = Executors.newSingleThreadExecutor();
    private volatile Process 进程值;
    private final String 库 = "/opt/jkoros/lib/中文Java.jar";

    private void 通知(String 文本) { SwingUtilities.invokeLater(() -> 输出.append(文本 + "\n")); }
    private void 按钮(JPanel 版本值, String 名称, Runnable 行为值) {
        JButton 按钮 = new JButton(名称);
        按钮.addActionListener(事件 -> 行为值.run());
        版本值.add(按钮);
    }
    private boolean 存储值() {
        try {
            Path 路径 = 工作中目录.resolve(文件条目名称.getText());
            Files.createDirectories(路径.getParent());
            文件.写入(路径, 源代码.getText());
            通知("存储值: " + 路径);
            return true;
        } catch (Exception 错误) { 通知(错误.toString()); return false; }
    }
    private void 打开() {
        try { 源代码.setText(文件.读取(工作中目录.resolve(文件条目名称.getText()))); }
        catch (Exception 错误) { 通知(错误.toString()); }
    }
    private int 命令(List<String> 命令) throws Exception {
        进程值 = new ProcessBuilder(命令).directory(工作中目录.toFile()).redirectErrorStream(true).start();
        try (BufferedReader 行 = new BufferedReader(new InputStreamReader(进程值.getInputStream(), StandardCharsets.UTF_8))) {
            String 文本;
            while ((文本 = 行.readLine()) != null) 通知(文本);
        }
        int 状态值 = 进程值.waitFor(); 进程值 = null;
        通知("退出程序 代码值: " + 状态值);
        return 状态值;
    }
    private void 翻译源代码(boolean 执行命令, boolean 可执行文件文件) {
        if (!存储值()) return;
        String 输入值 = 文件条目名称.getText(), 条目分值 = 类条目名称.getText();
        后台任务值.submit(() -> {
            try {
                Files.createDirectories(工作中目录.resolve("classes"));
                if (可执行文件文件) {
                    命令(Arrays.asList("jclassc", "--target", "openjdk", "--entry", 条目分值,
                        "--classpath", 库, "-o", "실행프로그램", 输入值));
                } else if (命令(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", 库,
                        "-d", "classes", 输入值)) == 0 && 执行命令) {
                    命令(Arrays.asList("java", "-cp", "classes:" + 库, 条目分值));
                }
            } catch (Exception 错误) { 通知(错误.toString()); }
        });
    }
    private void 暂停执行状态() {
        Process 当前项目 = 进程值;
        if (当前项目 != null) { 当前项目.descendants().forEach(ProcessHandle::destroy); 当前项目.destroy(); }
    }
    private 工作区() throws IOException {
        Files.createDirectories(工作中目录);
        Font 字体值 = new Font("Monospaced", Font.PLAIN, 16);
        源代码.setFont(字体值); 输出.setFont(字体值); 输出.setEditable(false);
        源代码.setTabSize(4);
        源代码.setMargin(new Insets(10, 12, 10, 12));
        输出.setMargin(new Insets(8, 12, 8, 12));
        源代码.setBackground(new Color(250, 251, 252));
        源代码.setForeground(new Color(32, 43, 58));
        JPanel 命令面板 = new JPanel();
        命令面板.add(new JLabel("文件")); 命令面板.add(文件条目名称);
        命令面板.add(new JLabel("주 类值")); 命令面板.add(类条目名称);
        按钮(命令面板, "打开", this::打开); 按钮(命令面板, "存储值", this::存储值);
        按钮(命令面板, "编译源代码", () -> 翻译源代码(false, false));
        按钮(命令面板, "执行命令", () -> 翻译源代码(true, false));
        按钮(命令面板, "执行命令 文件 创建条目", () -> 翻译源代码(false, true));
        按钮(命令面板, "暂停执行状态", this::暂停执行状态);
        JSplitPane 除法结果 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(源代码), new JScrollPane(输出));
        除法结果.setResizeWeight(0.75);
        窗口.add(命令面板, BorderLayout.NORTH); 窗口.add(除法结果, BorderLayout.CENTER);
        窗口.setSize(1200, 750); 窗口.setLocationRelativeTo(null);
        窗口.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        窗口.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent 事件) { 暂停执行状态(); 后台任务值.shutdownNow(); }
        });
        打开(); 窗口.setVisible(true);
    }
    public static void main(String[] 实参) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource 默认字体 = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object 条目值 : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(条目值) instanceof Font) UIManager.put(条目值, 默认字体);
                }
                new 工作区();
            } catch (Exception 错误) { 错误.printStackTrace(); }
        });
    }
}
