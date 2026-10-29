// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자바;

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

/** потребител 홈에서 Java 원문을 редакция_стойност·компилирам_източник·실행하는 작은 Swing работна_област. */
public final class работна_област {
    private final JFrame Прозорец = new JFrame("jkoros — 자바 работна_област");
    private final JTextArea ИЗТОЧНИК = new JTextArea();
    private final JTextArea Изход = new JTextArea(8, 80);
    private final JTextField Файл_запис_препратка_към_клетка = new JTextField("인사.java", 20);
    private final JTextField Клас_запис_препратка_към_клетка = new JTextField("인사", 16);
    private final Path 작업폴더 = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process Процес_стойност;
    private final String библиотека = "/opt/jkoros/lib/한국어자바.jar";

    private void предупреждение(String Текст) { SwingUtilities.invokeLater(() -> Изход.append(Текст + "\n")); }
    private void бутон(JPanel версия_стойност, String Име, Runnable 행동) {
        JButton бутон = new JButton(Име);
        бутон.addActionListener(Събитие -> 행동.run());
        версия_стойност.add(бутон);
    }
    private boolean хранилище_стойност() {
        try {
            Path ПЪТ = 작업폴더.resolve(Файл_запис_препратка_към_клетка.getText());
            Files.createDirectories(ПЪТ.getParent());
            Файл.Писане(ПЪТ, ИЗТОЧНИК.getText());
            предупреждение("хранилище_стойност: " + ПЪТ);
            return true;
        } catch (Exception ГРЕШКА) { предупреждение(ГРЕШКА.toString()); return false; }
    }
    private void Отваряне() {
        try { ИЗТОЧНИК.setText(Файл.Четене(작업폴더.resolve(Файл_запис_препратка_към_клетка.getText()))); }
        catch (Exception ГРЕШКА) { предупреждение(ГРЕШКА.toString()); }
    }
    private int Команда(List<String> Команда) throws Exception {
        Процес_стойност = new ProcessBuilder(Команда).directory(작업폴더.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ред = new BufferedReader(new InputStreamReader(Процес_стойност.getInputStream(), StandardCharsets.UTF_8))) {
            String Текст;
            while ((Текст = ред.readLine()) != null) предупреждение(Текст);
        }
        int Състояние_стойност = Процес_стойност.waitFor(); Процес_стойност = null;
        предупреждение("Изход_програма код_стойност: " + Състояние_стойност);
        return Състояние_стойност;
    }
    private void Превод_източник(boolean изпълнявам_команда, boolean 실행파일) {
        if (!хранилище_стойност()) return;
        String 입력 = Файл_запис_препратка_към_клетка.getText(), запис_пункт_стойност = Клас_запис_препратка_към_клетка.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(작업폴더.resolve("classes"));
                if (실행파일) {
                    Команда(Arrays.asList("jclassc", "--target", "openjdk", "--entry", запис_пункт_стойност,
                        "--classpath", библиотека, "-o", "실행프로그램", 입력));
                } else if (Команда(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", библиотека,
                        "-d", "classes", 입력)) == 0 && изпълнявам_команда) {
                    Команда(Arrays.asList("java", "-cp", "classes:" + библиотека, запис_пункт_стойност));
                }
            } catch (Exception ГРЕШКА) { предупреждение(ГРЕШКА.toString()); }
        });
    }
    private void 멈춤() {
        Process в_срок_артикул = Процес_стойност;
        if (в_срок_артикул != null) { в_срок_артикул.descendants().forEach(ProcessHandle::destroy); в_срок_артикул.destroy(); }
    }
    private работна_област() throws IOException {
        Files.createDirectories(작업폴더);
        Font шрифт_стойност = new Font("Monospaced", Font.PLAIN, 16);
        ИЗТОЧНИК.setFont(шрифт_стойност); Изход.setFont(шрифт_стойност); Изход.setEditable(false);
        ИЗТОЧНИК.setTabSize(4);
        ИЗТОЧНИК.setMargin(new Insets(10, 12, 10, 12));
        Изход.setMargin(new Insets(8, 12, 8, 12));
        ИЗТОЧНИК.setBackground(new Color(250, 251, 252));
        ИЗТОЧНИК.setForeground(new Color(32, 43, 58));
        JPanel команда_панел = new JPanel();
        команда_панел.add(new JLabel("Файл")); команда_панел.add(Файл_запис_препратка_към_клетка);
        команда_панел.add(new JLabel("주 Клас_стойност")); команда_панел.add(Клас_запис_препратка_към_клетка);
        бутон(команда_панел, "Отваряне", this::Отваряне); бутон(команда_панел, "хранилище_стойност", this::хранилище_стойност);
        бутон(команда_панел, "компилирам_източник", () -> Превод_източник(false, false));
        бутон(команда_панел, "изпълнявам_команда", () -> Превод_източник(true, false));
        бутон(команда_панел, "изпълнявам_команда Файл Създаване_запис", () -> Превод_източник(false, true));
        бутон(команда_панел, "멈춤", this::멈춤);
        JSplitPane отдел_мярка = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ИЗТОЧНИК), new JScrollPane(Изход));
        отдел_мярка.setResizeWeight(0.75);
        Прозорец.add(команда_панел, BorderLayout.NORTH); Прозорец.add(отдел_мярка, BorderLayout.CENTER);
        Прозорец.setSize(1200, 750); Прозорец.setLocationRelativeTo(null);
        Прозорец.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Прозорец.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Събитие) { 멈춤(); 일꾼.shutdownNow(); }
        });
        Отваряне(); Прозорец.setVisible(true);
    }
    public static void main(String[] Параметри) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource шрифт_по_подразбиране = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object запис_стойност : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(запис_стойност) instanceof Font) UIManager.put(запис_стойност, шрифт_по_подразбиране);
                }
                new работна_област();
            } catch (Exception ГРЕШКА) { ГРЕШКА.printStackTrace(); }
        });
    }
}
