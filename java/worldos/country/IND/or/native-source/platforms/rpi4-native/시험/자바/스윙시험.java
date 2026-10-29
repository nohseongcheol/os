// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame ଓ୍ୱିଣ୍ଡୋ;
    JLabel ମତେପଢନ୍ତୁ_eb81d7d9;
    JTextField 입력;
    public void run() {
        ଓ୍ୱିଣ୍ଡୋ = new JFrame("자체 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ Swing");
        ଓ୍ୱିଣ୍ଡୋ.setSize(400, 280);
        ଓ୍ୱିଣ୍ଡୋ.setLocationRelativeTo(null);
        ଓ୍ୱିଣ୍ଡୋ.setLayout(null);
        ଓ୍ୱିଣ୍ଡୋ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ମତେପଢନ୍ତୁ_eb81d7d9 = new JLabel("한글로 Java 코딩");
        ମତେପଢନ୍ତୁ_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ନାମ");
        입력.setBounds(20, 65, 340, 30);
        JButton ବଟନ୍ = new JButton("인사하기");
        ବଟନ୍.setBounds(20, 110, 180, 32);
        ବଟନ୍.addActionListener(this);
        ଓ୍ୱିଣ୍ଡୋ.add(ମତେପଢନ୍ତୁ_eb81d7d9); ଓ୍ୱିଣ୍ଡୋ.add(입력); ଓ୍ୱିଣ୍ଡୋ.add(ବଟନ୍);
        ଓ୍ୱିଣ୍ଡୋ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ଘଟଣା) {
        ମତେପଢନ୍ତୁ_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
