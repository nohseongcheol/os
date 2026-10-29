// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Java;

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

/** Small Swing workspace for editing, compiling and running Java sources in the user's home directory. */
public final class Workspace {
    private final JFrame window = new JFrame("jkoros — Java Workspace");
    private final JTextArea source = new JTextArea();
    private final JTextArea Output = new JTextArea(8, 80);
    private final JTextField fileEntryName = new JTextField("Greeting.java", 20);
    private final JTextField classEntryName = new JTextField("Greeting", 16);
    private final Path workingDirectory = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService workerValue = Executors.newSingleThreadExecutor();
    private volatile Process processValue;
    private final String library = "/opt/jkoros/lib/NativeJava.jar";

    private void notice(String text) { SwingUtilities.invokeLater(() -> Output.append(text + "\n")); }
    private void button(JPanel versionValue, String name, Runnable behaviourValue) {
        JButton button = new JButton(name);
        button.addActionListener(event -> behaviourValue.run());
        versionValue.add(button);
    }
    private boolean storeValue() {
        try {
            Path path = workingDirectory.resolve(fileEntryName.getText());
            Files.createDirectories(path.getParent());
            file.write(path, source.getText());
            notice("storeValue: " + path);
            return true;
        } catch (Exception error) { notice(error.toString()); return false; }
    }
    private void open() {
        try { source.setText(file.read(workingDirectory.resolve(fileEntryName.getText()))); }
        catch (Exception error) { notice(error.toString()); }
    }
    private int command(List<String> command) throws Exception {
        processValue = new ProcessBuilder(command).directory(workingDirectory.toFile()).redirectErrorStream(true).start();
        try (BufferedReader line = new BufferedReader(new InputStreamReader(processValue.getInputStream(), StandardCharsets.UTF_8))) {
            String text;
            while ((text = line.readLine()) != null) notice(text);
        }
        int stateValue = processValue.waitFor(); processValue = null;
        notice("exitProgram codeValue: " + stateValue);
        return stateValue;
    }
    private void translateSource(boolean executeCommand, boolean executableFile) {
        if (!storeValue()) return;
        String inputValue = fileEntryName.getText(), entryPointValue = classEntryName.getText();
        workerValue.submit(() -> {
            try {
                Files.createDirectories(workingDirectory.resolve("classes"));
                if (executableFile) {
                    command(Arrays.asList("jclassc", "--target", "openjdk", "--entry", entryPointValue,
                        "--classpath", library, "-o", "실행프로그램", inputValue));
                } else if (command(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", library,
                        "-d", "classes", inputValue)) == 0 && executeCommand) {
                    command(Arrays.asList("java", "-cp", "classes:" + library, entryPointValue));
                }
            } catch (Exception error) { notice(error.toString()); }
        });
    }
    private void pauseExecution() {
        Process currentItem = processValue;
        if (currentItem != null) { currentItem.descendants().forEach(ProcessHandle::destroy); currentItem.destroy(); }
    }
    private Workspace() throws IOException {
        Files.createDirectories(workingDirectory);
        Font fontValue = new Font("Monospaced", Font.PLAIN, 16);
        source.setFont(fontValue); Output.setFont(fontValue); Output.setEditable(false);
        source.setTabSize(4);
        source.setMargin(new Insets(10, 12, 10, 12));
        Output.setMargin(new Insets(8, 12, 8, 12));
        source.setBackground(new Color(250, 251, 252));
        source.setForeground(new Color(32, 43, 58));
        JPanel commandPanel = new JPanel();
        commandPanel.add(new JLabel("file")); commandPanel.add(fileEntryName);
        commandPanel.add(new JLabel("주 classValue")); commandPanel.add(classEntryName);
        button(commandPanel, "open", this::open); button(commandPanel, "storeValue", this::storeValue);
        button(commandPanel, "compileSource", () -> translateSource(false, false));
        button(commandPanel, "executeCommand", () -> translateSource(true, false));
        button(commandPanel, "executeCommand file createEntry", () -> translateSource(false, true));
        button(commandPanel, "pauseExecution", this::pauseExecution);
        JSplitPane divisionResult = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(source), new JScrollPane(Output));
        divisionResult.setResizeWeight(0.75);
        window.add(commandPanel, BorderLayout.NORTH); window.add(divisionResult, BorderLayout.CENTER);
        window.setSize(1200, 750); window.setLocationRelativeTo(null);
        window.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        window.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent event) { pauseExecution(); workerValue.shutdownNow(); }
        });
        open(); window.setVisible(true);
    }
    public static void main(String[] arguments) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource defaultFont = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object entryValue : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(entryValue) instanceof Font) UIManager.put(entryValue, defaultFont);
                }
                new Workspace();
            } catch (Exception error) { error.printStackTrace(); }
        });
    }
}
