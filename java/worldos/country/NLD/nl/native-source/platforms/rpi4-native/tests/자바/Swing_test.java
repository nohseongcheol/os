// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Venster;
    JLabel LEESMIJ_eb81d7d9;
    JTextField invoer_WAARDE;
    public void run() {
        Venster = new JFrame("Eigen kernel_WAARDE Swing");
        Venster.setSize(400, 280);
        Venster.setLocationRelativeTo(null);
        Venster.setLayout(null);
        Venster.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LEESMIJ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LEESMIJ_eb81d7d9.setBounds(20, 20, 340, 30);
        invoer_WAARDE = new JTextField("Naam");
        invoer_WAARDE.setBounds(20, 65, 340, 30);
        JButton knop = new JButton("인사하기");
        knop.setBounds(20, 110, 180, 32);
        knop.addActionListener(this);
        Venster.add(LEESMIJ_eb81d7d9); Venster.add(invoer_WAARDE); Venster.add(knop);
        Venster.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Gebeurtenis) {
        LEESMIJ_eb81d7d9.setText("안녕하세요 " + invoer_WAARDE.getText());
        System.out.println("SWING CLICK " + invoer_WAARDE.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
