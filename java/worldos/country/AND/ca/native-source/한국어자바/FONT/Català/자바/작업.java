// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Executa_2(String Nom, Runnable Acció) {
        Thread fil_VALOR = new Thread(Acció, Nom);
        fil_VALOR.start();
        return fil_VALOR;
    }
    public static void 기다리기(Thread fil_VALOR) throws InterruptedException { fil_VALOR.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int fil_COMPT) { return Executors.newFixedThreadPool(fil_COMPT); }
}
