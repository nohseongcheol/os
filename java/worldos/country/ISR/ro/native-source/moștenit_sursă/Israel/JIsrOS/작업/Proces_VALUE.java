// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Israel.JIsrOS.작업;

import Israel.JIsrOS.Memorie_regiune.쪽관리자;
import Israel.JIsrOS.sistem_de_fișiere.파일서술자표;

public final class Proces_VALUE {
    private final int identificator_VALUE;
    private final int părinte_identificator;
    private final 쪽관리자.adresa_SPAȚIU adresa_SPAȚIU;
    private final 파일서술자표 파일서술자;
    private Proces_Stare Stare_VALUE = Proces_Stare.Pregătiți;
    private int ieși_cod;
    private int program_pauză = 0x06000000;
    private int executare_buta_adresa;
    private String[] executare_argument = new String[0];
    private String[] 환경값 = new String[0];

    Proces_VALUE(int identificator_VALUE, int părinte_identificator, 쪽관리자.adresa_SPAȚIU adresa_SPAȚIU, 파일서술자표 파일서술자) {
        this.identificator_VALUE = identificator_VALUE;
        this.părinte_identificator = părinte_identificator;
        this.adresa_SPAȚIU = adresa_SPAȚIU;
        this.파일서술자 = 파일서술자;
    }

    public int identificator_VALUE() {
        return identificator_VALUE;
    }

    public int părinte_identificator() {
        return părinte_identificator;
    }

    public 쪽관리자.adresa_SPAȚIU adresa_SPAȚIU() {
        return adresa_SPAȚIU;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_Stare Stare_VALUE() {
        return Stare_VALUE;
    }

    public void set_Stare(Proces_Stare 새상태) {
        Stare_VALUE = 새상태;
    }

    public int ieși_cod() {
        return ieși_cod;
    }

    public void ieși_program(int VALUE) {
        ieși_cod = VALUE & 0xff;
        Stare_VALUE = Proces_Stare.ieși_program;
    }

    public int program_pauză() {
        return program_pauză;
    }

    public void set_program_pauză(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        program_pauză = 새끝;
    }

    public void set_executare_context(int buta_adresa, String[] parametru_argument, String[] 환경) {
        executare_buta_adresa = buta_adresa;
        executare_argument = parametru_argument.clone();
        환경값 = 환경.clone();
    }

    public int executare_buta_adresa() { return executare_buta_adresa; }
    public String[] executare_argument() { return executare_argument.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
