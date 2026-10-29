// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Alefaso() {
        사용자.Manoratra("Hello from a separate Java ELF!\n");
        사용자.Manoratra(사용자.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int 번호 = 0; 번호 < 사용자.인수개수(); 번호++) {
            사용자.Manoratra("arg: "); 사용자.Manoratra(사용자.인수(번호)); 사용자.Manoratra("\n");
        }
        return 사용자.실행권한() == 3 ? 0 : 1;
    }
}
