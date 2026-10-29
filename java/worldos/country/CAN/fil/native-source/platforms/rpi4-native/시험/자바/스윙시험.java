// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame window;
    JLabel BASAHINAKO_eb81d7d9;
    JTextField 입력;
    public void run() {
        window = new JFrame("자체 kernel_VALUE Swing");
        window.setSize(400, 280);
        window.setLocationRelativeTo(null);
        window.setLayout(null);
        window.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        BASAHINAKO_eb81d7d9 = new JLabel("한글로 Java 코딩");
        BASAHINAKO_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("pangalan");
        입력.setBounds(20, 65, 340, 30);
        JButton button = new JButton("인사하기");
        button.setBounds(20, 110, 180, 32);
        button.addActionListener(this);
        window.add(BASAHINAKO_eb81d7d9); window.add(입력); window.add(button);
        window.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent kaganapan) {
        BASAHINAKO_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
