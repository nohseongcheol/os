// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Duitsland.JDeuOS.Kern;

/** Java 관리 커널과 CPU UNIEK_WAARDE CODE_WAARDE 사이의 유일한 경계다. */
public interface hardware_WAARDE {
    void 직렬출력(String Inhoud_WAARDE);

    int 포트바이트읽기(int hardware_poortnummer);

    void schrijven_poort_byte(int hardware_poortnummer, int WAARDE);

    void 중앙처리장치멈춤();
}

