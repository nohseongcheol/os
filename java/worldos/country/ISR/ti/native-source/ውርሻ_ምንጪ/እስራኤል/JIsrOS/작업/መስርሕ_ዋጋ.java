// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.작업;

import እስራኤል.JIsrOS.기억공간.ገጽ_ኣካያዲ;
import እስራኤል.JIsrOS.ናይ_ፋይል_ስርዓት.파일서술자표;

public final class መስርሕ_ዋጋ {
    private final int ፈላዪ_ዋጋ_5b7b8b77;
    private final int 부모식별자;
    private final ገጽ_ኣካያዲ.ኣድራሻ_ቦታ ኣድራሻ_ቦታ;
    private final 파일서술자표 파일서술자;
    private መስርሕ_ደረጃ ደረጃ_ዋጋ = መስርሕ_ደረጃ.ኣዳልው;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    መስርሕ_ዋጋ(int ፈላዪ_ዋጋ_5b7b8b77, int 부모식별자, ገጽ_ኣካያዲ.ኣድራሻ_ቦታ ኣድራሻ_ቦታ, 파일서술자표 파일서술자) {
        this.ፈላዪ_ዋጋ_5b7b8b77 = ፈላዪ_ዋጋ_5b7b8b77;
        this.부모식별자 = 부모식별자;
        this.ኣድራሻ_ቦታ = ኣድራሻ_ቦታ;
        this.파일서술자 = 파일서술자;
    }

    public int ፈላዪ_ዋጋ_5b7b8b77() {
        return ፈላዪ_ዋጋ_5b7b8b77;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ገጽ_ኣካያዲ.ኣድራሻ_ቦታ ኣድራሻ_ቦታ() {
        return ኣድራሻ_ቦታ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public መስርሕ_ደረጃ ደረጃ_ዋጋ() {
        return ደረጃ_ዋጋ;
    }

    public void እኩብ_ደረጃ(መስርሕ_ደረጃ 새상태) {
        ደረጃ_ዋጋ = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void ውጻእ_መተግበሪ(int ዋጋ) {
        종료값 = ዋጋ & 0xff;
        ደረጃ_ዋጋ = መስርሕ_ደረጃ.ውጻእ_መተግበሪ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("መተግበሪ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ጀምር_ኣድራሻ, String[] 인자, String[] 환경) {
        실행시작주소 = ጀምር_ኣድራሻ;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
