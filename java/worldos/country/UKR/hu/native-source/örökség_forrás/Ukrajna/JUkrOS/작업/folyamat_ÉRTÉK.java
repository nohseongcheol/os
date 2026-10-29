// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukrajna.JUkrOS.작업;

import Ukrajna.JUkrOS.Memória_régió.lap_kezelő;
import Ukrajna.JUkrOS.fájlrendszer.파일서술자표;

public final class folyamat_ÉRTÉK {
    private final int azonosító_ÉRTÉK;
    private final int szülő_azonosító;
    private final lap_kezelő.címtartomány címtartomány;
    private final 파일서술자표 파일서술자;
    private folyamat_Állapot Állapot_ÉRTÉK = folyamat_Állapot.Előkészítés;
    private int kilép_KÓD;
    private int app_szünet = 0x06000000;
    private int végrehajtás_START_CÍM;
    private String[] végrehajtás_argumentum = new String[0];
    private String[] környezet_ÉRTÉK_60cdc2a6 = new String[0];

    folyamat_ÉRTÉK(int azonosító_ÉRTÉK, int szülő_azonosító, lap_kezelő.címtartomány címtartomány, 파일서술자표 파일서술자) {
        this.azonosító_ÉRTÉK = azonosító_ÉRTÉK;
        this.szülő_azonosító = szülő_azonosító;
        this.címtartomány = címtartomány;
        this.파일서술자 = 파일서술자;
    }

    public int azonosító_ÉRTÉK() {
        return azonosító_ÉRTÉK;
    }

    public int szülő_azonosító() {
        return szülő_azonosító;
    }

    public lap_kezelő.címtartomány címtartomány() {
        return címtartomány;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public folyamat_Állapot Állapot_ÉRTÉK() {
        return Állapot_ÉRTÉK;
    }

    public void halmaz_Állapot(folyamat_Állapot 새상태) {
        Állapot_ÉRTÉK = 새상태;
    }

    public int kilép_KÓD() {
        return kilép_KÓD;
    }

    public void kilép_app(int ÉRTÉK) {
        kilép_KÓD = ÉRTÉK & 0xff;
        Állapot_ÉRTÉK = folyamat_Állapot.kilép_app;
    }

    public int app_szünet() {
        return app_szünet;
    }

    public void halmaz_app_szünet(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_szünet = 새끝;
    }

    public void halmaz_végrehajtás_környezet(int START_CÍM, String[] paraméter_argumentum, String[] környezet_5d36e09c) {
        végrehajtás_START_CÍM = START_CÍM;
        végrehajtás_argumentum = paraméter_argumentum.clone();
        környezet_ÉRTÉK_60cdc2a6 = környezet_5d36e09c.clone();
    }

    public int végrehajtás_START_CÍM() { return végrehajtás_START_CÍM; }
    public String[] végrehajtás_argumentum() { return végrehajtás_argumentum.clone(); }
    public String[] környezet_ÉRTÉK_60cdc2a6() { return környezet_ÉRTÉK_60cdc2a6.clone(); }
}
