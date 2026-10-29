// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame کړکۍ;
    JLabel ماولوله_eb81d7d9;
    JTextField 입력;
    public void run() {
        کړکۍ = new JFrame("자체 نوغی_ارزښت Swing");
        کړکۍ.setSize(400, 280);
        کړکۍ.setLocationRelativeTo(null);
        کړکۍ.setLayout(null);
        کړکۍ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ماولوله_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ماولوله_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("نوم");
        입력.setBounds(20, 65, 340, 30);
        JButton تڼۍ = new JButton("인사하기");
        تڼۍ.setBounds(20, 110, 180, 32);
        تڼۍ.addActionListener(this);
        کړکۍ.add(ماولوله_eb81d7d9); کړکۍ.add(입력); کړکۍ.add(تڼۍ);
        کړکۍ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent پېښه) {
        ماولوله_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
