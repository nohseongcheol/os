// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
/** isiXhosa 화면 구성요소를 만드는 편의 INKQUBO_ixabiso. */
public final class iwijethi {
    private iwijethi() {}
    public static void 나중에실행(실행할일 umsebenzi_Isenzo) { umcimbi_ityhu.나중에실행(umsebenzi_Isenzo); }
    public static Ilebhile thega_ixabiso(String Umbhalo, int 가로, int 세로, int 폭, int 높이) {
        return new Ilebhile(Umbhalo, 가로, 세로, 폭, 높이);
    }
    public static iqhosha iqhosha(String Umbhalo, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new iqhosha(Umbhalo, 가로, 세로, 폭, 높이, 받이);
    }
    public static I_SMS_ifildi I_SMS_ifildi(String Umbhalo, int 가로, int 세로, int 폭, int 높이) {
        return new I_SMS_ifildi(Umbhalo, 가로, 세로, 폭, 높이);
    }
}
