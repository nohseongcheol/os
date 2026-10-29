// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.자바;

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

/** простір_користувача 홈에서 Java 원문을 правка_значення·компілювати_джерело·실행하는 작은 Swing робоча_область. */
public final class робоча_область {
    private final JFrame Вікно = new JFrame("jkoros — 자바 робоча_область");
    private final JTextArea вихіднийКод = new JTextArea();
    private final JTextArea Вивід = new JTextArea(8, 80);
    private final JTextField Файл_запис_ім_я = new JTextField("인사.java", 20);
    private final JTextField Клас_запис_ім_я = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process процес_значення;
    private final String бібліотека = "/opt/jkoros/lib/한국어자바.jar";

    private void повідомлення_12ddd6ca(String текст) { SwingUtilities.invokeLater(() -> Вивід.append(текст + "\n")); }
    private void кнопка(JPanel версія_значення, String Назва, Runnable 행동) {
        JButton кнопка = new JButton(Назва);
        кнопка.addActionListener(Подія -> 행동.run());
        версія_значення.add(кнопка);
    }
    private boolean сховище_значення() {
        try {
            Path шлях = 작업폴더.resolve(Файл_запис_ім_я.getText());
            Files.createDirectories(шлях.getParent());
            файл.Запис(шлях, вихіднийКод.getText());
            повідомлення_12ddd6ca("сховище_значення: " + шлях);
            return true;
        } catch (Exception ПОМИЛКА) { повідомлення_12ddd6ca(ПОМИЛКА.toString()); return false; }
    }
    private void Відкрити() {
        try { вихіднийКод.setText(файл.Читання(작업폴더.resolve(Файл_запис_ім_я.getText()))); }
        catch (Exception ПОМИЛКА) { повідомлення_12ddd6ca(ПОМИЛКА.toString()); }
    }
    private int команда(List<String> команда) throws Exception {
        процес_значення = new ProcessBuilder(команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader рядок_введення = new BufferedReader(new InputStreamReader(процес_значення.getInputStream(), StandardCharsets.UTF_8))) {
            String текст;
            while ((текст = рядок_введення.readLine()) != null) повідомлення_12ddd6ca(текст);
        }
        int Стан_значення = процес_значення.waitFor(); процес_значення = null;
        повідомлення_12ddd6ca("Вийти_програма код_значення: " + Стан_значення);
        return Стан_значення;
    }
    private void Перекласти_джерело(boolean Виконати_команда, boolean 실행파일) {
        if (!сховище_значення()) return;
        String 입력 = Файл_запис_ім_я.getText(), запис_бал_значення = Клас_запис_ім_я.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", запис_бал_значення,
                        "--classpath", бібліотека, "-o", "실행프로그램", 입력));
                } else if (команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", бібліотека,
                        "-d", "classes", 입력)) == 0 && Виконати_команда) {
                    команда(Arrays.asList("java", "-cp", "classes:" + бібліотека, запис_бал_значення));
                }
            } catch (Exception ПОМИЛКА) { повідомлення_12ddd6ca(ПОМИЛКА.toString()); }
        });
    }
    private void 멈춤() {
        Process чинний_елемент = процес_значення;
        if (чинний_елемент != null) { чинний_елемент.descendants().forEach(ProcessHandle::destroy); чинний_елемент.destroy(); }
    }
    private робоча_область() throws IOException {
        Files.createDirectories(작업폴더);
        Font шрифт_значення = new Font("Monospaced", Font.PLAIN, 16);
        вихіднийКод.setFont(шрифт_значення); Вивід.setFont(шрифт_значення); Вивід.setEditable(false);
        вихіднийКод.setTabSize(4);
        вихіднийКод.setMargin(new Insets(10, 12, 10, 12));
        Вивід.setMargin(new Insets(8, 12, 8, 12));
        вихіднийКод.setBackground(new Color(250, 251, 252));
        вихіднийКод.setForeground(new Color(32, 43, 58));
        JPanel команда_панель = new JPanel();
        команда_панель.add(new JLabel("файл")); команда_панель.add(Файл_запис_ім_я);
        команда_панель.add(new JLabel("주 Клас_значення")); команда_панель.add(Клас_запис_ім_я);
        кнопка(команда_панель, "Відкрити", this::Відкрити); кнопка(команда_панель, "сховище_значення", this::сховище_значення);
        кнопка(команда_панель, "компілювати_джерело", () -> Перекласти_джерело(false, false));
        кнопка(команда_панель, "Виконати_команда", () -> Перекласти_джерело(true, false));
        кнопка(команда_панель, "Виконати_команда файл Створення_запис", () -> Перекласти_джерело(false, true));
        кнопка(команда_панель, "멈춤", this::멈춤);
        JSplitPane ділення_КР = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(вихіднийКод), new JScrollPane(Вивід));
        ділення_КР.setResizeWeight(0.75);
        Вікно.add(команда_панель, BorderLayout.NORTH); Вікно.add(ділення_КР, BorderLayout.CENTER);
        Вікно.setSize(1200, 750); Вікно.setLocationRelativeTo(null);
        Вікно.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Вікно.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Подія) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Відкрити(); Вікно.setVisible(true);
    }
    public static void main(String[] аргументи) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource шрифт_за_замовчуванням = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object запис_значення_962f286b : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(запис_значення_962f286b) instanceof Font) UIManager.put(запис_значення_962f286b, шрифт_за_замовчуванням);
                }
                new робоча_область();
            } catch (Exception ПОМИЛКА) { ПОМИЛКА.printStackTrace(); }
        });
    }
}
