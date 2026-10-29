// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.ISR.l_he;
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
public final class סביבתעבודה {
    private final JFrame חלון = new JFrame();
    private final JTextArea קודמקור = new JTextArea();
    private final JTextArea פלטטקסט = new JTextArea();
    private final JTextField נתיב = new JTextField("קודמקור.java", 26);
    private final JTextField שם = new JTextField("קודמקור", 15);
    private final JTextField ארגומנטים = new JTextField(25);
    private final Properties הודעות = new Properties();
    private final Path תיקייה = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService משימתרקע = Executors.newSingleThreadExecutor();
    private volatile Process תהליך;

    private String תווית(String מפתח) {
        return הודעות.getProperty(מפתח, מפתח);
    }

    private void append(String טקסט) {
        SwingUtilities.invokeLater(() -> {
            פלטטקסט.append(טקסט);
            פלטטקסט.setCaretPosition(פלטטקסט.getDocument().getLength());
        });
    }

    private void שגיאה(Exception exception) {
        append(תווית("error") + ": " + exception.toString() + "\n");
    }

    private void לחצן(JPanel לוח, String מפתח, Runnable פעולה) {
        JButton לחצן = new JButton(תווית(מפתח));
        לחצן.addActionListener(event -> פעולה.run());
        לוח.add(לחצן);
    }

    private void טעןמקור() {
        try {
            קודמקור.setText(Files.readString(תיקייה.resolve(נתיב.getText()), StandardCharsets.UTF_8));
            קודמקור.setCaretPosition(0);
        } catch (Exception exception) { שגיאה(exception); }
    }

    private boolean שמירה() {
        try {
            Path קובץ = תיקייה.resolve(נתיב.getText()).normalize();
            Files.createDirectories(קובץ.getParent());
            Files.writeString(קובץ, קודמקור.getText(), StandardCharsets.UTF_8);
            append(תווית("save") + ": " + קובץ + "\n");
            return true;
        } catch (Exception exception) { שגיאה(exception); return false; }
    }

    private int בצע(List<String> פקודה) throws Exception {
        תהליך = new ProcessBuilder(פקודה).directory(תיקייה.toFile()).redirectErrorStream(true).start();
        try (BufferedReader קוראטקסט = new BufferedReader(new InputStreamReader(תהליך.getInputStream(), StandardCharsets.UTF_8))) {
            String שורה;
            while ((שורה = קוראטקסט.readLine()) != null) append(שורה + "\n");
        }
        int תוצאה = תהליך.waitFor();
        תהליך = null;
        append(תווית("result") + ": " + תוצאה + "\n");
        return תוצאה;
    }

    private void הידור(boolean הפעלה) {
        if (!שמירה()) return;
        String קובץ = תיקייה.resolve(נתיב.getText()).toString();
        String מחלקה = שם.getText().trim();
        String טקסט = ארגומנטים.getText();
        משימתרקע.submit(() -> {
            try {
                Files.createDirectories(תיקייה.resolve("classes"));
                int תוצאה = בצע(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", תיקייה.resolve("classes").toString(), קובץ));
                if (הפעלה && תוצאה == 0) {
                    List<String> פקודה = new ArrayList<>(Arrays.asList("java", "-cp", תיקייה.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", מחלקה));
                    StreamTokenizer מנתחארגומנטים = new StreamTokenizer(new StringReader(טקסט));
                    מנתחארגומנטים.resetSyntax(); מנתחארגומנטים.wordChars(33, 65535); מנתחארגומנטים.whitespaceChars(0, 32);
                    מנתחארגומנטים.quoteChar('"'); מנתחארגומנטים.quoteChar('\'');
                    while (מנתחארגומנטים.nextToken() != StreamTokenizer.TT_EOF) פקודה.add(מנתחארגומנטים.sval);
                    בצע(פקודה);
                }
            } catch (Exception exception) { שגיאה(exception); }
        });
    }

    private void עצירה() {
        Process תהליךנוכחי = תהליך;
        if (תהליךנוכחי != null) {
            תהליךנוכחי.descendants().forEach(ProcessHandle::destroyForcibly);
            תהליךנוכחי.destroyForcibly();
        }
    }

    private void מסוף() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(תיקייה.toFile()).start(); }
        catch (Exception exception) { שגיאה(exception); }
    }

    private void בחירה() {
        JFileChooser chooser = new JFileChooser(תיקייה.toFile());
        if (chooser.showOpenDialog(חלון) == JFileChooser.APPROVE_OPTION) {
            נתיב.setText(chooser.getSelectedFile().getAbsolutePath());
            טעןמקור();
        }
    }

    private void אתחול() {
        try (Reader קוראטקסט = new InputStreamReader(סביבתעבודה.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            הודעות.load(קוראטקסט);
            Files.createDirectories(תיקייה);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        חלון.setTitle(תווית("workspace") + " · WorldOS " + תווית("identity"));
        חלון.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        חלון.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent event) {
                עצירה(); משימתרקע.shutdownNow(); System.exit(0);
            }
        });
        קודמקור.setFont(new Font("Monospaced", Font.PLAIN, 17));
        קודמקור.setTabSize(4);
        פלטטקסט.setFont(new Font("Monospaced", Font.PLAIN, 14));
        פלטטקסט.setEditable(false);
        JPanel לוח = new JPanel(new GridLayout(0, 1));
        JPanel קובץ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        קובץ.add(new JLabel(תווית("file"))); קובץ.add(נתיב);
        לוח.add(קובץ);
        JPanel סרגל_כלים = new JPanel(new FlowLayout(FlowLayout.LEADING));
        לחצן(סרגל_כלים, "open", () -> בחירה());
        לחצן(סרגל_כלים, "save", () -> שמירה());
        לחצן(סרגל_כלים, "compile", () -> הידור(false));
        לחצן(סרגל_כלים, "run", () -> הידור(true));
        לחצן(סרגל_כלים, "stop", () -> עצירה());
        לחצן(סרגל_כלים, "terminal", () -> מסוף());
        לוח.add(סרגל_כלים);
        JPanel הגדרות = new JPanel(new FlowLayout(FlowLayout.LEADING));
        הגדרות.add(new JLabel(תווית("class"))); הגדרות.add(שם);
        הגדרות.add(new JLabel(תווית("arguments"))); הגדרות.add(ארגומנטים);
        לוח.add(הגדרות);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(קודמקור), new JScrollPane(פלטטקסט));
        split.setResizeWeight(0.72);
        חלון.add(לוח, BorderLayout.NORTH);
        חלון.add(split, BorderLayout.CENTER);
        לוח.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(תווית("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        קודמקור.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        פלטטקסט.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension גודל = Toolkit.getDefaultToolkit().getScreenSize();
        חלון.setSize(Math.min(1240, גודל.width - 40), Math.min(760, גודל.height - 60));
        חלון.setLocationRelativeTo(null);
        חלון.setVisible(true);
        טעןמקור();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(תווית("help") + "\n");
    }

    public static void main(String[] ארגומנטים) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new סביבתעבודה().אתחול());
    }
}
