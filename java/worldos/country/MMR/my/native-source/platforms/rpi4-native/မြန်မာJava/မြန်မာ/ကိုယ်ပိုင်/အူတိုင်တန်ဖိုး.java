// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
/** ကိုယ်ပိုင် JVM က ချိတ်ဆက်ပေးသော ပုံသေ ABI။ JNI သို့မဟုတ် အလိုရှိသည့် native နည်း တင်စက် မဟုတ်ပါ။ */
public final class အူတိုင်တန်ဖိုး {
    private အူတိုင်တန်ဖိုး() {}
    public static native int မီလီစက္ကန့်();
    public static native int ပုံစောင့်();
    public static native int မျက်နှာပြင်အနံ();
    public static native int မျက်နှာပြင်အမြင့်();
    public static native int စတုဂံ(int အလျားတည်နေရာ, int ဒေါင်လိုက်တည်နေရာ, int အကျယ်အဝန်း, int အမြင့်တန်ဖိုး, int အရောင်တန်ဖိုး);
}
