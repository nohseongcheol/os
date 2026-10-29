// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.작업;

import Naịjịrịa.JNgaOS.기억공간.ihuakwụkwọ_njikwa;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.파일서술자표;

public final class ùsòrò_valuu_6712bde7 {
    private final int ihe_nkọwapụta_valuu;
    private final int 부모식별자;
    private final ihuakwụkwọ_njikwa.àdreèsì_ohere àdreèsì_ohere;
    private final 파일서술자표 파일서술자;
    private ùsòrò_ọnọdụ ọnọdụ_valuu = ùsòrò_ọnọdụ.Kwado;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ùsòrò_valuu_6712bde7(int ihe_nkọwapụta_valuu, int 부모식별자, ihuakwụkwọ_njikwa.àdreèsì_ohere àdreèsì_ohere, 파일서술자표 파일서술자) {
        this.ihe_nkọwapụta_valuu = ihe_nkọwapụta_valuu;
        this.부모식별자 = 부모식별자;
        this.àdreèsì_ohere = àdreèsì_ohere;
        this.파일서술자 = 파일서술자;
    }

    public int ihe_nkọwapụta_valuu() {
        return ihe_nkọwapụta_valuu;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ihuakwụkwọ_njikwa.àdreèsì_ohere àdreèsì_ohere() {
        return àdreèsì_ohere;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ùsòrò_ọnọdụ ọnọdụ_valuu() {
        return ọnọdụ_valuu;
    }

    public void Seti_ọnọdụ(ùsòrò_ọnọdụ 새상태) {
        ọnọdụ_valuu = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void pụọ_app(int valuu) {
        종료값 = valuu & 0xff;
        ọnọdụ_valuu = ùsòrò_ọnọdụ.pụọ_app;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Mbido_àdreèsì, String[] 인자, String[] 환경) {
        실행시작주소 = Mbido_àdreèsì;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
