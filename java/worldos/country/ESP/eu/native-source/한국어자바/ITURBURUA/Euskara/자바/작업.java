// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Exekutatu_2(String Izena, Runnable Ekintza) {
        Thread hari_balio = new Thread(Ekintza, Izena);
        hari_balio.start();
        return hari_balio;
    }
    public static void 기다리기(Thread hari_balio) throws InterruptedException { hari_balio.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int hari_ZENBATU) { return Executors.newFixedThreadPool(hari_ZENBATU); }
}
