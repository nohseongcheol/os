// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.작업;

import భారతదేశం.JIndOS.기억공간.పుట_కార్యనిర్వాహి;
import భారతదేశం.JIndOS.ఫైల్_వ్యవస్థ.파일서술자표;

public final class విధానం_మూల్యం {
    private final int ఐడెంటిఫయర్_మూల్యం;
    private final int 부모식별자;
    private final పుట_కార్యనిర్వాహి.ఇమెయిల్_ఖాళీ ఇమెయిల్_ఖాళీ;
    private final 파일서술자표 파일서술자;
    private విధానం_స్థితి స్థితి_మూల్యం = విధానం_స్థితి.సిద్ధం_చేయు;
    private int నిష్క్రమణ_కోడ్;
    private int అనువర్తనం_విరామం = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    విధానం_మూల్యం(int ఐడెంటిఫయర్_మూల్యం, int 부모식별자, పుట_కార్యనిర్వాహి.ఇమెయిల్_ఖాళీ ఇమెయిల్_ఖాళీ, 파일서술자표 파일서술자) {
        this.ఐడెంటిఫయర్_మూల్యం = ఐడెంటిఫయర్_మూల్యం;
        this.부모식별자 = 부모식별자;
        this.ఇమెయిల్_ఖాళీ = ఇమెయిల్_ఖాళీ;
        this.파일서술자 = 파일서술자;
    }

    public int ఐడెంటిఫయర్_మూల్యం() {
        return ఐడెంటిఫయర్_మూల్యం;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public పుట_కార్యనిర్వాహి.ఇమెయిల్_ఖాళీ ఇమెయిల్_ఖాళీ() {
        return ఇమెయిల్_ఖాళీ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public విధానం_స్థితి స్థితి_మూల్యం() {
        return స్థితి_మూల్యం;
    }

    public void సెట్_స్థితి(విధానం_స్థితి 새상태) {
        స్థితి_మూల్యం = 새상태;
    }

    public int నిష్క్రమణ_కోడ్() {
        return నిష్క్రమణ_కోడ్;
    }

    public void నిష్క్రమణ_అనువర్తనం(int మూల్యం) {
        నిష్క్రమణ_కోడ్ = మూల్యం & 0xff;
        స్థితి_మూల్యం = విధానం_స్థితి.నిష్క్రమణ_అనువర్తనం;
    }

    public int అనువర్తనం_విరామం() {
        return అనువర్తనం_విరామం;
    }

    public void సెట్_అనువర్తనం_విరామం(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("అనువర్తనం_f5044b9b 끝 범위를 벗어났습니다.");
        }
        అనువర్తనం_విరామం = 새끝;
    }

    public void 실행문맥설정(int ప్రారంభం_ఇమెయిల్, String[] పారామీటర్_కారకం, String[] 환경) {
        실행시작주소 = ప్రారంభం_ఇమెయిల్;
        실행인자 = పారామీటర్_కారకం.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
