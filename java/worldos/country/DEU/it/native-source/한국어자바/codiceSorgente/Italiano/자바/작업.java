// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread avvia(String Nome, Runnable Azione) {
        Thread thread_VALORE = new Thread(Azione, Nome);
        thread_VALORE.start();
        return thread_VALORE;
    }
    public static void 기다리기(Thread thread_VALORE) throws InterruptedException { thread_VALORE.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_VALORE(int Conteggio_dei_thread) { return Executors.newFixedThreadPool(Conteggio_dei_thread); }
}
