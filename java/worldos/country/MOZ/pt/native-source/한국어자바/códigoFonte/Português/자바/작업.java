// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.자바;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class 작업 {
    private 작업() {}
    public static Thread iniciar(String Nome, Runnable Acção) {
        Thread thread_VALOR = new Thread(Acção, Nome);
        thread_VALOR.start();
        return thread_VALOR;
    }
    public static void 기다리기(Thread thread_VALOR) throws InterruptedException { thread_VALOR.join(); }
    public static void 쉬기(long 밀리초) throws InterruptedException { Thread.sleep(밀리초); }
    /** 호출자가 shutdown()으로 자원을 반환해야 한다. */
    public static ExecutorService Workbench_VALOR(int contagem_de_threads) { return Executors.newFixedThreadPool(contagem_de_threads); }
}
