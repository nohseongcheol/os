// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.ፍረ;

/** Java 관리 커널과 CPU 고유 코드 사이의 유일한 경계다. */
public interface ሃርድዌር_ዋጋ {
    void 직렬출력(String ትሕዝቶ_ዋጋ);

    int 포트바이트읽기(int 포트번호);

    void ጸሓፍ_ወደብ_ባይት(int 포트번호, int ዋጋ);

    void 중앙처리장치멈춤();
}

