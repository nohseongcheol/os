// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class स्विंग_चाचणी_da272923 implements Runnable, ActionListener {
    JFrame विंडो;
    JLabel वापरमार्गदर्शिका_eb81d7d9;
    JTextField आदान_मूल्य;
    public void run() {
        विंडो = new JFrame("स्वकीय गाभा_मूल्य Swing");
        विंडो.setSize(400, 280);
        विंडो.setLocationRelativeTo(null);
        विंडो.setLayout(null);
        विंडो.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        वापरमार्गदर्शिका_eb81d7d9 = new JLabel("한글로 Java 코딩");
        वापरमार्गदर्शिका_eb81d7d9.setBounds(20, 20, 340, 30);
        आदान_मूल्य = new JTextField("नाव");
        आदान_मूल्य.setBounds(20, 65, 340, 30);
        JButton बटण = new JButton("अभिवादनकरा");
        बटण.setBounds(20, 110, 180, 32);
        बटण.addActionListener(this);
        विंडो.add(वापरमार्गदर्शिका_eb81d7d9); विंडो.add(आदान_मूल्य); विंडो.add(बटण);
        विंडो.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent इव्हेंट) {
        वापरमार्गदर्शिका_eb81d7d9.setText("안녕하세요 " + आदान_मूल्य.getText());
        System.out.println("SWING CLICK " + आदान_मूल्य.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new स्विंग_चाचणी_da272923());
    }
}
