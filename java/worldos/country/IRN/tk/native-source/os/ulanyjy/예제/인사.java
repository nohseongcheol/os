// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Bitir() {
        ulanyjy.Ýaz("Hello from a separate Java ELF!\n");
        ulanyjy.Ýaz(ulanyjy.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int indeks = 0; indeks < ulanyjy.인수개수(); indeks++) {
            ulanyjy.Ýaz("arg: "); ulanyjy.Ýaz(ulanyjy.인수(indeks)); ulanyjy.Ýaz("\n");
        }
        return ulanyjy.실행권한() == 3 ? 0 : 1;
    }
}
