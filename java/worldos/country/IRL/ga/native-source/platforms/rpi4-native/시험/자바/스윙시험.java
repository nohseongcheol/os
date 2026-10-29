// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame fuinneog;
    JLabel LÉIGHMÉ_eb81d7d9;
    JTextField 입력;
    public void run() {
        fuinneog = new JFrame("자체 eithne_VALUE Swing");
        fuinneog.setSize(400, 280);
        fuinneog.setLocationRelativeTo(null);
        fuinneog.setLayout(null);
        fuinneog.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        LÉIGHMÉ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        LÉIGHMÉ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("Ainm");
        입력.setBounds(20, 65, 340, 30);
        JButton cnaipe = new JButton("인사하기");
        cnaipe.setBounds(20, 110, 180, 32);
        cnaipe.addActionListener(this);
        fuinneog.add(LÉIGHMÉ_eb81d7d9); fuinneog.add(입력); fuinneog.add(cnaipe);
        fuinneog.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ócáid) {
        LÉIGHMÉ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
