// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.작업;

import Y_Deyrnas_Unedig.JGbrOS.기억공간.tudalen_rheolwr;
import Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau.파일서술자표;

public final class Proses_VALUE {
    private final int dynodwr_VALUE;
    private final int 부모식별자;
    private final tudalen_rheolwr.ADDRESS_lle ADDRESS_lle;
    private final 파일서술자표 파일서술자;
    private Proses_cyflwr cyflwr_VALUE = Proses_cyflwr.Paratoi;
    private int gadael_cod;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proses_VALUE(int dynodwr_VALUE, int 부모식별자, tudalen_rheolwr.ADDRESS_lle ADDRESS_lle, 파일서술자표 파일서술자) {
        this.dynodwr_VALUE = dynodwr_VALUE;
        this.부모식별자 = 부모식별자;
        this.ADDRESS_lle = ADDRESS_lle;
        this.파일서술자 = 파일서술자;
    }

    public int dynodwr_VALUE() {
        return dynodwr_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public tudalen_rheolwr.ADDRESS_lle ADDRESS_lle() {
        return ADDRESS_lle;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proses_cyflwr cyflwr_VALUE() {
        return cyflwr_VALUE;
    }

    public void set_cyflwr(Proses_cyflwr 새상태) {
        cyflwr_VALUE = 새상태;
    }

    public int gadael_cod() {
        return gadael_cod;
    }

    public void gadael_Rhaglen(int VALUE) {
        gadael_cod = VALUE & 0xff;
        cyflwr_VALUE = Proses_cyflwr.gadael_Rhaglen;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("Rhaglen_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int cyfeiriad_cychwyn, String[] paramedr_arg, String[] 환경) {
        실행시작주소 = cyfeiriad_cychwyn;
        실행인자 = paramedr_arg.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
