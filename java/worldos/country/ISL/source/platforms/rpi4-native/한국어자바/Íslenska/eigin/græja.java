// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** Íslenska 화면 구성요소를 만드는 편의 fall_VALUE. */
public final class græja {
    private græja() {}
    public static void 나중에실행(실행할일 verk_aðgerð) { atvik_biðröð.나중에실행(verk_aðgerð); }
    public static Skýring merki_VALUE(String Texti, int 가로, int Lóðrétt_staða, int 폭, int 높이) {
        return new Skýring(Texti, 가로, Lóðrétt_staða, 폭, 높이);
    }
    public static hnappur hnappur(String Texti, int 가로, int Lóðrétt_staða, int 폭, int 높이, 동작받이 받이) {
        return new hnappur(Texti, 가로, Lóðrétt_staða, 폭, 높이, 받이);
    }
    public static SMS_reitur SMS_reitur(String Texti, int 가로, int Lóðrétt_staða, int 폭, int 높이) {
        return new SMS_reitur(Texti, 가로, Lóðrétt_staða, 폭, 높이);
    }
}
