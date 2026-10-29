// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class μετρητής_τιμή {
    int 수;
    synchronized void 더하기() { int μπροστινή_τιμή = 수; Thread.yield(); 수 = μπροστινή_τιμή + 1; }
}
class εργασία_έργο implements Runnable {
    μετρητής_τιμή μετρητής_Αναφορά; εργασία_έργο(μετρητής_τιμή μετρητής_Αναφορά) { this.μετρητής_Αναφορά = μετρητής_Αναφορά; }
    public void run() { for (int i = 0; i < 20; i++) μετρητής_Αναφορά.더하기(); }
}
class νήμα_τιμή extends Thread { public void run() { synchronized (가닥시험.κλείδωμα_τιμή) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object κλείδωμα_τιμή = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        μετρητής_τιμή μετρητής_Αναφορά = new μετρητής_τιμή(); Thread 하나 = new Thread(new εργασία_έργο(μετρητής_Αναφορά)); Thread 둘 = new Thread(new εργασία_έργο(μετρητής_Αναφορά));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(μετρητής_Αναφορά.수); System.out.println(하나.isAlive());
        νήμα_τιμή 셋 = new νήμα_τιμή(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 απορρίπτω_τιμή"); }
        System.out.println("νήμα_τιμή 완료");
    }
}
