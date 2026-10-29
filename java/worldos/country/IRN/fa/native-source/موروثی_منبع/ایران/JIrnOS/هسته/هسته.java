// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ایران.JIrnOS.هسته;

import ایران.JIrnOS.기억공간.حافظه_مدیر;
import ایران.JIrnOS.기억공간.صفحه_مدیر;
import ایران.JIrnOS.입력.입력관리자;
import ایران.JIrnOS.작업.فرآیند_مقدار;
import ایران.JIrnOS.작업.زمان_بند;
import ایران.JIrnOS.체계호출.체계호출;
import ایران.JIrnOS.سیستم_پرونده.파일서술자표;
import ایران.JIrnOS.سیستم_پرونده.سیستم_پرونده;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class هسته {
    private final 하드웨어 دستگاه_مقدار;
    private final حافظه_مدیر 기억공간 = new حافظه_مدیر(32 * 1024 * 1024);
    private final صفحه_مدیر 쪽관리 = new صفحه_مدیر();
    private final سیستم_پرونده سیستم_پرونده = new سیستم_پرونده();
    private final زمان_بند زمان_بند = new زمان_بند(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final فرآیند_مقدار 첫과정;
    private final 체계호출 체계호출;

    public هسته(하드웨어 دستگاه_مقدار) {
        this.دستگاه_مقدار = دستگاه_مقدار;
        첫과정 = زمان_بند.첫과정(new 파일서술자표(سیستم_پرونده));
        체계호출 = new 체계호출(سیستم_پرونده, 쪽관리, زمان_بند, دستگاه_مقدار, 입력관리);
    }

    public void اجرا_2() {
        دستگاه_مقدار.직렬출력("=== JIrnOS 관리 هسته_مقدار ===\n");
    }

    public void 한단계실행() {
        دستگاه_مقدار.중앙처리장치멈춤();
    }

    public حافظه_مدیر 기억공간() {
        return 기억공간;
    }

    public صفحه_مدیر 쪽관리() {
        return 쪽관리;
    }

    public سیستم_پرونده سیستم_پرونده() {
        return سیستم_پرونده;
    }

    public زمان_بند زمان_بند() {
        return زمان_بند;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public فرآیند_مقدار 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
