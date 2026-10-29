// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ရေတွက်သူတန်ဖိုး {
    int ကိန်းတန်ဖိုး;
    synchronized void တန်ဖိုးများထည့်() { int ရှေ့တန်ဖိုး = ကိန်းတန်ဖိုး; Thread.yield(); ကိန်းတန်ဖိုး = ရှေ့တန်ဖိုး + 1; }
}
class အလုပ်လုပ်ဆောင်ချက် implements Runnable {
    ရေတွက်သူတန်ဖိုး ရေတွက်သူကိုးကားချက်; အလုပ်လုပ်ဆောင်ချက်(ရေတွက်သူတန်ဖိုး ရေတွက်သူကိုးကားချက်) { this.ရေတွက်သူကိုးကားချက် = ရေတွက်သူကိုးကားချက်; }
    public void run() { for (int i = 0; i < 20; i++) ရေတွက်သူကိုးကားချက်.တန်ဖိုးများထည့်(); }
}
class အလုပ်ကြိုးတန်ဖိုး extends Thread { public void run() { synchronized (အလုပ်ကြိုးများစမ်းသပ်.သော့ခတ်တန်ဖိုး) { အလုပ်ကြိုးများစမ်းသပ်.ဖြစ်သောအပြည့်အစုံ = 1; } } }
public class အလုပ်ကြိုးများစမ်းသပ် {
    static Object သော့ခတ်တန်ဖိုး = new Object(); static int ဖြစ်သောအပြည့်အစုံ;
    public static void main(String[] a) throws Exception {
        ရေတွက်သူတန်ဖိုး ရေတွက်သူကိုးကားချက် = new ရေတွက်သူတန်ဖိုး(); Thread တစ်တန်ဖိုး = new Thread(new အလုပ်လုပ်ဆောင်ချက်(ရေတွက်သူကိုးကားချက်)); Thread နှစ်တန်ဖိုး = new Thread(new အလုပ်လုပ်ဆောင်ချက်(ရေတွက်သူကိုးကားချက်));
        တစ်တန်ဖိုး.start(); နှစ်တန်ဖိုး.start(); တစ်တန်ဖိုး.join(); နှစ်တန်ဖိုး.join(); System.out.println(ရေတွက်သူကိုးကားချက်.ကိန်းတန်ဖိုး); System.out.println(တစ်တန်ဖိုး.isAlive());
        အလုပ်ကြိုးတန်ဖိုး တတိယအချက် = new အလုပ်ကြိုးတန်ဖိုး(); တတိယအချက်.start(); တတိယအချက်.join(); System.out.println(ဖြစ်သောအပြည့်အစုံ);
        try { တစ်တန်ဖိုး.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 တန်ဖိုးငြင်းပယ်"); }
        System.out.println("အလုပ်ကြိုးတန်ဖိုး ဖြစ်သောအပြည့်အစုံ");
    }
}
