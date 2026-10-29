// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int serje() {
        utent.kiteb("Hello from a separate Java ELF!\n");
        utent.kiteb(utent.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < utent.인수개수(); INDEX++) {
            utent.kiteb("arg: "); utent.kiteb(utent.인수(INDEX)); utent.kiteb("\n");
        }
        return utent.실행권한() == 3 ? 0 : 1;
    }
}
