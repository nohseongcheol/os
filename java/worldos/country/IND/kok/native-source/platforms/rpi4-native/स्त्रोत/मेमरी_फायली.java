// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM फायल 64개, 파일당 16384바이트, 서술자 16개. 모든 डेटा/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 चूक 번호다.
 */
public final class मेमरी_फायली {
    static final int फायल_COUNT = 64;
    static int[] नांव = new int[फायल_COUNT * 64];
    static int[] 이름길이 = new int[फायल_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] अनुक्रमणिका_मोल = new int[फायल_COUNT * 4096];
    static int[] लांबाय_मोल = new int[फायल_COUNT];
    static int[] संदर्भ_COUNT = new int[फायल_COUNT];
    static int[] 사용 = new int[16];
    static int[] लक्ष्य = new int[16];
    static int[] स्थिती = new int[16];
    static int[] पद्दत_मोड = new int[16];
    static int[] पाथ = new int[64];
    static int पाथ_लांबाय;

    public static int 파일한도() { return फायल_COUNT; }
    static int 자료읽기(int फायल, int स्थिती_INDEX) { return (अनुक्रमणिका_मोल[फायल * 4096 + स्थिती_INDEX / 4] >>> ((स्थिती_INDEX & 3) * 8)) & 255; }
    static void बरोवचें_डेटा(int फायल, int स्थिती_INDEX, int मोल) {
        int स्लॉट_प्रवेश = फायल * 4096 + स्थिती_INDEX / 4, हालोवचें_मोल = (स्थिती_INDEX & 3) * 8;
        अनुक्रमणिका_मोल[स्लॉट_प्रवेश] = (अनुक्रमणिका_मोल[स्लॉट_प्रवेश] & ~(255 << हालोवचें_मोल)) | ((मोल & 255) << हालोवचें_मोल);
    }

    public static int पाथ_Start(int आवाठ) {
        पाथ_लांबाय = 0;
        if (आवाठ < 1 || आवाठ > 63) return -36;
        पाथ_लांबाय = आवाठ;
        for (int लूप_INDEX = 0; लूप_INDEX < आवाठ; लूप_INDEX++) पाथ[लूप_INDEX] = 0;
        return 0;
    }
    public static int पाथ_बायट(int INDEX, int मोल) {
        if (INDEX < 0 || INDEX >= पाथ_लांबाय || मोल < 1 || मोल > 255) return -22;
        पाथ[INDEX] = मोल; return 0;
    }
    static int FIND_प्रवेश() {
        for (int फायल_INDEX = 0; फायल_INDEX < फायल_COUNT; फायल_INDEX++) if (이름길이[फायल_INDEX] > 0 && 이름길이[फायल_INDEX] == 정규길이 && 접두(नांव, फायल_INDEX * 64, 이름길이[फायल_INDEX], 정규, 정규길이)) return फायल_INDEX;
        return -1;
    }
    public static int उगडचें(int 플래그) {
        if (पाथ_लांबाय == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int लूप_INDEX = 0; लूप_INDEX < पाथ_लांबाय; लूप_INDEX++) if (पाथ[लूप_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int मेजप = सामान्य_स्थितीर_येवचें_मोल(); if (मेजप < 0) return मेजप;
        if (FIND_नामावळ(정규길이) >= 0) return -21;
        मेजप = 부모확인(); if (मेजप < 0) return मेजप;
        int फायल = FIND_प्रवेश();
        if (फायल >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (फायल < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int लूप_INDEX = 0; लूप_INDEX < 16; लूप_INDEX++) if (사용[लूप_INDEX] == 0) { 서술자 = लूप_INDEX; break; }
        if (서술자 < 0) return -24;
        if (फायल < 0) {
            for (int लूप_INDEX = 0; लूप_INDEX < फायल_COUNT; लूप_INDEX++) if (이름길이[लूप_INDEX] == 0 && संदर्भ_COUNT[लूप_INDEX] == 0) { फायल = लूप_INDEX; break; }
            if (फायल < 0) return -28;
            이름길이[फायल] = 정규길이;
            for (int लूप_INDEX = 0; लूप_INDEX < 정규길이; लूप_INDEX++) नांव[फायल * 64 + लूप_INDEX] = 정규[लूप_INDEX];
            लांबाय_मोल[फायल] = 0;
        }
        if ((플래그 & 0x200) != 0) लांबाय_मोल[फायल] = 0;
        사용[서술자] = 1; लक्ष्य[서술자] = फायल; स्थिती[서술자] = 0; पद्दत_मोड[서술자] = 플래그;
        संदर्भ_COUNT[फायल]++;
        return 서술자 + 3;
    }
    static int पुनर्तपासणी_करची(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(서술자);
        if (स्लॉट_प्रवेश < 0 || (पद्दत_मोड[स्लॉट_प्रवेश] & 3) == 1) return -9;
        int फायल = लक्ष्य[स्लॉट_प्रवेश];
        if (स्थिती[स्लॉट_प्रवेश] >= लांबाय_मोल[फायल]) return 256; // EOF와 प्रत्यक्ष_डेटा 0x00..0xff 구별
        return 자료읽기(फायल, स्थिती[स्लॉट_प्रवेश]++);
    }
    public static int बरोवचें(int 서술자, int मोल) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(서술자);
        if (स्लॉट_प्रवेश < 0 || (पद्दत_मोड[स्लॉट_प्रवेश] & 3) == 0) return -9;
        int फायल = लक्ष्य[स्लॉट_प्रवेश];
        if ((पद्दत_मोड[स्लॉट_प्रवेश] & 0x400) != 0) स्थिती[स्लॉट_प्रवेश] = लांबाय_मोल[फायल];
        if (स्थिती[स्लॉट_प्रवेश] >= 16384) return -28;
        while (लांबाय_मोल[फायल] < स्थिती[स्लॉट_प्रवेश]) बरोवचें_डेटा(फायल, लांबाय_मोल[फायल]++, 0);
        बरोवचें_डेटा(फायल, स्थिती[स्लॉट_प्रवेश]++, मोल);
        if (लांबाय_मोल[फायल] < स्थिती[स्लॉट_प्रवेश]) लांबाय_मोल[फायल] = स्थिती[स्लॉट_प्रवेश];
        return 1;
    }
    public static int सोद_स्थिती(int 서술자, int 거리, int प्रॉजॅक्ट_रूट) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(서술자);
        if (स्लॉट_प्रवेश < 0) return -9;
        if (प्रॉजॅक्ट_रूट < 0 || प्रॉजॅक्ट_रूट > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (प्रॉजॅक्ट_रूट == 0 ? 0 : प्रॉजॅक्ट_रूट == 1 ? स्थिती[स्लॉट_प्रवेश] : लांबाय_मोल[लक्ष्य[स्लॉट_प्रवेश]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        स्थिती[स्लॉट_प्रवेश] = 새위치; return 새위치;
    }
    public static int शेवट(int 서술자) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(서술자);
        if (स्लॉट_प्रवेश < 0) return -9;
        संदर्भ_COUNT[लक्ष्य[स्लॉट_प्रवेश]]--; 사용[स्लॉट_प्रवेश] = 0; return 0;
    }
    public static int आवाठ(int 서술자) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(서술자); return स्लॉट_प्रवेश < 0 ? -9 : लांबाय_मोल[लक्ष्य[स्लॉट_प्रवेश]];
    }
    public static int संच_लांबाय(int 서술자, int आवाठ) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(서술자);
        if (स्लॉट_प्रवेश < 0 || (पद्दत_मोड[स्लॉट_प्रवेश] & 3) == 0) return -9;
        if (आवाठ < 0 || आवाठ > 16384) return -22;
        int फायल = लक्ष्य[स्लॉट_प्रवेश];
        while (लांबाय_मोल[फायल] < आवाठ) बरोवचें_डेटा(फायल, लांबाय_मोल[फायल]++, 0);
        लांबाय_मोल[फायल] = आवाठ; return 0;
    }
    public static int 지우기() {
        if (पाथ_लांबाय == 0) return -22;
        int मेजप = सामान्य_स्थितीर_येवचें_मोल(); if (मेजप < 0) return मेजप;
        if (FIND_नामावळ(정규길이) >= 0) return -21;
        मेजप = 부모확인(); if (मेजप < 0) return मेजप;
        int फायल = FIND_प्रवेश();
        if (फायल < 0) return -2;
        이름길이[फायल] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void प्रवेश_सुची() {
        पाथ_Start(1); पाथ_बायट(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= फायल_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int लूप_INDEX = 0; लूप_INDEX < 이름길이[INDEX]; लूप_INDEX++) if (नांव[INDEX * 64 + लूप_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int स्थिती_INDEX) {
        return INDEX >= 0 && INDEX < फायल_COUNT && स्थिती_INDEX >= 0 && स्थिती_INDEX < 이름길이[INDEX] ? नांव[INDEX * 64 + स्थिती_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < फायल_COUNT ? लांबाय_मोल[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], नामावळ_नांव = new int[16 * 64], नामावळ_लांबाय = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int चलोवप, int पाथ_मोल, int[] 앞, int प्रधान_पाथ) {
        if (पाथ_मोल < प्रधान_पाथ) return false;
        for (int लूप_INDEX = 0; लूप_INDEX < प्रधान_पाथ; लूप_INDEX++) if (이름들[चलोवप + लूप_INDEX] != 앞[लूप_INDEX]) return false;
        return true;
    }
    static int सामान्य_स्थितीर_येवचें_मोल() {
        if (पाथ_लांबाय == 0) return -22;
        정규길이 = पाथ[0] == '/' ? 0 : 현재길이;
        for (int लूप_INDEX = 0; लूप_INDEX < 정규길이; लूप_INDEX++) 정규[लूप_INDEX] = 현재[लूप_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < पाथ_लांबाय) {
            while (읽는자리 < पाथ_लांबाय && पाथ[읽는자리] == '/') 읽는자리++;
            int Start_स्थिती = 읽는자리; while (읽는자리 < पाथ_लांबाय && पाथ[읽는자리] != '/') { if (पाथ[읽는자리] == 0) return -22; 읽는자리++; }
            int प्रवेश_COUNT = 읽는자리 - Start_स्थिती; if (प्रवेश_COUNT == 0 || प्रवेश_COUNT == 1 && पाथ[Start_स्थिती] == '.') continue;
            if (प्रवेश_COUNT == 2 && पाथ[Start_स्थिती] == '.' && पाथ[Start_स्थिती + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + प्रवेश_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int लूप_INDEX = Start_स्थिती; लूप_INDEX < 읽는자리; लूप_INDEX++) 정규[정규길이++] = पाथ[लूप_INDEX];
        }
        return 0;
    }
    static int FIND_नामावळ(int प्रवेश_COUNT) {
        if (प्रवेश_COUNT == 0) return 0;
        for (int लूप_INDEX = 1; लूप_INDEX < 16; लूप_INDEX++) if (नामावळ_लांबाय[लूप_INDEX] == प्रवेश_COUNT && 접두(नामावळ_नांव, लूप_INDEX * 64, प्रवेश_COUNT, 정규, प्रवेश_COUNT)) return लूप_INDEX;
        return -1;
    }
    static int 부모확인() {
        int प्रवेश_COUNT = 정규길이; while (प्रवेश_COUNT > 0 && 정규[प्रवेश_COUNT - 1] != '/') प्रवेश_COUNT--;
        return FIND_नामावळ(प्रवेश_COUNT == 0 ? 0 : प्रवेश_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int निर्माण_करचें_नामावळ() {
        int 처리값 = सामान्य_स्थितीर_येवचें_मोल(); if (처리값 < 0) return 처리값;
        if (FIND_नामावळ(정규길이) >= 0 || FIND_प्रवेश() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int लूप_INDEX = 1; लूप_INDEX < 16; लूप_INDEX++) if (नामावळ_लांबाय[लूप_INDEX] == 0) {
            नामावळ_लांबाय[लूप_INDEX] = 정규길이; for (int भीतरलो_संयोग_स्थिती = 0; भीतरलो_संयोग_स्थिती < 정규길이; भीतरलो_संयोग_स्थिती++) नामावळ_नांव[लूप_INDEX * 64 + भीतरलो_संयोग_स्थिती] = 정규[भीतरलो_संयोग_स्थिती]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = सामान्य_स्थितीर_येवचें_मोल(); if (처리값 < 0) return 처리값;
        if (FIND_नामावळ(정규길이) >= 0) return 2;
        return FIND_प्रवेश() >= 0 ? 1 : 0;
    }
    public static int बदलचें_नामावळ() {
        int 처리값 = सामान्य_स्थितीर_येवचें_मोल(); if (처리값 < 0) return 처리값;
        if (FIND_नामावळ(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int लूप_INDEX = 0; लूप_INDEX < 현재길이; लूप_INDEX++) 현재[लूप_INDEX] = 정규[लूप_INDEX]; return 0;
    }
    public static int काडचें_नामावळ() {
        int 처리값 = सामान्य_स्थितीर_येवचें_मोल(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_नामावळ(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int लूप_INDEX = 0; लूप_INDEX < फायल_COUNT; लूप_INDEX++) {
            if (이름길이[लूप_INDEX] > 정규길이 && 접두(नांव, लूप_INDEX * 64, 이름길이[लूप_INDEX], 정규, 정규길이) && नांव[लूप_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int लूप_INDEX = 0; लूप_INDEX < 16; लूप_INDEX++) {
            if (नामावळ_लांबाय[लूप_INDEX] > 정규길이 && 접두(नामावळ_नांव, लूप_INDEX * 64, नामावळ_लांबाय[लूप_INDEX], 정규, 정규길이) && नामावळ_नांव[लूप_INDEX * 64 + 정규길이] == '/') return -39;
        }
        नामावळ_लांबाय[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= फायल_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = सामान्य_स्थितीर_येवचें_मोल(); if (처리값 < 0) return 처리값;
        if (FIND_नामावळ(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_प्रवेश(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int लूप_INDEX = 0; लूप_INDEX < 정규길이; लूप_INDEX++) नांव[원본번호 * 64 + लूप_INDEX] = 정규[लूप_INDEX]; return 0;
    }
    static int प्रवेश_Start(int[] डेटा_क्रम, int 시작점, int प्रवेश_COUNT) {
        if (!접두(डेटा_क्रम, 시작점, प्रवेश_COUNT, 정규, 정규길이)) return -1;
        int Start_स्थिती = 정규길이;
        if (Start_स्थिती > 0) { if (प्रवेश_COUNT <= Start_स्थिती || डेटा_क्रम[시작점 + Start_स्थिती] != '/') return -1; Start_स्थिती++; }
        if (प्रवेश_COUNT <= Start_स्थिती) return -1;
        for (int लूप_INDEX = Start_स्थिती; लूप_INDEX < प्रवेश_COUNT; लूप_INDEX++) if (डेटा_क्रम[시작점 + लूप_INDEX] == '/') return -1;
        return Start_स्थिती;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int लूप_INDEX = 0; लूप_INDEX < 현재길이; लूप_INDEX++) बोर्ड.직렬쓰기(현재[लूप_INDEX]); }
    static int 경로목록() {
        int 처리값 = सामान्य_स्थितीर_येवचें_मोल(); if (처리값 < 0) return 처리값;
        int फायल_लक्ष्य = FIND_प्रवेश();
        if (फायल_लक्ष्य >= 0) { for (int लूप_INDEX = 0; लूप_INDEX < 정규길이; लूप_INDEX++) बोर्ड.직렬쓰기(정규[लूप_INDEX]); 단말.बरोवचें("  "); 단말.수(लांबाय_मोल[फायल_लक्ष्य]); 단말.बरोवचें("बायट_मोल(주기억 फायल)\n"); return 0; }
        if (FIND_नामावळ(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (नामावळ_लांबाय[뒷값] > 0) {
            int Start_स्थिती = प्रवेश_Start(नामावळ_नांव, 뒷값 * 64, नामावळ_लांबाय[뒷값]); if (Start_स्थिती < 0) continue;
            for (int लूप_INDEX = Start_स्थिती; लूप_INDEX < नामावळ_लांबाय[뒷값]; लूप_INDEX++) बोर्ड.직렬쓰기(नामावळ_नांव[뒷값 * 64 + लूप_INDEX]); 단말.बरोवचें("/\n");
        }
        for (int फायल_INDEX = 0; फायल_INDEX < फायल_COUNT; फायल_INDEX++) if (이름길이[फायल_INDEX] > 0) {
            int Start_स्थिती = प्रवेश_Start(नांव, फायल_INDEX * 64, 이름길이[फायल_INDEX]); if (Start_स्थिती < 0) continue;
            for (int लूप_INDEX = Start_स्थिती; लूप_INDEX < 이름길이[फायल_INDEX]; लूप_INDEX++) बोर्ड.직렬쓰기(नांव[फायल_INDEX * 64 + लूप_INDEX]);
            단말.बरोवचें("  "); 단말.수(लांबाय_मोल[फायल_INDEX]); 단말.बरोवचें("बायट_मोल(주기억 फायल)\n");
        }
        return 0;
    }
}
