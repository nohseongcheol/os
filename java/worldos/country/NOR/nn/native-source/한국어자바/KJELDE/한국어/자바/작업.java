// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Køyr_2(String Namn, Runnable Handling) {
        Thread tråd_VALUE = new Thread(Handling, Namn);
        tråd_VALUE.start();
        return tråd_VALUE;
    }
    public static void 기다리기(Thread tråd_VALUE) throws InterruptedException { tråd_VALUE.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int tråd_COUNT) { return Executors.newFixedThreadPool(tråd_COUNT); }
}
