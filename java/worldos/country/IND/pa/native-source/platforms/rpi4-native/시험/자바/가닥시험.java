// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ਕਾਉਂਟਰ_ਕੀਮਤ {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ਕਾਰਜ_ਕਿਰਿਆ implements Runnable {
    ਕਾਉਂਟਰ_ਕੀਮਤ ਕਾਉਂਟਰ_ਸੰਦਰਭ; ਕਾਰਜ_ਕਿਰਿਆ(ਕਾਉਂਟਰ_ਕੀਮਤ ਕਾਉਂਟਰ_ਸੰਦਰਭ) { this.ਕਾਉਂਟਰ_ਸੰਦਰਭ = ਕਾਉਂਟਰ_ਸੰਦਰਭ; }
    public void run() { for (int i = 0; i < 20; i++) ਕਾਉਂਟਰ_ਸੰਦਰਭ.더하기(); }
}
class ਥ੍ਰੈਡ_ਕੀਮਤ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ਕਾਉਂਟਰ_ਕੀਮਤ ਕਾਉਂਟਰ_ਸੰਦਰਭ = new ਕਾਉਂਟਰ_ਕੀਮਤ(); Thread 하나 = new Thread(new ਕਾਰਜ_ਕਿਰਿਆ(ਕਾਉਂਟਰ_ਸੰਦਰਭ)); Thread 둘 = new Thread(new ਕਾਰਜ_ਕਿਰਿਆ(ਕਾਉਂਟਰ_ਸੰਦਰਭ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ਕਾਉਂਟਰ_ਸੰਦਰਭ.수); System.out.println(하나.isAlive());
        ਥ੍ਰੈਡ_ਕੀਮਤ 셋 = new ਥ੍ਰੈਡ_ਕੀਮਤ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("ਥ੍ਰੈਡ_ਕੀਮਤ 완료");
    }
}
