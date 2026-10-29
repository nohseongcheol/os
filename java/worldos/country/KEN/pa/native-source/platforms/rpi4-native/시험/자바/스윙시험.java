// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ਵਿੰਡੋ;
    JLabel ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9;
    JTextField 입력;
    public void run() {
        ਵਿੰਡੋ = new JFrame("자체 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ Swing");
        ਵਿੰਡੋ.setSize(400, 280);
        ਵਿੰਡੋ.setLocationRelativeTo(null);
        ਵਿੰਡੋ.setLayout(null);
        ਵਿੰਡੋ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ਨਾਂ");
        입력.setBounds(20, 65, 340, 30);
        JButton ਬਟਨ = new JButton("인사하기");
        ਬਟਨ.setBounds(20, 110, 180, 32);
        ਬਟਨ.addActionListener(this);
        ਵਿੰਡੋ.add(ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9); ਵਿੰਡੋ.add(입력); ਵਿੰਡੋ.add(ਬਟਨ);
        ਵਿੰਡੋ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ਇਵੈਂਟ) {
        ਫਈਲ_ਮੈਨੂੰ_ਪੜਨ_ਦਿਉ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
