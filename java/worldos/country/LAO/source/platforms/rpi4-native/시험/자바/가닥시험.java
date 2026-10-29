// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class ເຄື່ອງ_ນັບ_ຄ່າ {
    int 수;
    synchronized void 더하기() { int ດ້ານຫນ້າ_ຄ່າ = 수; Thread.yield(); 수 = ດ້ານຫນ້າ_ຄ່າ + 1; }
}
class ຫນ້າວຽກ_ຄໍາສັ່ງ implements Runnable {
    ເຄື່ອງ_ນັບ_ຄ່າ ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ; ຫນ້າວຽກ_ຄໍາສັ່ງ(ເຄື່ອງ_ນັບ_ຄ່າ ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ) { this.ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ = ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ; }
    public void run() { for (int i = 0; i < 20; i++) ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ.더하기(); }
}
class ສອດຕໍ່_ຄ່າ extends Thread { public void run() { synchronized (가닥시험.잠금) { 가닥시험.완료 = 1; } } }
public class 가닥시험 {
    static Object 잠금 = new Object(); static int 완료;
    public static void main(String[] a) throws Exception {
        ເຄື່ອງ_ນັບ_ຄ່າ ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ = new ເຄື່ອງ_ນັບ_ຄ່າ(); Thread 하나 = new Thread(new ຫນ້າວຽກ_ຄໍາສັ່ງ(ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ)); Thread 둘 = new Thread(new ຫນ້າວຽກ_ຄໍາສັ່ງ(ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ));
        하나.start(); 둘.start(); 하나.join(); 둘.join(); System.out.println(ເຄື່ອງ_ນັບ_ການ_ອ້າງ_ອີງ.수); System.out.println(하나.isAlive());
        ສອດຕໍ່_ຄ່າ 셋 = new ສອດຕໍ່_ຄ່າ(); 셋.start(); 셋.join(); System.out.println(완료);
        try { 하나.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 ປະຕິເສດ_ຄ່າ"); }
        System.out.println("ສອດຕໍ່_ຄ່າ 완료");
    }
}
