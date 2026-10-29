// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ڕادان() {
        بەکارهێنەر.ڕایت_کردن("Hello from a separate Java ELF!\n");
        بەکارهێنەر.ڕایت_کردن(بەکارهێنەر.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int پێرست = 0; پێرست < بەکارهێنەر.인수개수(); پێرست++) {
            بەکارهێنەر.ڕایت_کردن("arg: "); بەکارهێنەر.ڕایت_کردن(بەکارهێنەر.인수(پێرست)); بەکارهێنەر.ڕایت_کردن("\n");
        }
        return بەکارهێنەر.실행권한() == 3 ? 0 : 1;
    }
}
