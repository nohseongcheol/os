// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame акно;
    JLabel файл_звестак_eb81d7d9;
    JTextField 입력;
    public void run() {
        акно = new JFrame("자체 ядро_значэнне Swing");
        акно.setSize(400, 280);
        акно.setLocationRelativeTo(null);
        акно.setLayout(null);
        акно.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        файл_звестак_eb81d7d9 = new JLabel("한글로 Java 코딩");
        файл_звестак_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Назва");
        입력.setBounds(20, 65, 340, 30);
        JButton кнопка = new JButton("인사하기");
        кнопка.setBounds(20, 110, 180, 32);
        кнопка.addActionListener(this);
        акно.add(файл_звестак_eb81d7d9); акно.add(입력); акно.add(кнопка);
        акно.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Падзея) {
        файл_звестак_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
