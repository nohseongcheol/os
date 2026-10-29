// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.kärna;

/** Java 관리 커널과 CPU UNIK_värde KOD_värde 사이의 유일한 경계다. */
public interface maskinvara_värde {
    void 직렬출력(String Innehåll_värde);

    int läsa_port_byte(int maskinvara_portnummer);

    void skriva_port_byte(int maskinvara_portnummer, int värde);

    void 중앙처리장치멈춤();
}

