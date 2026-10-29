// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class счетчик_ЗНАЧЕН {
    int 수;
    synchronized void 더하기() { int лицевая_камера_ЗНАЧЕН = 수; Thread.yield(); 수 = лицевая_камера_ЗНАЧЕН + 1; }
}
class дело_задача implements Runnable {
    счетчик_ЗНАЧЕН счетчик_ссылка; дело_задача(счетчик_ЗНАЧЕН счетчик_ссылка) { this.счетчик_ссылка = счетчик_ссылка; }
    public void run() { for (int i = 0; i < 20; i++) счетчик_ссылка.더하기(); }
}
class поток_ЗНАЧЕН_5b72a632 extends Thread { public void run() { synchronized (가닥시험.блокировка_ЗНАЧЕН) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object блокировка_ЗНАЧЕН = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        счетчик_ЗНАЧЕН счетчик_ссылка = new счетчик_ЗНАЧЕН(); Thread 하나 = new Thread(new дело_задача(счетчик_ссылка)); Thread 둘 = new Thread(new дело_задача(счетчик_ссылка));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(счетчик_ссылка.수); System.out.println(하나.isAlive());
        поток_ЗНАЧЕН_5b72a632 셋 = new поток_ЗНАЧЕН_5b72a632(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 отклонить_ЗНАЧЕН"); }
        System.out.println("поток_ЗНАЧЕН_5b72a632 완료");
    }
}
