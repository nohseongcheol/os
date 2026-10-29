// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class санагыч_VALUE {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class мәсьәлә_гамәл implements Runnable {
    санагыч_VALUE санагыч_Белешмәлекләр; мәсьәлә_гамәл(санагыч_VALUE санагыч_Белешмәлекләр) { this.санагыч_Белешмәлекләр = санагыч_Белешмәлекләр; }
    public void run() { for (int i = 0; i < 20; i++) санагыч_Белешмәлекләр.더하기(); }
}
class агым_VALUE_5b72a632 extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        санагыч_VALUE санагыч_Белешмәлекләр = new санагыч_VALUE(); Thread 하나 = new Thread(new мәсьәлә_гамәл(санагыч_Белешмәлекләр)); Thread 둘 = new Thread(new мәсьәлә_гамәл(санагыч_Белешмәлекләр));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(санагыч_Белешмәлекләр.수); System.out.println(하나.isAlive());
        агым_VALUE_5b72a632 셋 = new агым_VALUE_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("агым_VALUE_5b72a632 완료");
    }
}
