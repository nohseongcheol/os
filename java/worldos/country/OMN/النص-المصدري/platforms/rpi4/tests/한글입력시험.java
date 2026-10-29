// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] وسائط) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame نافذة = new JFrame("한글 إدخال_قيمة · خط_قيمة يتحقق");
            JPanel إصدار_قيمة = new JPanel(new BorderLayout(10, 15));
            إصدار_قيمة.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel 안내 = new JLabel("Ctrl+Space → 한글 إدخال_قيمة → Ctrl+Space → Enter");
            JTextField إدخال_قيمة = new JTextField();
            Font خط_قيمة = new Font("Dialog", Font.PLAIN, 20);
            안내.setFont(خط_قيمة.deriveFont(16f)); إدخال_قيمة.setFont(خط_قيمة);
            إدخال_قيمة.enableInputMethods(true);
            إدخال_قيمة.addActionListener(حدث -> {
                String نتيجة = إدخال_قيمة.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), نتيجة, StandardCharsets.UTF_8);
                } catch (Exception خطأ) { throw new RuntimeException(خطأ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(نتيجة.getBytes(StandardCharsets.UTF_8)));
            });
            إصدار_قيمة.add(안내, BorderLayout.NORTH); إصدار_قيمة.add(إدخال_قيمة, BorderLayout.CENTER);
            نافذة.add(إصدار_قيمة); نافذة.setSize(850, 230); نافذة.setLocation(100, 100);
            نافذة.setAlwaysOnTop(true); نافذة.setVisible(true); إدخال_قيمة.requestFocusInWindow();
            Timer إعداد = new Timer(1000, حدث -> {
                Point موضع = إدخال_قيمة.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (موضع.x + 100) + " " + (موضع.y + 30));
            });
            إعداد.setRepeats(false); إعداد.start();
        });
    }
}
