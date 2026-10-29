// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.Java;

import javax.swing.*;

public final class မျက်နှာပြင် {
    private မျက်နှာပြင်() {}
    public static void နောက်မှ(Runnable လှုပ်ရှားမှု) { SwingUtilities.invokeLater(လှုပ်ရှားမှု); }
    /** Swing ဖြစ်ရပ်ကိုင်တွယ်အလုပ်ကြိုးမှ ခေါ်ပါ။ */
    public static JFrame ဝင်း(String ဝင်းခေါင်းစဉ်, JComponent အကြောင်းအရာတန်ဖိုး, int အနံတန်ဖိုး, int အမြင့်တန်ဖိုး) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("မျက်နှာပြင်.နောက်မှ 안에서 창을 만드세요");
        JFrame ဝင်း = new JFrame(ဝင်းခေါင်းစဉ်);
        ဝင်း.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ဝင်း.setContentPane(အကြောင်းအရာတန်ဖိုး);
        ဝင်း.setSize(အနံတန်ဖိုး, အမြင့်တန်ဖိုး);
        ဝင်း.setLocationByPlatform(true);
        ဝင်း.setVisible(true);
        return ဝင်း;
    }
}
