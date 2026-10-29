// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Εκτέλεση_2(String Όνομα, Runnable Ενέργεια) {
        Thread νήμα_τιμή = new Thread(Ενέργεια, Όνομα);
        νήμα_τιμή.start();
        return νήμα_τιμή;
    }
    public static void 기다리기(Thread νήμα_τιμή) throws InterruptedException { νήμα_τιμή.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int πλήθος_νημάτων) { return Executors.newFixedThreadPool(πλήθος_νημάτων); }
}
