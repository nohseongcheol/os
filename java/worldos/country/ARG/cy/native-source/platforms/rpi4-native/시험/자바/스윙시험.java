// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ffenestr;
    JLabel GWYBODAETH_eb81d7d9;
    JTextField 입력;
    public void run() {
        ffenestr = new JFrame("자체 cnewyllyn_VALUE Swing");
        ffenestr.setSize(400, 280);
        ffenestr.setLocationRelativeTo(null);
        ffenestr.setLayout(null);
        ffenestr.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        GWYBODAETH_eb81d7d9 = new JLabel("한글로 Java 코딩");
        GWYBODAETH_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Enw");
        입력.setBounds(20, 65, 340, 30);
        JButton botwm = new JButton("인사하기");
        botwm.setBounds(20, 110, 180, 32);
        botwm.addActionListener(this);
        ffenestr.add(GWYBODAETH_eb81d7d9); ffenestr.add(입력); ffenestr.add(botwm);
        ffenestr.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent digwyddiad) {
        GWYBODAETH_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
