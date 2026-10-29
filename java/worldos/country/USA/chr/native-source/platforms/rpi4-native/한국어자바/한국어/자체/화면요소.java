// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ. */
public final class 화면요소 {
    private 화면요소() {}
    public static void 나중에실행(실행할일 ᏯᏛᏁᏗ_ᎠᏛᏁᎵᏓ) { ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ_ᎠᏍᏓᏅᏅ.나중에실행(ᏯᏛᏁᏗ_ᎠᏛᏁᎵᏓ); }
    public static ᏗᎦᏯᎸᏗ ᎦᏗ_ᏧᎬᏩᎶᏗᏯ(String ᎠᎪᎵᏰᏗ, int 가로, int 세로, int 폭, int 높이) {
        return new ᏗᎦᏯᎸᏗ(ᎠᎪᎵᏰᏗ, 가로, 세로, 폭, 높이);
    }
    public static ᎠᏐᏅᏍᏙᏗ ᎠᏐᏅᏍᏙᏗ(String ᎠᎪᎵᏰᏗ, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new ᎠᏐᏅᏍᏙᏗ(ᎠᎪᎵᏰᏗ, 가로, 세로, 폭, 높이, 받이);
    }
    public static ᎠᎪᎵᏰᏗ_ᏠᎨᏏ ᎠᎪᎵᏰᏗ_ᏠᎨᏏ(String ᎠᎪᎵᏰᏗ, int 가로, int 세로, int 폭, int 높이) {
        return new ᎠᎪᎵᏰᏗ_ᏠᎨᏏ(ᎠᎪᎵᏰᏗ, 가로, 세로, 폭, 높이);
    }
}
