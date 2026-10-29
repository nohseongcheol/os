// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.체계호출;

public final class 체계정보 {
    private final String sistema_isem;
    private final String node_isem;
    private final String 배포판;
    private final String verżjoni_VALUE;
    private final String kompjuter;

    public 체계정보(String sistema_isem, String node_isem, String 배포판, String verżjoni_VALUE, String kompjuter) {
        this.sistema_isem = sistema_isem;
        this.node_isem = node_isem;
        this.배포판 = 배포판;
        this.verżjoni_VALUE = verżjoni_VALUE;
        this.kompjuter = kompjuter;
    }

    public String sistema_isem() { return sistema_isem; }
    public String node_isem() { return node_isem; }
    public String 배포판() { return 배포판; }
    public String verżjoni_VALUE() { return verżjoni_VALUE; }
    public String kompjuter() { return kompjuter; }
}
