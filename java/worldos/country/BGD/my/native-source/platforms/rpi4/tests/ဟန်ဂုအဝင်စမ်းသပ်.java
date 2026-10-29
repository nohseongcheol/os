// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import javax.swing.*;
import java.awt.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Base64;

public class ဟန်ဂုအဝင်စမ်းသပ် {
    public static void main(String[] အချက်များ) throws Exception {
        System.setProperty("awt.useSystemAAFontSettings", "on");
        System.setProperty("swing.aatext", "true");
        SwingUtilities.invokeLater(() -> {
            JFrame ဝင်း = new JFrame("한글 ဝင်ဒေတာ · စာလုံးပုံစံတန်ဖိုး အတည်ပြု");
            JPanel ထုတ်ဝေမှုတန်ဖိုး = new JPanel(new BorderLayout(10, 15));
            ထုတ်ဝေမှုတန်ဖိုး.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
            JLabel လမ်းညွှန် = new JLabel("Ctrl+Space → 한글 ဝင်ဒေတာ → Ctrl+Space → Enter");
            JTextField ဝင်ဒေတာ = new JTextField();
            Font စာလုံးပုံစံတန်ဖိုး = new Font("Dialog", Font.PLAIN, 20);
            လမ်းညွှန်.setFont(စာလုံးပုံစံတန်ဖိုး.deriveFont(16f)); ဝင်ဒေတာ.setFont(စာလုံးပုံစံတန်ဖိုး);
            ဝင်ဒေတာ.enableInputMethods(true);
            ဝင်ဒေတာ.addActionListener(ဖြစ်ရပ် -> {
                String ရလဒ် = ဝင်ဒေတာ.getText().trim();
                try {
                    Files.writeString(Path.of(System.getProperty("user.home"), "한글입력검증.txt"), ရလဒ်, StandardCharsets.UTF_8);
                } catch (Exception အမှား) { throw new RuntimeException(အမှား); }
                System.out.println("JKOROS_HANGUL_RESULT " + Base64.getEncoder().encodeToString(ရလဒ်.getBytes(StandardCharsets.UTF_8)));
            });
            ထုတ်ဝေမှုတန်ဖိုး.add(လမ်းညွှန်, BorderLayout.NORTH); ထုတ်ဝေမှုတန်ဖိုး.add(ဝင်ဒေတာ, BorderLayout.CENTER);
            ဝင်း.add(ထုတ်ဝေမှုတန်ဖိုး); ဝင်း.setSize(850, 230); ဝင်း.setLocation(100, 100);
            ဝင်း.setAlwaysOnTop(true); ဝင်း.setVisible(true); ဝင်ဒေတာ.requestFocusInWindow();
            Timer ပြင်ဆင် = new Timer(1000, ဖြစ်ရပ် -> {
                Point နေရာ = ဝင်ဒေတာ.getLocationOnScreen();
                System.out.println("JKOROS_HANGUL_READY " + (နေရာ.x + 100) + " " + (နေရာ.y + 30));
            });
            ပြင်ဆင်.setRepeats(false); ပြင်ဆင်.start();
        });
    }
}
