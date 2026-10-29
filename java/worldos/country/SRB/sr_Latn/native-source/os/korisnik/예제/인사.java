// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int koristiti() {
        korisnik.쓰기("Hello from a separate Java ELF!\n");
        korisnik.쓰기(korisnik.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < korisnik.인수개수(); INDEX++) {
            korisnik.쓰기("arg: "); korisnik.쓰기(korisnik.인수(INDEX)); korisnik.쓰기("\n");
        }
        return korisnik.실행권한() == 3 ? 0 : 1;
    }
}
