// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.자바;

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

/** χρήστης 홈에서 Java 원문을 Τροποποίησε_τιμή·δόμηση_προέλευση·실행하는 작은 Swing χώρος_εργασίας. */
public final class χώρος_εργασίας {
    private final JFrame Παράθυρο = new JFrame("jkoros — 자바 χώρος_εργασίας");
    private final JTextArea ΠΗΓΗ = new JTextArea();
    private final JTextArea Έξοδος = new JTextArea(8, 80);
    private final JTextField Αρχείο_καταχώρηση_όνομα = new JTextField("인사.java", 20);
    private final JTextField Τάξη_καταχώρηση_όνομα = new JTextField("인사", 16);
    private final Path κατάλογος_εργασίας = Path.of(System.getProperty("user.home"), "workspace");
    private final ExecutorService 일꾼 = Executors.newSingleThreadExecutor();
    private volatile Process διεργασία_τιμή;
    private final String βιβλιοθήκη = "/opt/jkoros/lib/한국어자바.jar";

    private void γνωστοποίηση(String Κείμενο) { SwingUtilities.invokeLater(() -> Έξοδος.append(Κείμενο + "\n")); }
    private void κουμπί(JPanel έκδοση_τιμή, String Όνομα, Runnable 행동) {
        JButton κουμπί = new JButton(Όνομα);
        κουμπί.addActionListener(Συμβάν -> 행동.run());
        έκδοση_τιμή.add(κουμπί);
    }
    private boolean αποθηκεύω_τιμή() {
        try {
            Path ΔΙΑΔΡΟΜΗ = κατάλογος_εργασίας.resolve(Αρχείο_καταχώρηση_όνομα.getText());
            Files.createDirectories(ΔΙΑΔΡΟΜΗ.getParent());
            Αρχείο.Εγγραφή(ΔΙΑΔΡΟΜΗ, ΠΗΓΗ.getText());
            γνωστοποίηση("αποθηκεύω_τιμή: " + ΔΙΑΔΡΟΜΗ);
            return true;
        } catch (Exception ΣΦΑΛΜΑ) { γνωστοποίηση(ΣΦΑΛΜΑ.toString()); return false; }
    }
    private void Άνοιγμα() {
        try { ΠΗΓΗ.setText(Αρχείο.Ανάγνωση(κατάλογος_εργασίας.resolve(Αρχείο_καταχώρηση_όνομα.getText()))); }
        catch (Exception ΣΦΑΛΜΑ) { γνωστοποίηση(ΣΦΑΛΜΑ.toString()); }
    }
    private int Εντολή(List<String> Εντολή) throws Exception {
        διεργασία_τιμή = new ProcessBuilder(Εντολή).directory(κατάλογος_εργασίας.toFile()).redirectErrorStream(true).start();
        try (BufferedReader Γραμμή = new BufferedReader(new InputStreamReader(διεργασία_τιμή.getInputStream(), StandardCharsets.UTF_8))) {
            String Κείμενο;
            while ((Κείμενο = Γραμμή.readLine()) != null) γνωστοποίηση(Κείμενο);
        }
        int Κατάσταση_τιμή = διεργασία_τιμή.waitFor(); διεργασία_τιμή = null;
        γνωστοποίηση("Έξοδος_εφαρμογή κωδικός_τιμή: " + Κατάσταση_τιμή);
        return Κατάσταση_τιμή;
    }
    private void Μετάφραση_προέλευση(boolean εκτελώ_εντολή, boolean εκτελέσιμο) {
        if (!αποθηκεύω_τιμή()) return;
        String είσοδος_τιμή = Αρχείο_καταχώρηση_όνομα.getText(), σημείο_εισόδου_τιμή = Τάξη_καταχώρηση_όνομα.getText();
        일꾼.submit(() -> {
            try {
                Files.createDirectories(κατάλογος_εργασίας.resolve("classes"));
                if (εκτελέσιμο) {
                    Εντολή(Arrays.asList("jclassc", "--target", "openjdk", "--entry", σημείο_εισόδου_τιμή,
                        "--classpath", βιβλιοθήκη, "-o", "실행프로그램", είσοδος_τιμή));
                } else if (Εντολή(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", βιβλιοθήκη,
                        "-d", "classes", είσοδος_τιμή)) == 0 && εκτελώ_εντολή) {
                    Εντολή(Arrays.asList("java", "-cp", "classes:" + βιβλιοθήκη, σημείο_εισόδου_τιμή));
                }
            } catch (Exception ΣΦΑΛΜΑ) { γνωστοποίηση(ΣΦΑΛΜΑ.toString()); }
        });
    }
    private void Παύση_εκτέλεση() {
        Process τρέχων_στοιχείο = διεργασία_τιμή;
        if (τρέχων_στοιχείο != null) { τρέχων_στοιχείο.descendants().forEach(ProcessHandle::destroy); τρέχων_στοιχείο.destroy(); }
    }
    private χώρος_εργασίας() throws IOException {
        Files.createDirectories(κατάλογος_εργασίας);
        Font γραμματοσειρά_τιμή = new Font("Monospaced", Font.PLAIN, 16);
        ΠΗΓΗ.setFont(γραμματοσειρά_τιμή); Έξοδος.setFont(γραμματοσειρά_τιμή); Έξοδος.setEditable(false);
        ΠΗΓΗ.setTabSize(4);
        ΠΗΓΗ.setMargin(new Insets(10, 12, 10, 12));
        Έξοδος.setMargin(new Insets(8, 12, 8, 12));
        ΠΗΓΗ.setBackground(new Color(250, 251, 252));
        ΠΗΓΗ.setForeground(new Color(32, 43, 58));
        JPanel εντολή_πίνακας = new JPanel();
        εντολή_πίνακας.add(new JLabel("Αρχείο")); εντολή_πίνακας.add(Αρχείο_καταχώρηση_όνομα);
        εντολή_πίνακας.add(new JLabel("주 Τάξη_τιμή")); εντολή_πίνακας.add(Τάξη_καταχώρηση_όνομα);
        κουμπί(εντολή_πίνακας, "Άνοιγμα", this::Άνοιγμα); κουμπί(εντολή_πίνακας, "αποθηκεύω_τιμή", this::αποθηκεύω_τιμή);
        κουμπί(εντολή_πίνακας, "δόμηση_προέλευση", () -> Μετάφραση_προέλευση(false, false));
        κουμπί(εντολή_πίνακας, "εκτελώ_εντολή", () -> Μετάφραση_προέλευση(true, false));
        κουμπί(εντολή_πίνακας, "εκτελώ_εντολή Αρχείο ανοίγω_καταχώρηση", () -> Μετάφραση_προέλευση(false, true));
        κουμπί(εντολή_πίνακας, "Παύση_εκτέλεση", this::Παύση_εκτέλεση);
        JSplitPane τμήμα_μέτρηση = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(ΠΗΓΗ), new JScrollPane(Έξοδος));
        τμήμα_μέτρηση.setResizeWeight(0.75);
        Παράθυρο.add(εντολή_πίνακας, BorderLayout.NORTH); Παράθυρο.add(τμήμα_μέτρηση, BorderLayout.CENTER);
        Παράθυρο.setSize(1200, 750); Παράθυρο.setLocationRelativeTo(null);
        Παράθυρο.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Παράθυρο.addWindowListener(new WindowAdapter() {
            public void windowClosed(WindowEvent Συμβάν) { Παύση_εκτέλεση(); 일꾼.shutdownNow(); }
        });
        Άνοιγμα(); Παράθυρο.setVisible(true);
    }
    public static void main(String[] Παράμετροι) {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
                FontUIResource προεπιλεγμένη_γραμματοσειρά = new FontUIResource("Dialog", Font.PLAIN, 14);
                for (Object καταχώρηση_τιμή : new ArrayList<>(UIManager.getDefaults().keySet())) {
                    if (UIManager.get(καταχώρηση_τιμή) instanceof Font) UIManager.put(καταχώρηση_τιμή, προεπιλεγμένη_γραμματοσειρά);
                }
                new χώρος_εργασίας();
            } catch (Exception ΣΦΑΛΜΑ) { ΣΦΑΛΜΑ.printStackTrace(); }
        });
    }
}
