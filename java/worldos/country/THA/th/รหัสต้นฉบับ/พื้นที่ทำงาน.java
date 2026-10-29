// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.THA.l_th;
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
public final class พื้นที่ทำงาน {
    private final JFrame หน้าต่าง = new JFrame();
    private final JTextArea รหัสต้นฉบับ = new JTextArea();
    private final JTextArea ข้อความออก = new JTextArea();
    private final JTextField เส้นทาง = new JTextField("รหัสต้นฉบับ.java", 26);
    private final JTextField ชื่อ = new JTextField("รหัสต้นฉบับ", 15);
    private final JTextField อาร์กิวเมนต์ = new JTextField(25);
    private final Properties ข้อความแจ้ง = new Properties();
    private final Path ไดเรกทอรี = Paths.get(System.getProperty("user.home"), "workspace");
    private final ExecutorService งานเบื้องหลัง = Executors.newSingleThreadExecutor();
    private volatile Process โพรเซส;

    private String ฉลาก(String คีย์) {
        return ข้อความแจ้ง.getProperty(คีย์, คีย์);
    }

    private void append(String ข้อความ) {
        SwingUtilities.invokeLater(() -> {
            ข้อความออก.append(ข้อความ);
            ข้อความออก.setCaretPosition(ข้อความออก.getDocument().getLength());
        });
    }

    private void ข้อผิดพลาด(Exception exception) {
        append(ฉลาก("error") + ": " + exception.toString() + "\n");
    }

    private void ปุ่ม(JPanel พาเนล, String คีย์, Runnable การกระทำ) {
        JButton ปุ่ม = new JButton(ฉลาก(คีย์));
        ปุ่ม.addActionListener(เหตุการณ์ -> การกระทำ.run());
        พาเนล.add(ปุ่ม);
    }

    private void โหลดต้นฉบับ() {
        try {
            รหัสต้นฉบับ.setText(Files.readString(ไดเรกทอรี.resolve(เส้นทาง.getText()), StandardCharsets.UTF_8));
            รหัสต้นฉบับ.setCaretPosition(0);
        } catch (Exception exception) { ข้อผิดพลาด(exception); }
    }

    private boolean บันทึก() {
        try {
            Path แฟ้ม = ไดเรกทอรี.resolve(เส้นทาง.getText()).normalize();
            Files.createDirectories(แฟ้ม.getParent());
            Files.writeString(แฟ้ม, รหัสต้นฉบับ.getText(), StandardCharsets.UTF_8);
            append(ฉลาก("save") + ": " + แฟ้ม + "\n");
            return true;
        } catch (Exception exception) { ข้อผิดพลาด(exception); return false; }
    }

    private int เรียกทำงาน(List<String> คำสั่ง) throws Exception {
        โพรเซส = new ProcessBuilder(คำสั่ง).directory(ไดเรกทอรี.toFile()).redirectErrorStream(true).start();
        try (BufferedReader ตัวอ่านข้อความ = new BufferedReader(new InputStreamReader(โพรเซส.getInputStream(), StandardCharsets.UTF_8))) {
            String บรรทัด;
            while ((บรรทัด = ตัวอ่านข้อความ.readLine()) != null) append(บรรทัด + "\n");
        }
        int ผลลัพธ์ = โพรเซส.waitFor();
        โพรเซส = null;
        append(ฉลาก("result") + ": " + ผลลัพธ์ + "\n");
        return ผลลัพธ์;
    }

    private void คอมไพล์(boolean เรียกใช้งาน) {
        if (!บันทึก()) return;
        String แฟ้ม = ไดเรกทอรี.resolve(เส้นทาง.getText()).toString();
        String คลาส = ชื่อ.getText().trim();
        String ข้อความ = อาร์กิวเมนต์.getText();
        งานเบื้องหลัง.submit(() -> {
            try {
                Files.createDirectories(ไดเรกทอรี.resolve("classes"));
                int ผลลัพธ์ = เรียกทำงาน(Arrays.asList("javac", "-encoding", "UTF-8", "-cp", "/opt/worldos/edition.jar",
                        "-d", ไดเรกทอรี.resolve("classes").toString(), แฟ้ม));
                if (เรียกใช้งาน && ผลลัพธ์ == 0) {
                    List<String> คำสั่ง = new ArrayList<>(Arrays.asList("java", "-cp", ไดเรกทอรี.resolve("classes")
                            + File.pathSeparator + "/opt/worldos/edition.jar", คลาส));
                    StreamTokenizer ตัวแยกอาร์กิวเมนต์ = new StreamTokenizer(new StringReader(ข้อความ));
                    ตัวแยกอาร์กิวเมนต์.resetSyntax(); ตัวแยกอาร์กิวเมนต์.wordChars(33, 65535); ตัวแยกอาร์กิวเมนต์.whitespaceChars(0, 32);
                    ตัวแยกอาร์กิวเมนต์.quoteChar('"'); ตัวแยกอาร์กิวเมนต์.quoteChar('\'');
                    while (ตัวแยกอาร์กิวเมนต์.nextToken() != StreamTokenizer.TT_EOF) คำสั่ง.add(ตัวแยกอาร์กิวเมนต์.sval);
                    เรียกทำงาน(คำสั่ง);
                }
            } catch (Exception exception) { ข้อผิดพลาด(exception); }
        });
    }

    private void หยุด() {
        Process กระบวนการปัจจุบัน = โพรเซส;
        if (กระบวนการปัจจุบัน != null) {
            กระบวนการปัจจุบัน.descendants().forEach(ProcessHandle::destroyForcibly);
            กระบวนการปัจจุบัน.destroyForcibly();
        }
    }

    private void เทอร์มินัล() {
        try { new ProcessBuilder("xterm", "-fa", "monospace", "-fs", "12", "-e", "/bin/sh")
                .directory(ไดเรกทอรี.toFile()).start(); }
        catch (Exception exception) { ข้อผิดพลาด(exception); }
    }

    private void choose() {
        JFileChooser chooser = new JFileChooser(ไดเรกทอรี.toFile());
        if (chooser.showOpenDialog(หน้าต่าง) == JFileChooser.APPROVE_OPTION) {
            เส้นทาง.setText(chooser.getSelectedFile().getAbsolutePath());
            โหลดต้นฉบับ();
        }
    }

    private void เริ่มต้น() {
        try (Reader ตัวอ่านข้อความ = new InputStreamReader(พื้นที่ทำงาน.class.getResourceAsStream("/messages.properties"), StandardCharsets.UTF_8)) {
            ข้อความแจ้ง.load(ตัวอ่านข้อความ);
            Files.createDirectories(ไดเรกทอรี);
        } catch (Exception exception) { throw new IllegalStateException(exception); }
        หน้าต่าง.setTitle(ฉลาก("workspace") + " · WorldOS " + ฉลาก("identity"));
        หน้าต่าง.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        หน้าต่าง.addWindowListener(new WindowAdapter() {
            @Override public void windowClosed(WindowEvent เหตุการณ์) {
                หยุด(); งานเบื้องหลัง.shutdownNow(); System.exit(0);
            }
        });
        รหัสต้นฉบับ.setFont(new Font("Monospaced", Font.PLAIN, 17));
        รหัสต้นฉบับ.setTabSize(4);
        ข้อความออก.setFont(new Font("Monospaced", Font.PLAIN, 14));
        ข้อความออก.setEditable(false);
        JPanel พาเนล = new JPanel(new GridLayout(0, 1));
        JPanel แฟ้ม = new JPanel(new FlowLayout(FlowLayout.LEADING));
        แฟ้ม.add(new JLabel(ฉลาก("file"))); แฟ้ม.add(เส้นทาง);
        พาเนล.add(แฟ้ม);
        JPanel แถบเครื่องมือ = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ปุ่ม(แถบเครื่องมือ, "open", () -> choose());
        ปุ่ม(แถบเครื่องมือ, "save", () -> บันทึก());
        ปุ่ม(แถบเครื่องมือ, "compile", () -> คอมไพล์(false));
        ปุ่ม(แถบเครื่องมือ, "run", () -> คอมไพล์(true));
        ปุ่ม(แถบเครื่องมือ, "stop", () -> หยุด());
        ปุ่ม(แถบเครื่องมือ, "terminal", () -> เทอร์มินัล());
        พาเนล.add(แถบเครื่องมือ);
        JPanel ตั้งค่า = new JPanel(new FlowLayout(FlowLayout.LEADING));
        ตั้งค่า.add(new JLabel(ฉลาก("class"))); ตั้งค่า.add(ชื่อ);
        ตั้งค่า.add(new JLabel(ฉลาก("arguments"))); ตั้งค่า.add(อาร์กิวเมนต์);
        พาเนล.add(ตั้งค่า);
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(รหัสต้นฉบับ), new JScrollPane(ข้อความออก));
        split.setResizeWeight(0.72);
        หน้าต่าง.add(พาเนล, BorderLayout.NORTH);
        หน้าต่าง.add(split, BorderLayout.CENTER);
        พาเนล.applyComponentOrientation(ComponentOrientation.getOrientation(Locale.forLanguageTag(ฉลาก("locale"))));
        split.applyComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        // Source code has its own bidirectional ordering; do not reverse the source editor.
        รหัสต้นฉบับ.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        ข้อความออก.setComponentOrientation(ComponentOrientation.LEFT_TO_RIGHT);
        Dimension ขนาด = Toolkit.getDefaultToolkit().getScreenSize();
        หน้าต่าง.setSize(Math.min(1240, ขนาด.width - 40), Math.min(760, ขนาด.height - 60));
        หน้าต่าง.setLocationRelativeTo(null);
        หน้าต่าง.setVisible(true);
        โหลดต้นฉบับ();
        split.setDividerLocation(0.72);
        append("OpenJDK " + System.getProperty("java.version") + " · " + System.getProperty("os.name") + "\n");
        append(ฉลาก("help") + "\n");
    }

    public static void main(String[] อาร์กิวเมนต์) {
        Locale.setDefault(Locale.forLanguageTag(System.getProperty("worldos.locale", "en")));
        SwingUtilities.invokeLater(() -> new พื้นที่ทำงาน().เริ่มต้น());
    }
}
