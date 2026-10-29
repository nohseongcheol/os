// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** Lietuvių 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class valdiklis {
    private valdiklis() {}
    public static void 나중에실행(실행할일 užduotis_gavinys) { įvykis_eilė.나중에실행(užduotis_gavinys); }
    public static Pavadinimas žyma_VALUE(String Tekstas, int 가로, int segmentas_padėtis, int 폭, int 높이) {
        return new Pavadinimas(Tekstas, 가로, segmentas_padėtis, 폭, 높이);
    }
    public static mygtukas mygtukas(String Tekstas, int 가로, int segmentas_padėtis, int 폭, int 높이, 동작받이 받이) {
        return new mygtukas(Tekstas, 가로, segmentas_padėtis, 폭, 높이, 받이);
    }
    public static teksto_laukas teksto_laukas(String Tekstas, int 가로, int segmentas_padėtis, int 폭, int 높이) {
        return new teksto_laukas(Tekstas, 가로, segmentas_padėtis, 폭, 높이);
    }
}
