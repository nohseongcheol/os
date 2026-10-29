// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame Прозорец;
    JLabel 안내;
    JTextField 입력;
    public void run() {
        Прозорец = new JFrame("자체 ядро_стойност Swing");
        Прозорец.setSize(400, 280);
        Прозорец.setLocationRelativeTo(null);
        Прозорец.setLayout(null);
        Прозорец.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        안내 = new JLabel("한글로 Java 코딩");
        안내.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Име");
        입력.setBounds(20, 65, 340, 30);
        JButton бутон = new JButton("인사하기");
        бутон.setBounds(20, 110, 180, 32);
        бутон.addActionListener(this);
        Прозорец.add(안내); Прозорец.add(입력); Прозорец.add(бутон);
        Прозорец.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent Събитие) {
        안내.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
