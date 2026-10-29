// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread çalıştır(String İsim, Runnable Eylem) {
        Thread yazışma_değer = new Thread(Eylem, İsim);
        yazışma_değer.start();
        return yazışma_değer;
    }
    public static void 기다리기(Thread yazışma_değer) throws InterruptedException { yazışma_değer.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_değer(int yazışma_BAĞ_DEĞ_SAY) { return Executors.newFixedThreadPool(yazışma_BAĞ_DEĞ_SAY); }
}
