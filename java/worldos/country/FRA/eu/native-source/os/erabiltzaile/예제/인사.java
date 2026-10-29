// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Exekutatu_2() {
        erabiltzaile.Idatzi("Hello from a separate Java ELF!\n");
        erabiltzaile.Idatzi(erabiltzaile.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDIZE = 0; INDIZE < erabiltzaile.인수개수(); INDIZE++) {
            erabiltzaile.Idatzi("arg: "); erabiltzaile.Idatzi(erabiltzaile.Argumentuak(INDIZE)); erabiltzaile.Idatzi("\n");
        }
        return erabiltzaile.실행권한() == 3 ? 0 : 1;
    }
}
