// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class SwingPrüfung implements Runnable, ActionListener {
    JFrame fenster;
    JLabel Anleitung;
    JTextField Eingabewert;
    public void run() {
        fenster = new JFrame("eigen betriebskernWert Swing");
        fenster.setSize(400, 280);
        fenster.setLocationRelativeTo(null);
        fenster.setLayout(null);
        fenster.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Anleitung = new JLabel("한글로 Java 코딩");
        Anleitung.setBounds(20, 20, 340, 30);
        Eingabewert = new JTextField("Name");
        Eingabewert.setBounds(20, 65, 340, 30);
        JButton schaltfläche = new JButton("grüßen");
        schaltfläche.setBounds(20, 110, 180, 32);
        schaltfläche.addActionListener(this);
        fenster.add(Anleitung); fenster.add(Eingabewert); fenster.add(schaltfläche);
        fenster.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ereignis) {
        Anleitung.setText("안녕하세요 " + Eingabewert.getText());
        System.out.println("SWING CLICK " + Eingabewert.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new SwingPrüfung());
    }
}
