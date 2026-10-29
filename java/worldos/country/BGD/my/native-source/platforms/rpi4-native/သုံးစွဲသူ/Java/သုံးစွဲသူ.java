// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 Java ကိရိယာများအတွက် သီးသန့် SVC ဆက်သွယ်မှု။ မူလ x86 ကိရိယာကုဒ်နှင့်အတူ တည်ဆောက်သည်။ */
public final class သုံးစွဲသူ {
    public static native int ဖိုင်အညွှန်းဖွင့်(int[] အမည်, int သတ်မှတ်ချက်);
    public static native int ဖိုင်ဘိုက်တစ်ခုဖတ်(int အညွှန်း);
    public static native int ဖိုင်ဘိုက်တစ်ခုရေး(int အညွှန်း, int တန်ဖိုး);
    public static native int ဖိုင်အညွှန်းပိတ်(int အညွှန်း);
    public static native int ဖိုင်ဖတ်(int[] အမည်, int[] ဒေတာ);
    public static native int ဖိုင်ရေး(int[] အမည်, int[] ဒေတာ, int အလျား);
    public static native int ရေး(String စာသား);
    public static native int အက္ခရာတန်ဖိုးရေး(int တန်ဖိုး);
    public static native int ပေးအချက်များအရေအတွက်();
    public static native String အချက်များ(int နံပါတ်);
    public static native int ကိရိယာတစ်ခုကိန်း();
    public static native int မျက်နှာပြင်ချိတ်ဆက်မှု(int လှုပ်ရှားမှု, int နံပါတ်, int ပထမတွက်ချက်ခံ, int ဒုတိယတွက်ချက်ခံ, int တတိယအော်ပရန်း, int စတုတ္ထအော်ပရန်း);
    public static native int မျက်နှာပြင်စာသား(int နံပါတ်, int[] စာသား, int အလျား);
    public static native int မျက်နှာပြင်အနံ();
    public static native int မျက်နှာပြင်အမြင့်();
    public static native int စီးကြောင်းထိန်းချုပ်(int လှုပ်ရှားမှု, int အညွှန်း, int တန်ဖိုး);
    public static native int စီးကြောင်းချိတ်ဆက်(int အညွှန်း, int လိပ်စာ, int ဆက်သွယ်ပေါက်တန်ဖိုး);
    public static native int ကွန်ရက်ဖွင့်(int ဆက်သွယ်ပေါက်တန်ဖိုး);
    public static native int ကွန်ရက်ပို့(int အညွှန်း, int လိပ်စာ, int ဆက်သွယ်ပေါက်တန်ဖိုး, int[] ဒေတာ, int အလျား);
    public static native int ကွန်ရက်လက်ခံရယူ(int အညွှန်း, int[] ဒေတာ, int အလျား);
    public static native int ကွန်ရက်ဆက်သွယ်ပေါက်(int အညွှန်း);
    public static native int မီလီစက္ကန့်();
    public static native int ပုံစောင့်();
    public static native int စတုဂံ(int အလျားတည်နေရာ, int ဒေါင်လိုက်တည်နေရာ, int အကျယ်အဝန်း, int အမြင့်တန်ဖိုး, int အရောင်တန်ဖိုး);
}
