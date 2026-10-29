// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.작업;

import ଭାରତ.JIndOS.기억공간.ପେଜ୍_ପରିଚାଳକ;
import ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍.파일서술자표;

public final class ପ୍ରୋସେସ୍_ମୂଲ୍ୟ {
    private final int ପରିଚାୟକ_ମୂଲ୍ୟ;
    private final int 부모식별자;
    private final ପେଜ୍_ପରିଚାଳକ.ଠିକଣା_ସ୍ଥାନ ଠିକଣା_ସ୍ଥାନ;
    private final 파일서술자표 파일서술자;
    private ପ୍ରୋସେସ୍_ସ୍ଥିତି ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = ପ୍ରୋସେସ୍_ସ୍ଥିତି.ପ୍ରସ୍ତୁତ;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ପ୍ରୋସେସ୍_ମୂଲ୍ୟ(int ପରିଚାୟକ_ମୂଲ୍ୟ, int 부모식별자, ପେଜ୍_ପରିଚାଳକ.ଠିକଣା_ସ୍ଥାନ ଠିକଣା_ସ୍ଥାନ, 파일서술자표 파일서술자) {
        this.ପରିଚାୟକ_ମୂଲ୍ୟ = ପରିଚାୟକ_ମୂଲ୍ୟ;
        this.부모식별자 = 부모식별자;
        this.ଠିକଣା_ସ୍ଥାନ = ଠିକଣା_ସ୍ଥାନ;
        this.파일서술자 = 파일서술자;
    }

    public int ପରିଚାୟକ_ମୂଲ୍ୟ() {
        return ପରିଚାୟକ_ମୂଲ୍ୟ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ପେଜ୍_ପରିଚାଳକ.ଠିକଣା_ସ୍ଥାନ ଠିକଣା_ସ୍ଥାନ() {
        return ଠିକଣା_ସ୍ଥାନ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ପ୍ରୋସେସ୍_ସ୍ଥିତି ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1() {
        return ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1;
    }

    public void ସେଟ୍_ସ୍ଥିତି(ପ୍ରୋସେସ୍_ସ୍ଥିତି 새상태) {
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ(int ମୂଲ୍ୟ) {
        종료값 = ମୂଲ୍ୟ & 0xff;
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = ପ୍ରୋସେସ୍_ସ୍ଥିତି.ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ଅନୁପ୍ରୟୋଗ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ଆରମ୍ଭ_ଠିକଣା, String[] ପାରାମିଟର୍_ଯୁକ୍ତି, String[] 환경) {
        실행시작주소 = ଆରମ୍ଭ_ଠିକଣା;
        실행인자 = ପାରାମିଟର୍_ଯୁକ୍ତି.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
