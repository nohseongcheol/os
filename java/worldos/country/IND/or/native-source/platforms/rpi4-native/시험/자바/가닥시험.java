// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ଗଣନାକାରୀ_ମୂଲ୍ୟ {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class ଟାସ୍କ_କ୍ରିୟା implements Runnable {
    ଗଣନାକାରୀ_ମୂଲ୍ୟ ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ; ଟାସ୍କ_କ୍ରିୟା(ଗଣନାକାରୀ_ମୂଲ୍ୟ ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ) { this.ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ = ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ; }
    public void run() { for (int i = 0; i < 20; i++) ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ.더하기(); }
}
class ଧାରା_ମୂଲ୍ୟ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ଗଣନାକାରୀ_ମୂଲ୍ୟ ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ = new ଗଣନାକାରୀ_ମୂଲ୍ୟ(); Thread 하나 = new Thread(new ଟାସ୍କ_କ୍ରିୟା(ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ)); Thread 둘 = new Thread(new ଟାସ୍କ_କ୍ରିୟା(ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ଗଣନାକାରୀ_ପ୍ରସଙ୍ଗ.수); System.out.println(하나.isAlive());
        ଧାରା_ମୂଲ୍ୟ 셋 = new ଧାରା_ମୂଲ୍ୟ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 ପ୍ରତ୍ୟାକ୍ଷାନ_ମୂଲ୍ୟ"); }
        System.out.println("ଧାରା_ମୂଲ୍ୟ 완료");
    }
}
