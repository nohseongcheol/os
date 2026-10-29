// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ተቃራኒ_እሴት {
    int 수;
    synchronized void 더하기() { int ፊት_እሴት = 수; Thread.yield(); 수 = ፊት_እሴት + 1; }
}
class ተግባር_ምክር implements Runnable {
    ተቃራኒ_እሴት ተቃራኒ_ማጣቀሻ; ተግባር_ምክር(ተቃራኒ_እሴት ተቃራኒ_ማጣቀሻ) { this.ተቃራኒ_ማጣቀሻ = ተቃራኒ_ማጣቀሻ; }
    public void run() { for (int i = 0; i < 20; i++) ተቃራኒ_ማጣቀሻ.더하기(); }
}
class ክር_እሴት extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ተቃራኒ_እሴት ተቃራኒ_ማጣቀሻ = new ተቃራኒ_እሴት(); Thread 하나 = new Thread(new ተግባር_ምክር(ተቃራኒ_ማጣቀሻ)); Thread 둘 = new Thread(new ተግባር_ምክር(ተቃራኒ_ማጣቀሻ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ተቃራኒ_ማጣቀሻ.수); System.out.println(하나.isAlive());
        ክር_እሴት 셋 = new ክር_እሴት(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 አትቀበል_እሴት"); }
        System.out.println("ክር_እሴት 완료");
    }
}
