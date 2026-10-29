// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char အရေအတွက်နှင့် ယူနီကုဒ်ကုဒ်အမှတ် အရေအတွက်ကို ခွဲခြားသည်။ */
public final class အက္ခရာ {
    private အက္ခရာ() {}
    public static byte[] ကုဒ်သွင်း(String အကြောင်းအရာတန်ဖိုး) { return အကြောင်းအရာတန်ဖိုး.getBytes(StandardCharsets.UTF_8); }
    public static String လျှို့ဝှက်ကုဒ်ဖြည်(byte[] အကြောင်းအရာတန်ဖိုး) { return new String(အကြောင်းအရာတန်ဖိုး, StandardCharsets.UTF_8); }
    public static String စံပုံစံပြောင်း(String အကြောင်းအရာတန်ဖိုး) { return Normalizer.normalize(အကြောင်းအရာတန်ဖိုး, Normalizer.Form.NFC); }
    public static int ကုဒ်အမှတ်တစ်ခုအရေအတွက်(String အကြောင်းအရာတန်ဖိုး) { return အကြောင်းအရာတန်ဖိုး.codePointCount(0, အကြောင်းအရာတန်ဖိုး.length()); }
    public static List<String> ဝေါဟာရ(String အကြောင်းအရာတန်ဖိုး, Locale ဘာသာစကား) {
        BreakIterator စားကိန်း = BreakIterator.getWordInstance(ဘာသာစကား);
        စားကိန်း.setText(အကြောင်းအရာတန်ဖိုး);
        List<String> ရလဒ် = new ArrayList<>();
        int လုပ်ဆောင် = စားကိန်း.first();
        for (int အဆုံး = စားကိန်း.next(); အဆုံး != BreakIterator.DONE; လုပ်ဆောင် = အဆုံး, အဆုံး = စားကိန်း.next())
            ရလဒ်.add(အကြောင်းအရာတန်ဖိုး.substring(လုပ်ဆောင်, အဆုံး));
        return ရလဒ်;
    }
}
