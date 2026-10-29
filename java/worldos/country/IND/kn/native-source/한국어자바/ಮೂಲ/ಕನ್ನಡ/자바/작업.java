// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread ಚಲಾಯಿಸು_2(String ಹೆಸರು, Runnable ಹಕ್ರಿಯೆ) {
        Thread ಎಳೆ_ಮೌಲ್ಯ = new Thread(ಹಕ್ರಿಯೆ, ಹೆಸರು);
        ಎಳೆ_ಮೌಲ್ಯ.start();
        return ಎಳೆ_ಮೌಲ್ಯ;
    }
    public static void 기다리기(Thread ಎಳೆ_ಮೌಲ್ಯ) throws InterruptedException { ಎಳೆ_ಮೌಲ್ಯ.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int 가닥수) { return Executors.newFixedThreadPool(가닥수); }
}
