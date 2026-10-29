// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.โฮสต์;

import java.util.HashMap;
import java.util.Map;
import ประเทศไทย.JThaOS.แก่นระบบ.ฮาร์ดแวร์_ค่า;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 ฮาร์ดแวร์_ค่า 대역이다. */
public final class โฮสต์_ฮาร์ดแวร์ implements ฮาร์ดแวร์_ค่า {
    private final Map<Integer, Integer> ฮาร์ดแวร์_แปลง_ค่า = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String เนื้อหา_ค่า) {
        직렬기록.append(เนื้อหา_ค่า);
        System.out.print(เนื้อหา_ค่า);
    }

    @Override
    public int 포트바이트읽기(int ฮาร์ดแวร์_หมายเลขพอร์ต) {
        Integer ค่า = ฮาร์ดแวร์_แปลง_ค่า.get(Integer.valueOf(ฮาร์ดแวร์_หมายเลขพอร์ต));
        return ค่า == null ? 0 : ค่า.intValue();
    }

    @Override
    public void 포트바이트쓰기(int ฮาร์ดแวร์_หมายเลขพอร์ต, int ค่า) {
        ฮาร์ดแวร์_แปลง_ค่า.put(Integer.valueOf(ฮาร์ดแวร์_หมายเลขพอร์ต), Integer.valueOf(ค่า & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // โฮสต์ 시험에서는 ถัดไป_รายการ 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

