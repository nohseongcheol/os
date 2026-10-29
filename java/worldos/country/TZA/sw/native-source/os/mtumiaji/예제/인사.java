// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int endesha() {
        mtumiaji.andika("Hello from a separate Java ELF!\n");
        mtumiaji.andika(mtumiaji.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int kielezo = 0; kielezo < mtumiaji.인수개수(); kielezo++) {
            mtumiaji.andika("arg: "); mtumiaji.andika(mtumiaji.인수(kielezo)); mtumiaji.andika("\n");
        }
        return mtumiaji.실행권한() == 3 ? 0 : 1;
    }
}
