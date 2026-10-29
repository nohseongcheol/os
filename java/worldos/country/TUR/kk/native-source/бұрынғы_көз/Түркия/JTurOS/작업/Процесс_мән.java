// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Түркия.JTurOS.작업;

import Түркия.JTurOS.Жад_аумақ.бет_менеджер;
import Түркия.JTurOS.файлдық_жүйе.파일서술자표;

public final class Процесс_мән {
    private final int идентификатор_мән;
    private final int басты_идентификатор;
    private final бет_менеджер.мекенжай_орын мекенжай_орын;
    private final 파일서술자표 파일서술자;
    private Процесс_күй күй_мән = Процесс_күй.Дайындау;
    private int Шығу_код;
    private int бағдарлама_үзу = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Процесс_мән(int идентификатор_мән, int басты_идентификатор, бет_менеджер.мекенжай_орын мекенжай_орын, 파일서술자표 파일서술자) {
        this.идентификатор_мән = идентификатор_мән;
        this.басты_идентификатор = басты_идентификатор;
        this.мекенжай_орын = мекенжай_орын;
        this.파일서술자 = 파일서술자;
    }

    public int идентификатор_мән() {
        return идентификатор_мән;
    }

    public int басты_идентификатор() {
        return басты_идентификатор;
    }

    public бет_менеджер.мекенжай_орын мекенжай_орын() {
        return мекенжай_орын;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Процесс_күй күй_мән() {
        return күй_мән;
    }

    public void жинақ_күй(Процесс_күй 새상태) {
        күй_мән = 새상태;
    }

    public int Шығу_код() {
        return Шығу_код;
    }

    public void Шығу_бағдарлама(int мән) {
        Шығу_код = мән & 0xff;
        күй_мән = Процесс_күй.Шығу_бағдарлама;
    }

    public int бағдарлама_үзу() {
        return бағдарлама_үзу;
    }

    public void жинақ_бағдарлама_үзу(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("бағдарлама_f5044b9b 끝 범위를 벗어났습니다.");
        }
        бағдарлама_үзу = 새끝;
    }

    public void 실행문맥설정(int басы_мекенжай, String[] параметр_аргумент, String[] 환경) {
        실행시작주소 = басы_мекенжай;
        실행인자 = параметр_аргумент.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
