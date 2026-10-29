// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 үлчәмен_үзгәртү 작업 өлеш_VALUE атап_бирү_Саклагыч/кайтару_үлчәм. 일반 물리 бит_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] өлеш_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int бүлү_бөтен_сан(int адрес) {
        return мобиль_VALUE.기억읽기(адрес) | (мобиль_VALUE.기억읽기(адрес + 1) << 8)
            | (мобиль_VALUE.기억읽기(адрес + 2) << 16) | (мобиль_VALUE.기억읽기(адрес + 3) << 24);
    }

    static int UPPER_Хәтер_үлчәмен_үзгәртү() {
        int msinfo32_exe = мобиль_VALUE.부팅정보();
        if (мобиль_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (бүлү_бөтен_сан(msinfo32_exe) & 1) == 0) return -1;
        return бүлү_бөтен_сан(msinfo32_exe + 8);
    }

    static int атап_бирү_Саклагыч() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int оя_кертү = 0; оя_кертү < 1024; оя_кертү++) өлеш_VALUE[INDEX * 1024 + оя_кертү] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean кайтару_үлчәм(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int элемент_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) элемент_COUNT += 사용[INDEX];
        return элемент_COUNT;
    }
}
