// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class бројач_VALUE {
    int 수;
    synchronized void 더하기() { int предна_VALUE = 수; Thread.yield(); 수 = предна_VALUE + 1; }
}
class задача_Дејство implements Runnable {
    бројач_VALUE бројач_Референци; задача_Дејство(бројач_VALUE бројач_Референци) { this.бројач_Референци = бројач_Референци; }
    public void run() { for (int i = 0; i < 20; i++) бројач_Референци.더하기(); }
}
class нишка_VALUE extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        бројач_VALUE бројач_Референци = new бројач_VALUE(); Thread 하나 = new Thread(new задача_Дејство(бројач_Референци)); Thread 둘 = new Thread(new задача_Дејство(бројач_Референци));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(бројач_Референци.수); System.out.println(하나.isAlive());
        нишка_VALUE 셋 = new нишка_VALUE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 одбива_VALUE"); }
        System.out.println("нишка_VALUE 완료");
    }
}
