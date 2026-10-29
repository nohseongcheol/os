// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class PruebaSwing implements Runnable, ActionListener {
    JFrame ventana;
    JLabel Guía;
    JTextField valorEntrada;
    public void run() {
        ventana = new JFrame("propio valorNúcleo Swing");
        ventana.setSize(400, 280);
        ventana.setLocationRelativeTo(null);
        ventana.setLayout(null);
        ventana.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Guía = new JLabel("한글로 Java 코딩");
        Guía.setBounds(20, 20, 340, 30);
        valorEntrada = new JTextField("nombre");
        valorEntrada.setBounds(20, 65, 340, 30);
        JButton botón = new JButton("saludar");
        botón.setBounds(20, 110, 180, 32);
        botón.addActionListener(this);
        ventana.add(Guía); ventana.add(valorEntrada); ventana.add(botón);
        ventana.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent evento) {
        Guía.setText("안녕하세요 " + valorEntrada.getText());
        System.out.println("SWING CLICK " + valorEntrada.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new PruebaSwing());
    }
}
