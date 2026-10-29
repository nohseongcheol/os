// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int run() {
        gumagamit.sumulat("Hello from a separate Java ELF!\n");
        gumagamit.sumulat(gumagamit.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < gumagamit.인수개수(); INDEX++) {
            gumagamit.sumulat("arg: "); gumagamit.sumulat(gumagamit.인수(INDEX)); gumagamit.sumulat("\n");
        }
        return gumagamit.실행권한() == 3 ? 0 : 1;
    }
}
