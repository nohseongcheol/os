// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 आवाठ 작업 विभाग_मोल नेमून_दिवचें_सांठवण/return_मेजप. 일반 물리 पान_मोल 관리자는 아니다. */
public final class 기억공간 {
    static int[] विभाग_मोल = new int[8192];
    static int[] 사용 = new int[8];

    static int व्याकरणी_फोडणिशी_पुर्णांक(int नामो) {
        return मोबायल_मोल.기억읽기(नामो) | (मोबायल_मोल.기억읽기(नामो + 1) << 8)
            | (मोबायल_मोल.기억읽기(नामो + 2) << 16) | (मोबायल_मोल.기억읽기(नामो + 3) << 24);
    }

    static int UPPER_मेमरी_आवाठ() {
        int msinfo32_exe = मोबायल_मोल.부팅정보();
        if (मोबायल_मोल.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (व्याकरणी_फोडणिशी_पुर्णांक(msinfo32_exe) & 1) == 0) return -1;
        return व्याकरणी_फोडणिशी_पुर्णांक(msinfo32_exe + 8);
    }

    static int नेमून_दिवचें_सांठवण() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 1024; स्लॉट_प्रवेश++) विभाग_मोल[INDEX * 1024 + स्लॉट_प्रवेश] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean return_मेजप(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int आयटम_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) आयटम_COUNT += 사용[INDEX];
        return आयटम_COUNT;
    }
}
