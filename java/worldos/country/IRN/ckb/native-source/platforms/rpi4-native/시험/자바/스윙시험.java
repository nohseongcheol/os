// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame پەنجەرە;
    JLabel رێخۆشکەر_eb81d7d9;
    JTextField 입력;
    public void run() {
        پەنجەرە = new JFrame("자체 کوورەک_نرخ Swing");
        پەنجەرە.setSize(400, 280);
        پەنجەرە.setLocationRelativeTo(null);
        پەنجەرە.setLayout(null);
        پەنجەرە.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        رێخۆشکەر_eb81d7d9 = new JLabel("한글로 Java 코딩");
        رێخۆشکەر_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ناو");
        입력.setBounds(20, 65, 340, 30);
        JButton دوگمه = new JButton("인사하기");
        دوگمه.setBounds(20, 110, 180, 32);
        دوگمه.addActionListener(this);
        پەنجەرە.add(رێخۆشکەر_eb81d7d9); پەنجەرە.add(입력); پەنجەرە.add(دوگمه);
        پەنجەرە.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent پێشهات) {
        رێخۆشکەر_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
