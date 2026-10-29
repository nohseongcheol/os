// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NLD.JNldOS.호스트;

import NLD.JNldOS.핵심.핵심;

public final class 호스트시작 {
    private 호스트시작() {
    }

    public static void main(String[] 인자) {
        핵심 커널 = new 핵심(new 호스트하드웨어());
        커널.Oetveure();
        커널.한단계실행();
    }
}

