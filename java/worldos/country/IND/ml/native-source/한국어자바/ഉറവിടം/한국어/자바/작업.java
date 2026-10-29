// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread നടപ്പിലാക്കുക(String പേരു്, Runnable നടപടി) {
        Thread ത്രെഡ്_മൂല്യം = new Thread(നടപടി, പേരു്);
        ത്രെഡ്_മൂല്യം.start();
        return ത്രെഡ്_മൂല്യം;
    }
    public static void 기다리기(Thread ത്രെഡ്_മൂല്യം) throws InterruptedException { ത്രെഡ്_മൂല്യം.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int 가닥수) { return Executors.newFixedThreadPool(가닥수); }
}
