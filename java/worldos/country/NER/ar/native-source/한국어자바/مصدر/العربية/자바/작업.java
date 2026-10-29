// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread تشغيل(String اسم, Runnable إجراء) {
        Thread محادثة_قيمة = new Thread(إجراء, اسم);
        محادثة_قيمة.start();
        return محادثة_قيمة;
    }
    public static void 기다리기(Thread محادثة_قيمة) throws InterruptedException { محادثة_قيمة.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int عدد_العمليات_الجزئية) { return Executors.newFixedThreadPool(عدد_العمليات_الجزئية); }
}
