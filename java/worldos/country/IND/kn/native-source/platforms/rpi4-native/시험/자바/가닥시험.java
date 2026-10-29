// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ಕೌಂಟರ್_ಮೌಲ್ಯ {
    int 수;
    synchronized void 더하기() { int ಮುಂದೆ_ಮೌಲ್ಯ = 수; Thread.yield(); 수 = ಮುಂದೆ_ಮೌಲ್ಯ + 1; }
}
class ಕಾರ್ಯ_ಕ್ರಿಯೆ implements Runnable {
    ಕೌಂಟರ್_ಮೌಲ್ಯ ಕೌಂಟರ್_ಉಲ್ಲೇಖ; ಕಾರ್ಯ_ಕ್ರಿಯೆ(ಕೌಂಟರ್_ಮೌಲ್ಯ ಕೌಂಟರ್_ಉಲ್ಲೇಖ) { this.ಕೌಂಟರ್_ಉಲ್ಲೇಖ = ಕೌಂಟರ್_ಉಲ್ಲೇಖ; }
    public void run() { for (int i = 0; i < 20; i++) ಕೌಂಟರ್_ಉಲ್ಲೇಖ.더하기(); }
}
class ಎಳೆ_ಮೌಲ್ಯ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ಕೌಂಟರ್_ಮೌಲ್ಯ ಕೌಂಟರ್_ಉಲ್ಲೇಖ = new ಕೌಂಟರ್_ಮೌಲ್ಯ(); Thread 하나 = new Thread(new ಕಾರ್ಯ_ಕ್ರಿಯೆ(ಕೌಂಟರ್_ಉಲ್ಲೇಖ)); Thread 둘 = new Thread(new ಕಾರ್ಯ_ಕ್ರಿಯೆ(ಕೌಂಟರ್_ಉಲ್ಲೇಖ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ಕೌಂಟರ್_ಉಲ್ಲೇಖ.수); System.out.println(하나.isAlive());
        ಎಳೆ_ಮೌಲ್ಯ 셋 = new ಎಳೆ_ಮೌಲ್ಯ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 ನಿರಾಕರಿಸು_ಮೌಲ್ಯ"); }
        System.out.println("ಎಳೆ_ಮೌಲ್ಯ 완료");
    }
}
