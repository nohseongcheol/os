// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame taga;
    JLabel README_eb81d7d9;
    JTextField 입력;
    public void run() {
        taga = new JFrame("자체 Kwara_Daraja Swing");
        taga.setSize(400, 280);
        taga.setLocationRelativeTo(null);
        taga.setLayout(null);
        taga.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README_eb81d7d9 = new JLabel("한글로 Java 코딩");
        README_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Suna");
        입력.setBounds(20, 65, 340, 30);
        JButton maɓali = new JButton("인사하기");
        maɓali.setBounds(20, 110, 180, 32);
        maɓali.addActionListener(this);
        taga.add(README_eb81d7d9); taga.add(입력); taga.add(maɓali);
        taga.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Faruwa) {
        README_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
