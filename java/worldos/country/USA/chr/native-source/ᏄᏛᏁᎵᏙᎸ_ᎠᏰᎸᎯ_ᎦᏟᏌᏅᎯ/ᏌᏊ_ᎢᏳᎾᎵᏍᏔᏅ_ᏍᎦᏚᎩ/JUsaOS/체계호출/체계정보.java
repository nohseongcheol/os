// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.체계호출;

public final class 체계정보 {
    private final String ᏄᏍᏗᏓᏅᎢ_ᏚᏙᎥᎢ;
    private final String ᏃᏗ_ᏚᏙᎥᎢ;
    private final String 배포판;
    private final String ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ;
    private final String 기계;

    public 체계정보(String ᏄᏍᏗᏓᏅᎢ_ᏚᏙᎥᎢ, String ᏃᏗ_ᏚᏙᎥᎢ, String 배포판, String ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ, String 기계) {
        this.ᏄᏍᏗᏓᏅᎢ_ᏚᏙᎥᎢ = ᏄᏍᏗᏓᏅᎢ_ᏚᏙᎥᎢ;
        this.ᏃᏗ_ᏚᏙᎥᎢ = ᏃᏗ_ᏚᏙᎥᎢ;
        this.배포판 = 배포판;
        this.ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ = ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ;
        this.기계 = 기계;
    }

    public String ᏄᏍᏗᏓᏅᎢ_ᏚᏙᎥᎢ() { return ᏄᏍᏗᏓᏅᎢ_ᏚᏙᎥᎢ; }
    public String ᏃᏗ_ᏚᏙᎥᎢ() { return ᏃᏗ_ᏚᏙᎥᎢ; }
    public String 배포판() { return 배포판; }
    public String ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ() { return ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ; }
    public String 기계() { return 기계; }
}
