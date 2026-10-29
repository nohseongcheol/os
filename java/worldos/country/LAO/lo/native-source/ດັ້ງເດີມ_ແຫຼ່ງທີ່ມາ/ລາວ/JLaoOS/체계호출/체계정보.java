// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.체계호출;

public final class 체계정보 {
    private final String ລະບົບ_ຊື່;
    private final String ຈອມ_ຊື່;
    private final String 배포판;
    private final String 판;
    private final String ເຄື່ອງຈັກ;

    public 체계정보(String ລະບົບ_ຊື່, String ຈອມ_ຊື່, String 배포판, String 판, String ເຄື່ອງຈັກ) {
        this.ລະບົບ_ຊື່ = ລະບົບ_ຊື່;
        this.ຈອມ_ຊື່ = ຈອມ_ຊື່;
        this.배포판 = 배포판;
        this.판 = 판;
        this.ເຄື່ອງຈັກ = ເຄື່ອງຈັກ;
    }

    public String ລະບົບ_ຊື່() { return ລະບົບ_ຊື່; }
    public String ຈອມ_ຊື່() { return ຈອມ_ຊື່; }
    public String 배포판() { return 배포판; }
    public String 판() { return 판; }
    public String ເຄື່ອງຈັກ() { return ເຄື່ອງຈັກ; }
}
