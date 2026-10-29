// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Suorita_2() {
        käyttäjätila.Kirjoitus("Hello from a separate Java ELF!\n");
        käyttäjätila.Kirjoitus(käyttäjätila.suoritus_lupa() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEKSI = 0; INDEKSI < käyttäjätila.인수개수(); INDEKSI++) {
            käyttäjätila.Kirjoitus("arg: "); käyttäjätila.Kirjoitus(käyttäjätila.argumentit(INDEKSI)); käyttäjätila.Kirjoitus("\n");
        }
        return käyttäjätila.suoritus_lupa() == 3 ? 0 : 1;
    }
}
