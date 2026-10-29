// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int اجرا_2() {
        کاربر.نوشتن("Hello from a separate Java ELF!\n");
        کاربر.نوشتن(کاربر.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int فهرست = 0; فهرست < کاربر.인수개수(); فهرست++) {
            کاربر.نوشتن("arg: "); کاربر.نوشتن(کاربر.نشانوندها(فهرست)); کاربر.نوشتن("\n");
        }
        return کاربر.실행권한() == 3 ? 0 : 1;
    }
}
