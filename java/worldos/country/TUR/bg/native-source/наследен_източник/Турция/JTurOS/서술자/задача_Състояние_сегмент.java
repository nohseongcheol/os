// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.서술자;

/** x86 작업 комутатор_режим 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class задача_Състояние_сегмент {
    private int стек_нула_блок;
    private int стек_нула_адрес;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int адрес) {
        стек_нула_блок = 조각;
        стек_нула_адрес = адрес;
    }

    public int стек_нула_блок() { return стек_нула_блок; }
    public int стек_нула_адрес() { return стек_нула_адрес; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

