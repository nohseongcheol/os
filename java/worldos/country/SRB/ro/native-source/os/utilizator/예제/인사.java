// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Pornește() {
        utilizator.Scriere("Hello from a separate Java ELF!\n");
        utilizator.Scriere(utilizator.executare_permisiune() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < utilizator.인수개수(); INDEX++) {
            utilizator.Scriere("arg: "); utilizator.Scriere(utilizator.Argumente(INDEX)); utilizator.Scriere("\n");
        }
        return utilizator.executare_permisiune() == 3 ? 0 : 1;
    }
}
