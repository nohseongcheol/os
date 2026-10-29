// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ವಿಂಡೋ;
    JLabel README_ಫೈಲ್_eb81d7d9;
    JTextField 입력;
    public void run() {
        ವಿಂಡೋ = new JFrame("자체 ಕರ್ನಲ್_ಮೌಲ್ಯ Swing");
        ವಿಂಡೋ.setSize(400, 280);
        ವಿಂಡೋ.setLocationRelativeTo(null);
        ವಿಂಡೋ.setLayout(null);
        ವಿಂಡೋ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README_ಫೈಲ್_eb81d7d9 = new JLabel("한글로 Java 코딩");
        README_ಫೈಲ್_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ಹೆಸರು");
        입력.setBounds(20, 65, 340, 30);
        JButton ಬಟನ್ = new JButton("인사하기");
        ಬಟನ್.setBounds(20, 110, 180, 32);
        ಬಟನ್.addActionListener(this);
        ವಿಂಡೋ.add(README_ಫೈಲ್_eb81d7d9); ವಿಂಡೋ.add(입력); ವಿಂಡೋ.add(ಬಟನ್);
        ವಿಂಡೋ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ಸಂಗತಿ) {
        README_ಫೈಲ್_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
