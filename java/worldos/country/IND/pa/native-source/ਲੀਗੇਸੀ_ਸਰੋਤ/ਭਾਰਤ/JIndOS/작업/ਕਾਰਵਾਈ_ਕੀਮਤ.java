// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਭਾਰਤ.JIndOS.작업;

import ਭਾਰਤ.JIndOS.기억공간.ਪੰਨਾ_ਪ੍ਰਬੰਧਕ;
import ਭਾਰਤ.JIndOS.ਫਾਈਲ_ਸਿਸਟਮ.파일서술자표;

public final class ਕਾਰਵਾਈ_ਕੀਮਤ {
    private final int ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ;
    private final int 부모식별자;
    private final ਪੰਨਾ_ਪ੍ਰਬੰਧਕ.ਪਤਾ_ਥਾਂ ਪਤਾ_ਥਾਂ;
    private final 파일서술자표 파일서술자;
    private ਕਾਰਵਾਈ_ਸਥਿਤੀ ਸਥਿਤੀ_ਕੀਮਤ = ਕਾਰਵਾਈ_ਸਥਿਤੀ.ਤਿਆਰ_ਕਰੋ;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ਕਾਰਵਾਈ_ਕੀਮਤ(int ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ, int 부모식별자, ਪੰਨਾ_ਪ੍ਰਬੰਧਕ.ਪਤਾ_ਥਾਂ ਪਤਾ_ਥਾਂ, 파일서술자표 파일서술자) {
        this.ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ = ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ;
        this.부모식별자 = 부모식별자;
        this.ਪਤਾ_ਥਾਂ = ਪਤਾ_ਥਾਂ;
        this.파일서술자 = 파일서술자;
    }

    public int ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ() {
        return ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ਪੰਨਾ_ਪ੍ਰਬੰਧਕ.ਪਤਾ_ਥਾਂ ਪਤਾ_ਥਾਂ() {
        return ਪਤਾ_ਥਾਂ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ਕਾਰਵਾਈ_ਸਥਿਤੀ ਸਥਿਤੀ_ਕੀਮਤ() {
        return ਸਥਿਤੀ_ਕੀਮਤ;
    }

    public void ਸੈਟ_ਸਥਿਤੀ(ਕਾਰਵਾਈ_ਸਥਿਤੀ 새상태) {
        ਸਥਿਤੀ_ਕੀਮਤ = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼(int ਕੀਮਤ) {
        종료값 = ਕੀਮਤ & 0xff;
        ਸਥਿਤੀ_ਕੀਮਤ = ਕਾਰਵਾਈ_ਸਥਿਤੀ.ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ਐਪਲੀਕੇਸ਼_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ਸੁਰੂ_ਪਤਾ, String[] 인자, String[] 환경) {
        실행시작주소 = ਸੁਰੂ_ਪਤਾ;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
