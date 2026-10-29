// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.event.*;
public class ThửSwing implements Runnable, ActionListener {
    JFrame cửaSổ;
    JLabel HướngDẫn;
    JTextField giáTrịVào;
    public void run() {
        cửaSổ = new JFrame("tựThân giáTrịNhân Swing");
        cửaSổ.setSize(400, 280);
        cửaSổ.setLocationRelativeTo(null);
        cửaSổ.setLayout(null);
        cửaSổ.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        HướngDẫn = new JLabel("한글로 Java 코딩");
        HướngDẫn.setBounds(20, 20, 340, 30);
        giáTrịVào = new JTextField("tên");
        giáTrịVào.setBounds(20, 65, 340, 30);
        JButton nút = new JButton("chào");
        nút.setBounds(20, 110, 180, 32);
        nút.addActionListener(this);
        cửaSổ.add(HướngDẫn); cửaSổ.add(giáTrịVào); cửaSổ.add(nút);
        cửaSổ.setVisible(true);
        System.out.println("SWING READY");
    }
    public void actionPerformed(ActionEvent sựKiện) {
        HướngDẫn.setText("안녕하세요 " + giáTrịVào.getText());
        System.out.println("SWING CLICK " + giáTrịVào.getText());
        System.out.println(SwingUtilities.isEventDispatchThread());
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new ThửSwing());
    }
}
