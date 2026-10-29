// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Finestra;
    JLabel LLEGIU_ME_eb81d7d9;
    JTextField 입력;
    public void run() {
        Finestra = new JFrame("propi nucli_VALOR Swing");
        Finestra.setSize(400, 280);
        Finestra.setLocationRelativeTo(null);
        Finestra.setLayout(null);
        Finestra.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LLEGIU_ME_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LLEGIU_ME_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nom");
        입력.setBounds(20, 65, 340, 30);
        JButton Botó = new JButton("인사하기");
        Botó.setBounds(20, 110, 180, 32);
        Botó.addActionListener(this);
        Finestra.add(LLEGIU_ME_eb81d7d9); Finestra.add(입력); Finestra.add(Botó);
        Finestra.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Esdeveniment) {
        LLEGIU_ME_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
