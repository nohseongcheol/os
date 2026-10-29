// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Стартиране() {
        потребител.Писане("Hello from a separate Java ELF!\n");
        потребител.Писане(потребител.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int индекс = 0; индекс < потребител.인수개수(); индекс++) {
            потребител.Писане("arg: "); потребител.Писане(потребител.Параметри(индекс)); потребител.Писане("\n");
        }
        return потребител.실행권한() == 3 ? 0 : 1;
    }
}
