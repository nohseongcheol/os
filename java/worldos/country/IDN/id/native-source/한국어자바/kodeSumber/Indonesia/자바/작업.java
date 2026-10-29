// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread jalankan(String Nama_2, Runnable Aksi) {
        Thread alur_VALUE = new Thread(Aksi, Nama_2);
        alur_VALUE.start();
        return alur_VALUE;
    }
    public static void 기다리기(Thread alur_VALUE) throws InterruptedException { alur_VALUE.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int alur_COUNT) { return Executors.newFixedThreadPool(alur_COUNT); }
}
