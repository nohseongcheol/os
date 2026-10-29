// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Fönster;
    JLabel VIKTIGT_eb81d7d9;
    JTextField indata_värde;
    public void run() {
        Fönster = new JFrame("eget kärna_värde Swing");
        Fönster.setSize(400, 280);
        Fönster.setLocationRelativeTo(null);
        Fönster.setLayout(null);
        Fönster.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        VIKTIGT_eb81d7d9 = new JLabel("한글로 Java 코딩");
        VIKTIGT_eb81d7d9.setBounds(20, 20, 340, 30);
        indata_värde = new JTextField("Namn");
        indata_värde.setBounds(20, 65, 340, 30);
        JButton knapp = new JButton("인사하기");
        knapp.setBounds(20, 110, 180, 32);
        knapp.addActionListener(this);
        Fönster.add(VIKTIGT_eb81d7d9); Fönster.add(indata_värde); Fönster.add(knapp);
        Fönster.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Händelse) {
        VIKTIGT_eb81d7d9.setText("안녕하세요 " + indata_värde.getText());
        System.out.println("SWING CLICK " + indata_värde.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
