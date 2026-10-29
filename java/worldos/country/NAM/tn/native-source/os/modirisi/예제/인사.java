// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int dirisa() {
        modirisi.kwala("Hello from a separate Java ELF!\n");
        modirisi.kwala(modirisi.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int tshupane = 0; tshupane < modirisi.인수개수(); tshupane++) {
            modirisi.kwala("arg: "); modirisi.kwala(modirisi.인수(tshupane)); modirisi.kwala("\n");
        }
        return modirisi.실행권한() == 3 ? 0 : 1;
    }
}
