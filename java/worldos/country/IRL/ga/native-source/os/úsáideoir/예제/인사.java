// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Rith_2() {
        úsáideoir.Scríobh("Hello from a separate Java ELF!\n");
        úsáideoir.Scríobh(úsáideoir.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < úsáideoir.인수개수(); INDEX++) {
            úsáideoir.Scríobh("arg: "); úsáideoir.Scríobh(úsáideoir.Argóintí(INDEX)); úsáideoir.Scríobh("\n");
        }
        return úsáideoir.실행권한() == 3 ? 0 : 1;
    }
}
