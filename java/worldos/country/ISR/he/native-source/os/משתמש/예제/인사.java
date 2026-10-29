// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int הפעלה() {
        משתמש.כתוב("Hello from a separate Java ELF!\n");
        משתמש.כתוב(משתמש.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int מדד = 0; מדד < משתמש.인수개수(); מדד++) {
            משתמש.כתוב("arg: "); משתמש.כתוב(משתמש.ארגומנטים(מדד)); משתמש.כתוב("\n");
        }
        return משתמש.실행권한() == 3 ? 0 : 1;
    }
}
