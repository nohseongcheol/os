// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame सन्झ्याल;
    JLabel readme_फाइल_eb81d7d9;
    JTextField 입력;
    public void run() {
        सन्झ्याल = new JFrame("निज कर्णेल_मान Swing");
        सन्झ्याल.setSize(400, 280);
        सन्झ्याल.setLocationRelativeTo(null);
        सन्झ्याल.setLayout(null);
        सन्झ्याल.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        readme_फाइल_eb81d7d9 = new JLabel("한글로 Java 코딩");
        readme_फाइल_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("नाम");
        입력.setBounds(20, 65, 340, 30);
        JButton बटन = new JButton("인사하기");
        बटन.setBounds(20, 110, 180, 32);
        बटन.addActionListener(this);
        सन्झ्याल.add(readme_फाइल_eb81d7d9); सन्झ्याल.add(입력); सन्झ्याल.add(बटन);
        सन्झ्याल.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent घटना) {
        readme_फाइल_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
