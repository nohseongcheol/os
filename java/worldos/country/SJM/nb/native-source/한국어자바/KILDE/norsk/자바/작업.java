// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Kjør_2(String Navn, Runnable Handling) {
        Thread tråd_VERDI = new Thread(Handling, Navn);
        tråd_VERDI.start();
        return tråd_VERDI;
    }
    public static void 기다리기(Thread tråd_VERDI) throws InterruptedException { tråd_VERDI.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_VERDI(int Trådteller) { return Executors.newFixedThreadPool(Trådteller); }
}
