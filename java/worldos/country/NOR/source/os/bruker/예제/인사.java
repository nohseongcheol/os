// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Kjør_2() {
        bruker.Skriv("Hello from a separate Java ELF!\n");
        bruker.Skriv(bruker.kjøring_tillatelse() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEKS = 0; INDEKS < bruker.인수개수(); INDEKS++) {
            bruker.Skriv("arg: "); bruker.Skriv(bruker.Argumenter(INDEKS)); bruker.Skriv("\n");
        }
        return bruker.kjøring_tillatelse() == 3 ? 0 : 1;
    }
}
