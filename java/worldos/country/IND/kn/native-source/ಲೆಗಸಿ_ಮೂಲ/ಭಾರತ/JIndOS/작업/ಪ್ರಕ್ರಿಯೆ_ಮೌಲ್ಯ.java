// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.작업;

import ಭಾರತ.JIndOS.기억공간.ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ;
import ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ.파일서술자표;

public final class ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ {
    private final int ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ;
    private final int 부모식별자;
    private final ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ.ಇಮೇಲ್_ಸ್ಪೇಸ್ ಇಮೇಲ್_ಸ್ಪೇಸ್;
    private final 파일서술자표 파일서술자;
    private ಪ್ರಕ್ರಿಯೆ_ಸ್ಥಿತಿ ಸ್ಥಿತಿ_ಮೌಲ್ಯ = ಪ್ರಕ್ರಿಯೆ_ಸ್ಥಿತಿ.ಸಿದ್ಧಪಡಿಸು;
    private int ನಿರ್ಗಮನ_ಕೋಡ್;
    private int ಅಪ್ಲಿ_ವಿರಾಮ = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ(int ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ, int 부모식별자, ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ.ಇಮೇಲ್_ಸ್ಪೇಸ್ ಇಮೇಲ್_ಸ್ಪೇಸ್, 파일서술자표 파일서술자) {
        this.ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ = ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ;
        this.부모식별자 = 부모식별자;
        this.ಇಮೇಲ್_ಸ್ಪೇಸ್ = ಇಮೇಲ್_ಸ್ಪೇಸ್;
        this.파일서술자 = 파일서술자;
    }

    public int ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ() {
        return ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ.ಇಮೇಲ್_ಸ್ಪೇಸ್ ಇಮೇಲ್_ಸ್ಪೇಸ್() {
        return ಇಮೇಲ್_ಸ್ಪೇಸ್;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ಪ್ರಕ್ರಿಯೆ_ಸ್ಥಿತಿ ಸ್ಥಿತಿ_ಮೌಲ್ಯ() {
        return ಸ್ಥಿತಿ_ಮೌಲ್ಯ;
    }

    public void ಸೆಟ್_ಸ್ಥಿತಿ(ಪ್ರಕ್ರಿಯೆ_ಸ್ಥಿತಿ 새상태) {
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ = 새상태;
    }

    public int ನಿರ್ಗಮನ_ಕೋಡ್() {
        return ನಿರ್ಗಮನ_ಕೋಡ್;
    }

    public void ನಿರ್ಗಮನ_ಅಪ್ಲಿ(int ಮೌಲ್ಯ) {
        ನಿರ್ಗಮನ_ಕೋಡ್ = ಮೌಲ್ಯ & 0xff;
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ = ಪ್ರಕ್ರಿಯೆ_ಸ್ಥಿತಿ.ನಿರ್ಗಮನ_ಅಪ್ಲಿ;
    }

    public int ಅಪ್ಲಿ_ವಿರಾಮ() {
        return ಅಪ್ಲಿ_ವಿರಾಮ;
    }

    public void ಸೆಟ್_ಅಪ್ಲಿ_ವಿರಾಮ(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ಅಪ್ಲಿ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        ಅಪ್ಲಿ_ವಿರಾಮ = 새끝;
    }

    public void 실행문맥설정(int ಆರಂಭಿಸು_ಇಮೇಲ್, String[] ಪ್ಯಾರಾಮೀಟರ್_ವಾದ, String[] 환경) {
        실행시작주소 = ಆರಂಭಿಸು_ಇಮೇಲ್;
        실행인자 = ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
