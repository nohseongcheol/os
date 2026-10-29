// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class contatore_VALORE {
    int numero;
    synchronized void 더하기() { int frontale_VALORE = numero; Thread.yield(); numero = frontale_VALORE + 1; }
}
class task_Action implements Runnable {
    contatore_VALORE contatore_fonti; task_Action(contatore_VALORE contatore_fonti) { this.contatore_fonti = contatore_fonti; }
    public void run() { for (int i = 0; i < 20; i++) contatore_fonti.더하기(); }
}
class thread_VALORE extends Thread { public void run() { synchronized (가닥시험.blocco_VALORE_978a15a5) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object blocco_VALORE_978a15a5 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        contatore_VALORE contatore_fonti = new contatore_VALORE(); Thread 하나 = new Thread(new task_Action(contatore_fonti)); Thread 둘 = new Thread(new task_Action(contatore_fonti));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(contatore_fonti.numero); System.out.println(하나.isAlive());
        thread_VALORE 셋 = new thread_VALORE(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 rifiutare_VALORE"); }
        System.out.println("thread_VALORE 완료");
    }
}
