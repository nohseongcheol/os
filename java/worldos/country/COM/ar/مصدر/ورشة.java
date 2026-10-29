// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.COM.l_ar;
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
public final class ورشة {
    private final JFrame نافذة = new JFrame();
    private final JTextArea مصدر = new JTextArea();
    private final JTextArea مخرجات = new JTextArea();
    private final JTextField مسار = new JTextField("مصدر.java", 26);
    private final JTextField اسم = new JTextField("مصدر", 15);
    private final JTextField وسائط = new JTextField(25);
    private final Properties رسائل = new Properties();
    private final Path دليل = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService خيطالعمل = Executors.newSingleThreadExecutor();
    private volatile Process عملية;

    private String تسمية(String مفتاح) {
        return رسائل.getProperty(مفتاح, مفتاح);
    }

    private void إلحاق(String نص) {
        SwingUtilities.invokeLater(() -> {
            مخرجات.append(نص);
            مخرجات.setCaretPosition(مخرجات.getDocument().getLength());
        });
    }

    private void خطأ(Exception استثناء) {
        إلحاق(تسمية("error") + ": " + استثناء.toString() + "\n");
    }

    private void زر(JPanel لوحة, String مفتاح, Runnable إجراء) {
        JButton زر = new JButton(تسمية(مفتاح));
        زر.addActionListener(حدث -> إجراء.run());
        لوحة.add(زر);
    }

    private void تحميل() {
        try {
            مصدر.setText(Files.readString(دليل.resolve(مسار.getText()), StandardCharsets.UTF_8));
            مصدر.setCaretPosition(0);
        } catch (Exception استثناء) { خطأ(استثناء); }
    }

    private boolean حفظ() {
        try {
            Path ملف = دليل.resolve(مسار.getText()).normalize();
            Files.createDirectories(ملف.getParent());
            Files.writeString(ملف, مصدر.getText(), StandardCharsets.UTF_8);
            إلحاق(تسمية("save") + ": " + ملف + "\n");
            return true;
        } catch (Exception استثناء) { خطأ(استثناء); return false; }
    }

    private int تنفيذ(List<String> أمر) throws Exception {
        عملية = new ProcessBuilder(أمر).directory(دليل.toFile()).redirectErrorStream(true).start();
        try (BufferedReader قارئ = new BufferedReader(new InputStreamReader(عملية.getInputStream(), StandardCharsets.UTF_8))) {
            String سطر;
            while ((سطر = قارئ.readLine()) != null) إلحاق(سطر + "\n");
        }
        int نتيجة = عملية.waitFor();
        عملية = null;
        إلحاق(تسمية("result") + ": " + نتيجة + "\n");
        return نتيجة;
    }

    private void ترجمة(boolean تشغيل) {
        if (!حفظ()) return;
        String ملف = دليل.resolve(مسار.getText()).toString();
        String اسمالصنف = اسم.getText().trim();
        String نص = وسائط.getText();
        خيطالعمل.submit(() -> {
            try {
                Files.createDirectories(دليل.resolve("classes"));
                int نتيجة = تنفيذ(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", دليل.resolve("classes").toString(), ملف));
                if (تشغيل && نتيجة == 0) {
                    List<String> أمر = new ArrayList<>(Arrays.asList("java", "-cp", دليل.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", اسمالصنف));
                    StreamTokenizer محلل = new StreamTokenizer(new StringReader(نص));
                    محلل.resetSyntax(); محلل.wordChars(33, 65535); محلل.whitespaceChars(0, 32);
                    محلل.quoteChar('"'); محلل.quoteChar('\'');
                    while (محلل.nextToken() != StreamTokenizer.TT_EOF) أمر.add(محلل.sval);
                    تنفيذ(أمر);
                }
            } catch (Exception استثناء) { خطأ(استثناء); }
        });
    }

    private void إيقاف() {
        Process العمليةالحالية = عملية;
        if (العمليةالحالية != null) {
            العمليةالحالية.descendants().forEach(ProcessHandle::destroyForcibly);
            العمليةالحالية.destroyForcibly();
        }
    }

    private void طرفية() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(دليل.toFile()).start(); }
        catch (Exception استثناء) { خطأ(استثناء); }
    }

    private void اختيار() {
        JFileChooser منتقي = new JFileChooser(دليل.toFile());
        if (منتقي.showOpenDialog(نافذة) == JFileChooser.APPROVE_OPTION) {
            مسار.setText(منتقي.getSelectedFile().getAbsolutePath());
            تحميل();
        }
    }

    private void تهيئة() {
        try (Reader قارئ = new InputStreamReader(ورشة.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            رسائل.load(قارئ);
            Files.createDirectories(دليل);
        } catch (Exception استثناء) { throw new IllegalStateException(استثناء); }
        نافذة.setTitle(تسمية("workspace") + " · WorldOS " + تسمية("identity"));
        نافذة.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        نافذة.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent حدث) {
                إيقاف(); خيطالعمل.shutdownNow(); System.exit(0);
            }
        });
        مصدر.setFont(new Font("Monospaced", Font.PLAIN, 17));
        مصدر.setTabSize(4);
        مخرجات.setFont(new Font("Monospaced", Font.PLAIN, 14));
        مخرجات.setEditable(false);
        JPanel لوحة = new JPanel(new GridLayout(0, 1));
        JPanel ملف = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ملف.add(new JLabel(تسمية("file"))); ملف.add(مسار);
        لوحة.add(ملف);
        JPanel شريطالأدوات = new JPanel(new FlowLayout(FlowLayout.LEADING));
        زر(شريطالأدوات, "open", () -> اختيار());
        زر(شريطالأدوات, "save", () -> حفظ());
        زر(شريطالأدوات, "compile", () -> ترجمة(false));
        زر(شريطالأدوات, "run", () -> ترجمة(true));
        زر(شريطالأدوات, "stop", () -> إيقاف());
        زر(شريطالأدوات, "terminal", () -> طرفية());
        لوحة.add(شريطالأدوات);
        JPanel إعدادات = new JPanel(new FlowLayout(FlowLayout.LEADING));
        إعدادات.add(new JLabel(تسمية("class"))); إعدادات.add(اسم);
        إعدادات.add(new JLabel(تسمية("arguments"))); إعدادات.add(وسائط);
        لوحة.add(إعدادات);
        JSplitPane تقسيم = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(مصدر), new JScrollPane(مخرجات));
        تقسيم.setResizeWeight(0.72);
        نافذة.add(لوحة, BorderLayout.NORTH);
        نافذة.add(تقسيم, BorderLayout.CENTER);
        لوحة.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(تسمية("locale"))));
        تقسيم.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        مصدر.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        مخرجات.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension حجم = Toolkit.getDefaultToolkit().getScreenSize();
        نافذة.setSize(Math.min(1240, حجم.width - 40), Math.min(760, حجم.height - 60));
        نافذة.setLocationRelativeTo(null);
        نافذة.setVisible(true);
        تحميل();
        تقسيم.setDividerLocation(0.72);
        إلحاق("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        إلحاق(تسمية("help") + "\n");
    }

    public static void main(String[] وسائط) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new ورشة().تهيئة());
    }
}
