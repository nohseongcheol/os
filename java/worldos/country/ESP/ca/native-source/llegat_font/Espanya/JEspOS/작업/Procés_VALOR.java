// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.작업;

import Espanya.JEspOS.기억공간.pàgina_administrador;
import Espanya.JEspOS.sistema_d_arxius.파일서술자표;

public final class Procés_VALOR {
    private final int identificador_VALOR;
    private final int 부모식별자;
    private final pàgina_administrador.ADREÇA_espai ADREÇA_espai;
    private final 파일서술자표 파일서술자;
    private Procés_Estat Estat_VALOR = Procés_Estat.Prepara;
    private int Surt_CODI;
    private int programa_pausa = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] entorn_VALOR = new String[0];

    Procés_VALOR(int identificador_VALOR, int 부모식별자, pàgina_administrador.ADREÇA_espai ADREÇA_espai, 파일서술자표 파일서술자) {
        this.identificador_VALOR = identificador_VALOR;
        this.부모식별자 = 부모식별자;
        this.ADREÇA_espai = ADREÇA_espai;
        this.파일서술자 = 파일서술자;
    }

    public int identificador_VALOR() {
        return identificador_VALOR;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public pàgina_administrador.ADREÇA_espai ADREÇA_espai() {
        return ADREÇA_espai;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Procés_Estat Estat_VALOR() {
        return Estat_VALOR;
    }

    public void conjunt_Estat(Procés_Estat 새상태) {
        Estat_VALOR = 새상태;
    }

    public int Surt_CODI() {
        return Surt_CODI;
    }

    public void Surt_programa(int VALOR) {
        Surt_CODI = VALOR & 0xff;
        Estat_VALOR = Procés_Estat.Surt_programa;
    }

    public int programa_pausa() {
        return programa_pausa;
    }

    public void conjunt_programa_pausa(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programa_f5044b9b 끝 범위를 벗어났습니다.");
        }
        programa_pausa = 새끝;
    }

    public void 실행문맥설정(int Inici_ADREÇA, String[] paràmetre_arg, String[] entorn) {
        실행시작주소 = Inici_ADREÇA;
        실행인자 = paràmetre_arg.clone();
        entorn_VALOR = entorn.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] entorn_VALOR() { return entorn_VALOR.clone(); }
}
