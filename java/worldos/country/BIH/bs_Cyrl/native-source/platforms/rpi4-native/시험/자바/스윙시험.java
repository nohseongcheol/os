// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame прозор;
    JLabel Прочитај_ме_eb81d7d9;
    JTextField 입력;
    public void run() {
        прозор = new JFrame("자체 језгро_вриједност Swing");
        прозор.setSize(400, 280);
        прозор.setLocationRelativeTo(null);
        прозор.setLayout(null);
        прозор.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Прочитај_ме_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Прочитај_ме_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("назив");
        입력.setBounds(20, 65, 340, 30);
        JButton дугме = new JButton("인사하기");
        дугме.setBounds(20, 110, 180, 32);
        дугме.addActionListener(this);
        прозор.add(Прочитај_ме_eb81d7d9); прозор.add(입력); прозор.add(дугме);
        прозор.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent догађај) {
        Прочитај_ме_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
