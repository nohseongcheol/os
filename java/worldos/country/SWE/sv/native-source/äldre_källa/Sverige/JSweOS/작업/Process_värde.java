// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.작업;

import Sverige.JSweOS.Minne_område.Sidhanteraren;
import Sverige.JSweOS.filsystem.파일서술자표;

public final class Process_värde {
    private final int identifierare_värde;
    private final int överordnad_identifierare;
    private final Sidhanteraren.adressutrymme adressutrymme;
    private final 파일서술자표 파일서술자;
    private Process_status status_värde = Process_status.Förbereda;
    private int slutkod;
    private int app_rast = 0x06000000;
    private int körning_START_ADRESS;
    private String[] körning_argument = new String[0];
    private String[] miljö_värde = new String[0];

    Process_värde(int identifierare_värde, int överordnad_identifierare, Sidhanteraren.adressutrymme adressutrymme, 파일서술자표 파일서술자) {
        this.identifierare_värde = identifierare_värde;
        this.överordnad_identifierare = överordnad_identifierare;
        this.adressutrymme = adressutrymme;
        this.파일서술자 = 파일서술자;
    }

    public int identifierare_värde() {
        return identifierare_värde;
    }

    public int överordnad_identifierare() {
        return överordnad_identifierare;
    }

    public Sidhanteraren.adressutrymme adressutrymme() {
        return adressutrymme;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Process_status status_värde() {
        return status_värde;
    }

    public void uppsättning_status(Process_status 새상태) {
        status_värde = 새상태;
    }

    public int slutkod() {
        return slutkod;
    }

    public void Utgång_app(int värde) {
        slutkod = värde & 0xff;
        status_värde = Process_status.Utgång_app;
    }

    public int app_rast() {
        return app_rast;
    }

    public void uppsättning_app_rast(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_rast = 새끝;
    }

    public void uppsättning_körning_sammanhang(int START_ADRESS, String[] parameter_argument, String[] miljö) {
        körning_START_ADRESS = START_ADRESS;
        körning_argument = parameter_argument.clone();
        miljö_värde = miljö.clone();
    }

    public int körning_START_ADRESS() { return körning_START_ADRESS; }
    public String[] körning_argument() { return körning_argument.clone(); }
    public String[] miljö_värde() { return miljö_värde.clone(); }
}
