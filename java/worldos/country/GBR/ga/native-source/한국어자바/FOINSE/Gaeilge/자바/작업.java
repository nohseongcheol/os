// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Rith_2(String Ainm, Runnable Gníomh) {
        Thread snáithe_VALUE = new Thread(Gníomh, Ainm);
        snáithe_VALUE.start();
        return snáithe_VALUE;
    }
    public static void 기다리기(Thread snáithe_VALUE) throws InterruptedException { snáithe_VALUE.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int snáithe_COUNT) { return Executors.newFixedThreadPool(snáithe_COUNT); }
}
