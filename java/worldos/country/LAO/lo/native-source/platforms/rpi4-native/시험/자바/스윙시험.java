// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ວິນໂດ;
    JLabel ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9;
    JTextField 입력;
    public void run() {
        ວິນໂດ = new JFrame("자체 ແກນກາງ_ຄ່າ Swing");
        ວິນໂດ.setSize(400, 280);
        ວິນໂດ.setLocationRelativeTo(null);
        ວິນໂດ.setLayout(null);
        ວິນໂດ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ຊື່");
        입력.setBounds(20, 65, 340, 30);
        JButton ປຸ່ມ = new JButton("인사하기");
        ປຸ່ມ.setBounds(20, 110, 180, 32);
        ປຸ່ມ.addActionListener(this);
        ວິນໂດ.add(ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9); ວິນໂດ.add(입력); ວິນໂດ.add(ປຸ່ມ);
        ວິນໂດ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ງານ) {
        ຂໍ້ແນະນໍາການໃຊ້_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
