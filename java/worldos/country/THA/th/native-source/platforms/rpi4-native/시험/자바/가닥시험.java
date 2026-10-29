// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ตัวนับ_ค่า {
    int หมายเลข;
    synchronized void 더하기() { int กล้องหน้า_ค่า = หมายเลข; Thread.yield(); หมายเลข = กล้องหน้า_ค่า + 1; }
}
class งาน_แอคชัน implements Runnable {
    ตัวนับ_ค่า ตัวนับ_อ้างอิง; งาน_แอคชัน(ตัวนับ_ค่า ตัวนับ_อ้างอิง) { this.ตัวนับ_อ้างอิง = ตัวนับ_อ้างอิง; }
    public void run() { for (int i = 0; i < 20; i++) ตัวนับ_อ้างอิง.더하기(); }
}
class เธรด_ค่า extends Thread { public void run() { synchronized (가닥시험.ล็อก_ค่า) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object ล็อก_ค่า = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ตัวนับ_ค่า ตัวนับ_อ้างอิง = new ตัวนับ_ค่า(); Thread 하나 = new Thread(new งาน_แอคชัน(ตัวนับ_อ้างอิง)); Thread 둘 = new Thread(new งาน_แอคชัน(ตัวนับ_อ้างอิง));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ตัวนับ_อ้างอิง.หมายเลข); System.out.println(하나.isAlive());
        เธรด_ค่า 셋 = new เธรด_ค่า(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 ปฏิเสธ_ค่า"); }
        System.out.println("เธรด_ค่า 완료");
    }
}
