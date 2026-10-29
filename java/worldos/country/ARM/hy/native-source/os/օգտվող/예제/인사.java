// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Գործարկել() {
        օգտվող.Գրել("Hello from a separate Java ELF!\n");
        օգտվող.Գրել(օգտվող.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int դասիչ = 0; դասիչ < օգտվող.인수개수(); դասիչ++) {
            օգտվող.Գրել("arg: "); օգտվող.Գրել(օգտվող.인수(դասիչ)); օգտվող.Գրել("\n");
        }
        return օգտվող.실행권한() == 3 ? 0 : 1;
    }
}
