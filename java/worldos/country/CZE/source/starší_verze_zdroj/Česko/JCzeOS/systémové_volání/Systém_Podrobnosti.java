// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.systémové_volání;

public final class Systém_Podrobnosti {
    private final String Systém_název;
    private final String uzel_název;
    private final String edice_HODNOTA;
    private final String verze_HODNOTA;
    private final String počítač;

    public Systém_Podrobnosti(String Systém_název, String uzel_název, String edice_HODNOTA, String verze_HODNOTA, String počítač) {
        this.Systém_název = Systém_název;
        this.uzel_název = uzel_název;
        this.edice_HODNOTA = edice_HODNOTA;
        this.verze_HODNOTA = verze_HODNOTA;
        this.počítač = počítač;
    }

    public String Systém_název() { return Systém_název; }
    public String uzel_název() { return uzel_název; }
    public String edice_HODNOTA() { return edice_HODNOTA; }
    public String verze_HODNOTA() { return verze_HODNOTA; }
    public String počítač() { return počítač; }
}
