// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int เรียกใช้งาน() {
        ผู้ใช้.เขียน("Hello from a separate Java ELF!\n");
        ผู้ใช้.เขียน(ผู้ใช้.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ดัชนี = 0; ดัชนี < ผู้ใช้.인수개수(); ดัชนี++) {
            ผู้ใช้.เขียน("arg: "); ผู้ใช้.เขียน(ผู้ใช้.อาร์กิวเมนต์(ดัชนี)); ผู้ใช้.เขียน("\n");
        }
        return ผู้ใช้.실행권한() == 3 ? 0 : 1;
    }
}
