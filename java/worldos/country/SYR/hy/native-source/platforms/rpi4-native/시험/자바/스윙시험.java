// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame պատուհան;
    JLabel ԿԱՐԴԱ_ԻՆՁ_eb81d7d9;
    JTextField 입력;
    public void run() {
        պատուհան = new JFrame("자체 միջուկ_արժեք Swing");
        պատուհան.setSize(400, 280);
        պատուհան.setLocationRelativeTo(null);
        պատուհան.setLayout(null);
        պատուհան.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ԿԱՐԴԱ_ԻՆՁ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ԿԱՐԴԱ_ԻՆՁ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Անուն");
        입력.setBounds(20, 65, 340, 30);
        JButton կոճակ = new JButton("인사하기");
        կոճակ.setBounds(20, 110, 180, 32);
        կոճակ.addActionListener(this);
        պատուհան.add(ԿԱՐԴԱ_ԻՆՁ_eb81d7d9); պատուհան.add(입력); պատուհան.add(կոճակ);
        պատուհան.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent միջոցառում) {
        ԿԱՐԴԱ_ԻՆՁ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
