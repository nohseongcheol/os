// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Uruchom_2() {
        przestrzeń_użytkownika.Zapis("Hello from a separate Java ELF!\n");
        przestrzeń_użytkownika.Zapis(przestrzeń_użytkownika.wykonanie_pozwolenie() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEKS = 0; INDEKS < przestrzeń_użytkownika.인수개수(); INDEKS++) {
            przestrzeń_użytkownika.Zapis("arg: "); przestrzeń_użytkownika.Zapis(przestrzeń_użytkownika.argumenty(INDEKS)); przestrzeń_użytkownika.Zapis("\n");
        }
        return przestrzeń_użytkownika.wykonanie_pozwolenie() == 3 ? 0 : 1;
    }
}
