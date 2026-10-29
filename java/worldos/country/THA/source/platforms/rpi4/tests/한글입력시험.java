// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame หน้าต่าง = new JFrame("한글 입력 · ฟอนต์_ค่า ยืนยัน");
            JPanel รุ่น_ค่า = new JPanel(new BorderLayout(10, 15));
            รุ่น_ค่า.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ฟอนต์_ค่า = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(ฟอนต์_ค่า.deriveFont(16f)); 입력.setFont(ฟอนต์_ค่า);
            입력.enableInputMethods(true);
            입력.addActionListener(เหตุการณ์ -> {
                String ผลลัพธ์ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ผลลัพธ์, StandardCharsets.UTF_8);
                } catch (Exception ข้อผิดพลาด) { throw new RuntimeException(ข้อผิดพลาด); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ผลลัพธ์.getBytes(StandardCharsets.UTF_8)));
            });
            รุ่น_ค่า.add(안내, BorderLayout.NORTH); รุ่น_ค่า.add(입력, BorderLayout.CENTER);
            หน้าต่าง.add(รุ่น_ค่า); หน้าต่าง.setSize(850, 230); หน้าต่าง.setLocation(100, 100);
            หน้าต่าง.setAlwaysOnTop(true); หน้าต่าง.setVisible(true); 입력.requestFocusInWindow();
            Timer จัดเตรียม = new Timer(1000, เหตุการณ์ -> {
                Point ตําแหน่ง = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ตําแหน่ง.x + 100) + " " + (ตําแหน่ง.y + 30));
            });
            จัดเตรียม.setRepeats(false); จัดเตรียม.start();
        });
    }
}
