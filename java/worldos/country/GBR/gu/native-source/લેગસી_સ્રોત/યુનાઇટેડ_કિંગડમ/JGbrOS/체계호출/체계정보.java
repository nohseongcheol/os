// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package યુનાઇટેડ_કિંગડમ.JGbrOS.체계호출;

public final class 체계정보 {
    private final String સિસ્ટમ_નામ;
    private final String નોડ_નામ;
    private final String 배포판;
    private final String વર્ઝન_મૂલ્ય;
    private final String મશીન;

    public 체계정보(String સિસ્ટમ_નામ, String નોડ_નામ, String 배포판, String વર્ઝન_મૂલ્ય, String મશીન) {
        this.સિસ્ટમ_નામ = સિસ્ટમ_નામ;
        this.નોડ_નામ = નોડ_નામ;
        this.배포판 = 배포판;
        this.વર્ઝન_મૂલ્ય = વર્ઝન_મૂલ્ય;
        this.મશીન = મશીન;
    }

    public String સિસ્ટમ_નામ() { return સિસ્ટમ_નામ; }
    public String નોડ_નામ() { return નોડ_નામ; }
    public String 배포판() { return 배포판; }
    public String વર્ઝન_મૂલ્ય() { return વર્ઝન_મૂલ્ય; }
    public String મશીન() { return મશીન; }
}
