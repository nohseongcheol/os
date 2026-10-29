// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.कर्नेल;

import भारत.JIndOS.기억공간.मेमरी_वेवस्थापक;
import भारत.JIndOS.기억공간.पान_वेवस्थापक;
import भारत.JIndOS.입력.입력관리자;
import भारत.JIndOS.작업.प्रक्रिया_मोल;
import भारत.JIndOS.작업.नियोजक;
import भारत.JIndOS.체계호출.체계호출;
import भारत.JIndOS.फायल_प्रणाली.파일서술자표;
import भारत.JIndOS.फायल_प्रणाली.फायल_प्रणाली;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class कर्नेल {
    private final हार्डवॅर_मोल मोबायल_मोल;
    private final मेमरी_वेवस्थापक 기억공간 = new मेमरी_वेवस्थापक(32 * 1024 * 1024);
    private final पान_वेवस्थापक 쪽관리 = new पान_वेवस्थापक();
    private final फायल_प्रणाली फायल_प्रणाली = new फायल_प्रणाली();
    private final नियोजक नियोजक = new नियोजक(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final प्रक्रिया_मोल 첫과정;
    private final 체계호출 체계호출;

    public कर्नेल(हार्डवॅर_मोल मोबायल_मोल) {
        this.मोबायल_मोल = मोबायल_मोल;
        첫과정 = नियोजक.첫과정(new 파일서술자표(फायल_प्रणाली));
        체계호출 = new 체계호출(फायल_प्रणाली, 쪽관리, नियोजक, मोबायल_मोल, 입력관리);
    }

    public void चलोवप() {
        मोबायल_मोल.직렬출력("=== JIndOS 관리 कर्नेल_मोल ===\n");
    }

    public void 한단계실행() {
        मोबायल_मोल.중앙처리장치멈춤();
    }

    public मेमरी_वेवस्थापक 기억공간() {
        return 기억공간;
    }

    public पान_वेवस्थापक 쪽관리() {
        return 쪽관리;
    }

    public फायल_प्रणाली फायल_प्रणाली() {
        return फायल_प्रणाली;
    }

    public नियोजक नियोजक() {
        return नियोजक;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public प्रक्रिया_मोल 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
