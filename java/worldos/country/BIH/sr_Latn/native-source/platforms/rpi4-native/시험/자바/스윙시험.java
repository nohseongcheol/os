// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame prozor;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        prozor = new JFrame("자체 jezgro_VALUE Swing");
        prozor.setSize(400, 280);
        prozor.setLocationRelativeTo(null);
        prozor.setLayout(null);
        prozor.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ime");
        입력.setBounds(20, 65, 340, 30);
        JButton taster = new JButton("인사하기");
        taster.setBounds(20, 110, 180, 32);
        taster.addActionListener(this);
        prozor.add(안내); prozor.add(입력); prozor.add(taster);
        prozor.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent događaj) {
        안내.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
