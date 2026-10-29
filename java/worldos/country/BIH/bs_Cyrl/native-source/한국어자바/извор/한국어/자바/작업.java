// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread 시작(String назив, Runnable радња) {
        Thread нит_вриједност = new Thread(радња, назив);
        нит_вриједност.start();
        return нит_вриједност;
    }
    public static void 기다리기(Thread нит_вриједност) throws InterruptedException { нит_вриједност.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int 가닥수) { return Executors.newFixedThreadPool(가닥수); }
}
