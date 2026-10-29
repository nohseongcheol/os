// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread koristiti(String ime, Runnable radnja) {
        Thread nit_VALUE = new Thread(radnja, ime);
        nit_VALUE.start();
        return nit_VALUE;
    }
    public static void 기다리기(Thread nit_VALUE) throws InterruptedException { nit_VALUE.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int nit_COUNT) { return Executors.newFixedThreadPool(nit_COUNT); }
}
