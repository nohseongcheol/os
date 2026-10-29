// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame መስኮት;
    JLabel ኣንብበኒ_eb81d7d9;
    JTextField 입력;
    public void run() {
        መስኮት = new JFrame("자체 ፍረ_ዋጋ Swing");
        መስኮት.setSize(400, 280);
        መስኮት.setLocationRelativeTo(null);
        መስኮት.setLayout(null);
        መስኮት.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ኣንብበኒ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ኣንብበኒ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ሽም");
        입력.setBounds(20, 65, 340, 30);
        JButton መጠወቒ = new JButton("인사하기");
        መጠወቒ.setBounds(20, 110, 180, 32);
        መጠወቒ.addActionListener(this);
        መስኮት.add(ኣንብበኒ_eb81d7d9); መስኮት.add(입력); መስኮት.add(መጠወቒ);
        መስኮት.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ፍጻመ) {
        ኣንብበኒ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
