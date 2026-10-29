// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame نافذة;
    JLabel 안내;
    JTextField إدخال_قيمة;
    public void run() {
        نافذة = new JFrame("ذاتي نواة_قيمة Swing");
        نافذة.setSize(400, 280);
        نافذة.setLocationRelativeTo(null);
        نافذة.setLayout(null);
        نافذة.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        إدخال_قيمة = new JTextField("اسم");
        إدخال_قيمة.setBounds(20, 65, 340, 30);
        JButton زر = new JButton("인사하기");
        زر.setBounds(20, 110, 180, 32);
        زر.addActionListener(this);
        نافذة.add(안내); نافذة.add(إدخال_قيمة); نافذة.add(زر);
        نافذة.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent حدث) {
        안내.setText("안녕하세요 " + إدخال_قيمة.getText());
        System.out.println("SWING CLICK " + إدخال_قيمة.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
