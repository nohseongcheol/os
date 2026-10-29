// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class TácVụ {
    private TácVụ() {}
    public static Thread chạy(String tên, Runnable hànhĐộng) {
        Thread giáTrịLuồngChạy = new Thread(hànhĐộng, tên);
        giáTrịLuồngChạy.start();
        return giáTrịLuồngChạy;
    }
    public static void đợi(Thread giáTrịLuồngChạy) throws InterruptedException { giáTrịLuồngChạy.join(); }
    public static void ngắnPhầnCòn(long miliGiây) throws InterruptedException { Thread.sleep(miliGiây); }
    /** Bên gọi phải gọi shutdown() để trả lại tài nguyên. */
    public static ExecutorService giáTrịBànLàmViệc(int sốLượngLuồngChạy) { return Executors.newFixedThreadPool(sốLượngLuồngChạy); }
}
