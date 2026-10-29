// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.작업;

import Norge.JNorOS.Minne_område.Sidebehandling;
import Norge.JNorOS.filsystem.파일서술자표;

public final class Prosess_VERDI {
    private final int identifikator_VERDI;
    private final int overordnet_identifikator;
    private final Sidebehandling.adresseområde adresseområde;
    private final 파일서술자표 파일서술자;
    private Prosess_status status_VERDI = Prosess_status.Forbered;
    private int avslutningskode;
    private int app_pause = 0x06000000;
    private int kjøring_START_e_post;
    private String[] kjøring_argument = new String[0];
    private String[] miljø_VERDI = new String[0];

    Prosess_VERDI(int identifikator_VERDI, int overordnet_identifikator, Sidebehandling.adresseområde adresseområde, 파일서술자표 파일서술자) {
        this.identifikator_VERDI = identifikator_VERDI;
        this.overordnet_identifikator = overordnet_identifikator;
        this.adresseområde = adresseområde;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VERDI() {
        return identifikator_VERDI;
    }

    public int overordnet_identifikator() {
        return overordnet_identifikator;
    }

    public Sidebehandling.adresseområde adresseområde() {
        return adresseområde;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Prosess_status status_VERDI() {
        return status_VERDI;
    }

    public void sett_status(Prosess_status 새상태) {
        status_VERDI = 새상태;
    }

    public int avslutningskode() {
        return avslutningskode;
    }

    public void Utgang_app(int VERDI) {
        avslutningskode = VERDI & 0xff;
        status_VERDI = Prosess_status.Utgang_app;
    }

    public int app_pause() {
        return app_pause;
    }

    public void sett_app_pause(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_pause = 새끝;
    }

    public void sett_kjøring_kontekst(int START_e_post, String[] parameter_argument, String[] miljø) {
        kjøring_START_e_post = START_e_post;
        kjøring_argument = parameter_argument.clone();
        miljø_VERDI = miljø.clone();
    }

    public int kjøring_START_e_post() { return kjøring_START_e_post; }
    public String[] kjøring_argument() { return kjøring_argument.clone(); }
    public String[] miljø_VERDI() { return miljø_VERDI.clone(); }
}
