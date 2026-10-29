// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class கவுண்ட்டர்_மதிப்பு {
    int 수;
    synchronized void 더하기() { int முன்_மதிப்பு = 수; Thread.yield(); 수 = முன்_மதிப்பு + 1; }
}
class பணி_செயல் implements Runnable {
    கவுண்ட்டர்_மதிப்பு கவுண்ட்டர்_மேற்கோள்; பணி_செயல்(கவுண்ட்டர்_மதிப்பு கவுண்ட்டர்_மேற்கோள்) { this.கவுண்ட்டர்_மேற்கோள் = கவுண்ட்டர்_மேற்கோள்; }
    public void run() { for (int i = 0; i < 20; i++) கவுண்ட்டர்_மேற்கோள்.더하기(); }
}
class தொடரிழை_மதிப்பு extends Thread { public void run() { synchronized (가닥시험.பூட்டு_மதிப்பு) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object பூட்டு_மதிப்பு = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        கவுண்ட்டர்_மதிப்பு கவுண்ட்டர்_மேற்கோள் = new கவுண்ட்டர்_மதிப்பு(); Thread 하나 = new Thread(new பணி_செயல்(கவுண்ட்டர்_மேற்கோள்)); Thread 둘 = new Thread(new பணி_செயல்(கவுண்ட்டர்_மேற்கோள்));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(கவுண்ட்டர்_மேற்கோள்.수); System.out.println(하나.isAlive());
        தொடரிழை_மதிப்பு 셋 = new தொடரிழை_மதிப்பு(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 புறக்கணி_மதிப்பு"); }
        System.out.println("தொடரிழை_மதிப்பு 완료");
    }
}
