// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread הפעלה(String שם, Runnable פעולה) {
        Thread שרשור_ערך = new Thread(פעולה, שם);
        שרשור_ערך.start();
        return שרשור_ערך;
    }
    public static void 기다리기(Thread שרשור_ערך) throws InterruptedException { שרשור_ערך.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int ספירת_הליכי_משנה_Thread) { return Executors.newFixedThreadPool(ספירת_הליכי_משנה_Thread); }
}
