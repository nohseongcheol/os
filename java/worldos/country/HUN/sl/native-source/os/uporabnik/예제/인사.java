// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Zaženi() {
        uporabnik.Pisanje("Hello from a separate Java ELF!\n");
        uporabnik.Pisanje(uporabnik.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < uporabnik.인수개수(); INDEX++) {
            uporabnik.Pisanje("arg: "); uporabnik.Pisanje(uporabnik.Argumenti(INDEX)); uporabnik.Pisanje("\n");
        }
        return uporabnik.실행권한() == 3 ? 0 : 1;
    }
}
