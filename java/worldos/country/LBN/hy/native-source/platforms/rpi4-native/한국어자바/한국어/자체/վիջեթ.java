// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 ՖՈՒՆԿՑԻԱ_արժեք. */
public final class վիջեթ {
    private վիջեթ() {}
    public static void 나중에실행(실행할일 խնդիր_գործողություն) { միջոցառում_հերթ.나중에실행(խնդիր_գործողություն); }
    public static Պիտակ պիտակ_արժեք(String Տեքստ, int 가로, int Ուղղահայաց_դիրք, int 폭, int 높이) {
        return new Պիտակ(Տեքստ, 가로, Ուղղահայաց_դիրք, 폭, 높이);
    }
    public static կոճակ կոճակ(String Տեքստ, int 가로, int Ուղղահայաց_դիրք, int 폭, int 높이, 동작받이 받이) {
        return new կոճակ(Տեքստ, 가로, Ուղղահայաց_դիրք, 폭, 높이, 받이);
    }
    public static գրվածքի_դաշտ գրվածքի_դաշտ(String Տեքստ, int 가로, int Ուղղահայաց_դիրք, int 폭, int 높이) {
        return new գրվածքի_դաշտ(Տեքստ, 가로, Ուղղահայաց_դիրք, 폭, 높이);
    }
}
