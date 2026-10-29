// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class เครื่องมือ_รายการ {
    public static int เรียกใช้งาน() {
        return ผู้ใช้.เครื่องมือ_หมายเลข() == 0 ? 자바컴파일러.เรียกใช้งาน() : 자바가상기계.เรียกใช้งาน();
    }
}
