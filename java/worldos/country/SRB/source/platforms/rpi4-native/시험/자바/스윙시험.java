// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Прозор;
    JLabel Прочитај_ме_eb81d7d9;
    JTextField 입력;
    public void run() {
        Прозор = new JFrame("자체 језгро_вриједност Swing");
        Прозор.setSize(400, 280);
        Прозор.setLocationRelativeTo(null);
        Прозор.setLayout(null);
        Прозор.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Прочитај_ме_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Прочитај_ме_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Назив");
        입력.setBounds(20, 65, 340, 30);
        JButton дугме = new JButton("인사하기");
        дугме.setBounds(20, 110, 180, 32);
        дугме.addActionListener(this);
        Прозор.add(Прочитај_ме_eb81d7d9); Прозор.add(입력); Прозор.add(дугме);
        Прозор.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Догађај) {
        Прочитај_ме_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
