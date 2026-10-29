// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class бројач_вриједност {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class задатак_радња implements Runnable {
    бројач_вриједност бројач_Литература; задатак_радња(бројач_вриједност бројач_Литература) { this.бројач_Литература = бројач_Литература; }
    public void run() { for (int i = 0; i < 20; i++) бројач_Литература.더하기(); }
}
class нит_вриједност extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        бројач_вриједност бројач_Литература = new бројач_вриједност(); Thread 하나 = new Thread(new задатак_радња(бројач_Литература)); Thread 둘 = new Thread(new задатак_радња(бројач_Литература));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(бројач_Литература.수); System.out.println(하나.isAlive());
        нит_вриједност 셋 = new нит_вриједност(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 одбацити_вриједност_e3ecc00b"); }
        System.out.println("нит_вриједност 완료");
    }
}
