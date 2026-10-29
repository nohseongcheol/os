// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.SRB.l_uk;
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
public final class РобочеСередовище {
    private final JFrame Вікно = new JFrame();
    private final JTextArea вихіднийКод = new JTextArea();
    private final JTextArea текстовеВиведення = new JTextArea();
    private final JTextField шлях = new JTextField("вихіднийКод.java", 26);
    private final JTextField Назва = new JTextField("вихіднийКод", 15);
    private final JTextField аргументи = new JTextField(25);
    private final Properties повідомлення = new Properties();
    private final Path каталог = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService фоноваЗадача = Executors.newSingleThreadExecutor();
    private volatile Process Процеси;

    private String Мітка(String Ключ) {
        return повідомлення.getProperty(Ключ, Ключ);
    }

    private void додати_в_кінець_списку(String текст) {
        SwingUtilities.invokeLater(() -> {
            текстовеВиведення.append(текст);
            текстовеВиведення.setCaretPosition(текстовеВиведення.getDocument().getLength());
        });
    }

    private void ПОМИЛКА(Exception exception) {
        додати_в_кінець_списку(Мітка("error") + ": " + exception.toString() + "\n");
    }

    private void кнопка(JPanel Панель, String Ключ, Runnable Дія) {
        JButton кнопка = new JButton(Мітка(Ключ));
        кнопка.addActionListener(Подія -> Дія.run());
        Панель.add(кнопка);
    }

    private void завантажитиДжерело() {
        try {
            вихіднийКод.setText(Files.readString(каталог.resolve(шлях.getText()), StandardCharsets.UTF_8));
            вихіднийКод.setCaretPosition(0);
        } catch (Exception exception) { ПОМИЛКА(exception); }
    }

    private boolean Зберегти() {
        try {
            Path файл = каталог.resolve(шлях.getText()).normalize();
            Files.createDirectories(файл.getParent());
            Files.writeString(файл, вихіднийКод.getText(), StandardCharsets.UTF_8);
            додати_в_кінець_списку(Мітка("save") + ": " + файл + "\n");
            return true;
        } catch (Exception exception) { ПОМИЛКА(exception); return false; }
    }

    private int Виконати(List<String> команда) throws Exception {
        Процеси = new ProcessBuilder(команда).directory(каталог.toFile()).redirectErrorStream(true).start();
        try (BufferedReader зчитувачТексту = new BufferedReader(new InputStreamReader(Процеси.getInputStream(), StandardCharsets.UTF_8))) {
            String рядок_введення;
            while ((рядок_введення = зчитувачТексту.readLine()) != null) додати_в_кінець_списку(рядок_введення + "\n");
        }
        int результат = Процеси.waitFor();
        Процеси = null;
        додати_в_кінець_списку(Мітка("result") + ": " + результат + "\n");
        return результат;
    }

    private void компілювати(boolean запустити) {
        if (!Зберегти()) return;
        String файл = каталог.resolve(шлях.getText()).toString();
        String Клас = Назва.getText().trim();
        String текст = аргументи.getText();
        фоноваЗадача.submit(() -> {
            try {
                Files.createDirectories(каталог.resolve("classes"));
                int результат = Виконати(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", каталог.resolve("classes").toString(), файл));
                if (запустити && результат == 0) {
                    List<String> команда = new ArrayList<>(Arrays.asList("java", "-cp", каталог.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Клас));
                    StreamTokenizer аналізаторАргументів = new StreamTokenizer(new StringReader(текст));
                    аналізаторАргументів.resetSyntax(); аналізаторАргументів.wordChars(33, 65535); аналізаторАргументів.whitespaceChars(0, 32);
                    аналізаторАргументів.quoteChar('"'); аналізаторАргументів.quoteChar('\'');
                    while (аналізаторАргументів.nextToken() != StreamTokenizer.TT_EOF) команда.add(аналізаторАргументів.sval);
                    Виконати(команда);
                }
            } catch (Exception exception) { ПОМИЛКА(exception); }
        });
    }

    private void Зупинити() {
        Process поточнийПроцес = Процеси;
        if (поточнийПроцес != null) {
            поточнийПроцес.descendants().forEach(ProcessHandle::destroyForcibly);
            поточнийПроцес.destroyForcibly();
        }
    }

    private void термінал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(каталог.toFile()).start(); }
        catch (Exception exception) { ПОМИЛКА(exception); }
    }

    private void вибрати() {
        JFileChooser chooser = new JFileChooser(каталог.toFile());
        if (chooser.showOpenDialog(Вікно) == JFileChooser.APPROVE_OPTION) {
            шлях.setText(chooser.getSelectedFile().getAbsolutePath());
            завантажитиДжерело();
        }
    }

    private void ініціалізувати() {
        try (Reader зчитувачТексту = new InputStreamReader(РобочеСередовище.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            повідомлення.load(зчитувачТексту);
            Files.createDirectories(каталог);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Вікно.setTitle(Мітка("workspace") + " · WorldOS " + Мітка("identity"));
        Вікно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Вікно.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Подія) {
                Зупинити(); фоноваЗадача.shutdownNow(); System.exit(0);
            }
        });
        вихіднийКод.setFont(new Font("Monospaced", Font.PLAIN, 17));
        вихіднийКод.setTabSize(4);
        текстовеВиведення.setFont(new Font("Monospaced", Font.PLAIN, 14));
        текстовеВиведення.setEditable(false);
        JPanel Панель = new JPanel(new GridLayout(0, 1));
        JPanel файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        файл.add(new JLabel(Мітка("file"))); файл.add(шлях);
        Панель.add(файл);
        JPanel Панель_знарядь = new JPanel(new FlowLayout(FlowLayout.LEADING));
        кнопка(Панель_знарядь, "open", () -> вибрати());
        кнопка(Панель_знарядь, "save", () -> Зберегти());
        кнопка(Панель_знарядь, "compile", () -> компілювати(false));
        кнопка(Панель_знарядь, "run", () -> компілювати(true));
        кнопка(Панель_знарядь, "stop", () -> Зупинити());
        кнопка(Панель_знарядь, "terminal", () -> термінал());
        Панель.add(Панель_знарядь);
        JPanel Налаштування = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Налаштування.add(new JLabel(Мітка("class"))); Налаштування.add(Назва);
        Налаштування.add(new JLabel(Мітка("arguments"))); Налаштування.add(аргументи);
        Панель.add(Налаштування);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(вихіднийКод), new JScrollPane(текстовеВиведення));
        split.setResizeWeight(0.72);
        Вікно.add(Панель, BorderLayout.NORTH);
        Вікно.add(split, BorderLayout.CENTER);
        Панель.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Мітка("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        вихіднийКод.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        текстовеВиведення.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Розмір = Toolkit.getDefaultToolkit().getScreenSize();
        Вікно.setSize(Math.min(1240, Розмір.width - 40), Math.min(760, Розмір.height - 60));
        Вікно.setLocationRelativeTo(null);
        Вікно.setVisible(true);
        завантажитиДжерело();
        split.setDividerLocation(0.72);
        додати_в_кінець_списку("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        додати_в_кінець_списку(Мітка("help") + "\n");
    }

    public static void main(String[] аргументи) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new РобочеСередовище().ініціалізувати());
    }
}
