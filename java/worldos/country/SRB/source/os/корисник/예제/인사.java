// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Покрени() {
        корисник.Пише("Hello from a separate Java ELF!\n");
        корисник.Пише(корисник.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int индекс = 0; индекс < корисник.인수개수(); индекс++) {
            корисник.Пише("arg: "); корисник.Пише(корисник.Аргументи(индекс)); корисник.Пише("\n");
        }
        return корисник.실행권한() == 3 ? 0 : 1;
    }
}
