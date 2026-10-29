// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread चलोवप(String नांव, Runnable कृती) {
        Thread थ्रॅड_मोल = new Thread(कृती, नांव);
        थ्रॅड_मोल.start();
        return थ्रॅड_मोल;
    }
    public static void 기다리기(Thread थ्रॅड_मोल) throws InterruptedException { थ्रॅड_मोल.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int थ्रॅड_COUNT) { return Executors.newFixedThreadPool(थ्रॅड_COUNT); }
}
