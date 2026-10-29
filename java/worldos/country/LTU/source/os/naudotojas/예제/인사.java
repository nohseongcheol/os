// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Paleisti() {
        naudotojas.Rašymas("Hello from a separate Java ELF!\n");
        naudotojas.Rašymas(naudotojas.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < naudotojas.인수개수(); INDEX++) {
            naudotojas.Rašymas("arg: "); naudotojas.Rašymas(naudotojas.Argumentai(INDEX)); naudotojas.Rašymas("\n");
        }
        return naudotojas.실행권한() == 3 ? 0 : 1;
    }
}
