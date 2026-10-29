// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame 창;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        창 = new JFrame("자체 커널 Swing");
        창.setSize(400, 280);
        창.setLocationRelativeTo(null);
        창.setLayout(null);
        창.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nom");
        입력.setBounds(20, 65, 340, 30);
        JButton Boton = new JButton("인사하기");
        Boton.setBounds(20, 110, 180, 32);
        Boton.addActionListener(this);
        창.add(안내); 창.add(입력); 창.add(Boton);
        창.setVisible(true);
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
