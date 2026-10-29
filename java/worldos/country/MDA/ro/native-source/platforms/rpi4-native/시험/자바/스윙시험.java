// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Fereastră;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        Fereastră = new JFrame("propriu nucleu_VALUE Swing");
        Fereastră.setSize(400, 280);
        Fereastră.setLocationRelativeTo(null);
        Fereastră.setLayout(null);
        Fereastră.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nume");
        입력.setBounds(20, 65, 340, 30);
        JButton buton = new JButton("인사하기");
        buton.setBounds(20, 110, 180, 32);
        buton.addActionListener(this);
        Fereastră.add(안내); Fereastră.add(입력); Fereastră.add(buton);
        Fereastră.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Eveniment) {
        안내.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
