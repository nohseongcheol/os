// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4 UDP ဒေတာစာ ဆက်သွယ်မှု။ ပြင်ပလိပ်စာများအတွက် ဂဏန်းလိပ်စာကို သုံးသည်။ */
public final class ဆက်သွယ်မှု {
    private ဆက်သွယ်မှု() {}
    public static DatagramSocket ဖွင့်(int ဆက်သွယ်ပေါက်တန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try { return new DatagramSocket(ဆက်သွယ်ပေါက်တန်ဖိုး);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static void ပို့(DatagramSocket ဆုံးမှတ်, int ဆက်သွယ်ပေါက်တန်ဖိုး, String အကြောင်းအရာတန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try {
        ပို့(ဆုံးမှတ်, "127.0.0.1", ဆက်သွယ်ပေါက်တန်ဖိုး, အကြောင်းအရာတန်ဖိုး);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static void ပို့(DatagramSocket ဆုံးမှတ်, String လိပ်စာ, int ဆက်သွယ်ပေါက်တန်ဖိုး, String အကြောင်းအရာတန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try {
        byte[] ဘိုက်တန်ဖိုး = အက္ခရာ.ကုဒ်သွင်း(အကြောင်းအရာတန်ဖိုး);
        ဆုံးမှတ်.send(new DatagramPacket(ဘိုက်တန်ဖိုး, ဘိုက်တန်ဖိုး.length, InetAddress.getByName(လိပ်စာ), ဆက်သွယ်ပေါက်တန်ဖိုး));
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static String လက်ခံ(DatagramSocket ဆုံးမှတ်) throws အဝင်အထွက်ခြွင်းချက် {
        try {
        byte[] ဘိုက်တန်ဖိုး = new byte[512]; DatagramPacket ဒေတာစာ = new DatagramPacket(ဘိုက်တန်ဖိုး, ဘိုက်တန်ဖိုး.length); ဆုံးမှတ်.receive(ဒေတာစာ);
        byte[] ရလဒ် = new byte[ဒေတာစာ.getLength()]; System.arraycopy(ဘိုက်တန်ဖိုး, 0, ရလဒ်, 0, ရလဒ်.length); return အက္ခရာ.လျှို့ဝှက်ကုဒ်ဖြည်(ရလဒ်);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static void စောင့်ချိန်(DatagramSocket ဆုံးမှတ်, int မီလီစက္ကန့်) throws အဝင်အထွက်ခြွင်းချက် {
        try { ဆုံးမှတ်.setSoTimeout(မီလီစက္ကန့်);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static void ပိတ်(DatagramSocket ဆုံးမှတ်) { ဆုံးမှတ်.close(); }
}
