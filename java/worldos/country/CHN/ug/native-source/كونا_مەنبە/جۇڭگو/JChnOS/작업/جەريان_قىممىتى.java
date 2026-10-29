// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.작업;

import جۇڭگو.JChnOS.기억공간.بەت_باشقۇرغۇچى;
import جۇڭگو.JChnOS.ھۆججەت_سىستېمىسى.파일서술자표;

public final class جەريان_قىممىتى {
    private final int پەرقلەندۈرگۈچ_قىممىتى;
    private final int 부모식별자;
    private final بەت_باشقۇرغۇچى.ئادرېس_بوشلۇق ئادرېس_بوشلۇق;
    private final 파일서술자표 파일서술자;
    private جەريان_ھالەت_4346e67f ھالەت_قىممىتى = جەريان_ھالەت_4346e67f.تەييارلىماق;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    جەريان_قىممىتى(int پەرقلەندۈرگۈچ_قىممىتى, int 부모식별자, بەت_باشقۇرغۇچى.ئادرېس_بوشلۇق ئادرېس_بوشلۇق, 파일서술자표 파일서술자) {
        this.پەرقلەندۈرگۈچ_قىممىتى = پەرقلەندۈرگۈچ_قىممىتى;
        this.부모식별자 = 부모식별자;
        this.ئادرېس_بوشلۇق = ئادرېس_بوشلۇق;
        this.파일서술자 = 파일서술자;
    }

    public int پەرقلەندۈرگۈچ_قىممىتى() {
        return پەرقلەندۈرگۈچ_قىممىتى;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public بەت_باشقۇرغۇچى.ئادرېس_بوشلۇق ئادرېس_بوشلۇق() {
        return ئادرېس_بوشلۇق;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public جەريان_ھالەت_4346e67f ھالەت_قىممىتى() {
        return ھالەت_قىممىتى;
    }

    public void توپ_ھالەت(جەريان_ھالەت_4346e67f 새상태) {
        ھالەت_قىممىتى = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void چىقىش_ئەپ(int قىممىتى) {
        종료값 = قىممىتى & 0xff;
        ھالەت_قىممىتى = جەريان_ھالەت_4346e67f.چىقىش_ئەپ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ئەپ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int باشلاش_ئادرېس, String[] 인자, String[] 환경) {
        실행시작주소 = باشلاش_ئادرېس;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
