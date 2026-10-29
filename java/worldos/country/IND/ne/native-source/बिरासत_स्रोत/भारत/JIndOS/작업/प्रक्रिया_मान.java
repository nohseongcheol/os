// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.작업;

import भारत.JIndOS.기억공간.पृष्ठ_प्रबन्धक;
import भारत.JIndOS.फाइल_प्रणाली.파일서술자표;

public final class प्रक्रिया_मान {
    private final int परिचायक_मान;
    private final int 부모식별자;
    private final पृष्ठ_प्रबन्धक.ठेगाना_स्थान ठेगाना_स्थान;
    private final 파일서술자표 파일서술자;
    private प्रक्रिया_स्थिति स्थिति_मान = प्रक्रिया_स्थिति.तयार_गर्नुहोस्;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    प्रक्रिया_मान(int परिचायक_मान, int 부모식별자, पृष्ठ_प्रबन्धक.ठेगाना_स्थान ठेगाना_स्थान, 파일서술자표 파일서술자) {
        this.परिचायक_मान = परिचायक_मान;
        this.부모식별자 = 부모식별자;
        this.ठेगाना_स्थान = ठेगाना_स्थान;
        this.파일서술자 = 파일서술자;
    }

    public int परिचायक_मान() {
        return परिचायक_मान;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public पृष्ठ_प्रबन्धक.ठेगाना_स्थान ठेगाना_स्थान() {
        return ठेगाना_स्थान;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public प्रक्रिया_स्थिति स्थिति_मान() {
        return स्थिति_मान;
    }

    public void सेट_स्थिति(प्रक्रिया_स्थिति 새상태) {
        स्थिति_मान = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void बाहिर_जानुहोस्_अनुप्रयोग(int मान) {
        종료값 = मान & 0xff;
        स्थिति_मान = प्रक्रिया_स्थिति.बाहिर_जानुहोस्_अनुप्रयोग;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("अनुप्रयोग_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int सुरु_ठेगाना, String[] 인자, String[] 환경) {
        실행시작주소 = सुरु_ठेगाना;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
