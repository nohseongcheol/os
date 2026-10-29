// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int порча() {
        корбар.Навиштан("Hello from a separate Java ELF!\n");
        корбар.Навиштан(корбар.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int индекс = 0; индекс < корбар.인수개수(); индекс++) {
            корбар.Навиштан("arg: "); корбар.Навиштан(корбар.인수(индекс)); корбар.Навиштан("\n");
        }
        return корбар.실행권한() == 3 ? 0 : 1;
    }
}
