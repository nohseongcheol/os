// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int эшләтү() {
        кулланучы.язу("Hello from a separate Java ELF!\n");
        кулланучы.язу(кулланучы.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < кулланучы.인수개수(); INDEX++) {
            кулланучы.язу("arg: "); кулланучы.язу(кулланучы.인수(INDEX)); кулланучы.язу("\n");
        }
        return кулланучы.실행권한() == 3 ? 0 : 1;
    }
}
