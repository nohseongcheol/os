// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ไทย.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 หมายเลข 있는 작은 Java จุดเข้าใช้งาน. */
public final class 문자명령 {
    public static void main(String[] อาร์กิวเมนต์) {
        if (อาร์กิวเมนต์.length != 1) {
            System.err.println("사용법: 문자명령 สตริง_ค่า");
            System.exit(2);
        }
        System.out.println(문자.코드포인트수(อาร์กิวเมนต์[0]));
    }
}
