// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Prozor;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        Prozor = new JFrame("vlastiti jezgra_sustava_VALUE Swing");
        Prozor.setSize(400, 280);
        Prozor.setLocationRelativeTo(null);
        Prozor.setLayout(null);
        Prozor.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ime");
        입력.setBounds(20, 65, 340, 30);
        JButton gumb = new JButton("인사하기");
        gumb.setBounds(20, 110, 180, 32);
        gumb.addActionListener(this);
        Prozor.add(안내); Prozor.add(입력); Prozor.add(gumb);
        Prozor.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Događaj) {
        안내.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
