// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class zählerWert {
    int Zahl;
    synchronized void werteHinzufügen() { int vorderseiteWert = Zahl; Thread.yield(); Zahl = vorderseiteWert + 1; }
}
class AufgabeAktion implements Runnable {
    zählerWert zählerVerweis; AufgabeAktion(zählerWert zählerVerweis) { this.zählerVerweis = zählerVerweis; }
    public void run() { for (int i = 0; i < 20; i++) zählerVerweis.werteHinzufügen(); }
}
class ausführungsfadenWert extends Thread { public void run() { synchronized (ausführungsfädenPrüfung.sperreWert) { ausführungsfädenPrüfung.istFertig = 1; } } }
public class ausführungsfädenPrüfung {
    static Object sperreWert = new Object(); static int istFertig;
    public static void main(String[] a) throws Exception {
        zählerWert zählerVerweis = new zählerWert(); Thread einsWert = new Thread(new AufgabeAktion(zählerVerweis)); Thread zweiWert = new Thread(new AufgabeAktion(zählerVerweis));
        einsWert.start(); zweiWert.start(); einsWert.join(); zweiWert.join(); System.out.println(zählerVerweis.Zahl); System.out.println(einsWert.isAlive());
        ausführungsfadenWert dritterElementeintrag = new ausführungsfadenWert(); dritterElementeintrag.start(); dritterElementeintrag.join(); System.out.println(istFertig);
        try { einsWert.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 wertZurückweisen"); }
        System.out.println("ausführungsfadenWert istFertig");
    }
}
