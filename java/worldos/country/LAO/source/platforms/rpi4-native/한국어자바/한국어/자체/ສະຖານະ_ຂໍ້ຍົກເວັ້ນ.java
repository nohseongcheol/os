// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 ການປະກາດ·던지기·잡기를 할 수 있는 ສະຖານະ_ຂໍ້ຍົກເວັ້ນ. */
public class ສະຖານະ_ຂໍ້ຍົກເວັ້ນ extends java.lang.IllegalStateException {
    public ສະຖານະ_ຂໍ້ຍົກເວັ້ນ() { super(); }
    public ສະຖານະ_ຂໍ້ຍົກເວັ້ນ(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
