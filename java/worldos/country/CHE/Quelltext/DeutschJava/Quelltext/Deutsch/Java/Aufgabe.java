// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class Aufgabe {
    private Aufgabe() {}
    public static Thread ausführenVorgang(String Name, Runnable aktion) {
        Thread ausführungsfadenWert = new Thread(aktion, Name);
        ausführungsfadenWert.start();
        return ausführungsfadenWert;
    }
    public static void abwarten(Thread ausführungsfadenWert) throws InterruptedException { ausführungsfadenWert.join(); }
    public static void übrigKurzzeitigTun(long millisekunden) throws InterruptedException { Thread.sleep(millisekunden); }
    /** Der Aufrufer muss Ressourcen mit shutdown() freigeben. */
    public static ExecutorService werkbankWert(int ausführungsfadenAnzahl) { return Executors.newFixedThreadPool(ausführungsfadenAnzahl); }
}
