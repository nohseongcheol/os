// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int whakahaere() {
        kaiwhakamahi.Tuhia("Hello from a separate Java ELF!\n");
        kaiwhakamahi.Tuhia(kaiwhakamahi.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < kaiwhakamahi.인수개수(); INDEX++) {
            kaiwhakamahi.Tuhia("arg: "); kaiwhakamahi.Tuhia(kaiwhakamahi.인수(INDEX)); kaiwhakamahi.Tuhia("\n");
        }
        return kaiwhakamahi.실행권한() == 3 ? 0 : 1;
    }
}
