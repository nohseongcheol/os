// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class հաշվիչ_արժեք {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class խնդիր_գործողություն implements Runnable {
    հաշվիչ_արժեք հաշվիչ_Տեղեկատուներ; խնդիր_գործողություն(հաշվիչ_արժեք հաշվիչ_Տեղեկատուներ) { this.հաշվիչ_Տեղեկատուներ = հաշվիչ_Տեղեկատուներ; }
    public void run() { for (int i = 0; i < 20; i++) հաշվիչ_Տեղեկատուներ.더하기(); }
}
class շղթա_արժեք extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        հաշվիչ_արժեք հաշվիչ_Տեղեկատուներ = new հաշվիչ_արժեք(); Thread 하나 = new Thread(new խնդիր_գործողություն(հաշվիչ_Տեղեկատուներ)); Thread 둘 = new Thread(new խնդիր_գործողություն(հաշվիչ_Տեղեկատուներ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(հաշվիչ_Տեղեկատուներ.수); System.out.println(하나.isAlive());
        շղթա_արժեք 셋 = new շղթա_արժեք(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("շղթա_արժեք 완료");
    }
}
