// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.자바;

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

/** пространство_пользователя 홈에서 Java 원문을 правка_ЗНАЧЕН·компилировать_источник·실행하는 작은 Swing рабочая_область. */
public final class рабочая_область {
    private final JFrame Окно = new JFrame("jkoros — 자바 рабочая_область");
    private final JTextArea исходныйКод = new JTextArea();
    private final JTextArea текстовыйВывод = new JTextArea(8, 80);
    private final JTextField файл_ввод_имя = new JTextField("приветствие_ae353e94.java", 20);
    private final JTextField Класс_ввод_имя = new JTextField("приветствие_ae353e94", 16);
    private final Path рабочая_папка = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService работник_ЗНАЧЕН = Executors.newSingleThreadExecutor();
    private volatile Process Процесс_ЗНАЧЕН;
    private final String библиотека = "/opt/jkoros/lib/한국어자바.jar";

    private void уведомление(String текст) { SwingUtilities.invokeLater(() -> текстовыйВывод.append(текст + "\n")); }
    private void кнопка(JPanel версия_ЗНАЧЕН_65c6ecdc, String Название, Runnable 행동) {
        JButton кнопка = new JButton(Название);
        кнопка.addActionListener(Событие -> 행동.run());
        версия_ЗНАЧЕН_65c6ecdc.add(кнопка);
    }
    private boolean Store_ЗНАЧЕН() {
        try {
            Path путь = рабочая_папка.resolve(файл_ввод_имя.getText());
            Files.createDirectories(путь.getParent());
            файл.Запись(путь, исходныйКод.getText());
            уведомление("Store_ЗНАЧЕН: " + путь);
            return true;
        } catch (Exception ошибка) { уведомление(ошибка.toString()); return false; }
    }
    private void Открыть() {
        try { исходныйКод.setText(файл.Чтение(рабочая_папка.resolve(файл_ввод_имя.getText()))); }
        catch (Exception ошибка) { уведомление(ошибка.toString()); }
    }
    private int команда(List<String> команда) throws Exception {
        Процесс_ЗНАЧЕН = new ProcessBuilder(команда).directory(рабочая_папка.toFile()).redirectErrorStream(true).start();
        try (BufferedReader строка_ввода = new BufferedReader(new InputStreamReader(Процесс_ЗНАЧЕН.getInputStream(), StandardCharsets.UTF_8))) {
            String текст;
            while ((текст = строка_ввода.readLine()) != null) уведомление(текст);
        }
        int Состояние_ЗНАЧЕН = Процесс_ЗНАЧЕН.waitFor(); Процесс_ЗНАЧЕН = null;
        уведомление("Выход_программа кодовое_значение: " + Состояние_ЗНАЧЕН);
        return Состояние_ЗНАЧЕН;
    }
    private void ПЕРЕВОД_источник(boolean 실행, boolean исполняемый_файл) {
        if (!Store_ЗНАЧЕН()) return;
        String входные_данные_ЗНАЧЕН = файл_ввод_имя.getText(), точка_входа_ЗНАЧЕН = Класс_ввод_имя.getText();
        работник_ЗНАЧЕН.submit(() -> {
            try {
                Files.createDirectories(рабочая_папка.resolve("classes"));
                if (исполняемый_файл) {
                    команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", точка_входа_ЗНАЧЕН,
                        "--classpath", библиотека, "-o", "실행프로그램", входные_данные_ЗНАЧЕН));
                } else if (команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", библиотека,
                        "-d", "classes", входные_данные_ЗНАЧЕН)) == 0 && 실행) {
                    команда(Arrays.asList("java", "-cp", "classes:" + библиотека, точка_входа_ЗНАЧЕН));
                }
            } catch (Exception ошибка) { уведомление(ошибка.toString()); }
        });
    }
    private void пауза_выполнение() {
        Process текущий_товар = Процесс_ЗНАЧЕН;
        if (текущий_товар != null) { текущий_товар.descendants().forEach(ProcessHandle::destroy); текущий_товар.destroy(); }
    }
    private рабочая_область() throws IOException {
        Files.createDirectories(рабочая_папка);
        Font шрифт_ЗНАЧЕН = new Font("Monospaced", Font.PLAIN, 16);
        исходныйКод.setFont(шрифт_ЗНАЧЕН); текстовыйВывод.setFont(шрифт_ЗНАЧЕН); текстовыйВывод.setEditable(false);
        исходныйКод.setTabSize(4);
        исходныйКод.setMargin(new Insets(10, 12, 10, 12));
        текстовыйВывод.setMargin(new Insets(8, 12, 8, 12));
        исходныйКод.setBackground(new Color(250, 251, 252));
        исходныйКод.setForeground(new Color(32, 43, 58));
        JPanel 명령판 = new JPanel();
        명령판.add(new JLabel("файл")); 명령판.add(файл_ввод_имя);
        명령판.add(new JLabel("주 Класс_ЗНАЧЕН")); 명령판.add(Класс_ввод_имя);
        кнопка(명령판, "Открыть", this::Открыть); кнопка(명령판, "Store_ЗНАЧЕН", this::Store_ЗНАЧЕН);
        кнопка(명령판, "компилировать_источник", () -> ПЕРЕВОД_источник(false, false));
        кнопка(명령판, "실행", () -> ПЕРЕВОД_источник(true, false));
        кнопка(명령판, "실행 файл Create_ввод", () -> ПЕРЕВОД_источник(false, true));
        кнопка(명령판, "пауза_выполнение", this::пауза_выполнение);
        JSplitPane отдел_KR = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(исходныйКод), new JScrollPane(текстовыйВывод));
        отдел_KR.setResizeWeight(0.75);
        Окно.add(명령판, BorderLayout.NORTH); Окно.add(отдел_KR, BorderLayout.CENTER);
        Окно.setSize(1200, 750); Окно.setLocationRelativeTo(null);
        Окно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Окно.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Событие) { пауза_выполнение(); работник_ЗНАЧЕН.shutdownNow(); }
        });
        Открыть(); Окно.setVisible(true);
    }
    public static void main(String[] аргументы) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource шрифт_по_умолчанию = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ввод_ЗНАЧЕН : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ввод_ЗНАЧЕН) instanceof Font) UIManager.put(ввод_ЗНАЧЕН, шрифт_по_умолчанию);
                }
                new рабочая_область();
            } catch (Exception ошибка) { ошибка.printStackTrace(); }
        });
    }
}
