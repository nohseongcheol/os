// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာ.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class အလုပ် {
    private အလုပ်() {}
    public static Thread လုပ်ဆောင်(String အမည်, Runnable လှုပ်ရှားမှု) {
        Thread အလုပ်ကြိုးတန်ဖိုး = new Thread(လှုပ်ရှားမှု, အမည်);
        အလုပ်ကြိုးတန်ဖိုး.start();
        return အလုပ်ကြိုးတန်ဖိုး;
    }
    public static void စောင့်(Thread အလုပ်ကြိုးတန်ဖိုး) throws InterruptedException { အလုပ်ကြိုးတန်ဖိုး.join(); }
    public static void ခဏနား(long မီလီစက္ကန့်) throws InterruptedException { Thread.sleep(မီလီစက္ကန့်); }
    /** ခေါ်ဆိုသူသည် shutdown() ဖြင့် အရင်းအမြစ်များကို ပြန်လွှတ်ရမည်။ */
    public static ExecutorService အလုပ်ခုံတန်ဖိုး(int အလုပ်ကြိုးအရေအတွက်) { return Executors.newFixedThreadPool(အလုပ်ကြိုးအရေအတွက်); }
}
