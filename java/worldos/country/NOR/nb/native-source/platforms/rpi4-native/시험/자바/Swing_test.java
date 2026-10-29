// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Vindu;
    JLabel Viktig_fil_eb81d7d9;
    JTextField inndata_VERDI;
    public void run() {
        Vindu = new JFrame("eget kjerne_VERDI Swing");
        Vindu.setSize(400, 280);
        Vindu.setLocationRelativeTo(null);
        Vindu.setLayout(null);
        Vindu.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Viktig_fil_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Viktig_fil_eb81d7d9.setBounds(20, 20, 340, 30);
        inndata_VERDI = new JTextField("Navn");
        inndata_VERDI.setBounds(20, 65, 340, 30);
        JButton Knapp = new JButton("인사하기");
        Knapp.setBounds(20, 110, 180, 32);
        Knapp.addActionListener(this);
        Vindu.add(Viktig_fil_eb81d7d9); Vindu.add(inndata_VERDI); Vindu.add(Knapp);
        Vindu.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Hendelse) {
        Viktig_fil_eb81d7d9.setText("안녕하세요 " + inndata_VERDI.getText());
        System.out.println("SWING CLICK " + inndata_VERDI.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
