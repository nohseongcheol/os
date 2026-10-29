// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM 스케줄러가 관리하는 ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ ສະຕຣີມ_ຄ່າ. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ຫນ້າວຽກ_ຄໍາສັ່ງ) {
        throw new ສະຖານະ_ຂໍ້ຍົກເວັ້ນ("자체 JVM의 한국어 작업 ສອດຕໍ່_ຄ່າ ສ້າງ_167eff27 기능이 필요합니다.");
    }
    public native void ເລີ່ມ_ຫນ້າວຽກ() throws ສອດຕໍ່_ສະຖານະ_ຂໍ້ຍົກເວັ້ນ;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void ລະງັບ_ຫນ້າວຽກ();
}
