// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.дескриптор_ввод;

/** x86 작업 перейти_МОДА 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class дело_Состояние_сегмент {
    private int стек_нуль_блок;
    private int стек_нуль_АДРЕС;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int блок_ЗНАЧЕН_652d4b53, int АДРЕС) {
        стек_нуль_блок = блок_ЗНАЧЕН_652d4b53;
        стек_нуль_АДРЕС = АДРЕС;
    }

    public int стек_нуль_блок() { return стек_нуль_блок; }
    public int стек_нуль_АДРЕС() { return стек_нуль_АДРЕС; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

