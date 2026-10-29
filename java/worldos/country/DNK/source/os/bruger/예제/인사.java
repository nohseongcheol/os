// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Kør_2() {
        bruger.Skrive("Hello from a separate Java ELF!\n");
        bruger.Skrive(bruger.udførelse_rettighed() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEKS = 0; INDEKS < bruger.인수개수(); INDEKS++) {
            bruger.Skrive("arg: "); bruger.Skrive(bruger.Argumenter(INDEKS)); bruger.Skrive("\n");
        }
        return bruger.udførelse_rettighed() == 3 ? 0 : 1;
    }
}
