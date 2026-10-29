// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class performTask {
    private performTask() {}
    public static Thread run(String name, Runnable action) {
        Thread threadValue = new Thread(action, name);
        threadValue.start();
        return threadValue;
    }
    public static void await(Thread threadValue) throws InterruptedException { threadValue.join(); }
    public static void restBriefly(long milliseconds) throws InterruptedException { Thread.sleep(milliseconds); }
    /** The caller must release resources by calling shutdown(). */
    public static ExecutorService workbenchValue(int threadCount) { return Executors.newFixedThreadPool(threadCount); }
}
