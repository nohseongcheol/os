// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** ဒေတာစာနယ်နိမိတ်ကို ထိန်း၍ UDP ဒေတာ ပို့လက်ခံသော အဆုံးမှတ်။ */
public final class ဒေတာပို့လမ်း {
    private final java.net.DatagramSocket စံအဆုံးမှတ်;
    private ဒေတာပို့လမ်း(int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံအဆုံးမှတ် = ဆက်သွယ်မှု.ဖွင့်(ဆက်သွယ်ပေါက်ကိန်း);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static ဒေတာပို့လမ်း ဖွင့်(int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try { return new ဒေတာပို့လမ်း(ဆက်သွယ်ပေါက်ကိန်း);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void ပို့(String လိပ်စာ, int ဆက်သွယ်ပေါက်ကိန်း, String ဒေတာ) throws အဝင်အထွက်ခြွင်းချက် {
        try { ဆက်သွယ်မှု.ပို့(စံအဆုံးမှတ်, လိပ်စာ, ဆက်သွယ်ပေါက်ကိန်း, ဒေတာ);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public String လက်ခံ() throws အဝင်အထွက်ခြွင်းချက် {
        try { return ဆက်သွယ်မှု.လက်ခံ(စံအဆုံးမှတ်);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void စောင့်ချိန်(int မီလီစက္ကန့်) throws အဝင်အထွက်ခြွင်းချက် {
        try { ဆက်သွယ်မှု.စောင့်ချိန်(စံအဆုံးမှတ်, မီလီစက္ကန့်);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public int ဆက်သွယ်ပေါက်ကိန်း() { return စံအဆုံးမှတ်.getLocalPort(); }
    public boolean ပိတ်ပြီးသလား() { return စံအဆုံးမှတ်.isClosed(); }
    public void ပိတ်() { ဆက်သွယ်မှု.ပိတ်(စံအဆုံးမှတ်); }
}
