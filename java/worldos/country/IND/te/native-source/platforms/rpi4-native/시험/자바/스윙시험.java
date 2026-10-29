// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame విండో;
    JLabel మార్గదర్శక_సమాచారం_eb81d7d9;
    JTextField 입력;
    public void run() {
        విండో = new JFrame("자체 కెర్నల్_మూల్యం Swing");
        విండో.setSize(400, 280);
        విండో.setLocationRelativeTo(null);
        విండో.setLayout(null);
        విండో.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        మార్గదర్శక_సమాచారం_eb81d7d9 = new JLabel("한글로 Java 코딩");
        మార్గదర్శక_సమాచారం_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("పేరు");
        입력.setBounds(20, 65, 340, 30);
        JButton బటన్ = new JButton("인사하기");
        బటన్.setBounds(20, 110, 180, 32);
        బటన్.addActionListener(this);
        విండో.add(మార్గదర్శక_సమాచారం_eb81d7d9); విండో.add(입력); విండో.add(బటన్);
        విండో.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ఈవెంట్) {
        మార్గదర్శక_సమాచారం_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
