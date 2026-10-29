// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.작업;

import Portugal.JPrtOS.기억공간.páxina_xefe;
import Portugal.JPrtOS.sistema_de_ficheiros.파일서술자표;

public final class Proceso_VALOR {
    private final int 식별자;
    private final int 부모식별자;
    private final páxina_xefe.ENDEREZO_espazo ENDEREZO_espazo;
    private final 파일서술자표 파일서술자;
    private Proceso_Estado Estado_VALOR = Proceso_Estado.준비;
    private int saír_CÓDIGO;
    private int apl_pausa = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proceso_VALOR(int 식별자, int 부모식별자, páxina_xefe.ENDEREZO_espazo ENDEREZO_espazo, 파일서술자표 파일서술자) {
        this.식별자 = 식별자;
        this.부모식별자 = 부모식별자;
        this.ENDEREZO_espazo = ENDEREZO_espazo;
        this.파일서술자 = 파일서술자;
    }

    public int 식별자() {
        return 식별자;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public páxina_xefe.ENDEREZO_espazo ENDEREZO_espazo() {
        return ENDEREZO_espazo;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proceso_Estado Estado_VALOR() {
        return Estado_VALOR;
    }

    public void conxunto_Estado(Proceso_Estado 새상태) {
        Estado_VALOR = 새상태;
    }

    public int saír_CÓDIGO() {
        return saír_CÓDIGO;
    }

    public void saír_apl(int VALOR) {
        saír_CÓDIGO = VALOR & 0xff;
        Estado_VALOR = Proceso_Estado.saír_apl;
    }

    public int apl_pausa() {
        return apl_pausa;
    }

    public void conxunto_apl_pausa(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("apl_f5044b9b 끝 범위를 벗어났습니다.");
        }
        apl_pausa = 새끝;
    }

    public void 실행문맥설정(int START_ENDEREZO, String[] parámetro_argumento, String[] 환경) {
        실행시작주소 = START_ENDEREZO;
        실행인자 = parámetro_argumento.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
