// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class giáTrịBộĐếm {
    int trịSố;
    synchronized void thêmCácGiáTrị() { int giáTrịPhíaTrước = trịSố; Thread.yield(); trịSố = giáTrịPhíaTrước + 1; }
}
class HànhĐộngTácVụ implements Runnable {
    giáTrịBộĐếm thamChiếuBộĐếm; HànhĐộngTácVụ(giáTrịBộĐếm thamChiếuBộĐếm) { this.thamChiếuBộĐếm = thamChiếuBộĐếm; }
    public void run() { for (int i = 0; i < 20; i++) thamChiếuBộĐếm.thêmCácGiáTrị(); }
}
class giáTrịLuồngChạy extends Thread { public void run() { synchronized (thửCácLuồngChạy.giáTrịKhóa) { thửCácLuồngChạy.làĐầyĐủ = 1; } } }
public class thửCácLuồngChạy {
    static Object giáTrịKhóa = new Object(); static int làĐầyĐủ;
    public static void main(String[] a) throws Exception {
        giáTrịBộĐếm thamChiếuBộĐếm = new giáTrịBộĐếm(); Thread giáTrịMột = new Thread(new HànhĐộngTácVụ(thamChiếuBộĐếm)); Thread giáTrịHai = new Thread(new HànhĐộngTácVụ(thamChiếuBộĐếm));
        giáTrịMột.start(); giáTrịHai.start(); giáTrịMột.join(); giáTrịHai.join(); System.out.println(thamChiếuBộĐếm.trịSố); System.out.println(giáTrịMột.isAlive());
        giáTrịLuồngChạy phầnMụcThứBa = new giáTrịLuồngChạy(); phầnMụcThứBa.start(); phầnMụcThứBa.join(); System.out.println(làĐầyĐủ);
        try { giáTrịMột.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 từChốiGiáTrị"); }
        System.out.println("giáTrịLuồngChạy làĐầyĐủ");
    }
}
