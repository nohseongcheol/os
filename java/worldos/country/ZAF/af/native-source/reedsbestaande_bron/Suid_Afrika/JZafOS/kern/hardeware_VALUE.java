// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.kern;

/** Java 관리 커널과 CPU UNIQUE_VALUE CODE_VALUE 사이의 유일한 경계다. */
public interface hardeware_VALUE {
    void 직렬출력(String Inhoud_VALUE);

    int 포트바이트읽기(int 포트번호);

    void skryf_ombou_greep(int 포트번호, int VALUE);

    void 중앙처리장치멈춤();
}

