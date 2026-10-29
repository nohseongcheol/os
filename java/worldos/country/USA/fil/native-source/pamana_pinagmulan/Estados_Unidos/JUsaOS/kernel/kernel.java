// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Estados_Unidos.JUsaOS.kernel;

import Estados_Unidos.JUsaOS.기억공간.Memory_tagapamahala;
import Estados_Unidos.JUsaOS.기억공간.page_tagapamahala;
import Estados_Unidos.JUsaOS.입력.입력관리자;
import Estados_Unidos.JUsaOS.작업.Proseso_VALUE;
import Estados_Unidos.JUsaOS.작업.Scheduler;
import Estados_Unidos.JUsaOS.체계호출.체계호출;
import Estados_Unidos.JUsaOS.sistema_ng_file.파일서술자표;
import Estados_Unidos.JUsaOS.sistema_ng_file.sistema_ng_file;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final 하드웨어 device_VALUE;
    private final Memory_tagapamahala 기억공간 = new Memory_tagapamahala(32 * 1024 * 1024);
    private final page_tagapamahala 쪽관리 = new page_tagapamahala();
    private final sistema_ng_file sistema_ng_file = new sistema_ng_file();
    private final Scheduler Scheduler = new Scheduler(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proseso_VALUE 첫과정;
    private final 체계호출 체계호출;

    public kernel(하드웨어 device_VALUE) {
        this.device_VALUE = device_VALUE;
        첫과정 = Scheduler.첫과정(new 파일서술자표(sistema_ng_file));
        체계호출 = new 체계호출(sistema_ng_file, 쪽관리, Scheduler, device_VALUE, 입력관리);
    }

    public void run() {
        device_VALUE.직렬출력("=== JUsaOS 관리 kernel_VALUE ===\n");
    }

    public void 한단계실행() {
        device_VALUE.중앙처리장치멈춤();
    }

    public Memory_tagapamahala 기억공간() {
        return 기억공간;
    }

    public page_tagapamahala 쪽관리() {
        return 쪽관리;
    }

    public sistema_ng_file sistema_ng_file() {
        return sistema_ng_file;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proseso_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
