// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Estados_Unidos.JUsaOS.작업;

import Estados_Unidos.JUsaOS.기억공간.page_tagapamahala;
import Estados_Unidos.JUsaOS.sistema_ng_file.파일서술자표;

public final class Proseso_VALUE {
    private final int tagakilala_VALUE;
    private final int 부모식별자;
    private final page_tagapamahala.email_SPACE email_SPACE;
    private final 파일서술자표 파일서술자;
    private Proseso_katayuan katayuan_VALUE = Proseso_katayuan.Ihanda;
    private int Paglabas_CODE;
    private int app_break = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proseso_VALUE(int tagakilala_VALUE, int 부모식별자, page_tagapamahala.email_SPACE email_SPACE, 파일서술자표 파일서술자) {
        this.tagakilala_VALUE = tagakilala_VALUE;
        this.부모식별자 = 부모식별자;
        this.email_SPACE = email_SPACE;
        this.파일서술자 = 파일서술자;
    }

    public int tagakilala_VALUE() {
        return tagakilala_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public page_tagapamahala.email_SPACE email_SPACE() {
        return email_SPACE;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proseso_katayuan katayuan_VALUE() {
        return katayuan_VALUE;
    }

    public void set_katayuan(Proseso_katayuan 새상태) {
        katayuan_VALUE = 새상태;
    }

    public int Paglabas_CODE() {
        return Paglabas_CODE;
    }

    public void Paglabas_app(int VALUE) {
        Paglabas_CODE = VALUE & 0xff;
        katayuan_VALUE = Proseso_katayuan.Paglabas_app;
    }

    public int app_break() {
        return app_break;
    }

    public void set_app_break(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_break = 새끝;
    }

    public void 실행문맥설정(int Start_email, String[] parameter_argumento, String[] 환경) {
        실행시작주소 = Start_email;
        실행인자 = parameter_argumento.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
