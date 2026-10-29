// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Diriša() {
        mošomiši.Ngwala("Hello from a separate Java ELF!\n");
        mošomiši.Ngwala(mošomiši.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int lokela = 0; lokela < mošomiši.인수개수(); lokela++) {
            mošomiši.Ngwala("arg: "); mošomiši.Ngwala(mošomiši.인수(lokela)); mošomiši.Ngwala("\n");
        }
        return mošomiši.실행권한() == 3 ? 0 : 1;
    }
}
