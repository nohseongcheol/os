// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.mkpụrụobī_kọmpùta;

import Naịjịrịa.JNgaOS.기억공간.memọrị_njikwa;
import Naịjịrịa.JNgaOS.기억공간.ihuakwụkwọ_njikwa;
import Naịjịrịa.JNgaOS.입력.입력관리자;
import Naịjịrịa.JNgaOS.작업.ùsòrò_valuu_6712bde7;
import Naịjịrịa.JNgaOS.작업.배정기;
import Naịjịrịa.JNgaOS.체계호출.체계호출;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.파일서술자표;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.sistèm_ọbọakwụkwo;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class mkpụrụobī_kọmpùta {
    private final ngwaike_valuu njìarụ_valuu;
    private final memọrị_njikwa 기억공간 = new memọrị_njikwa(32 * 1024 * 1024);
    private final ihuakwụkwọ_njikwa 쪽관리 = new ihuakwụkwọ_njikwa();
    private final sistèm_ọbọakwụkwo sistèm_ọbọakwụkwo = new sistèm_ọbọakwụkwo();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ùsòrò_valuu_6712bde7 첫과정;
    private final 체계호출 체계호출;

    public mkpụrụobī_kọmpùta(ngwaike_valuu njìarụ_valuu) {
        this.njìarụ_valuu = njìarụ_valuu;
        첫과정 = 배정기.첫과정(new 파일서술자표(sistèm_ọbọakwụkwo));
        체계호출 = new 체계호출(sistèm_ọbọakwụkwo, 쪽관리, 배정기, njìarụ_valuu, 입력관리);
    }

    public void Bido() {
        njìarụ_valuu.직렬출력("=== JNgaOS 관리 mkpụrụobī_kọmpùta_valuu ===\n");
    }

    public void 한단계실행() {
        njìarụ_valuu.중앙처리장치멈춤();
    }

    public memọrị_njikwa 기억공간() {
        return 기억공간;
    }

    public ihuakwụkwọ_njikwa 쪽관리() {
        return 쪽관리;
    }

    public sistèm_ọbọakwụkwo sistèm_ọbọakwụkwo() {
        return sistèm_ọbọakwụkwo;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ùsòrò_valuu_6712bde7 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
