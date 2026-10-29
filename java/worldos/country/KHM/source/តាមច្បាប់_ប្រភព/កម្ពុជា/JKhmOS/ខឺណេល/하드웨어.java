// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ខឺណេល;

/** Java 관리 커널과 CPU 고유 កូដ_តំលៃ 사이의 유일한 경계다. */
public interface 하드웨어 {
    void 직렬출력(String មាតិកា_តំលៃ);

    int 포트바이트읽기(int 포트번호);

    void សរសេរ_ច្រក_បៃ(int 포트번호, int តំលៃ);

    void 중앙처리장치멈춤();
}

