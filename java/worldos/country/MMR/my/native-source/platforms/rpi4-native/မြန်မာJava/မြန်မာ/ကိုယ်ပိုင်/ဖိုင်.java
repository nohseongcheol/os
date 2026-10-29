// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** ဖိုင်ဟူသော သုံးစွဲသူရင်းနှီးပြီး ဝေါဟာရကို ထိန်းထားသည်။ လက်ရှိ သိုလှောင်ရာသည် စက်ပြန်နှိုးလျှင် ပျောက်သွားသော RAM ဖိုင်ဖြစ်သည်။ */
public final class ဖိုင် {
    private ဖိုင်() {}
    public static byte[] ဘိုက်တန်ဖိုးဖတ်(String အမည်) throws အဝင်အထွက်ခြွင်းချက် {
        try {
        FileInputStream စီးကြောင်းတန်ဖိုး = new FileInputStream(အမည်);
        try {
            byte[] ယာယီတန်ဖိုး = new byte[16384]; int ကိန်းတန်ဖိုး = 0, တန်ဖိုး;
            while ((တန်ဖိုး = စီးကြောင်းတန်ဖိုး.read()) != -1) { if (ကိန်းတန်ဖိုး == ယာယီတန်ဖိုး.length) throw new အဝင်အထွက်ခြွင်းချက်("ဖိုင်အရွယ်အကန့်"); ယာယီတန်ဖိုး[ကိန်းတန်ဖိုး++] = (byte)တန်ဖိုး; }
            byte[] ရလဒ် = new byte[ကိန်းတန်ဖိုး]; System.arraycopy(ယာယီတန်ဖိုး, 0, ရလဒ်, 0, ကိန်းတန်ဖိုး); return ရလဒ်;
        } finally { စီးကြောင်းတန်ဖိုး.close(); }
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static void ဘိုက်တန်ဖိုးရေး(String အမည်, byte[] အကြောင်းအရာတန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try {
        FileOutputStream စီးကြောင်းတန်ဖိုး = new FileOutputStream(အမည်);
        try { for (int ထပ်ခါလည်ပတ်မှုအညွှန်းကိန်း = 0; ထပ်ခါလည်ပတ်မှုအညွှန်းကိန်း < အကြောင်းအရာတန်ဖိုး.length; ထပ်ခါလည်ပတ်မှုအညွှန်းကိန်း++) စီးကြောင်းတန်ဖိုး.write(အကြောင်းအရာတန်ဖိုး[ထပ်ခါလည်ပတ်မှုအညွှန်းကိန်း] & 255); } finally { စီးကြောင်းတန်ဖိုး.close(); }
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static String ဖတ်(String အမည်) throws အဝင်အထွက်ခြွင်းချက် {
        try { return အက္ခရာ.လျှို့ဝှက်ကုဒ်ဖြည်(ဘိုက်တန်ဖိုးဖတ်(အမည်));
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static void ရေး(String အမည်, String အကြောင်းအရာတန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try { ဘိုက်တန်ဖိုးရေး(အမည်, အက္ခရာ.ကုဒ်သွင်း(အကြောင်းအရာတန်ဖိုး));
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
}
