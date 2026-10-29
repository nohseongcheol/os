// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int İcra_Et() {
        istifadəçi.Yazma("Hello from a separate Java ELF!\n");
        istifadəçi.Yazma(istifadəçi.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < istifadəçi.인수개수(); INDEX++) {
            istifadəçi.Yazma("arg: "); istifadəçi.Yazma(istifadəçi.인수(INDEX)); istifadəçi.Yazma("\n");
        }
        return istifadəçi.실행권한() == 3 ? 0 : 1;
    }
}
