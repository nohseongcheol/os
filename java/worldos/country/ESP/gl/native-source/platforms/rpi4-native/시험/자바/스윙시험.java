// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Xanela;
    JLabel Léame_eb81d7d9;
    JTextField 입력;
    public void run() {
        Xanela = new JFrame("자체 kernel_VALOR Swing");
        Xanela.setSize(400, 280);
        Xanela.setLocationRelativeTo(null);
        Xanela.setLayout(null);
        Xanela.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Léame_eb81d7d9 = new JLabel("한글로 Java 코딩");
        Léame_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Nome");
        입력.setBounds(20, 65, 340, 30);
        JButton botón = new JButton("인사하기");
        botón.setBounds(20, 110, 180, 32);
        botón.addActionListener(this);
        Xanela.add(Léame_eb81d7d9); Xanela.add(입력); Xanela.add(botón);
        Xanela.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Evento) {
        Léame_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
