// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package कनाडा.JCanOS.작업;

import कनाडा.JCanOS.मेमोरी_क्षेत्र.पेज_प्रबंधक;
import कनाडा.JCanOS.फ़ाइल_सिस्टम.파일서술자표;

public final class प्रक्रिया_मान {
    private final int पहचानकर्ता_मान;
    private final int पैरेंट_पहचानकर्ता;
    private final पेज_प्रबंधक.पता_स्थान पता_स्थान;
    private final 파일서술자표 파일서술자;
    private प्रक्रिया_अवस्था अवस्था_मान = प्रक्रिया_अवस्था.준비;
    private int निर्गमन_कोड;
    private int ऐप_विराम = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    प्रक्रिया_मान(int पहचानकर्ता_मान, int पैरेंट_पहचानकर्ता, पेज_प्रबंधक.पता_स्थान पता_स्थान, 파일서술자표 파일서술자) {
        this.पहचानकर्ता_मान = पहचानकर्ता_मान;
        this.पैरेंट_पहचानकर्ता = पैरेंट_पहचानकर्ता;
        this.पता_स्थान = पता_स्थान;
        this.파일서술자 = 파일서술자;
    }

    public int पहचानकर्ता_मान() {
        return पहचानकर्ता_मान;
    }

    public int पैरेंट_पहचानकर्ता() {
        return पैरेंट_पहचानकर्ता;
    }

    public पेज_प्रबंधक.पता_स्थान पता_स्थान() {
        return पता_स्थान;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public प्रक्रिया_अवस्था अवस्था_मान() {
        return अवस्था_मान;
    }

    public void सेट_अवस्था(प्रक्रिया_अवस्था 새상태) {
        अवस्था_मान = 새상태;
    }

    public int निर्गमन_कोड() {
        return निर्गमन_कोड;
    }

    public void निर्गमन_ऐप(int मान) {
        निर्गमन_कोड = मान & 0xff;
        अवस्था_मान = प्रक्रिया_अवस्था.निर्गमन_ऐप;
    }

    public int ऐप_विराम() {
        return ऐप_विराम;
    }

    public void सेट_ऐप_विराम(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ऐप_f5044b9b 끝 범위를 벗어났습니다.");
        }
        ऐप_विराम = 새끝;
    }

    public void 실행문맥설정(int प्रारंभ_पता, String[] पैरामीटर_तर्क, String[] 환경) {
        실행시작주소 = प्रारंभ_पता;
        실행인자 = पैरामीटर_तर्क.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
