// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.서술자;

/** x86 작업 bytt_MODUS 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class oppgave_status_segment {
    private int stakk_null_blokk;
    private int stakk_null_e_post;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int e_post) {
        stakk_null_blokk = 조각;
        stakk_null_e_post = e_post;
    }

    public int stakk_null_blokk() { return stakk_null_blokk; }
    public int stakk_null_e_post() { return stakk_null_e_post; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

