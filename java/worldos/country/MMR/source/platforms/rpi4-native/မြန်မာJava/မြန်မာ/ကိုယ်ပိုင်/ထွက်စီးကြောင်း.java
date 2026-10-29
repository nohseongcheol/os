// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** အစဉ်ကို ထိန်း၍ ထုတ်ပေးသော ဘိုက်လမ်းကြောင်း။ */
public final class ထွက်စီးကြောင်း {
    private final java.io.OutputStream စံစီးကြောင်း;
    ထွက်စီးကြောင်း(java.io.OutputStream စံစီးကြောင်း) { this.စံစီးကြောင်း = စံစီးကြောင်း; }
    public void ရေး(int တန်ဖိုး) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစီးကြောင်း.write(တန်ဖိုး);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void ရေး(byte[] ဒေတာ) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစီးကြောင်း.write(ဒေတာ);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void ရေး(byte[] ဒေတာ, int လုပ်ဆောင်, int အလျား) throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစီးကြောင်း.write(ဒေတာ, လုပ်ဆောင်, အလျား);
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void တန်ဖိုးထုတ်လွှတ်() throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစီးကြောင်း.flush();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
    public void ပိတ်() throws အဝင်အထွက်ခြွင်းချက် {
        try { စံစီးကြောင်း.close();
        } catch (java.io.IOException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.အဝင်အထွက်(အမှား); }
        catch (RuntimeException အမှား) { throw ခြွင်းချက်ပြောင်းလဲ.စက်မောင်း(အမှား); }
    }
}
