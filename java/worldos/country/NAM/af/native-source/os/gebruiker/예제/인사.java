// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Loop() {
        gebruiker.Skryf("Hello from a separate Java ELF!\n");
        gebruiker.Skryf(gebruiker.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < gebruiker.인수개수(); INDEX++) {
            gebruiker.Skryf("arg: "); gebruiker.Skryf(gebruiker.인수(INDEX)); gebruiker.Skryf("\n");
        }
        return gebruiker.실행권한() == 3 ? 0 : 1;
    }
}
