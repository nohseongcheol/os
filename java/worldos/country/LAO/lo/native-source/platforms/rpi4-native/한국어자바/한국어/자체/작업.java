// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 작업 ສອດຕໍ່_ຄ່າ: 하나의 ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ ສະຕຣີມ_ຄ່າ. 자체 JVM 안에서 ຄໍາສັ່ງ_1f12b8e2 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ແລ່ນ(실행할일 ຫນ້າວຽກ_ຄໍາສັ່ງ) { 작업가닥 ສອດຕໍ່_ຄ່າ = new 작업가닥(ຫນ້າວຽກ_ຄໍາສັ່ງ); ສອດຕໍ່_ຄ່າ.ເລີ່ມ_ຫນ້າວຽກ(); return ສອດຕໍ່_ຄ່າ; }
    public static void 기다리기(작업가닥 ສອດຕໍ່_ຄ່າ) throws 대기중단예외 { ສອດຕໍ່_ຄ່າ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ສອດຕໍ່_ຄ່າ) { return ສອດຕໍ່_ຄ່າ.살아있는가(); }
    public static void ລະງັບ_ຫນ້າວຽກ() { 작업가닥.ລະງັບ_ຫນ້າວຽກ(); }
}
