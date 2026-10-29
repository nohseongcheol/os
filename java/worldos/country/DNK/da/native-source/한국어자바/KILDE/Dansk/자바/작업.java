// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Kør_2(String Navn, Runnable Handling) {
        Thread tråd_VÆRDI = new Thread(Handling, Navn);
        tråd_VÆRDI.start();
        return tråd_VÆRDI;
    }
    public static void 기다리기(Thread tråd_VÆRDI) throws InterruptedException { tråd_VÆRDI.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_VÆRDI(int Antal_tråde) { return Executors.newFixedThreadPool(Antal_tråde); }
}
