// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread запустить(String Название, Runnable Действие) {
        Thread поток_ЗНАЧЕН_5b72a632 = new Thread(Действие, Название);
        поток_ЗНАЧЕН_5b72a632.start();
        return поток_ЗНАЧЕН_5b72a632;
    }
    public static void 기다리기(Thread поток_ЗНАЧЕН_5b72a632) throws InterruptedException { поток_ЗНАЧЕН_5b72a632.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_ЗНАЧЕН(int количество_потоков) { return Executors.newFixedThreadPool(количество_потоков); }
}
