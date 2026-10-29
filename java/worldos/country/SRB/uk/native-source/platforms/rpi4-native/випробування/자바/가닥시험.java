// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class лічильник_значення {
    int 수;
    synchronized void 더하기() { int фронтальна_камера_значення = 수; Thread.yield(); 수 = фронтальна_камера_значення + 1; }
}
class справа_Дія implements Runnable {
    лічильник_значення лічильник_довідка; справа_Дія(лічильник_значення лічильник_довідка) { this.лічильник_довідка = лічильник_довідка; }
    public void run() { for (int i = 0; i < 20; i++) лічильник_довідка.더하기(); }
}
class потік_значення_5b72a632 extends Thread { public void run() { synchronized (가닥시험.блокувати_значення) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object блокувати_значення = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        лічильник_значення лічильник_довідка = new лічильник_значення(); Thread 하나 = new Thread(new справа_Дія(лічильник_довідка)); Thread 둘 = new Thread(new справа_Дія(лічильник_довідка));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(лічильник_довідка.수); System.out.println(하나.isAlive());
        потік_значення_5b72a632 셋 = new потік_значення_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 відхилити_значення"); }
        System.out.println("потік_значення_5b72a632 완료");
    }
}
