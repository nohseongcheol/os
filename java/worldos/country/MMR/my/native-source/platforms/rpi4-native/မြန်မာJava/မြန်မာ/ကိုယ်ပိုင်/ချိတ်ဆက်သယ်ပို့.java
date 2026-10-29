// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
import java.net.*;
public final class ချိတ်ဆက်သယ်ပို့ {
    private ချိတ်ဆက်သယ်ပို့() {}
    public static ဆက်သွယ်လမ်းကြောင်း ဖွင့်(String လိပ်စာ, int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try { return ဆက်သွယ်လမ်းကြောင်း.ဖွင့်(လိပ်စာ, ဆက်သွယ်ပေါက်ကိန်း);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static ဆက်သွယ်ပေါက်လက်ခံရယူ လက်ခံသူဖွင့်(int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try { return ဆက်သွယ်ပေါက်လက်ခံရယူ.ဖွင့်(ဆက်သွယ်ပေါက်ကိန်း);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static Socket ချိတ်ဆက်(String လိပ်စာ, int ဆက်သွယ်ပေါက်တန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try { return new Socket(လိပ်စာ, ဆက်သွယ်ပေါက်တန်ဖိုး);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static ServerSocket အဆုံးမှတ်နားထောင်(int ဆက်သွယ်ပေါက်တန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try { return new ServerSocket(ဆက်သွယ်ပေါက်တန်ဖိုး);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static Socket လက်ခံ(ServerSocket ဝန်ဆောင်စက်တန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try { return ဝန်ဆောင်စက်တန်ဖိုး.accept();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
}
