// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class 한글입력시험 {
    public static void main(String[] 인수) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame ວິນໂດ = new JFrame("한글 입력 · ຮູບແບບຕົວຫນັງສື_ຄ່າ 확인");
            JPanel 판 = new JPanel(new BorderLayout(10, 15));
            판.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9 = new JLabel("Ctrl+Space → 한글 입력 → Ctrl+Space → Enter");
            JTextField 입력 = new JTextField();
            Font ຮູບແບບຕົວຫນັງສື_ຄ່າ = new Font("Dialog", Font.PLAIN, 20);
            ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9.setFont(ຮູບແບບຕົວຫນັງສື_ຄ່າ.deriveFont(16f)); 입력.setFont(ຮູບແບບຕົວຫນັງສື_ຄ່າ);
            입력.enableInputMethods(true);
            입력.addActionListener(ງານ -> {
                String ມາດຕະການ = 입력.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ມາດຕະການ, StandardCharsets.UTF_8);
                } catch (Exception ຂໍ້ຜິດພາດ) { throw new RuntimeException(ຂໍ້ຜິດພາດ); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ມາດຕະການ.getBytes(StandardCharsets.UTF_8)));
            });
            판.add(ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9, BorderLayout.NORTH); 판.add(입력, BorderLayout.CENTER);
            ວິນໂດ.add(판); ວິນໂດ.setSize(850, 230); ວິນໂດ.setLocation(100, 100);
            ວິນໂດ.setAlwaysOnTop(true); ວິນໂດ.setVisible(true); 입력.requestFocusInWindow();
            Timer ກະ_ກຽມ = new Timer(1000, ງານ -> {
                Point ຈັດຕໍາແຫນ່ງ = 입력.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (ຈັດຕໍາແຫນ່ງ.x + 100) + " " + (ຈັດຕໍາແຫນ່ງ.y + 30));
            });
            ກະ_ກຽມ.setRepeats(false); ກະ_ກຽມ.start();
        });
    }
}
