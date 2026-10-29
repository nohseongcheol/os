// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread ચલાવો_2(String નામ, Runnable ક્રિયા) {
        Thread થ્રેડ_મૂલ્ય = new Thread(ક્રિયા, નામ);
        થ્રેડ_મૂલ્ય.start();
        return થ્રેડ_મૂલ્ય;
    }
    public static void 기다리기(Thread થ્રેડ_મૂલ્ય) throws InterruptedException { થ્રેડ_મૂલ્ય.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int 가닥수) { return Executors.newFixedThreadPool(가닥수); }
}
