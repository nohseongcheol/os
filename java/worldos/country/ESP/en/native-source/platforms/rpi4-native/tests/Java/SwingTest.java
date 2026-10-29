// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class SwingTest implements Runnable, ActionListener {
    JFrame window;
    JLabel README;
    JTextField inputValue;
    public void run() {
        window = new JFrame("Native kernelValue Swing");
        window.setSize(400, 280);
        window.setLocationRelativeTo(null);
        window.setLayout(null);
        window.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        README = new JLabel("한글로 Java 코딩");
        README.setBounds(20, 20, 340, 30);
        inputValue = new JTextField("name");
        inputValue.setBounds(20, 65, 340, 30);
        JButton button = new JButton("greet");
        button.setBounds(20, 110, 180, 32);
        button.addActionListener(this);
        window.add(README); window.add(inputValue); window.add(button);
        window.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent event) {
        README.setText("안녕하세요 " + inputValue.getText());
        System.out.println("SWING CLICK " + inputValue.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new SwingTest());
    }
}
