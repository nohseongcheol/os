// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class TestSwing implements Runnable, ActionListener {
    JFrame fenêtre;
    JLabel Guide;
    JTextField valeurEntrée;
    public void run() {
        fenêtre = new JFrame("interne valeurNoyau Swing");
        fenêtre.setSize(400, 280);
        fenêtre.setLocationRelativeTo(null);
        fenêtre.setLayout(null);
        fenêtre.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        Guide = new JLabel("한글로 Java 코딩");
        Guide.setBounds(20, 20, 340, 30);
        valeurEntrée = new JTextField("nom");
        valeurEntrée.setBounds(20, 65, 340, 30);
        JButton bouton = new JButton("saluer");
        bouton.setBounds(20, 110, 180, 32);
        bouton.addActionListener(this);
        fenêtre.add(Guide); fenêtre.add(valeurEntrée); fenêtre.add(bouton);
        fenêtre.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent évènement) {
        Guide.setText("안녕하세요 " + valeurEntrée.getText());
        System.out.println("SWING CLICK " + valeurEntrée.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new TestSwing());
    }
}
