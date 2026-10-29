// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Phumeza() {
        umsebenzisi.Bhala("Hello from a separate Java ELF!\n");
        umsebenzisi.Bhala(umsebenzisi.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int indeksa = 0; indeksa < umsebenzisi.인수개수(); indeksa++) {
            umsebenzisi.Bhala("arg: "); umsebenzisi.Bhala(umsebenzisi.인수(indeksa)); umsebenzisi.Bhala("\n");
        }
        return umsebenzisi.실행권한() == 3 ? 0 : 1;
    }
}
