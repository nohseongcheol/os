// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame matapihi;
    JLabel PĀNUIMAI_eb81d7d9;
    JTextField 입력;
    public void run() {
        matapihi = new JFrame("자체 kākano_uara_0611a8a8 Swing");
        matapihi.setSize(400, 280);
        matapihi.setLocationRelativeTo(null);
        matapihi.setLayout(null);
        matapihi.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        PĀNUIMAI_eb81d7d9 = new JLabel("한글로 Java 코딩");
        PĀNUIMAI_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ingoa");
        입력.setBounds(20, 65, 340, 30);
        JButton pātene = new JButton("인사하기");
        pātene.setBounds(20, 110, 180, 32);
        pātene.addActionListener(this);
        matapihi.add(PĀNUIMAI_eb81d7d9); matapihi.add(입력); matapihi.add(pātene);
        matapihi.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent hui) {
        PĀNUIMAI_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
