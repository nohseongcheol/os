// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** တစ်ဖက်နှင့် ချိတ်ထားသော TCP ဘိုက်စီးကြောင်း၏ အဆုံးမှတ်။ */
public final class ဆက်သွယ်လမ်းကြောင်း {
    private final java.net.Socket စံစာကြည့်တိုက်တံတား;
    ဆက်သွယ်လမ်းကြောင်း(java.net.Socket စံစာကြည့်တိုက်တံတား) { this.စံစာကြည့်တိုက်တံတား = စံစာကြည့်တိုက်တံတား; }
    public static ဆက်သွယ်လမ်းကြောင်း ဖွင့်(String လိပ်စာ, int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try {
            return new ဆက်သွယ်လမ်းကြောင်း(new java.net.Socket(လိပ်စာ, ဆက်သွယ်ပေါက်ကိန်း));
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public ဝင်စီးကြောင်း ဝင်ဒေတာ() throws အဝင်အထွက်ခြွင်းချက် {
        try { return new ဝင်စီးကြောင်း(စံစာကြည့်တိုက်တံတား.getInputStream());
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public ထွက်စီးကြောင်း အထွက်() throws အဝင်အထွက်ခြွင်းချက် {
        try { return new ထွက်စီးကြောင်း(စံစာကြည့်တိုက်တံတား.getOutputStream());
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void စောင့်ချိန်(int မီလီစက္ကန့်) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစာကြည့်တိုက်တံတား.setSoTimeout(မီလီစက္ကန့်);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public int ဆက်သွယ်ပေါက်ကိန်း() { return စံစာကြည့်တိုက်တံတား.getPort(); }
    public int ဒေသတွင်းဆက်သွယ်ပေါက်ကိန်း() { return စံစာကြည့်တိုက်တံတား.getLocalPort(); }
    public boolean ပိတ်ပြီးသလား() { return စံစာကြည့်တိုက်တံတား.isClosed(); }
    public boolean ချိတ်ဆက်ပြီး() { return စံစာကြည့်တိုက်တံတား.isConnected(); }
    public void ပိတ်() throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစာကြည့်တိုက်တံတား.close();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
}
