// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame खिड़की;
    JLabel ReadMe_फ़ाइल_eb81d7d9;
    JTextField 입력;
    public void run() {
        खिड़की = new JFrame("निज कर्नेल_मान Swing");
        खिड़की.setSize(400, 280);
        खिड़की.setLocationRelativeTo(null);
        खिड़की.setLayout(null);
        खिड़की.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ReadMe_फ़ाइल_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ReadMe_फ़ाइल_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("नाम");
        입력.setBounds(20, 65, 340, 30);
        JButton बटन = new JButton("인사하기");
        बटन.setBounds(20, 110, 180, 32);
        बटन.addActionListener(this);
        खिड़की.add(ReadMe_फ़ाइल_eb81d7d9); खिड़की.add(입력); खिड़की.add(बटन);
        खिड़की.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent घटना) {
        ReadMe_फ़ाइल_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
