// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Island.JIslOS.작업;

import Island.JIslOS.Hukommelse_område.Sidestyring;
import Island.JIslOS.filsystem.파일서술자표;

public final class Proces_VÆRDI {
    private final int identifikator_VÆRDI;
    private final int overordnet_identifikator;
    private final Sidestyring.adresseinterval adresseinterval;
    private final 파일서술자표 파일서술자;
    private Proces_status status_VÆRDI = Proces_status.Tilrettelæg;
    private int Afslut_KODE;
    private int app_pause = 0x06000000;
    private int udførelse_START_mail;
    private String[] udførelse_argument = new String[0];
    private String[] miljø_VÆRDI = new String[0];

    Proces_VÆRDI(int identifikator_VÆRDI, int overordnet_identifikator, Sidestyring.adresseinterval adresseinterval, 파일서술자표 파일서술자) {
        this.identifikator_VÆRDI = identifikator_VÆRDI;
        this.overordnet_identifikator = overordnet_identifikator;
        this.adresseinterval = adresseinterval;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VÆRDI() {
        return identifikator_VÆRDI;
    }

    public int overordnet_identifikator() {
        return overordnet_identifikator;
    }

    public Sidestyring.adresseinterval adresseinterval() {
        return adresseinterval;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_status status_VÆRDI() {
        return status_VÆRDI;
    }

    public void sæt_status(Proces_status 새상태) {
        status_VÆRDI = 새상태;
    }

    public int Afslut_KODE() {
        return Afslut_KODE;
    }

    public void Afslut_app(int VÆRDI) {
        Afslut_KODE = VÆRDI & 0xff;
        status_VÆRDI = Proces_status.Afslut_app;
    }

    public int app_pause() {
        return app_pause;
    }

    public void sæt_app_pause(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_pause = 새끝;
    }

    public void sæt_udførelse_kontekst(int START_mail, String[] parameter_argument, String[] miljø) {
        udførelse_START_mail = START_mail;
        udførelse_argument = parameter_argument.clone();
        miljø_VÆRDI = miljø.clone();
    }

    public int udførelse_START_mail() { return udførelse_START_mail; }
    public String[] udførelse_argument() { return udførelse_argument.clone(); }
    public String[] miljø_VÆRDI() { return miljø_VÆRDI.clone(); }
}
