// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Seveniñ_2() {
        사용자.Skrivañ("Hello from a separate Java ELF!\n");
        사용자.Skrivañ(사용자.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int 번호 = 0; 번호 < 사용자.인수개수(); 번호++) {
            사용자.Skrivañ("arg: "); 사용자.Skrivañ(사용자.Arventennoù(번호)); 사용자.Skrivañ("\n");
        }
        return 사용자.실행권한() == 3 ? 0 : 1;
    }
}
