// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.서술자;

/** x86 작업 перехід_режим 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class справа_Стан_сегмент {
    private int Стіс_нуль_блок;
    private int Стіс_нуль_адреса;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int Адреса) {
        Стіс_нуль_блок = 조각;
        Стіс_нуль_адреса = Адреса;
    }

    public int Стіс_нуль_блок() { return Стіс_нуль_блок; }
    public int Стіс_нуль_адреса() { return Стіс_нуль_адреса; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

