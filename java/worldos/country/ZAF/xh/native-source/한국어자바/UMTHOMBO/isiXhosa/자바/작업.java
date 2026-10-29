// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Phumeza(String Igama, Runnable Intshukumo) {
        Thread ithredi_ixabiso = new Thread(Intshukumo, Igama);
        ithredi_ixabiso.start();
        return ithredi_ixabiso;
    }
    public static void 기다리기(Thread ithredi_ixabiso) throws InterruptedException { ithredi_ixabiso.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int 가닥수) { return Executors.newFixedThreadPool(가닥수); }
}
