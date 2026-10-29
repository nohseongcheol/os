// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ruith() {
        cleachdaiche.sgrìobh("Hello from a separate Java ELF!\n");
        cleachdaiche.sgrìobh(cleachdaiche.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < cleachdaiche.인수개수(); INDEX++) {
            cleachdaiche.sgrìobh("arg: "); cleachdaiche.sgrìobh(cleachdaiche.인수(INDEX)); cleachdaiche.sgrìobh("\n");
        }
        return cleachdaiche.실행권한() == 3 ? 0 : 1;
    }
}
