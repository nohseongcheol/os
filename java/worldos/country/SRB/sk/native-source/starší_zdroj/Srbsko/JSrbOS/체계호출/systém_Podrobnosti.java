// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbsko.JSrbOS.체계호출;

public final class systém_Podrobnosti {
    private final String systém_názov;
    private final String uzol_názov;
    private final String vydanie_VALUE;
    private final String verzia_VALUE;
    private final String počítač_5eb260fa;

    public systém_Podrobnosti(String systém_názov, String uzol_názov, String vydanie_VALUE, String verzia_VALUE, String počítač_5eb260fa) {
        this.systém_názov = systém_názov;
        this.uzol_názov = uzol_názov;
        this.vydanie_VALUE = vydanie_VALUE;
        this.verzia_VALUE = verzia_VALUE;
        this.počítač_5eb260fa = počítač_5eb260fa;
    }

    public String systém_názov() { return systém_názov; }
    public String uzol_názov() { return uzol_názov; }
    public String vydanie_VALUE() { return vydanie_VALUE; }
    public String verzia_VALUE() { return verzia_VALUE; }
    public String počítač_5eb260fa() { return počítač_5eb260fa; }
}
