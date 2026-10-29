// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.POL.l_ru;
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
public final class РабочаяСреда {
    private final JFrame Окно = new JFrame();
    private final JTextArea исходныйКод = new JTextArea();
    private final JTextArea текстовыйВывод = new JTextArea();
    private final JTextField путь = new JTextField("исходныйКод.java", 26);
    private final JTextField Название = new JTextField("исходныйКод", 15);
    private final JTextField аргументы = new JTextField(25);
    private final Properties сообщения = new Properties();
    private final Path каталог = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService фоноваяЗадача = Executors.newSingleThreadExecutor();
    private volatile Process Процесс;

    private String Метка(String Ключ) {
        return сообщения.getProperty(Ключ, Ключ);
    }

    private void добавить_в_конец_списка(String текст) {
        SwingUtilities.invokeLater(() -> {
            текстовыйВывод.append(текст);
            текстовыйВывод.setCaretPosition(текстовыйВывод.getDocument().getLength());
        });
    }

    private void ошибка(Exception exception) {
        добавить_в_конец_списка(Метка("error") + ": " + exception.toString() + "\n");
    }

    private void кнопка(JPanel Панель, String Ключ, Runnable Действие) {
        JButton кнопка = new JButton(Метка(Ключ));
        кнопка.addActionListener(Событие -> Действие.run());
        Панель.add(кнопка);
    }

    private void загрузитьИсходник() {
        try {
            исходныйКод.setText(Files.readString(каталог.resolve(путь.getText()), StandardCharsets.UTF_8));
            исходныйКод.setCaretPosition(0);
        } catch (Exception exception) { ошибка(exception); }
    }

    private boolean Сохранить() {
        try {
            Path файл = каталог.resolve(путь.getText()).normalize();
            Files.createDirectories(файл.getParent());
            Files.writeString(файл, исходныйКод.getText(), StandardCharsets.UTF_8);
            добавить_в_конец_списка(Метка("save") + ": " + файл + "\n");
            return true;
        } catch (Exception exception) { ошибка(exception); return false; }
    }

    private int Выполнить(List<String> команда) throws Exception {
        Процесс = new ProcessBuilder(команда).directory(каталог.toFile()).redirectErrorStream(true).start();
        try (BufferedReader считывательТекста = new BufferedReader(new InputStreamReader(Процесс.getInputStream(), StandardCharsets.UTF_8))) {
            String строка_ввода;
            while ((строка_ввода = считывательТекста.readLine()) != null) добавить_в_конец_списка(строка_ввода + "\n");
        }
        int результат = Процесс.waitFor();
        Процесс = null;
        добавить_в_конец_списка(Метка("result") + ": " + результат + "\n");
        return результат;
    }

    private void компилировать(boolean запустить) {
        if (!Сохранить()) return;
        String файл = каталог.resolve(путь.getText()).toString();
        String Класс = Название.getText().trim();
        String текст = аргументы.getText();
        фоноваяЗадача.submit(() -> {
            try {
                Files.createDirectories(каталог.resolve("classes"));
                int результат = Выполнить(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", каталог.resolve("classes").toString(), файл));
                if (запустить && результат == 0) {
                    List<String> команда = new ArrayList<>(Arrays.asList("java", "-cp", каталог.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", Класс));
                    StreamTokenizer анализаторАргументов = new StreamTokenizer(new StringReader(текст));
                    анализаторАргументов.resetSyntax(); анализаторАргументов.wordChars(33, 65535); анализаторАргументов.whitespaceChars(0, 32);
                    анализаторАргументов.quoteChar('"'); анализаторАргументов.quoteChar('\'');
                    while (анализаторАргументов.nextToken() != StreamTokenizer.TT_EOF) команда.add(анализаторАргументов.sval);
                    Выполнить(команда);
                }
            } catch (Exception exception) { ошибка(exception); }
        });
    }

    private void Остановить() {
        Process текущийПроцесс = Процесс;
        if (текущийПроцесс != null) {
            текущийПроцесс.descendants().forEach(ProcessHandle::destroyForcibly);
            текущийПроцесс.destroyForcibly();
        }
    }

    private void терминал() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(каталог.toFile()).start(); }
        catch (Exception exception) { ошибка(exception); }
    }

    private void выберите() {
        JFileChooser chooser = new JFileChooser(каталог.toFile());
        if (chooser.showOpenDialog(Окно) == JFileChooser.APPROVE_OPTION) {
            путь.setText(chooser.getSelectedFile().getAbsolutePath());
            загрузитьИсходник();
        }
    }

    private void инициализировать() {
        try (Reader считывательТекста = new InputStreamReader(РабочаяСреда.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            сообщения.load(считывательТекста);
            Files.createDirectories(каталог);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        Окно.setTitle(Метка("workspace") + " · WorldOS " + Метка("identity"));
        Окно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Окно.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent Событие) {
                Остановить(); фоноваяЗадача.shutdownNow(); System.exit(0);
            }
        });
        исходныйКод.setFont(new Font("Monospaced", Font.PLAIN, 17));
        исходныйКод.setTabSize(4);
        текстовыйВывод.setFont(new Font("Monospaced", Font.PLAIN, 14));
        текстовыйВывод.setEditable(false);
        JPanel Панель = new JPanel(new GridLayout(0, 1));
        JPanel файл = new JPanel(new FlowLayout(FlowLayout.LEADING));
        файл.add(new JLabel(Метка("file"))); файл.add(путь);
        Панель.add(файл);
        JPanel Панель_инструментов = new JPanel(new FlowLayout(FlowLayout.LEADING));
        кнопка(Панель_инструментов, "open", () -> выберите());
        кнопка(Панель_инструментов, "save", () -> Сохранить());
        кнопка(Панель_инструментов, "compile", () -> компилировать(false));
        кнопка(Панель_инструментов, "run", () -> компилировать(true));
        кнопка(Панель_инструментов, "stop", () -> Остановить());
        кнопка(Панель_инструментов, "terminal", () -> терминал());
        Панель.add(Панель_инструментов);
        JPanel Настройки = new JPanel(new FlowLayout(FlowLayout.LEADING));
        Настройки.add(new JLabel(Метка("class"))); Настройки.add(Название);
        Настройки.add(new JLabel(Метка("arguments"))); Настройки.add(аргументы);
        Панель.add(Настройки);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(исходныйКод), new JScrollPane(текстовыйВывод));
        split.setResizeWeight(0.72);
        Окно.add(Панель, BorderLayout.NORTH);
        Окно.add(split, BorderLayout.CENTER);
        Панель.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(Метка("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        исходныйКод.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        текстовыйВывод.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension Размер = Toolkit.getDefaultToolkit().getScreenSize();
        Окно.setSize(Math.min(1240, Размер.width - 40), Math.min(760, Размер.height - 60));
        Окно.setLocationRelativeTo(null);
        Окно.setVisible(true);
        загрузитьИсходник();
        split.setDividerLocation(0.72);
        добавить_в_конец_списка("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        добавить_в_конец_списка(Метка("help") + "\n");
    }

    public static void main(String[] аргументы) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new РабочаяСреда().инициализировать());
    }
}
