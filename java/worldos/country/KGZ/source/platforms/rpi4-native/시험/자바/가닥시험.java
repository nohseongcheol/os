// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class эсептөөч_маани {
    int 수;
    synchronized void 더하기() { int 앞 = 수; Thread.yield(); 수 = 앞 + 1; }
}
class маселе_иш_аракет implements Runnable {
    эсептөөч_маани эсептөөч_Шилтемелер; маселе_иш_аракет(эсептөөч_маани эсептөөч_Шилтемелер) { this.эсептөөч_Шилтемелер = эсептөөч_Шилтемелер; }
    public void run() { for (int i = 0; i < 20; i++) эсептөөч_Шилтемелер.더하기(); }
}
class трэд_маани extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        эсептөөч_маани эсептөөч_Шилтемелер = new эсептөөч_маани(); Thread 하나 = new Thread(new маселе_иш_аракет(эсептөөч_Шилтемелер)); Thread 둘 = new Thread(new маселе_иш_аракет(эсептөөч_Шилтемелер));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(эсептөөч_Шилтемелер.수); System.out.println(하나.isAlive());
        трэд_маани 셋 = new трэд_маани(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 거부"); }
        System.out.println("трэд_маани 완료");
    }
}
