// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ឧបករណ៍វាស់_តំលៃ {
    int 수;
    synchronized void 더하기() { int ខាងមុខ_តំលៃ = 수; Thread.yield(); 수 = ខាងមុខ_តំលៃ + 1; }
}
class ធូឌូ_ការណែនាំ implements Runnable {
    ឧបករណ៍វាស់_តំលៃ ឧបករណ៍វាស់_យោង; ធូឌូ_ការណែនាំ(ឧបករណ៍វាស់_តំលៃ ឧបករណ៍វាស់_យោង) { this.ឧបករណ៍វាស់_យោង = ឧបករណ៍វាស់_យោង; }
    public void run() { for (int i = 0; i < 20; i++) ឧបករណ៍វាស់_យោង.더하기(); }
}
class ស្រេត_តំលៃ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ឧបករណ៍វាស់_តំលៃ ឧបករណ៍វាស់_យោង = new ឧបករណ៍វាស់_តំលៃ(); Thread 하나 = new Thread(new ធូឌូ_ការណែនាំ(ឧបករណ៍វាស់_យោង)); Thread 둘 = new Thread(new ធូឌូ_ការណែនាំ(ឧបករណ៍វាស់_យោង));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ឧបករណ៍វាស់_យោង.수); System.out.println(하나.isAlive());
        ស្រេត_តំលៃ 셋 = new ស្រេត_តំលៃ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 បដិសេធ_តំលៃ"); }
        System.out.println("ស្រេត_តំលៃ 완료");
    }
}
