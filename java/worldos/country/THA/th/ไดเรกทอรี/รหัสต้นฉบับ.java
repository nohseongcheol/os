// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.*;
import javax.swing.*;
import java.nio.file.*;

public class รหัสต้นฉบับ {
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        Path แฟ้ม = Path.of("ข้อความ.txt");
        Files.writeString(แฟ้ม, "Hello from WorldOS!\n");
        System.out.print(Files.readString(แฟ้ม));
        SwingUtilities.invokeLater(() -> {
            JFrame หน้าต่าง = new JFrame("WorldOS · OpenJDK · Swing");
            JButton ปุ่ม = new JButton("Hello / 안녕하세요 / こんにちは / مرحباً");
            ปุ่ม.setFont(new Font("Dialog", Font.PLAIN, 24));
            ปุ่ม.addActionListener(เหตุการณ์ -> JOptionPane.showMessageDialog(หน้าต่าง, "Swing is running inside Linux."));
            หน้าต่าง.add(ปุ่ม);
            หน้าต่าง.setSize(720, 200);
            หน้าต่าง.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            หน้าต่าง.setLocationRelativeTo(null);
            หน้าต่าง.setVisible(true);
        });
    }
}
