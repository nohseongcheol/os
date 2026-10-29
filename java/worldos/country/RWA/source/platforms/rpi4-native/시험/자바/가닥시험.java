// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class mubazi_agaciro {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class umukoro_igikorwa implements Runnable {
    mubazi_agaciro mubazi_Indanga; umukoro_igikorwa(mubazi_agaciro mubazi_Indanga) { this.mubazi_Indanga = mubazi_Indanga; }
    public void run() { for (int i = 0; i < 20; i++) mubazi_Indanga.더하기(); }
}
class mugenaporogaramu_agaciro extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        mubazi_agaciro mubazi_Indanga = new mubazi_agaciro(); Thread 하나 = new Thread(new umukoro_igikorwa(mubazi_Indanga)); Thread 둘 = new Thread(new umukoro_igikorwa(mubazi_Indanga));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(mubazi_Indanga.수); System.out.println(하나.isAlive());
        mugenaporogaramu_agaciro 셋 = new mugenaporogaramu_agaciro(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("mugenaporogaramu_agaciro 완료");
    }
}
