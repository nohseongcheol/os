// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_preskusiti implements Runnable, ActionListener {
    JFrame okno;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        okno = new JFrame("lastno jedro_VALUE Swing");
        okno.setSize(400, 280);
        okno.setLocationRelativeTo(null);
        okno.setLayout(null);
        okno.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ime");
        입력.setBounds(20, 65, 340, 30);
        JButton Gumb = new JButton("인사하기");
        Gumb.setBounds(20, 110, 180, 32);
        Gumb.addActionListener(this);
        okno.add(안내); okno.add(입력); okno.add(Gumb);
        okno.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent dogodek) {
        안내.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_preskusiti());
    }
}
