// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class काउंटर_मान {
    int 수;
    synchronized void 더하기() { int सामने_मान = 수; Thread.yield(); 수 = सामने_मान + 1; }
}
class कार्य_एक्शन implements Runnable {
    काउंटर_मान काउंटर_संदर्भ; कार्य_एक्शन(काउंटर_मान काउंटर_संदर्भ) { this.काउंटर_संदर्भ = काउंटर_संदर्भ; }
    public void run() { for (int i = 0; i < 20; i++) काउंटर_संदर्भ.더하기(); }
}
class थ्रेड_मान extends Thread { public void run() { synchronized (가닥시험.लॉक_मान) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object लॉक_मान = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        काउंटर_मान काउंटर_संदर्भ = new काउंटर_मान(); Thread 하나 = new Thread(new कार्य_एक्शन(काउंटर_संदर्भ)); Thread 둘 = new Thread(new कार्य_एक्शन(काउंटर_संदर्भ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(काउंटर_संदर्भ.수); System.out.println(하나.isAlive());
        थ्रेड_मान 셋 = new थ्रेड_मान(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 अस्वीकृत_करें_मान"); }
        System.out.println("थ्रेड_मान 완료");
    }
}
