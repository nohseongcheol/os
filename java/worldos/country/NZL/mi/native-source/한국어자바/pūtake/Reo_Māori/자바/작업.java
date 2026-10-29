// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread whakahaere(String Ingoa, Runnable hohenga) {
        Thread miro_uara = new Thread(hohenga, Ingoa);
        miro_uara.start();
        return miro_uara;
    }
    public static void 기다리기(Thread miro_uara) throws InterruptedException { miro_uara.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int miro_COUNT) { return Executors.newFixedThreadPool(miro_COUNT); }
}
