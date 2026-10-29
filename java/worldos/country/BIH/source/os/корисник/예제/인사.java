// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int 시작() {
        корисник.писати("Hello from a separate Java ELF!\n");
        корисник.писати(корисник.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int индекс = 0; индекс < корисник.인수개수(); индекс++) {
            корисник.писати("arg: "); корисник.писати(корисник.인수(индекс)); корисник.писати("\n");
        }
        return корисник.실행권한() == 3 ? 0 : 1;
    }
}
