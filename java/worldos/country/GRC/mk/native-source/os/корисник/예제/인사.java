// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Изврши_2() {
        корисник.Запиши("Hello from a separate Java ELF!\n");
        корисник.Запиши(корисник.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < корисник.인수개수(); INDEX++) {
            корисник.Запиши("arg: "); корисник.Запиши(корисник.Аргументи(INDEX)); корисник.Запиши("\n");
        }
        return корисник.실행권한() == 3 ? 0 : 1;
    }
}
