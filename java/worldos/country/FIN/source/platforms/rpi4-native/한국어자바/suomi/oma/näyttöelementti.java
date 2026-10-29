// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** suomi 화면 구성요소를 만드는 편의 funktio_ARVO. */
public final class näyttöelementti {
    private näyttöelementti() {}
    public static void 나중에실행(실행할일 tehtävä_toimi) { tapahtuma_jono.나중에실행(tehtävä_toimi); }
    public static Nimike tunnus_ARVO(String teksti, int 가로, int toimiala_toimi, int 폭, int 높이) {
        return new Nimike(teksti, 가로, toimiala_toimi, 폭, 높이);
    }
    public static painike painike(String teksti, int 가로, int toimiala_toimi, int 폭, int 높이, 동작받이 받이) {
        return new painike(teksti, 가로, toimiala_toimi, 폭, 높이, 받이);
    }
    public static tekstikenttä tekstikenttä(String teksti, int 가로, int toimiala_toimi, int 폭, int 높이) {
        return new tekstikenttä(teksti, 가로, toimiala_toimi, 폭, 높이);
    }
}
