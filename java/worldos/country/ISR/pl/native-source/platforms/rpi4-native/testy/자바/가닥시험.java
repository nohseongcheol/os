// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class licznik_WARTOŚĆ {
    int identyfikator;
    synchronized void 더하기() { int przód_WARTOŚĆ = identyfikator; Thread.yield(); identyfikator = przód_WARTOŚĆ + 1; }
}
class zadanie_akcja implements Runnable {
    licznik_WARTOŚĆ licznik_odwołanie; zadanie_akcja(licznik_WARTOŚĆ licznik_odwołanie) { this.licznik_odwołanie = licznik_odwołanie; }
    public void run() { for (int i = 0; i < 20; i++) licznik_odwołanie.더하기(); }
}
class wątek_WARTOŚĆ extends Thread { public void run() { synchronized (가닥시험.blokada_WARTOŚĆ) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object blokada_WARTOŚĆ = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        licznik_WARTOŚĆ licznik_odwołanie = new licznik_WARTOŚĆ(); Thread 하나 = new Thread(new zadanie_akcja(licznik_odwołanie)); Thread 둘 = new Thread(new zadanie_akcja(licznik_odwołanie));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(licznik_odwołanie.identyfikator); System.out.println(하나.isAlive());
        wątek_WARTOŚĆ 셋 = new wątek_WARTOŚĆ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 odrzucić_WARTOŚĆ"); }
        System.out.println("wątek_WARTOŚĆ 완료");
    }
}
