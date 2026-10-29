// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Spustiť_2() {
        používateľ.Zápis("Hello from a separate Java ELF!\n");
        používateľ.Zápis(používateľ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < používateľ.인수개수(); INDEX++) {
            používateľ.Zápis("arg: "); používateľ.Zápis(používateľ.Argumenty(INDEX)); používateľ.Zápis("\n");
        }
        return používateľ.실행권한() == 3 ? 0 : 1;
    }
}
