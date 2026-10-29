// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Ажиллуулах() {
        хэрэглэгч.Бичих("Hello from a separate Java ELF!\n");
        хэрэглэгч.Бичих(хэрэглэгч.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int индекс = 0; индекс < хэрэглэгч.인수개수(); индекс++) {
            хэрэглэгч.Бичих("arg: "); хэрэглэгч.Бичих(хэрэглэгч.인수(индекс)); хэрэглэгч.Бичих("\n");
        }
        return хэрэглэгч.실행권한() == 3 ? 0 : 1;
    }
}
