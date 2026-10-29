// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Uruchom_2(String Nazwa, Runnable Akcja) {
        Thread wątek_WARTOŚĆ = new Thread(Akcja, Nazwa);
        wątek_WARTOŚĆ.start();
        return wątek_WARTOŚĆ;
    }
    public static void 기다리기(Thread wątek_WARTOŚĆ) throws InterruptedException { wątek_WARTOŚĆ.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_WARTOŚĆ(int liczba_wątków) { return Executors.newFixedThreadPool(liczba_wątków); }
}
