// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.자바;

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

/** משתמש 홈에서 Java 원문을 ערוך_ערך·בנה_מקור·실행하는 작은 Swing סביבת_עבודה. */
public final class סביבת_עבודה {
    private final JFrame חלון = new JFrame("jkoros — 자바 סביבת_עבודה");
    private final JTextArea קודמקור = new JTextArea();
    private final JTextArea פלטטקסט = new JTextArea(8, 80);
    private final JTextField קובץ_ערך_שם = new JTextField("인사.java", 20);
    private final JTextField כיתה_ערך_שם = new JTextField("인사", 16);
    private final Path ספריית_עבודה = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService עובד_ערך = Executors.newSingleThreadExecutor();
    private volatile Process תהליך_ערך;
    private final String ספריה = "/opt/jkoros/lib/한국어자바.jar";

    private void הודעה(String טקסט) { SwingUtilities.invokeLater(() -> פלטטקסט.append(טקסט + "\n")); }
    private void לחצן(JPanel גירסה_ערך, String שם, Runnable 행동) {
        JButton לחצן = new JButton(שם);
        לחצן.addActionListener(אירוע -> 행동.run());
        גירסה_ערך.add(לחצן);
    }
    private boolean מאגר_ערך() {
        try {
            Path נתיב = ספריית_עבודה.resolve(קובץ_ערך_שם.getText());
            Files.createDirectories(נתיב.getParent());
            קובץ.כתוב(נתיב, קודמקור.getText());
            הודעה("מאגר_ערך: " + נתיב);
            return true;
        } catch (Exception שגיאה) { הודעה(שגיאה.toString()); return false; }
    }
    private void פתח() {
        try { קודמקור.setText(קובץ.קרא(ספריית_עבודה.resolve(קובץ_ערך_שם.getText()))); }
        catch (Exception שגיאה) { הודעה(שגיאה.toString()); }
    }
    private int פקודה(List<String> פקודה) throws Exception {
        תהליך_ערך = new ProcessBuilder(פקודה).directory(ספריית_עבודה.toFile()).redirectErrorStream(true).start();
        try (BufferedReader שורה = new BufferedReader(new InputStreamReader(תהליך_ערך.getInputStream(), StandardCharsets.UTF_8))) {
            String טקסט;
            while ((טקסט = שורה.readLine()) != null) הודעה(טקסט);
        }
        int מצב_ערך = תהליך_ערך.waitFor(); תהליך_ערך = null;
        הודעה("יציאה_תוכנית קוד_ערך: " + מצב_ערך);
        return מצב_ערך;
    }
    private void תרגם_מקור(boolean לבצע_פקודה, boolean 실행파일) {
        if (!מאגר_ערך()) return;
        String קלט_ערך = קובץ_ערך_שם.getText(), נקודת_כניסה_ערך = כיתה_ערך_שם.getText();
        עובד_ערך.submit(() -> {
            try {
                Files.createDirectories(ספריית_עבודה.resolve("classes"));
                if (실행파일) {
                    פקודה(Arrays.asList("jclassc", "--target", "openjdk", "--entry", נקודת_כניסה_ערך,
                        "--classpath", ספריה, "-o", "실행프로그램", קלט_ערך));
                } else if (פקודה(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", ספריה,
                        "-d", "classes", קלט_ערך)) == 0 && לבצע_פקודה) {
                    פקודה(Arrays.asList("java", "-cp", "classes:" + ספריה, נקודת_כניסה_ערך));
                }
            } catch (Exception שגיאה) { הודעה(שגיאה.toString()); }
        });
    }
    private void 멈춤() {
        Process נוכחי_פריט = תהליך_ערך;
        if (נוכחי_פריט != null) { נוכחי_פריט.descendants().forEach(ProcessHandle::destroy); נוכחי_פריט.destroy(); }
    }
    private סביבת_עבודה() throws IOException {
        Files.createDirectories(ספריית_עבודה);
        Font גופן_ערך = new Font("Monospaced", Font.PLAIN, 16);
        קודמקור.setFont(גופן_ערך); פלטטקסט.setFont(גופן_ערך); פלטטקסט.setEditable(false);
        קודמקור.setTabSize(4);
        קודמקור.setMargin(new Insets(10, 12, 10, 12));
        פלטטקסט.setMargin(new Insets(8, 12, 8, 12));
        קודמקור.setBackground(new Color(250, 251, 252));
        קודמקור.setForeground(new Color(32, 43, 58));
        JPanel פקודה_לוח = new JPanel();
        פקודה_לוח.add(new JLabel("קובץ")); פקודה_לוח.add(קובץ_ערך_שם);
        פקודה_לוח.add(new JLabel("주 כיתה_ערך")); פקודה_לוח.add(כיתה_ערך_שם);
        לחצן(פקודה_לוח, "פתח", this::פתח); לחצן(פקודה_לוח, "מאגר_ערך", this::מאגר_ערך);
        לחצן(פקודה_לוח, "בנה_מקור", () -> תרגם_מקור(false, false));
        לחצן(פקודה_לוח, "לבצע_פקודה", () -> תרגם_מקור(true, false));
        לחצן(פקודה_לוח, "לבצע_פקודה קובץ ליצור_ערך", () -> תרגם_מקור(false, true));
        לחצן(פקודה_לוח, "멈춤", this::멈춤);
        JSplitPane בית_תוצאה = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(קודמקור), new JScrollPane(פלטטקסט));
        בית_תוצאה.setResizeWeight(0.75);
        חלון.add(פקודה_לוח, BorderLayout.NORTH); חלון.add(בית_תוצאה, BorderLayout.CENTER);
        חלון.setSize(1200, 750); חלון.setLocationRelativeTo(null);
        חלון.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        חלון.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent אירוע) { 멈춤(); עובד_ערך.shutdownNow(); }
        });
        פתח(); חלון.setVisible(true);
    }
    public static void main(String[] ארגומנטים) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource גופן_ברירת_מחדל = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object ערך_ערך : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(ערך_ערך) instanceof Font) UIManager.put(ערך_ערך, גופן_ברירת_מחדל);
                }
                new סביבת_עבודה();
            } catch (Exception שגיאה) { שגיאה.printStackTrace(); }
        });
    }
}
