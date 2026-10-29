// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Macau_SAR_China.JMacOS.체계호출;

public final class 체계정보 {
    private final String system_pangalan;
    private final String node_pangalan;
    private final String 배포판;
    private final String bersyon_VALUE;
    private final String machine;

    public 체계정보(String system_pangalan, String node_pangalan, String 배포판, String bersyon_VALUE, String machine) {
        this.system_pangalan = system_pangalan;
        this.node_pangalan = node_pangalan;
        this.배포판 = 배포판;
        this.bersyon_VALUE = bersyon_VALUE;
        this.machine = machine;
    }

    public String system_pangalan() { return system_pangalan; }
    public String node_pangalan() { return node_pangalan; }
    public String 배포판() { return 배포판; }
    public String bersyon_VALUE() { return bersyon_VALUE; }
    public String machine() { return machine; }
}
