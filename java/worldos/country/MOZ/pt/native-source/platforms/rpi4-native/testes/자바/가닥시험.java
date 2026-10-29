// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class contador_VALOR {
    int número;
    synchronized void 더하기() { int câmera_frontal_VALOR = número; Thread.yield(); número = câmera_frontal_VALOR + 1; }
}
class Tarefa_Ação implements Runnable {
    contador_VALOR contador_Referência; Tarefa_Ação(contador_VALOR contador_Referência) { this.contador_Referência = contador_Referência; }
    public void run() { for (int i = 0; i < 20; i++) contador_Referência.더하기(); }
}
class thread_VALOR extends Thread { public void run() { synchronized (가닥시험.bloquear_VALOR) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object bloquear_VALOR = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        contador_VALOR contador_Referência = new contador_VALOR(); Thread 하나 = new Thread(new Tarefa_Ação(contador_Referência)); Thread 둘 = new Thread(new Tarefa_Ação(contador_Referência));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(contador_Referência.número); System.out.println(하나.isAlive());
        thread_VALOR 셋 = new thread_VALOR(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 rejeitar_VALOR"); }
        System.out.println("thread_VALOR 완료");
    }
}
