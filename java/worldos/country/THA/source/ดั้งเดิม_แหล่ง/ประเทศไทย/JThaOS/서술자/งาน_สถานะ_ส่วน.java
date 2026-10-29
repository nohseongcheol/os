// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.서술자;

/** x86 작업 สลับ_โหมด 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class งาน_สถานะ_ส่วน {
    private int สแตก_ศูนย์_บล็อก;
    private int สแตก_ศูนย์_อีเมล;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int อีเมล) {
        สแตก_ศูนย์_บล็อก = 조각;
        สแตก_ศูนย์_อีเมล = อีเมล;
    }

    public int สแตก_ศูนย์_บล็อก() { return สแตก_ศูนย์_บล็อก; }
    public int สแตก_ศูนย์_อีเมล() { return สแตก_ศูนย์_อีเมล; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

