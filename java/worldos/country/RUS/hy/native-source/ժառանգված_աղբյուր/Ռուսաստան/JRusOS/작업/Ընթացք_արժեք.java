// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ռուսաստան.JRusOS.작업;

import Ռուսաստան.JRusOS.기억공간.էջ_կառավարիչ;
import Ռուսաստան.JRusOS.նիշքային_համակարգ.파일서술자표;

public final class Ընթացք_արժեք {
    private final int նույնացուցիչ_արժեք;
    private final int 부모식별자;
    private final էջ_կառավարիչ.հասցե_տեղ հասցե_տեղ;
    private final 파일서술자표 파일서술자;
    private Ընթացք_վիճակ վիճակ_արժեք = Ընթացք_վիճակ.Պատրաստել;
    private int Ելք_կոդ;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Ընթացք_արժեք(int նույնացուցիչ_արժեք, int 부모식별자, էջ_կառավարիչ.հասցե_տեղ հասցե_տեղ, 파일서술자표 파일서술자) {
        this.նույնացուցիչ_արժեք = նույնացուցիչ_արժեք;
        this.부모식별자 = 부모식별자;
        this.հասցե_տեղ = հասցե_տեղ;
        this.파일서술자 = 파일서술자;
    }

    public int նույնացուցիչ_արժեք() {
        return նույնացուցիչ_արժեք;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public էջ_կառավարիչ.հասցե_տեղ հասցե_տեղ() {
        return հասցե_տեղ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Ընթացք_վիճակ վիճակ_արժեք() {
        return վիճակ_արժեք;
    }

    public void կազմ_վիճակ(Ընթացք_վիճակ 새상태) {
        վիճակ_արժեք = 새상태;
    }

    public int Ելք_կոդ() {
        return Ելք_կոդ;
    }

    public void Ելք_ծրագիր(int արժեք) {
        Ելք_կոդ = արժեք & 0xff;
        վիճակ_արժեք = Ընթացք_վիճակ.Ելք_ծրագիր;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ծրագիր_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Մեկնարկ_հասցե, String[] 인자, String[] 환경) {
        실행시작주소 = Մեկնարկ_հասցե;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
