// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.କେନ୍ଦ୍ରିକ;

/** Java 관리 커널과 CPU 고유 코드 사이의 유일한 경계다. */
public interface ହାର୍ଡୱେର୍_ମୂଲ୍ୟ {
    void 직렬출력(String ବିଷୟ_ମୂଲ୍ୟ);

    int 포트바이트읽기(int ହାର୍ଡୱେର୍_ପୋର୍ଟ୍_ନମ୍ଵର୍);

    void ଲିଖନ_ପୋର୍ଟ_ବାଇଟ୍(int ହାର୍ଡୱେର୍_ପୋର୍ଟ୍_ନମ୍ଵର୍, int ମୂଲ୍ୟ);

    void 중앙처리장치멈춤();
}

