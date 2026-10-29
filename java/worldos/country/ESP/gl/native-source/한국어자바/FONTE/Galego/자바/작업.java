// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread Executar_2(String Nome, Runnable Acción) {
        Thread tema_VALOR = new Thread(Acción, Nome);
        tema_VALOR.start();
        return tema_VALOR;
    }
    public static void 기다리기(Thread tema_VALOR) throws InterruptedException { tema_VALOR.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService 작업대(int tema_CONTAR) { return Executors.newFixedThreadPool(tema_CONTAR); }
}
