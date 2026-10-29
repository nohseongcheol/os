// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
/** ကိုယ်ပိုင် JVM အလှည့်ခွဲဝေသူက စီမံသော လုပ်ဆောင်မှုစီးကြောင်း။ စံ Thread ကို ပတ်ထားခြင်း မဟုတ်ပါ။ */
public final class အလုပ်သမား {
    public အလုပ်သမား(လုပ်ဆောင်ရန်အလုပ် အလုပ်လုပ်ဆောင်ချက်) {
        throw new အခြေအနေခြွင်းချက်("ကိုယ်ပိုင် JVM တွင် မြန်မာ API အလုပ်ကြိုးဖန်တီးမှု ပံ့ပိုးရမည်။");
    }
    public native void အလုပ်စတင်() throws အလုပ်ကြိုးအခြေအနေခြွင်းချက်;
    public native void စောင့်() throws စောင့်ဆိုင်းပြတ်ခြွင်းချက်;
    public native boolean လည်ပတ်ဆဲလား();
    public static native void အလုပ်အလှည့်ပေး();
}
