// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.체계호출;

public final class 체계정보 {
    private final String سىستېما_نامى;
    private final String تۈگۈن_نامى;
    private final String 배포판;
    private final String نەشىر_نومۇرى_قىممىتى;
    private final String ماشىنا;

    public 체계정보(String سىستېما_نامى, String تۈگۈن_نامى, String 배포판, String نەشىر_نومۇرى_قىممىتى, String ماشىنا) {
        this.سىستېما_نامى = سىستېما_نامى;
        this.تۈگۈن_نامى = تۈگۈن_نامى;
        this.배포판 = 배포판;
        this.نەشىر_نومۇرى_قىممىتى = نەشىر_نومۇرى_قىممىتى;
        this.ماشىنا = ماشىنا;
    }

    public String سىستېما_نامى() { return سىستېما_نامى; }
    public String تۈگۈن_نامى() { return تۈگۈن_نامى; }
    public String 배포판() { return 배포판; }
    public String نەشىر_نومۇرى_قىممىتى() { return نەشىر_نومۇرى_قىممىتى; }
    public String ماشىنا() { return ماشىنا; }
}
