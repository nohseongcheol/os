// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Logs;
    JLabel fails_Lasi_mani_eb81d7d9;
    JTextField 입력;
    public void run() {
        Logs = new JFrame("savs kodols_VALUE Swing");
        Logs.setSize(400, 280);
        Logs.setLocationRelativeTo(null);
        Logs.setLayout(null);
        Logs.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        fails_Lasi_mani_eb81d7d9 = new JLabel("한글로 Java 코딩");
        fails_Lasi_mani_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nosaukums");
        입력.setBounds(20, 65, 340, 30);
        JButton Pogas = new JButton("인사하기");
        Pogas.setBounds(20, 110, 180, 32);
        Pogas.addActionListener(this);
        Logs.add(fails_Lasi_mani_eb81d7d9); Logs.add(입력); Logs.add(Pogas);
        Logs.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Notikums) {
        fails_Lasi_mani_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
