// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 作業 {
    private 作業() {}
    public static Thread 起動処理(String 名前, Runnable 動作) {
        Thread スレッド値 = new Thread(動作, 名前);
        スレッド値.start();
        return スレッド値;
    }
    public static void 待機(Thread スレッド値) throws InterruptedException { スレッド値.join(); }
    public static void 残部短時間だけ(long ミリ秒) throws InterruptedException { Thread.sleep(ミリ秒); }
    /** 呼出し元は shutdown() で資源を返却する必要がある。 */
    public static ExecutorService 作業台値(int スレッド個数) { return Executors.newFixedThreadPool(スレッド個数); }
}
