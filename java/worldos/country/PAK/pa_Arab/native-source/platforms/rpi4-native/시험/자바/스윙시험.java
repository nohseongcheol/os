// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame کھڑکی;
    JLabel فائل_مینوں_پڑھو_eb81d7d9;
    JTextField 입력;
    public void run() {
        کھڑکی = new JFrame("자체 کرنل_قدر Swing");
        کھڑکی.setSize(400, 280);
        کھڑکی.setLocationRelativeTo(null);
        کھڑکی.setLayout(null);
        کھڑکی.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        فائل_مینوں_پڑھو_eb81d7d9 = new JLabel("한글로 Java 코딩");
        فائل_مینوں_پڑھو_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ناں");
        입력.setBounds(20, 65, 340, 30);
        JButton بٹن = new JButton("인사하기");
        بٹن.setBounds(20, 110, 180, 32);
        بٹن.addActionListener(this);
        کھڑکی.add(فائل_مینوں_پڑھو_eb81d7d9); کھڑکی.add(입력); کھڑکی.add(بٹن);
        کھڑکی.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent واقعہ) {
        فائل_مینوں_پڑھو_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
