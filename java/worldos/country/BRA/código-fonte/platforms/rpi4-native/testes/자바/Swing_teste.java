// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swing_teste implements Runnable, ActionListener {
    JFrame Janela;
    JLabel LEIAME_eb81d7d9;
    JTextField entrada_VALOR;
    public void run() {
        Janela = new JFrame("nativo kernel_VALOR Swing");
        Janela.setSize(400, 280);
        Janela.setLocationRelativeTo(null);
        Janela.setLayout(null);
        Janela.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LEIAME_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LEIAME_eb81d7d9.setBounds(20, 20, 340, 30);
        entrada_VALOR = new JTextField("Nome");
        entrada_VALOR.setBounds(20, 65, 340, 30);
        JButton botão = new JButton("인사하기");
        botão.setBounds(20, 110, 180, 32);
        botão.addActionListener(this);
        Janela.add(LEIAME_eb81d7d9); Janela.add(entrada_VALOR); Janela.add(botão);
        Janela.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Evento) {
        LEIAME_eb81d7d9.setText("안녕하세요 " + entrada_VALOR.getText());
        System.out.println("SWING CLICK " + entrada_VALOR.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swing_teste());
    }
}
