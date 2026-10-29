// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;

/** စံ Java အမှားများကို မြန်မာ API နယ်နိမိတ်တွင် ပြောင်းလဲသည်။ Java catch ၏ အဓိပ္ပာယ်ကို မပြောင်းပါ။ */
final class ခြွင်းချက်ပြောင်းလဲ {
    private ခြွင်းချက်ပြောင်းလဲ() {}
    public static အဝင်အထွက်ခြွင်းချက် အဝင်အထွက်(java.io.IOException အမှား) {
        if (အမှား instanceof အဝင်အထွက်ခြွင်းချက်) return (အဝင်အထွက်ခြွင်းချက်)အမှား;
        if (အမှား instanceof java.net.SocketTimeoutException) return new စောင့်အချိန်လွန်ခြွင်းချက်("ဆက်သွယ်မှုစောင့်ချိန် ကျော်လွန်သွားသည်။");
        if (အမှား instanceof java.net.UnknownHostException) return new လိပ်စာရှာကြည့်ခြွင်းချက်("လိပ်စာကို မရှာနိုင်ပါ။ ယခု ဂဏန်း IPv4 လိပ်စာကို သုံးပါ။");
        if (အမှား instanceof java.io.FileNotFoundException) return new ဖိုင်မရှိခြွင်းချက်("ဖိုင်ကို မဖွင့်နိုင်ပါ။");
        if (အမှား instanceof java.net.SocketException) return new ဆက်သွယ်မှုခြွင်းချက်("ဆက်သွယ်ချိတ်ဆက်မှု မအောင်မြင်: " + အမှား.getMessage());
        return new အဝင်အထွက်ခြွင်းချက်("အဝင်အထွက်လုပ်ဆောင်မှု မအောင်မြင်: " + အမှား.getMessage());
    }
    public static RuntimeException စက်မောင်း(RuntimeException အမှား) {
        if (အမှား instanceof java.lang.NumberFormatException) return new ကိန်းပုံစံခြွင်းချက်("ကိန်းဂဏန်းပုံစံနှင့် နယ်နိမိတ်ကို စစ်ဆေးပါ။");
        if (အမှား instanceof java.lang.IllegalArgumentException) return new မမှန်ကန်ပေးအချက်ခြွင်းချက်("လက်ခံအချက်တန်ဖိုးနှင့် နယ်နိမိတ်ကို စစ်ဆေးပါ။");
        if (အမှား instanceof java.lang.ArrayIndexOutOfBoundsException) return new အခင်းအကန့်ခြွင်းချက်("အခင်းအကန့်ကို ကျော်လွန်သွားသည်။");
        if (အမှား instanceof java.lang.StringIndexOutOfBoundsException) return new စာသားအကန့်ခြွင်းချက်("စာသားအကန့်ကို ကျော်လွန်သွားသည်။");
        if (အမှား instanceof java.lang.IndexOutOfBoundsException) return new နယ်နိမိတ်ခြွင်းချက်("ခွင့်ပြုနယ်ပယ်ကို ကျော်လွန်သွားသည်။");
        if (အမှား instanceof java.lang.NullPointerException) return new အလွတ်ကိုးကားခြွင်းချက်("ကိုးကားချက်သည် အလွတ်ဖြစ်သည်။");
        return new လုပ်ဆောင်မှုခြွင်းချက်(အမှား.getMessage());
    }
}
