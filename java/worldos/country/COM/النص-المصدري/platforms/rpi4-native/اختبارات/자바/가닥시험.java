// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class عدّاد_قيمة {
    int رقم;
    synchronized void 더하기() { int الكاميرا_الأمامية_قيمة = رقم; Thread.yield(); رقم = الكاميرا_الأمامية_قيمة + 1; }
}
class مهمة_إجراء implements Runnable {
    عدّاد_قيمة عدّاد_مرجع; مهمة_إجراء(عدّاد_قيمة عدّاد_مرجع) { this.عدّاد_مرجع = عدّاد_مرجع; }
    public void run() { for (int i = 0; i < 20; i++) عدّاد_مرجع.더하기(); }
}
class محادثة_قيمة extends Thread { public void run() { synchronized (가닥시험.قفل_قيمة) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object قفل_قيمة = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        عدّاد_قيمة عدّاد_مرجع = new عدّاد_قيمة(); Thread 하나 = new Thread(new مهمة_إجراء(عدّاد_مرجع)); Thread 둘 = new Thread(new مهمة_إجراء(عدّاد_مرجع));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(عدّاد_مرجع.رقم); System.out.println(하나.isAlive());
        محادثة_قيمة 셋 = new محادثة_قيمة(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 يرفض_قيمة"); }
        System.out.println("محادثة_قيمة 완료");
    }
}
