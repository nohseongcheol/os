// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ቖፃሪ_ዋጋ {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ዕማም_ስጉምቲ implements Runnable {
    ቖፃሪ_ዋጋ ቖፃሪ_መወከሲ; ዕማም_ስጉምቲ(ቖፃሪ_ዋጋ ቖፃሪ_መወከሲ) { this.ቖፃሪ_መወከሲ = ቖፃሪ_መወከሲ; }
    public void run() { for (int i = 0; i < 20; i++) ቖፃሪ_መወከሲ.더하기(); }
}
class ፈትሊ_ዋጋ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ቖፃሪ_ዋጋ ቖፃሪ_መወከሲ = new ቖፃሪ_ዋጋ(); Thread 하나 = new Thread(new ዕማም_ስጉምቲ(ቖፃሪ_መወከሲ)); Thread 둘 = new Thread(new ዕማም_ስጉምቲ(ቖፃሪ_መወከሲ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ቖፃሪ_መወከሲ.수); System.out.println(하나.isAlive());
        ፈትሊ_ዋጋ 셋 = new ፈትሊ_ዋጋ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("ፈትሊ_ዋጋ 완료");
    }
}
