// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class mai_kirga_Daraja {
    int 수;
    synchronized void 더하기() { int kyamarar_gaba_Daraja = 수; Thread.yield(); 수 = kyamarar_gaba_Daraja + 1; }
}
class aiki_Aiki implements Runnable {
    mai_kirga_Daraja mai_kirga_Manazarta; aiki_Aiki(mai_kirga_Daraja mai_kirga_Manazarta) { this.mai_kirga_Manazarta = mai_kirga_Manazarta; }
    public void run() { for (int i = 0; i < 20; i++) mai_kirga_Manazarta.더하기(); }
}
class hira_Daraja extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        mai_kirga_Daraja mai_kirga_Manazarta = new mai_kirga_Daraja(); Thread 하나 = new Thread(new aiki_Aiki(mai_kirga_Manazarta)); Thread 둘 = new Thread(new aiki_Aiki(mai_kirga_Manazarta));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(mai_kirga_Manazarta.수); System.out.println(하나.isAlive());
        hira_Daraja 셋 = new hira_Daraja(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 kore_Daraja"); }
        System.out.println("hira_Daraja 완료");
    }
}
