// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Szving_teszt implements Runnable, ActionListener {
    JFrame Ablak;
    JLabel fontos_fájl_eb81d7d9;
    JTextField bevitel_ÉRTÉK;
    public void run() {
        Ablak = new JFrame("saját kernel_ÉRTÉK Swing");
        Ablak.setSize(400, 280);
        Ablak.setLocationRelativeTo(null);
        Ablak.setLayout(null);
        Ablak.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        fontos_fájl_eb81d7d9 = new JLabel("한글로 Java 코딩");
        fontos_fájl_eb81d7d9.setBounds(20, 20, 340, 30);
        bevitel_ÉRTÉK = new JTextField("Név");
        bevitel_ÉRTÉK.setBounds(20, 65, 340, 30);
        JButton gomb = new JButton("인사하기");
        gomb.setBounds(20, 110, 180, 32);
        gomb.addActionListener(this);
        Ablak.add(fontos_fájl_eb81d7d9); Ablak.add(bevitel_ÉRTÉK); Ablak.add(gomb);
        Ablak.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Esemény) {
        fontos_fájl_eb81d7d9.setText("안녕하세요 " + bevitel_ÉRTÉK.getText());
        System.out.println("SWING CLICK " + bevitel_ÉRTÉK.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Szving_teszt());
    }
}
