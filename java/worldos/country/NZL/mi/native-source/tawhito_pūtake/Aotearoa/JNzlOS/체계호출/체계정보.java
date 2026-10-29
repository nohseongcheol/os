// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.체계호출;

public final class 체계정보 {
    private final String pūnaha_ingoa;
    private final String kōpuku_ingoa;
    private final String 배포판;
    private final String putanga_uara;
    private final String mīhini;

    public 체계정보(String pūnaha_ingoa, String kōpuku_ingoa, String 배포판, String putanga_uara, String mīhini) {
        this.pūnaha_ingoa = pūnaha_ingoa;
        this.kōpuku_ingoa = kōpuku_ingoa;
        this.배포판 = 배포판;
        this.putanga_uara = putanga_uara;
        this.mīhini = mīhini;
    }

    public String pūnaha_ingoa() { return pūnaha_ingoa; }
    public String kōpuku_ingoa() { return kōpuku_ingoa; }
    public String 배포판() { return 배포판; }
    public String putanga_uara() { return putanga_uara; }
    public String mīhini() { return mīhini; }
}
