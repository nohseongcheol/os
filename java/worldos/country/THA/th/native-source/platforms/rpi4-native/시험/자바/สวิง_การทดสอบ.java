// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class สวิง_การทดสอบ implements Runnable, ActionListener {
    JFrame หน้าต่าง;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        หน้าต่าง = new JFrame("เอง เคอร์เนล_ค่า Swing");
        หน้าต่าง.setSize(400, 280);
        หน้าต่าง.setLocationRelativeTo(null);
        หน้าต่าง.setLayout(null);
        หน้าต่าง.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ชื่อ");
        입력.setBounds(20, 65, 340, 30);
        JButton ปุ่ม = new JButton("인사하기");
        ปุ่ม.setBounds(20, 110, 180, 32);
        ปุ่ม.addActionListener(this);
        หน้าต่าง.add(안내); หน้าต่าง.add(입력); หน้าต่าง.add(ปุ่ม);
        หน้าต่าง.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent เหตุการณ์) {
        안내.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new สวิง_การทดสอบ());
    }
}
