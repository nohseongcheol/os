// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.कर्णेल;

import भारत.JIndOS.기억공간.मेमोरी_प्रबन्धक;
import भारत.JIndOS.기억공간.पृष्ठ_प्रबन्धक;
import भारत.JIndOS.입력.입력관리자;
import भारत.JIndOS.작업.प्रक्रिया_मान;
import भारत.JIndOS.작업.निर्धारक;
import भारत.JIndOS.체계호출.체계호출;
import भारत.JIndOS.फाइल_प्रणाली.파일서술자표;
import भारत.JIndOS.फाइल_प्रणाली.फाइल_प्रणाली;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class कर्णेल {
    private final हार्डवेयर_मान मोबाइल_मान;
    private final मेमोरी_प्रबन्धक 기억공간 = new मेमोरी_प्रबन्धक(32 * 1024 * 1024);
    private final पृष्ठ_प्रबन्धक 쪽관리 = new पृष्ठ_प्रबन्धक();
    private final फाइल_प्रणाली फाइल_प्रणाली = new फाइल_प्रणाली();
    private final निर्धारक निर्धारक = new निर्धारक(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final प्रक्रिया_मान 첫과정;
    private final 체계호출 체계호출;

    public कर्णेल(हार्डवेयर_मान मोबाइल_मान) {
        this.मोबाइल_मान = मोबाइल_मान;
        첫과정 = निर्धारक.첫과정(new 파일서술자표(फाइल_प्रणाली));
        체계호출 = new 체계호출(फाइल_प्रणाली, 쪽관리, निर्धारक, मोबाइल_मान, 입력관리);
    }

    public void चलाउनुहोस्() {
        मोबाइल_मान.직렬출력("=== JIndOS 관리 कर्णेल_मान ===\n");
    }

    public void 한단계실행() {
        मोबाइल_मान.중앙처리장치멈춤();
    }

    public मेमोरी_प्रबन्धक 기억공간() {
        return 기억공간;
    }

    public पृष्ठ_प्रबन्धक 쪽관리() {
        return 쪽관리;
    }

    public फाइल_प्रणाली फाइल_प्रणाली() {
        return फाइल_प्रणाली;
    }

    public निर्धारक निर्धारक() {
        return निर्धारक;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public प्रक्रिया_मान 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
