// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Kusini.JZafOS.체계호출;

public final class 체계정보 {
    private final String mfumo_jina;
    private final String fundo_jina;
    private final String 배포판;
    private final String toleo_thamani;
    private final String mashine;

    public 체계정보(String mfumo_jina, String fundo_jina, String 배포판, String toleo_thamani, String mashine) {
        this.mfumo_jina = mfumo_jina;
        this.fundo_jina = fundo_jina;
        this.배포판 = 배포판;
        this.toleo_thamani = toleo_thamani;
        this.mashine = mashine;
    }

    public String mfumo_jina() { return mfumo_jina; }
    public String fundo_jina() { return fundo_jina; }
    public String 배포판() { return 배포판; }
    public String toleo_thamani() { return toleo_thamani; }
    public String mashine() { return mashine; }
}
