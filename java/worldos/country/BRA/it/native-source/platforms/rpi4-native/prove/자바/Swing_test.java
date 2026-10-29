// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_test implements Runnable, ActionListener {
    JFrame Finestra;
    JLabel README_eb81d7d9;
    JTextField input_VALORE;
    public void run() {
        Finestra = new JFrame("nativo kernel_VALORE Swing");
        Finestra.setSize(400, 280);
        Finestra.setLocationRelativeTo(null);
        Finestra.setLayout(null);
        Finestra.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README_eb81d7d9 = new JLabel("한글로 Java 코딩");
        README_eb81d7d9.setBounds(20, 20, 340, 30);
        input_VALORE = new JTextField("Nome");
        input_VALORE.setBounds(20, 65, 340, 30);
        JButton pulsante = new JButton("인사하기");
        pulsante.setBounds(20, 110, 180, 32);
        pulsante.addActionListener(this);
        Finestra.add(README_eb81d7d9); Finestra.add(input_VALORE); Finestra.add(pulsante);
        Finestra.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Evento) {
        README_eb81d7d9.setText("안녕하세요 " + input_VALORE.getText());
        System.out.println("SWING CLICK " + input_VALORE.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_test());
    }
}
