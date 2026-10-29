// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** ဝင်လာသော TCP ချိတ်ဆက်မှုများကို လက်ခံသော ဆက်သွယ်ပေါက်။ */
public final class ဆက်သွယ်ပေါက်လက်ခံရယူ {
    private final java.net.ServerSocket စံဆက်သွယ်ပေါက်;
    private ဆက်သွယ်ပေါက်လက်ခံရယူ(int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံဆက်သွယ်ပေါက် = new java.net.ServerSocket(ဆက်သွယ်ပေါက်ကိန်း);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public static ဆက်သွယ်ပေါက်လက်ခံရယူ ဖွင့်(int ဆက်သွယ်ပေါက်ကိန်း) throws အဝင်အထွက်ခြွင်းချက် {
        try { return new ဆက်သွယ်ပေါက်လက်ခံရယူ(ဆက်သွယ်ပေါက်ကိန်း);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public ဆက်သွယ်လမ်းကြောင်း လက်ခံ() throws အဝင်အထွက်ခြွင်းချက် {
        try { return new ဆက်သွယ်လမ်းကြောင်း(စံဆက်သွယ်ပေါက်.accept());
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public int ဆက်သွယ်ပေါက်ကိန်း() { return စံဆက်သွယ်ပေါက်.getLocalPort(); }
    public void စောင့်ချိန်(int မီလီစက္ကန့်) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံဆက်သွယ်ပေါက်.setSoTimeout(မီလီစက္ကန့်);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public boolean ပိတ်ပြီးသလား() { return စံဆက်သွယ်ပေါက်.isClosed(); }
    public void ပိတ်() throws အဝင်အထွက်ခြွင်းချက် {
        try { စံဆက်သွယ်ပေါက်.close();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
}
