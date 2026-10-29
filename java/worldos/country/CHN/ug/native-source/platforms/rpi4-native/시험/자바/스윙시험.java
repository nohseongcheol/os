// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class 스윙시험 implements Runnable, ActionListener {
    JFrame كۆزنەك;
    JLabel چۈشەندۈرۈش_ھۆججىتى_eb81d7d9;
    JTextField 입력;
    public void run() {
        كۆزنەك = new JFrame("자체 يادرو_قىممىتى Swing");
        كۆزنەك.setSize(400, 280);
        كۆزنەك.setLocationRelativeTo(null);
        كۆزنەك.setLayout(null);
        كۆزنەك.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        چۈشەندۈرۈش_ھۆججىتى_eb81d7d9 = new JLabel("한글로 Java 코딩");
        چۈشەندۈرۈش_ھۆججىتى_eb81d7d9.setBounds(20, 20, 340, 30);
        입력 = new JTextField("ئاتى");
        입력.setBounds(20, 65, 340, 30);
        JButton كۇنۇپكا = new JButton("인사하기");
        كۇنۇپكا.setBounds(20, 110, 180, 32);
        كۇنۇپكا.addActionListener(this);
        كۆزنەك.add(چۈشەندۈرۈش_ھۆججىتى_eb81d7d9); كۆزنەك.add(입력); كۆزنەك.add(كۇنۇپكا);
        كۆزنەك.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ھادىسە) {
        چۈشەندۈرۈش_ھۆججىتى_eb81d7d9.setText("안녕하세요 " + 입력.getText());
        System.out.println("SWING CLICK " + 입력.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new 스윙시험());
    }
}
