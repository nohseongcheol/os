// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.서술자;

/** x86 작업 byta_läge 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class uppgift_status_segment {
    private int Stack_noll_block;
    private int Stack_noll_ADRESS;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int Adress) {
        Stack_noll_block = 조각;
        Stack_noll_ADRESS = Adress;
    }

    public int Stack_noll_block() { return Stack_noll_block; }
    public int Stack_noll_ADRESS() { return Stack_noll_ADRESS; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

