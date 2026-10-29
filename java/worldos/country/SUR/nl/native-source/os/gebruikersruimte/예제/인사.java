// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int starten() {
        gebruikersruimte.Schrijven("Hello from a separate Java ELF!\n");
        gebruikersruimte.Schrijven(gebruikersruimte.uitvoerbewerking_machtiging() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < gebruikersruimte.인수개수(); INDEX++) {
            gebruikersruimte.Schrijven("arg: "); gebruikersruimte.Schrijven(gebruikersruimte.argumenten(INDEX)); gebruikersruimte.Schrijven("\n");
        }
        return gebruikersruimte.uitvoerbewerking_machtiging() == 3 ? 0 : 1;
    }
}
