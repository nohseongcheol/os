// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Futtatás(String Név, Runnable Művelet) {
        Thread szál_ÉRTÉK = new Thread(Művelet, Név);
        szál_ÉRTÉK.start();
        return szál_ÉRTÉK;
    }
    public static void 기다리기(Thread szál_ÉRTÉK) throws InterruptedException { szál_ÉRTÉK.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_ÉRTÉK(int szálak_száma) { return Executors.newFixedThreadPool(szálak_száma); }
}
