// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.체계호출;

public final class 체계정보 {
    private final String სისტემა_სახელი;
    private final String კვანძი_სახელი;
    private final String 배포판;
    private final String ვერსია_მნიშვნელობა;
    private final String კომპიუტერი;

    public 체계정보(String სისტემა_სახელი, String კვანძი_სახელი, String 배포판, String ვერსია_მნიშვნელობა, String კომპიუტერი) {
        this.სისტემა_სახელი = სისტემა_სახელი;
        this.კვანძი_სახელი = კვანძი_სახელი;
        this.배포판 = 배포판;
        this.ვერსია_მნიშვნელობა = ვერსია_მნიშვნელობა;
        this.კომპიუტერი = კომპიუტერი;
    }

    public String სისტემა_სახელი() { return სისტემა_სახელი; }
    public String კვანძი_სახელი() { return კვანძი_სახელი; }
    public String 배포판() { return 배포판; }
    public String ვერსია_მნიშვნელობა() { return ვერსია_მნიშვნელობა; }
    public String კომპიუტერი() { return კომპიუტერი; }
}
