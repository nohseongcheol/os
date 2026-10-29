// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread starten(String Naam, Runnable Actie) {
        Thread thread_WAARDE = new Thread(Actie, Naam);
        thread_WAARDE.start();
        return thread_WAARDE;
    }
    public static void 기다리기(Thread thread_WAARDE) throws InterruptedException { thread_WAARDE.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_WAARDE(int aantal_threads) { return Executors.newFixedThreadPool(aantal_threads); }
}
