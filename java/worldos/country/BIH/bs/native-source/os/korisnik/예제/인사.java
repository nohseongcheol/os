// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Pokreni() {
        korisnik.Piši("Hello from a separate Java ELF!\n");
        korisnik.Piši(korisnik.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < korisnik.인수개수(); INDEX++) {
            korisnik.Piši("arg: "); korisnik.Piši(korisnik.Argumenti(INDEX)); korisnik.Piši("\n");
        }
        return korisnik.실행권한() == 3 ? 0 : 1;
    }
}
