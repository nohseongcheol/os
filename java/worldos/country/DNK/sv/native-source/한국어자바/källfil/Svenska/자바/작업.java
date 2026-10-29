// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Kör(String Namn, Runnable Åtgärd) {
        Thread tråd_värde = new Thread(Åtgärd, Namn);
        tråd_värde.start();
        return tråd_värde;
    }
    public static void 기다리기(Thread tråd_värde) throws InterruptedException { tråd_värde.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_värde(int antal_trådar) { return Executors.newFixedThreadPool(antal_trådar); }
}
