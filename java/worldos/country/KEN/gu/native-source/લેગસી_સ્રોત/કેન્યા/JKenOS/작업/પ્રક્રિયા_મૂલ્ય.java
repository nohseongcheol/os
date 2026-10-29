// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેન્યા.JKenOS.작업;

import કેન્યા.JKenOS.기억공간.પેજ_પ્રબંધક;
import કેન્યા.JKenOS.ફાઇલ_સિસ્ટમ.파일서술자표;

public final class પ્રક્રિયા_મૂલ્ય {
    private final int ઓળખકર્તા_મૂલ્ય;
    private final int 부모식별자;
    private final પેજ_પ્રબંધક.સરનામું_જગ્યા સરનામું_જગ્યા;
    private final 파일서술자표 파일서술자;
    private પ્રક્રિયા_સ્થિતિ સ્થિતિ_મૂલ્ય_e10195a1 = પ્રક્રિયા_સ્થિતિ.તૈયાર_કરો;
    private int 종료값;
    private int એપ્લિકેશન_બ્રેક = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    પ્રક્રિયા_મૂલ્ય(int ઓળખકર્તા_મૂલ્ય, int 부모식별자, પેજ_પ્રબંધક.સરનામું_જગ્યા સરનામું_જગ્યા, 파일서술자표 파일서술자) {
        this.ઓળખકર્તા_મૂલ્ય = ઓળખકર્તા_મૂલ્ય;
        this.부모식별자 = 부모식별자;
        this.સરનામું_જગ્યા = સરનામું_જગ્યા;
        this.파일서술자 = 파일서술자;
    }

    public int ઓળખકર્તા_મૂલ્ય() {
        return ઓળખકર્તા_મૂલ્ય;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public પેજ_પ્રબંધક.સરનામું_જગ્યા સરનામું_જગ્યા() {
        return સરનામું_જગ્યા;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public પ્રક્રિયા_સ્થિતિ સ્થિતિ_મૂલ્ય_e10195a1() {
        return સ્થિતિ_મૂલ્ય_e10195a1;
    }

    public void સેટ_સ્થિતિ(પ્રક્રિયા_સ્થિતિ 새상태) {
        સ્થિતિ_મૂલ્ય_e10195a1 = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void પ્રસ્થાન_એપ્લિકેશન(int મૂલ્ય) {
        종료값 = મૂલ્ય & 0xff;
        સ્થિતિ_મૂલ્ય_e10195a1 = પ્રક્રિયા_સ્થિતિ.પ્રસ્થાન_એપ્લિકેશન;
    }

    public int એપ્લિકેશન_બ્રેક() {
        return એપ્લિકેશન_બ્રેક;
    }

    public void સેટ_એપ્લિકેશન_બ્રેક(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("એપ્લિકેશન_f5044b9b 끝 범위를 벗어났습니다.");
        }
        એપ્લિકેશન_બ્રેક = 새끝;
    }

    public void 실행문맥설정(int પ્રારંભ_સરનામું, String[] પેરામીટર_દલીલ, String[] 환경) {
        실행시작주소 = પ્રારંભ_સરનામું;
        실행인자 = પેરામીટર_દલીલ.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
