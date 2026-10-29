// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** အစဉ်လိုက် ဝင်လာသော ဘိုက်များကို ဖတ်သော လမ်းကြောင်း။ */
public final class ဝင်စီးကြောင်း {
    private final java.io.InputStream စံစီးကြောင်း;
    ဝင်စီးကြောင်း(java.io.InputStream စံစီးကြောင်း) { this.စံစီးကြောင်း = စံစီးကြောင်း; }
    public int ဖတ်() throws အဝင်အထွက်ခြွင်းချက် {
        try { return စံစီးကြောင်း.read();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public int ဖတ်(byte[] ဒေတာ) throws အဝင်အထွက်ခြွင်းချက် {
        try { return စံစီးကြောင်း.read(ဒေတာ);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public int ဖတ်(byte[] ဒေတာ, int လုပ်ဆောင်, int အလျား) throws အဝင်အထွက်ခြွင်းချက် {
        try { return စံစီးကြောင်း.read(ဒေတာ, လုပ်ဆောင်, အလျား);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void ပိတ်() throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစီးကြောင်း.close();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
}
