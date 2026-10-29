// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame پنجره;
    JLabel مرا_بخوان_eb81d7d9;
    JTextField 입력;
    public void run() {
        پنجره = new JFrame("بومی هسته_مقدار Swing");
        پنجره.setSize(400, 280);
        پنجره.setLocationRelativeTo(null);
        پنجره.setLayout(null);
        پنجره.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        مرا_بخوان_eb81d7d9 = new JLabel("한글로 Java 코딩");
        مرا_بخوان_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("نام");
        입력.setBounds(20, 65, 340, 30);
        JButton دکمه = new JButton("인사하기");
        دکمه.setBounds(20, 110, 180, 32);
        دکمه.addActionListener(this);
        پنجره.add(مرا_بخوان_eb81d7d9); پنجره.add(입력); پنجره.add(دکمه);
        پنجره.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent رویداد) {
        مرا_بخوان_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
