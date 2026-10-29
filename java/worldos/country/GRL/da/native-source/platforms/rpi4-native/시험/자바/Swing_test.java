// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Vindue;
    JLabel Vigtigt_eb81d7d9;
    JTextField input_VÆRDI;
    public void run() {
        Vindue = new JFrame("eget kerne_VÆRDI Swing");
        Vindue.setSize(400, 280);
        Vindue.setLocationRelativeTo(null);
        Vindue.setLayout(null);
        Vindue.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Vigtigt_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Vigtigt_eb81d7d9.setBounds(20, 20, 340, 30);
        input_VÆRDI = new JTextField("Navn");
        input_VÆRDI.setBounds(20, 65, 340, 30);
        JButton knap = new JButton("인사하기");
        knap.setBounds(20, 110, 180, 32);
        knap.addActionListener(this);
        Vindue.add(Vigtigt_eb81d7d9); Vindue.add(input_VÆRDI); Vindue.add(knap);
        Vindue.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent hændelse) {
        Vigtigt_eb81d7d9.setText("안녕하세요 " + input_VÆRDI.getText());
        System.out.println("SWING CLICK " + input_VÆRDI.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
