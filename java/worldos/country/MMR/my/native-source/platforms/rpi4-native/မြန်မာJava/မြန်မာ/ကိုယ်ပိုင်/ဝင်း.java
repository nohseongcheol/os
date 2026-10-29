// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
/** ကိုယ်ပိုင် JVM နှင့် အူတိုင်ဝင်းစီမံမှုသို့ တိုက်ရိုက် ချိတ်ဆက်သော ဝင်း။ */
public final class ဝင်း extends မျက်နှာပြင်အင်္ဂါရပ် {
    public ဝင်း(String ဝင်းခေါင်းစဉ်, int အကျယ်အဝန်း, int အမြင့်တန်ဖိုး) {
        throw new အခြေအနေခြွင်းချက်("ကိုယ်ပိုင် JVM တွင် မြန်မာ API ဝင်းဖန်တီးမှု ပံ့ပိုးရမည်။");
    }
    public native void ထည့်သွင်း(မျက်နှာပြင်အင်္ဂါရပ် အင်္ဂါရပ်တန်ဖိုး);
    public native void ပြသ();
    public native void ပိတ်();
    public native boolean ဖြစ်သောမြင်နိုင်();
}
