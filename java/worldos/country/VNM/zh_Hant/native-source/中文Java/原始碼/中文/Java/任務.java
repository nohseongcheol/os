// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 任務 {
    private 任務() {}
    public static Thread 運行(String 名稱, Runnable 動作) {
        Thread 執行緒值 = new Thread(動作, 名稱);
        執行緒值.start();
        return 執行緒值;
    }
    public static void 等待(Thread 執行緒值) throws InterruptedException { 執行緒值.join(); }
    public static void 剩餘部分短暫地(long 毫秒) throws InterruptedException { Thread.sleep(毫秒); }
    /** 呼叫者必須透過 shutdown() 釋放資源。 */
    public static ExecutorService 工作臺值(int 執行緒個數) { return Executors.newFixedThreadPool(執行緒個數); }
}
