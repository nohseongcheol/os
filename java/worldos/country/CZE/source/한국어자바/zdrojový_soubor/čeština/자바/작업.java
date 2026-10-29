// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Spustit_2(String Název, Runnable Akce) {
        Thread vlákno_HODNOTA = new Thread(Akce, Název);
        vlákno_HODNOTA.start();
        return vlákno_HODNOTA;
    }
    public static void 기다리기(Thread vlákno_HODNOTA) throws InterruptedException { vlákno_HODNOTA.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_HODNOTA(int počet_vláken) { return Executors.newFixedThreadPool(počet_vláken); }
}
