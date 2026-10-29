// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.ကိုယ်ပိုင်;
/** ကိုယ်ပိုင် အူတိုင်၏ စံအထွက်။ UTF-16 ကိုယ်စားပြုအတွဲများကို UART မှ UTF-8 ဖြင့် ပို့သည်။ */
public final class အထွက် {
    private အထွက်() {}
    public static void ရေး(String စာသား) { System.out.print(စာသား); }
    public static void စာကြောင်းထုတ်(String စာသား) { System.out.println(စာသား); }
    public static void ကိန်းထုတ်(int ကိန်းတန်ဖိုး) { System.out.println(ကိန်းတန်ဖိုး); }
}
