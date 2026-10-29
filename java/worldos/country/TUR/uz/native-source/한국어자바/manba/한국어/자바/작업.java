// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Bajarish(String Nomi, Runnable Amal) {
        Thread oqim_VALUE_5b72a632 = new Thread(Amal, Nomi);
        oqim_VALUE_5b72a632.start();
        return oqim_VALUE_5b72a632;
    }
    public static void 기다리기(Thread oqim_VALUE_5b72a632) throws InterruptedException { oqim_VALUE_5b72a632.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int oqim_COUNT) { return Executors.newFixedThreadPool(oqim_COUNT); }
}
