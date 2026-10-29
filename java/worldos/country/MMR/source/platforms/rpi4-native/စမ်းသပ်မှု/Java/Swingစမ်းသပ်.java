// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class Swingစမ်းသပ် implements Runnable, ActionListener {
    JFrame ဝင်း;
    JLabel လမ်းညွှန်;
    JTextField ဝင်ဒေတာ;
    public void run() {
        ဝင်း = new JFrame("ကိုယ်ပိုင် အူတိုင်တန်ဖိုး Swing");
        ဝင်း.setSize(400, 280);
        ဝင်း.setLocationRelativeTo(null);
        ဝင်း.setLayout(null);
        ဝင်း.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        လမ်းညွှန် = new JLabel("한글로 Java 코딩");
        လမ်းညွှန်.setBounds(20, 20, 340, 30);
        ဝင်ဒေတာ = new JTextField("အမည်");
        ဝင်ဒေတာ.setBounds(20, 65, 340, 30);
        JButton ခလုတ် = new JButton("နှုတ်ဆက်လုပ်ဆောင်");
        ခလုတ်.setBounds(20, 110, 180, 32);
        ခလုတ်.addActionListener(this);
        ဝင်း.add(လမ်းညွှန်); ဝင်း.add(ဝင်ဒေတာ); ဝင်း.add(ခလုတ်);
        ဝင်း.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent ဖြစ်ရပ်) {
        လမ်းညွှန်.setText("안녕하세요 " + ဝင်ဒေတာ.getText());
        System.out.println("SWING CLICK " + ဝင်ဒေတာ.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Swingစမ်းသပ်());
    }
}
