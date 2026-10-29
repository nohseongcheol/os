// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame windò;
    JLabel GỤ̀ỌM_eb81d7d9;
    JTextField 입력;
    public void run() {
        windò = new JFrame("자체 mkpụrụobī_kọmpùta_valuu Swing");
        windò.setSize(400, 280);
        windò.setLocationRelativeTo(null);
        windò.setLayout(null);
        windò.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        GỤ̀ỌM_eb81d7d9 = new JLabel("한글로 Java 코딩");
        GỤ̀ỌM_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Aha");
        입력.setBounds(20, 65, 340, 30);
        JButton ọdụmbi = new JButton("인사하기");
        ọdụmbi.setBounds(20, 110, 180, 32);
        ọdụmbi.addActionListener(this);
        windò.add(GỤ̀ỌM_eb81d7d9); windò.add(입력); windò.add(ọdụmbi);
        windò.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent mmèrème) {
        GỤ̀ỌM_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
