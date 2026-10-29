// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros သုံးစွဲသူ ELF အတွက် သီးသန့် API။ Linux/JVM အတွက် JNI သို့မဟုတ် java.net API မဟုတ်ပါ။ */
public final class သုံးစွဲသူ {
    public static native int ဖိုင်အညွှန်းဖွင့်(int[] ဖိုင်အချက်အမည်, int ဖွင့်ရန်သတ်မှတ်ချက်);
    public static native int ဖိုင်ဘိုက်တစ်ခုဖတ်(int ဖိုင်အညွှန်း);
    public static native int ဖိုင်ဘိုက်တစ်ခုရေး(int ဖိုင်အညွှန်း, int ဘိုက်တန်ဖိုး);
    public static native int ဖိုင်အညွှန်းပိတ်(int ဖိုင်အညွှန်း);
    public static native int ဖိုင်သိုလှောင်အတည်ပြု(int ဖိုင်အညွှန်း);
    public static native int ဖိုင်ဖတ်(int[] အမည်, int[] ဒေတာ);
    public static native int အက္ခရာတန်ဖိုးရေး(int အက္ခရာ);
    public static native int ဖိုင်ရေး(int[] အမည်, int[] ဒေတာ, int အလျား);
    public static native int ရေး(String အကြောင်းအရာတန်ဖိုး);
    public static native int ပေးအချက်များအရေအတွက်();
    public static native String အချက်များ(int နံပါတ်);
    public static native int လုပ်ဆောင်မှုခွင့်ပြုချက်();
    public static native int ကွန်ရက်ဖွင့်(int ဒေသတွင်းဆက်သွယ်ပေါက်);
    public static native int ဒေတာပို့(int ကိုင်တွယ်ရာတန်ဖိုး, int လိပ်စာ, int ဦးတည်ရာဆက်သွယ်ပေါက်, int[] ဒေတာ, int အလျား);
    public static native int ဒေတာလက်ခံရယူ(int ကိုင်တွယ်ရာတန်ဖိုး, int[] ဒေတာ, int အများဆုံးမီလီစက္ကန့်);
    public static native int ကွန်ရက်ပိတ်(int ကိုင်တွယ်ရာတန်ဖိုး);
    public static native int မိမိပိုင်လိပ်စာ();
    public static native int ပို့ပြီးလိပ်စာ(int ကိုင်တွယ်ရာတန်ဖိုး);
    public static native int ပို့ပြီးဆက်သွယ်ပေါက်(int ကိုင်တွယ်ရာတန်ဖိုး);
}
