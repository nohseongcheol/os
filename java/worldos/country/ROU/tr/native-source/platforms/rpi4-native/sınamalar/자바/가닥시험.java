// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class sayaç_değer {
    int 수;
    synchronized void 더하기() { int ön_kamera_değer = 수; Thread.yield(); 수 = ön_kamera_değer + 1; }
}
class Görev_Eylem implements Runnable {
    sayaç_değer sayaç_Başvuru; Görev_Eylem(sayaç_değer sayaç_Başvuru) { this.sayaç_Başvuru = sayaç_Başvuru; }
    public void run() { for (int i = 0; i < 20; i++) sayaç_Başvuru.더하기(); }
}
class yazışma_değer extends Thread { public void run() { synchronized (가닥시험.kilit_değer) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object kilit_değer = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        sayaç_değer sayaç_Başvuru = new sayaç_değer(); Thread 하나 = new Thread(new Görev_Eylem(sayaç_Başvuru)); Thread 둘 = new Thread(new Görev_Eylem(sayaç_Başvuru));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(sayaç_Başvuru.수); System.out.println(하나.isAlive());
        yazışma_değer 셋 = new yazışma_değer(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 reddetmek_değer"); }
        System.out.println("yazışma_değer 완료");
    }
}
