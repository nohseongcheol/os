// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. फायल/스택/संदर्भ/शाखा 경계를 पाळो_दिवचो_आदेश 중 검사한다. */
public final class 자바가상기계 {
    static int[] फायल = new int[16384], फायल_नांव_SMS = new int[64];
    static int[] अचल_टॅग = new int[512], 상가 = new int[512], अचल_SECOND_मोल = new int[512], स्ट्रिंग_संदर्भ = new int[512];
    static int[] पद्दत_नांव_SMS = new int[32], पद्दत_TYPE = new int[32], पद्दत_ऍक्सॅस = new int[32];
    static int[] पद्दत_Start = new int[32], पद्दत_सोपोवचें = new int[32], पद्दत_स्टॅक = new int[32], 함수지역 = new int[32];
    static int[] पद्दत_युक्तीवाद_COUNT = new int[32], पद्दत_युक्तीवाद_TYPE = new int[512], पद्दत_return = new int[32];
    static int[] 경계 = new int[16384];
    static int[] थळावो_मोल = new int[4096], थळावो_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] फ्रेम_पद्दत = new int[32], फ्रेम_स्थिती = new int[32], फ्रेम_स्टॅक = new int[32];
    static int[] 힙 = new int[8192];
    static int आवाठ, 읽기위치, अचल_COUNT, पद्दत_COUNT, वर्ग_नांव, फ्रेम_INDEX = -1, 힙끝 = 1, return_TYPE;
    static boolean चूक;

    static void अपेस_मोल(String Word_SMS) {
        if (!चूक) { उपेगकर्तो.बरोवचें("JVM error: "); उपेगकर्तो.बरोवचें(Word_SMS); उपेगकर्तो.बरोवचें_वर्ण_मोल(10); }
        चूक = true;
    }
    static boolean क्लिप(int चलोवप, int लांबाय_मोल) { return चलोवप >= 0 && लांबाय_मोल >= 0 && चलोवप <= आवाठ - लांबाय_मोल; }
    static int बायट_मोल() {
        if (!क्लिप(읽기위치, 1)) { अपेस_मोल("truncated class file"); return 0; }
        return फायल[읽기위치++];
    }
    static int 짧은수() { return बायट_मोल() << 8 | बायट_मोल(); }
    static int पुर्णांक() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int लांबाय_मोल) { if (!क्लिप(읽기위치, लांबाय_मोल)) अपेस_मोल("invalid attribute size"); else 읽기위치 += लांबाय_मोल; }
    static boolean तपासचें_अचल(int 수, int 종류) {
        if (수 <= 0 || 수 >= अचल_COUNT || अचल_टॅग[수] != 종류) { अपेस_मोल("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int चलोवप, int लांबाय_मोल, String Word_SMS) {
        if (!क्लिप(चलोवप, लांबाय_मोल) || लांबाय_मोल != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < लांबाय_मोल; 수++) if (फायल[चलोवप + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Word_SMS(int अचल_मोल, String Word_SMS) { return तपासचें_अचल(अचल_मोल, 1) && 구간(상가[अचल_मोल], अचल_SECOND_मोल[अचल_मोल], Word_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!तपासचें_अचल(가, 1) || !तपासचें_अचल(나, 1) || अचल_SECOND_मोल[가] != अचल_SECOND_मोल[나]) return false;
        for (int 수 = 0; 수 < अचल_SECOND_मोल[가]; 수++) if (फायल[상가[가] + 수] != फायल[상가[나] + 수]) return false;
        return true;
    }
    static int वर्ग_नांव_SMS(int 수) { return तपासचें_अचल(수, 7) && तपासचें_अचल(상가[수], 1) ? 상가[수] : 0; }
    static int संदर्भ_नांव(int 수) { return तपासचें_अचल(수, 12) && तपासचें_अचल(상가[수], 1) ? 상가[수] : 0; }
    static int संदर्भ_TYPE(int 수) { return तपासचें_अचल(수, 12) && तपासचें_अचल(अचल_SECOND_मोल[수], 1) ? अचल_SECOND_मोल[수] : 0; }
    static int 서술형(int 끝, boolean रिकामें_TYPE) {
        if (읽기위치 >= 끝) { अपेस_मोल("invalid descriptor"); return 0; }
        int मोल = बायट_मोल();
        if (मोल == 'V' && रिकामें_TYPE) return 0;
        if (मोल == 'I' || मोल == 'B' || मोल == 'C' || मोल == 'S' || मोल == 'Z') return 1;
        if (मोल == '[') { 서술형(끝, false); return 2; }
        if (मोल == 'L') {
            int चलोवप = 읽기위치;
            while (읽기위치 < 끝 && फायल[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == चलोवप) अपेस_मोल("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        अपेस_मोल("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int फंक्शन_मोल) {
        int 이전 = 읽기위치, 수 = पद्दत_TYPE[फंक्शन_मोल];
        if (!तपासचें_अचल(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + अचल_SECOND_मोल[수];
        if (बायट_मोल() != '(') अपेस_मोल("invalid method descriptor");
        int आयटम_COUNT = 0;
        while (!चूक && 읽기위치 < 끝 && फायल[읽기위치] != ')') {
            if (आयटम_COUNT == 16) { अपेस_मोल("too many method arguments"); break; }
            पद्दत_युक्तीवाद_TYPE[फंक्शन_मोल * 16 + आयटम_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || बायट_मोल() != ')') अपेस_मोल("invalid method descriptor");
        पद्दत_return[फंक्शन_मोल] = 서술형(끝, true); पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल] = आयटम_COUNT;
        if (읽기위치 != 끝) अपेस_मोल("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int आयटम_COUNT = 짧은수();
        for (int 수 = 0; 수 < आयटम_COUNT && !चूक; 수++) { तपासचें_अचल(짧은수(), 1); 건너(पुर्णांक()); }
    }
    static int आदेश_लांबाय(int मोल) {
        if (मोल == 16 || मोल == 18 || मोल == 21 || मोल == 25 || मोल == 54 || मोल == 58 || मोल == 188) return 2;
        if (मोल == 17 || मोल == 19 || मोल == 132 || मोल >= 153 && मोल <= 167
            || मोल >= 178 && मोल <= 184 || मोल == 187 || मोल == 189 || मोल == 192 || मोल == 198 || मोल == 199) return 3;
        if (मोल >= 0 && मोल <= 8 || मोल >= 26 && मोल <= 29 || मोल >= 42 && मोल <= 46 || मोल == 50
            || मोल >= 59 && मोल <= 62 || मोल >= 75 && मोल <= 79 || मोल == 83 || मोल == 87 || मोल == 89 || मोल == 95
            || मोल == 96 || मोल == 100 || मोल == 104 || मोल == 108 || मोल == 112 || मोल == 116
            || मोल == 120 || मोल == 122 || मोल == 124 || मोल == 126 || मोल == 128 || मोल == 130
            || मोल >= 145 && मोल <= 147 || मोल == 172 || मोल == 176 || मोल == 177 || मोल == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (पुर्णांक() != 0xcafebabe) अपेस_मोल("not a class file");
        int 부판 = 짧은수(), वर्जन_मोल = 짧은수();
        if (वर्जन_मोल < 45 || वर्जन_मोल > 52 || 부판 != 0) अपेस_मोल("supported class versions: 45..52, minor 0");
        अचल_COUNT = 짧은수();
        if (अचल_COUNT < 1 || अचल_COUNT > 512) { अपेस_मोल("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < अचल_COUNT && !चूक; 수++) {
            int 종류 = बायट_मोल(); अचल_टॅग[수] = 종류;
            if (종류 == 1) { अचल_SECOND_मोल[수] = 짧은수(); 상가[수] = 읽기위치; 건너(अचल_SECOND_मोल[수]); }
            else if (종류 == 3) 상가[수] = पुर्णांक();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); अचल_SECOND_मोल[수] = 짧은수(); }
            else अपेस_मोल("unsupported constant type");
        }
        int अनुमती_मोल = 짧은수();
        if ((अनुमती_मोल & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) अपेस_मोल("unsupported class flags");
        वर्ग_नांव = वर्ग_नांव_SMS(짧은수());
        if (!Word_SMS(वर्ग_नांव_SMS(짧은수()), "java/lang/Object")) अपेस_मोल("inheritance unsupported");
        if (짧은수() != 0) अपेस_मोल("interfaces unsupported");
        if (짧은수() != 0) अपेस_मोल("fields unsupported");
        पद्दत_COUNT = 짧은수();
        if (पद्दत_COUNT < 1 || पद्दत_COUNT > 32) { अपेस_मोल("method count limit (32)"); return; }
        for (int 수 = 0; 수 < पद्दत_COUNT && !चूक; 수++) {
            पद्दत_ऍक्सॅस[수] = 짧은수(); पद्दत_नांव_SMS[수] = 짧은수(); पद्दत_TYPE[수] = 짧은수();
            तपासचें_अचल(पद्दत_नांव_SMS[수], 1); 서술읽기(수);
            if ((पद्दत_ऍक्सॅस[수] & (0x100 | 0x400 | 0x20)) != 0) अपेस_मोल("native, abstract and synchronized methods unsupported");
            if ((पद्दत_ऍक्सॅस[수] & 8) == 0 && !Word_SMS(पद्दत_नांव_SMS[수], "<init>")) अपेस_मोल("instance methods unsupported");
            if (Word_SMS(पद्दत_नांव_SMS[수], "<clinit>")) अपेस_मोल("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(पद्दत_नांव_SMS[앞], पद्दत_नांव_SMS[수]) && 같은말(पद्दत_TYPE[앞], पद्दत_TYPE[수])) अपेस_मोल("duplicate method");
            int आयटम_COUNT = 짧은수();
            for (int खाशेलपण_मोल = 0; खाशेलपण_मोल < आयटम_COUNT && !चूक; खाशेलपण_मोल++) {
                int नांव = 짧은수(), लांबाय_मोल = पुर्णांक(), चलोवप = 읽기위치;
                if (!क्लिप(चलोवप, लांबाय_मोल)) { अपेस_मोल("truncated method attribute"); break; }
                if (Word_SMS(नांव, "Code")) {
                    if (पद्दत_Start[수] != 0) अपेस_मोल("duplicate Code attribute");
                    पद्दत_स्टॅक[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_लांबाय = पुर्णांक();
                    if (पद्दत_स्टॅक[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < पद्दत_युक्तीवाद_COUNT[수]
                        || CODE_लांबाय < 1 || CODE_लांबाय > 8192) अपेस_मोल("method memory limits exceeded");
                    पद्दत_Start[수] = 읽기위치; 건너(CODE_लांबाय); पद्दत_सोपोवचें[수] = 읽기위치;
                    if (짧은수() != 0) अपेस_मोल("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != चलोवप + लांबाय_मोल) अपेस_मोल("Code attribute size mismatch");
                } else 건너(लांबाय_मोल);
            }
            if (पद्दत_Start[수] == 0) अपेस_मोल("missing Code attribute");
            int स्लॉट_प्रवेश = पद्दत_Start[수];
            while (स्लॉट_प्रवेश < पद्दत_सोपोवचें[수] && !चूक) {
                int लांबाय_मोल = आदेश_लांबाय(फायल[स्लॉट_प्रवेश]);
                if (लांबाय_मोल == 0 || लांबाय_मोल > पद्दत_सोपोवचें[수] - स्लॉट_प्रवेश) { अपेस_मोल("unsupported or truncated bytecode"); break; }
                경계[स्लॉट_प्रवेश] = 수 + 1; स्लॉट_प्रवेश += लांबाय_मोल;
            }
            // 실행하지 않는 경로에도 잘못된 शाखा 목적지를 허용하지 않는다.
            स्लॉट_प्रवेश = पद्दत_Start[수];
            while (स्लॉट_प्रवेश < पद्दत_सोपोवचें[수] && !चूक) {
                int मोल = फायल[स्लॉट_प्रवेश];
                if (मोल >= 153 && मोल <= 167 || मोल == 198 || मोल == 199) {
                    int नियुक्त_स्थान_मोल = स्लॉट_प्रवेश + (short)(फायल[स्लॉट_प्रवेश + 1] << 8 | फायल[स्लॉट_प्रवेश + 2]);
                    if (नियुक्त_स्थान_मोल < पद्दत_Start[수] || नियुक्त_स्थान_मोल >= पद्दत_सोपोवचें[수] || 경계[नियुक्त_स्थान_मोल] != 수 + 1) अपेस_मोल("invalid branch target");
                }
                स्लॉट_प्रवेश += आदेश_लांबाय(मोल);
            }
        }
        if (!चूक) 속성건너();
        if (읽기위치 != आवाठ) अपेस_मोल("extra class file data");
    }
    static int नेमून_दिवचें_सांठवण(int 종류, int लांबाय_मोल) {
        if (लांबाय_मोल < 0 || लांबाय_मोल > 힙.length - 힙끝 - 2) { अपेस_मोल("object heap exhausted or negative array size"); return 0; }
        int संदर्भ = 힙끝; 힙끝 += लांबाय_मोल + 2; 힙[संदर्भ] = 종류; 힙[संदर्भ + 1] = लांबाय_मोल;
        return संदर्भ;
    }
    static boolean ऑब्जॅक्ट_मोल(int संदर्भ, int 종류) {
        if (संदर्भ < 1 || संदर्भ >= 힙끝 - 1 || 힙[संदर्भ] != 종류) { अपेस_मोल("null or invalid object reference"); return false; }
        return true;
    }
    static int अचल_SMS(int INDEX) {
        if (!तपासचें_अचल(INDEX, 1)) return 0;
        if (स्ट्रिंग_संदर्भ[INDEX] != 0) return स्ट्रिंग_संदर्भ[INDEX];
        int संदर्भ = नेमून_दिवचें_सांठवण(1, अचल_SECOND_मोल[INDEX]); if (चूक) return 0;
        int 끝 = 상가[INDEX] + अचल_SECOND_मोल[INDEX], 수 = 상가[INDEX], लांबाय_मोल = 0;
        while (수 < 끝 && !चूक) {
            int मोल = फायल[수++];
            if (मोल == 0) अपेस_मोल("invalid modified UTF-8");
            else if (मोल >= 192 && मोल <= 223 && 수 < 끝) {
                int फुडलें_आयटम = फायल[수++];
                if ((फुडलें_आयटम & 192) != 128) अपेस_मोल("invalid modified UTF-8");
                मोल = (मोल & 31) << 6 | फुडलें_आयटम & 63;
                if (मोल != 0 && मोल < 128) अपेस_मोल("overlong modified UTF-8");
            } else if (मोल >= 224 && मोल <= 239 && 수 + 1 < 끝) {
                int 가 = फायल[수++], 나 = फायल[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) अपेस_मोल("invalid modified UTF-8");
                मोल = (मोल & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (मोल < 2048) अपेस_मोल("overlong modified UTF-8");
            } else if (मोल >= 128) अपेस_मोल("invalid modified UTF-8");
            힙[संदर्भ + 2 + लांबाय_मोल++] = मोल;
        }
        힙[संदर्भ + 1] = लांबाय_मोल; स्ट्रिंग_संदर्भ[INDEX] = संदर्भ; return संदर्भ;
    }
    static int येजमान_वर्ण(String मोल) {
        int संदर्भ = नेमून_दिवचें_सांठवण(1, मोल.length()); if (चूक) return 0;
        for (int 수 = 0; 수 < मोल.length(); 수++) 힙[संदर्भ + 2 + 수] = मोल.charAt(수);
        return संदर्भ;
    }
    static void बरोवचें_SMS(int संदर्भ) {
        if (संदर्भ == 0) { उपेगकर्तो.बरोवचें("null"); return; }
        if (!ऑब्जॅक्ट_मोल(संदर्भ, 1)) return;
        for (int 수 = 0; 수 < 힙[संदर्भ + 1]; 수++) उपेगकर्तो.बरोवचें_वर्ण_मोल(힙[संदर्भ + 2 + 수]);
    }
    static int अंक_वर्ण(int मोल) {
        int संदर्भ = नेमून_दिवचें_सांठवण(1, 11); if (चूक) return 0;
        int लांबाय_मोल = 0;
        if (मोल < 0) 힙[संदर्भ + 2 + लांबाय_मोल++] = '-'; else मोल = -मोल;
        int स्थिती_INDEX = 1000000000; boolean चलोवप = false;
        while (स्थिती_INDEX != 0) {
            int 수 = -(मोल / स्थिती_INDEX);
            if (수 != 0 || चलोवप || स्थिती_INDEX == 1) { 힙[संदर्भ + 2 + लांबाय_मोल++] = '0' + 수; चलोवप = true; }
            मोल %= स्थिती_INDEX; स्थिती_INDEX /= 10;
        }
        힙[संदर्भ + 1] = लांबाय_मोल; return संदर्भ;
    }
    static int 정수해독(int संदर्भ) {
        if (!ऑब्जॅक्ट_मोल(संदर्भ, 1)) return 0;
        int लांबाय_मोल = 힙[संदर्भ + 1], 수 = 0, मोल = 0; boolean 음수 = false;
        if (लांबाय_मोल > 0 && (힙[संदर्भ + 2] == '-' || 힙[संदर्भ + 2] == '+')) { 음수 = 힙[संदर्भ + 2] == '-'; 수++; }
        if (수 == लांबाय_मोल) अपेस_मोल("NumberFormatException");
        for (; 수 < लांबाय_मोल && !चूक; 수++) {
            int अंक_मोल = 힙[संदर्भ + 2 + 수] - '0';
            if (अंक_मोल < 0 || अंक_मोल > 9 || मोल < -214748364 || मोल == -214748364 && अंक_मोल > (음수 ? 8 : 7)) अपेस_मोल("NumberFormatException");
            मोल = मोल * 10 - अंक_मोल;
        }
        return 음수 ? मोल : -मोल;
    }
    static void 넣기(int मोल, int TYPE_मोल) {
        if (चूक) return;
        if (फ्रेम_INDEX < 0 || फ्रेम_स्टॅक[फ्रेम_INDEX] >= पद्दत_स्टॅक[फ्रेम_पद्दत[फ्रेम_INDEX]]) { अपेस_मोल("operand stack overflow"); return; }
        int स्लॉट_प्रवेश = फ्रेम_INDEX * 128 + फ्रेम_स्टॅक[फ्रेम_INDEX]++; 스택값[स्लॉट_प्रवेश] = मोल; 스택형[स्लॉट_प्रवेश] = TYPE_मोल;
    }
    static int 빼기(int TYPE_मोल) {
        if (चूक) return 0;
        if (फ्रेम_INDEX < 0 || फ्रेम_स्टॅक[फ्रेम_INDEX] < 1) { अपेस_मोल("operand stack underflow"); return 0; }
        int स्लॉट_प्रवेश = फ्रेम_INDEX * 128 + --फ्रेम_स्टॅक[फ्रेम_INDEX]; return_TYPE = 스택형[स्लॉट_प्रवेश];
        if (TYPE_मोल != 0 && return_TYPE != TYPE_मोल) अपेस_मोल("operand type mismatch");
        return 스택값[स्लॉट_प्रवेश];
    }
    static void 지역읽기(int INDEX, int TYPE_मोल) {
        if (INDEX >= 함수지역[फ्रेम_पद्दत[फ्रेम_INDEX]] || INDEX < 0 || थळावो_TYPE[फ्रेम_INDEX * 128 + INDEX] != TYPE_मोल) { अपेस_मोल("invalid or uninitialized local"); return; }
        넣기(थळावो_मोल[फ्रेम_INDEX * 128 + INDEX], TYPE_मोल);
    }
    static void बरोवचें_थळावो(int INDEX, int TYPE_मोल) {
        if (INDEX >= 함수지역[फ्रेम_पद्दत[फ्रेम_INDEX]] || INDEX < 0) { अपेस_मोल("local index out of range"); return; }
        int मोल = 빼기(TYPE_मोल); थळावो_मोल[फ्रेम_INDEX * 128 + INDEX] = मोल; थळावो_TYPE[फ्रेम_INDEX * 128 + INDEX] = TYPE_मोल;
    }
    static int 명바() {
        int स्थिती = फ्रेम_स्थिती[फ्रेम_INDEX];
        if (स्थिती < पद्दत_Start[फ्रेम_पद्दत[फ्रेम_INDEX]] || स्थिती >= पद्दत_सोपोवचें[फ्रेम_पद्दत[फ्रेम_INDEX]]) { अपेस_मोल("instruction pointer out of range"); return 0; }
        फ्रेम_स्थिती[फ्रेम_INDEX]++; return फायल[स्थिती];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void हालोवचें_मोल(int स्थिती) {
        int फंक्शन_मोल = फ्रेम_पद्दत[फ्रेम_INDEX];
        if (स्थिती < पद्दत_Start[फंक्शन_मोल] || स्थिती >= पद्दत_सोपोवचें[फंक्शन_मोल] || 경계[स्थिती] != फंक्शन_मोल + 1) अपेस_मोल("invalid branch target");
        else फ्रेम_स्थिती[फ्रेम_INDEX] = स्थिती;
    }
    static void 호출(int फंक्शन_मोल) {
        if (फ्रेम_INDEX == 31) { अपेस_मोल("call stack limit (32)"); return; }
        int फुडलें_आयटम = फ्रेम_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) थळावो_TYPE[फुडलें_आयटम * 128 + 수] = 0;
        for (int 수 = पद्दत_युक्तीवाद_COUNT[फंक्शन_मोल] - 1; 수 >= 0; 수--) {
            थळावो_मोल[फुडलें_आयटम * 128 + 수] = 빼기(पद्दत_युक्तीवाद_TYPE[फंक्शन_मोल * 16 + 수]); थळावो_TYPE[फुडलें_आयटम * 128 + 수] = पद्दत_युक्तीवाद_TYPE[फंक्शन_मोल * 16 + 수];
        }
        फ्रेम_INDEX = फुडलें_आयटम; फ्रेम_पद्दत[फ्रेम_INDEX] = फंक्शन_मोल; फ्रेम_स्थिती[फ्रेम_INDEX] = पद्दत_Start[फंक्शन_मोल]; फ्रेम_स्टॅक[फ्रेम_INDEX] = 0;
    }
    static void return_मेजप(int TYPE_मोल) {
        if (TYPE_मोल != पद्दत_return[फ्रेम_पद्दत[फ्रेम_INDEX]]) { अपेस_मोल("return type mismatch"); return; }
        int मोल = TYPE_मोल == 0 ? 0 : 빼기(TYPE_मोल);
        फ्रेम_INDEX--; if (फ्रेम_INDEX >= 0 && TYPE_मोल != 0) 넣기(मोल, TYPE_मोल);
    }
    static int[] Stream_फायल_नांव = new int[64];
    static void फायल_Stream_कॉल(int धनी_मोल, int नांव, int स्वरूप_मोल, int आदेश) {
        boolean 출력 = Word_SMS(धनी_मोल, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (आदेश == 183 && Word_SMS(नांव, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_SMS(स्वरूप_मोल, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(स्वरूप_मोल, "(Ljava/lang/String;)V")) { अपेस_मोल("unsupported file stream constructor"); return; }
            int फायल_प्रवेश_नांव = 빼기(2), Stream_मोल = 빼기(2);
            if (!ऑब्जॅक्ट_मोल(फायल_प्रवेश_नांव, 1) || !ऑब्जॅक्ट_मोल(Stream_मोल, 종류) || चूक) return;
            if (힙[Stream_मोल + 3] != 0) { अपेस_मोल("file stream already initialized"); return; }
            int लांबाय_मोल = 힙[फायल_प्रवेश_नांव + 1];
            if (लांबाय_मोल < 1 || लांबाय_मोल > 63) { अपेस_मोल("invalid file name length"); return; }
            for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < लांबाय_मोल; स्लॉट_प्रवेश++) {
                int मोल = 힙[फायल_प्रवेश_नांव + 2 + स्लॉट_प्रवेश];
                if (मोल < 1 || मोल > 127) { अपेस_मोल("file stream paths currently require ASCII"); return; }
                Stream_फायल_नांव[स्लॉट_प्रवेश] = मोल;
            }
            Stream_फायल_नांव[लांबाय_मोल] = 0;
            int 서술자 = उपेगकर्तो.파일서술자열기(Stream_फायल_नांव, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { अपेस_मोल("FileNotFoundException: file open failed"); return; }
            힙[Stream_मोल + 2] = 서술자; 힙[Stream_मोल + 3] = 1;
            return;
        }
        if (आदेश != 182) { अपेस_मोल("invalid file stream invocation"); return; }
        int कृती = -1, मोल = 0;
        if (Word_SMS(नांव, "close") && Word_SMS(स्वरूप_मोल, "()V")) कृती = 0;
        if (!출력 && Word_SMS(नांव, "read") && Word_SMS(स्वरूप_मोल, "()I")) कृती = 1;
        if (출력 && Word_SMS(नांव, "write") && Word_SMS(स्वरूप_मोल, "(I)V")) { कृती = 2; मोल = 빼기(1); }
        if (कृती < 0) { अपेस_मोल("unsupported file stream method"); return; }
        int Stream_मोल = 빼기(2);
        if (!ऑब्जॅक्ट_मोल(Stream_मोल, 종류) || चूक) return;
        if (힙[Stream_मोल + 3] == 0) { अपेस_मोल("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_मोल + 2];
        if (कृती == 0) {
            if (서술자 >= 0 && उपेगकर्तो.파일서술자닫기(서술자) < 0) अपेस_मोल("IOException: close failed");
            힙[Stream_मोल + 2] = -1; return;
        }
        if (서술자 < 0) { अपेस_मोल("IOException: stream closed"); return; }
        if (कृती == 1) {
            int मेजप = उपेगकर्तो.파일한바이트읽기(서술자);
            if (मेजप < -1) अपेस_मोल("IOException: read failed"); else 넣기(मेजप, 1);
        } else if (उपेगकर्तो.파일한바이트쓰기(서술자, मोल) != 1) अपेस_मोल("IOException: write failed");
    }
    static void कॉल_पद्दत(int INDEX, int आदेश) {
        if (!तपासचें_अचल(INDEX, 10)) return;
        int धनी_मोल = वर्ग_नांव_SMS(상가[INDEX]), नांव = संदर्भ_नांव(अचल_SECOND_मोल[INDEX]), स्वरूप_मोल = संदर्भ_TYPE(अचल_SECOND_मोल[INDEX]);
        if (चूक) return;
        if (같은말(धनी_मोल, वर्ग_नांव)) {
            if (आदेश != 184) { अपेस_मोल("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < पद्दत_COUNT; 수++) if (같은말(नांव, पद्दत_नांव_SMS[수]) && 같은말(स्वरूप_मोल, पद्दत_TYPE[수])) {
                if ((पद्दत_ऍक्सॅस[수] & 8) == 0) अपेस_मोल("method is not static"); else 호출(수);
                return;
            }
            अपेस_मोल("NoSuchMethodError"); return;
        }
        if (Word_SMS(धनी_मोल, "java/io/FileInputStream") || Word_SMS(धनी_मोल, "java/io/FileOutputStream")) {
            फायल_Stream_कॉल(धनी_मोल, नांव, स्वरूप_मोल, आदेश); return;
        }
        if (आदेश == 184 && Word_SMS(धनी_मोल, "java/lang/Integer") && Word_SMS(नांव, "parseInt") && Word_SMS(स्वरूप_मोल, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (आदेश == 182 && Word_SMS(धनी_मोल, "java/io/PrintStream") && (Word_SMS(नांव, "println") || Word_SMS(नांव, "print"))) {
            int TYPE_मोल = 0, मोल = 0;
            if (Word_SMS(स्वरूप_मोल, "(I)V")) { TYPE_मोल = 1; मोल = 빼기(1); }
            else if (Word_SMS(स्वरूप_मोल, "(Z)V")) { TYPE_मोल = 2; मोल = 빼기(1); }
            else if (Word_SMS(स्वरूप_मोल, "(C)V")) { TYPE_मोल = 3; मोल = 빼기(1); }
            else if (Word_SMS(स्वरूप_मोल, "(Ljava/lang/String;)V")) { TYPE_मोल = 4; मोल = 빼기(2); }
            else if (!Word_SMS(स्वरूप_मोल, "()V") || !Word_SMS(नांव, "println")) अपेस_मोल("unsupported print descriptor");
            if (빼기(2) != -1) अपेस_मोल("invalid PrintStream receiver");
            if (चूक) return;
            if (TYPE_मोल == 1) 자바도구.수쓰기(मोल);
            if (TYPE_मोल == 2) उपेगकर्तो.बरोवचें(मोल == 0 ? "false" : "true");
            if (TYPE_मोल == 3) उपेगकर्तो.बरोवचें_वर्ण_मोल(मोल & 65535);
            if (TYPE_मोल == 4) बरोवचें_SMS(मोल);
            if (Word_SMS(नांव, "println")) उपेगकर्तो.बरोवचें_वर्ण_मोल(10);
            return;
        }
        if (आदेश == 182 && Word_SMS(धनी_मोल, "java/lang/String")) {
            if (Word_SMS(नांव, "length") && Word_SMS(स्वरूप_मोल, "()I")) {
                int संदर्भ = 빼기(2); if (ऑब्जॅक्ट_मोल(संदर्भ, 1)) 넣기(힙[संदर्भ + 1], 1); return;
            }
            if (Word_SMS(नांव, "charAt") && Word_SMS(स्वरूप_मोल, "(I)C")) {
                int सबस्क्रिप्ट_मोल = 빼기(1), संदर्भ = 빼기(2);
                if (ऑब्जॅक्ट_मोल(संदर्भ, 1)) {
                    if (सबस्क्रिप्ट_मोल < 0 || सबस्क्रिप्ट_मोल >= 힙[संदर्भ + 1]) अपेस_मोल("StringIndexOutOfBoundsException"); else 넣기(힙[संदर्भ + 2 + सबस्क्रिप्ट_मोल], 1);
                }
                return;
            }
        }
        if (Word_SMS(धनी_मोल, "java/lang/StringBuilder")) {
            if (आदेश == 183 && Word_SMS(नांव, "<init>") && Word_SMS(स्वरूप_मोल, "()V")) { ऑब्जॅक्ट_मोल(빼기(2), 4); return; }
            if (आदेश == 182 && Word_SMS(नांव, "toString") && Word_SMS(स्वरूप_मोल, "()Ljava/lang/String;")) {
                int संदर्भ = 빼기(2); if (ऑब्जॅक्ट_मोल(संदर्भ, 4)) 넣기(힙[संदर्भ + 2] == 0 ? येजमान_वर्ण("") : 힙[संदर्भ + 2], 2); return;
            }
            if (आदेश == 182 && Word_SMS(नांव, "append")) {
                int SMS = 0;
                if (Word_SMS(स्वरूप_मोल, "(I)Ljava/lang/StringBuilder;")) SMS = अंक_वर्ण(빼기(1));
                else if (Word_SMS(स्वरूप_मोल, "(Z)Ljava/lang/StringBuilder;")) SMS = येजमान_वर्ण(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(स्वरूप_मोल, "(C)Ljava/lang/StringBuilder;")) {
                    int मोल = 빼기(1); SMS = नेमून_दिवचें_सांठवण(1, 1); if (!चूक) 힙[SMS + 2] = मोल & 65535;
                }
                else if (Word_SMS(स्वरूप_मोल, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = येजमान_वर्ण("null"); }
                else { अपेस_मोल("unsupported StringBuilder append"); return; }
                int संदर्भ = 빼기(2); if (!ऑब्जॅक्ट_मोल(संदर्भ, 4) || !ऑब्जॅक्ट_मोल(SMS, 1)) return;
                int 앞 = 힙[संदर्भ + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], फाटीं_मोल_लांबाय = 힙[SMS + 1];
                int 새글 = नेमून_दिवचें_सांठवण(1, 앞길이 + फाटीं_मोल_लांबाय); if (चूक) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < फाटीं_मोल_लांबाय; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[संदर्भ + 2] = 새글; 넣기(संदर्भ, 2); return;
            }
        }
        अपेस_मोल("unsupported library method");
    }
    static int क्रम_स्लॉट(int संदर्भ, int सबस्क्रिप्ट_मोल, int TYPE_मोल) {
        if (!ऑब्जॅक्ट_मोल(संदर्भ, TYPE_मोल)) return 0;
        if (सबस्क्रिप्ट_मोल < 0 || सबस्क्रिप्ट_मोल >= 힙[संदर्भ + 1]) { अपेस_मोल("ArrayIndexOutOfBoundsException"); return 0; }
        return संदर्भ + 2 + सबस्क्रिप्ट_मोल;
    }
    static void पाळो_दिवचो_आदेश() {
        int 남음 = 500000;
        while (फ्रेम_INDEX >= 0 && !चूक) {
            if (--남음 == 0) { अपेस_मोल("instruction limit (500000)"); break; }
            int चलोवप = फ्रेम_स्थिती[फ्रेम_INDEX], मोल = 명바();
            if (चूक) break;
            if (मोल == 0) continue;
            if (मोल == 1) { 넣기(0, 2); continue; }
            if (मोल >= 2 && मोल <= 8) { 넣기(मोल - 3, 1); continue; }
            if (मोल == 16) { 넣기((byte)명바(), 1); continue; }
            if (मोल == 17) { 넣기((short)명짧(), 1); continue; }
            if (मोल == 18 || मोल == 19) {
                int 수 = मोल == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= अचल_COUNT) अपेस_मोल("invalid ldc constant");
                else if (अचल_टॅग[수] == 3) 넣기(상가[수], 1);
                else if (अचल_टॅग[수] == 8) 넣기(अचल_SMS(상가[수]), 2);
                else अपेस_मोल("unsupported ldc constant");
                continue;
            }
            if (मोल == 21 || मोल == 25) { 지역읽기(명바(), मोल == 21 ? 1 : 2); continue; }
            if (मोल >= 26 && मोल <= 29) { 지역읽기(मोल - 26, 1); continue; }
            if (मोल >= 42 && मोल <= 45) { 지역읽기(मोल - 42, 2); continue; }
            if (मोल == 54 || मोल == 58) { बरोवचें_थळावो(명바(), मोल == 54 ? 1 : 2); continue; }
            if (मोल >= 59 && मोल <= 62) { बरोवचें_थळावो(मोल - 59, 1); continue; }
            if (मोल >= 75 && मोल <= 78) { बरोवचें_थळावो(मोल - 75, 2); continue; }
            if (मोल == 46 || मोल == 50) {
                int सबस्क्रिप्ट_मोल = 빼기(1), संदर्भ = 빼기(2), स्लॉट_प्रवेश = क्रम_स्लॉट(संदर्भ, सबस्क्रिप्ट_मोल, मोल == 46 ? 2 : 3);
                if (!चूक) 넣기(힙[स्लॉट_प्रवेश], मोल == 46 ? 1 : 2); continue;
            }
            if (मोल == 79 || मोल == 83) {
                int आयटम_मूलतत्व = 빼기(मोल == 79 ? 1 : 2), सबस्क्रिप्ट_मोल = 빼기(1), संदर्भ = 빼기(2), स्लॉट_प्रवेश = क्रम_स्लॉट(संदर्भ, सबस्क्रिप्ट_मोल, मोल == 79 ? 2 : 3);
                if (मोल == 83 && आयटम_मूलतत्व != 0) ऑब्जॅक्ट_मोल(आयटम_मूलतत्व, 1);
                if (!चूक) 힙[स्लॉट_प्रवेश] = आयटम_मूलतत्व; continue;
            }
            if (मोल == 87) { 빼기(0); continue; }
            if (मोल == 89) { int 가 = 빼기(0), TYPE_मोल = return_TYPE; 넣기(가, TYPE_मोल); 넣기(가, TYPE_मोल); continue; }
            if (मोल == 95) { int 가 = 빼기(0), 가형 = return_TYPE, 나 = 빼기(0), 나형 = return_TYPE; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (मोल == 96 || मोल == 100 || मोल == 104 || मोल == 108 || मोल == 112 || मोल == 120
                || मोल == 122 || मोल == 124 || मोल == 126 || मोल == 128 || मोल == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), मेजप = 0;
                if ((मोल == 108 || मोल == 112) && 나 == 0) { अपेस_मोल("ArithmeticException: / by zero"); continue; }
                if (मोल == 96) मेजप = 가 + 나;
                if (मोल == 100) मेजप = 가 - 나;
                if (मोल == 104) मेजप = 가 * 나;
                if (मोल == 108) मेजप = 가 / 나;
                if (मोल == 112) मेजप = 가 % 나;
                if (मोल == 120) मेजप = 가 << 나;
                if (मोल == 122) मेजप = 가 >> 나;
                if (मोल == 124) मेजप = 가 >>> 나;
                if (मोल == 126) मेजप = 가 & 나;
                if (मोल == 128) मेजप = 가 | 나;
                if (मोल == 130) मेजप = 가 ^ 나;
                넣기(मेजप, 1); continue;
            }
            if (मोल == 116) { 넣기(-빼기(1), 1); continue; }
            if (मोल == 132) {
                int थळावो_मळ = 명바(), 증분 = (byte)명바(); 지역읽기(थळावो_मळ, 1); 넣기(빼기(1) + 증분, 1); बरोवचें_थळावो(थळावो_मळ, 1); continue;
            }
            if (मोल >= 145 && मोल <= 147) {
                int 수 = 빼기(1); 넣기(मोल == 145 ? (byte)수 : मोल == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (मोल >= 153 && मोल <= 167 || मोल == 198 || मोल == 199) {
                int नियुक्त_स्थान_मोल = चलोवप + (short)명짧(); boolean 갈까 = मोल == 167;
                if (मोल >= 153 && मोल <= 158) {
                    int 수 = 빼기(1); 갈까 = मोल == 153 ? 수 == 0 : मोल == 154 ? 수 != 0 : मोल == 155 ? 수 < 0 : मोल == 156 ? 수 >= 0 : मोल == 157 ? 수 > 0 : 수 <= 0;
                } else if (मोल >= 159 && मोल <= 166) {
                    int 나 = 빼기(मोल >= 165 ? 2 : 1), 가 = 빼기(मोल >= 165 ? 2 : 1);
                    갈까 = मोल == 159 || मोल == 165 ? 가 == 나 : मोल == 160 || मोल == 166 ? 가 != 나 : मोल == 161 ? 가 < 나 : मोल == 162 ? 가 >= 나 : मोल == 163 ? 가 > 나 : 가 <= 나;
                } else if (मोल == 198 || मोल == 199) { int 수 = 빼기(2); 갈까 = मोल == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) हालोवचें_मोल(नियुक्त_स्थान_मोल); continue;
            }
            if (मोल == 172 || मोल == 176 || मोल == 177) { return_मेजप(मोल == 172 ? 1 : मोल == 176 ? 2 : 0); continue; }
            if (मोल == 178) {
                int 수 = 명짧(); if (!तपासचें_अचल(수, 9)) continue;
                if (!Word_SMS(वर्ग_नांव_SMS(상가[수]), "java/lang/System") || !Word_SMS(संदर्भ_नांव(अचल_SECOND_मोल[수]), "out")
                    || !Word_SMS(संदर्भ_TYPE(अचल_SECOND_मोल[수]), "Ljava/io/PrintStream;")) अपेस_मोल("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (मोल == 182 || मोल == 183 || मोल == 184) { कॉल_पद्दत(명짧(), मोल); continue; }
            if (मोल == 187) {
                int नांव = वर्ग_नांव_SMS(명짧());
                if (Word_SMS(नांव, "java/lang/StringBuilder")) 넣기(नेमून_दिवचें_सांठवण(4, 1), 2);
                else if (Word_SMS(नांव, "java/io/FileInputStream") || Word_SMS(नांव, "java/io/FileOutputStream")) {
                    int संदर्भ = नेमून_दिवचें_सांठवण(Word_SMS(नांव, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!चूक) { 힙[संदर्भ + 2] = -1; 넣기(संदर्भ, 2); }
                } else अपेस_मोल("unsupported object construction");
                continue;
            }
            if (मोल == 188 || मोल == 189) {
                if (मोल == 188) { if (명바() != 10) अपेस_मोल("only int[] newarray is supported"); }
                else if (!Word_SMS(वर्ग_नांव_SMS(명짧()), "java/lang/String")) अपेस_मोल("only String[] anewarray is supported");
                int लांबाय_मोल = 빼기(1); 넣기(नेमून_दिवचें_सांठवण(मोल == 188 ? 2 : 3, लांबाय_मोल), 2); continue;
            }
            if (मोल == 190) {
                int संदर्भ = 빼기(2);
                if (संदर्भ < 1 || संदर्भ >= 힙끝 - 1 || (힙[संदर्भ] != 2 && 힙[संदर्भ] != 3)) अपेस_मोल("null or invalid array");
                else 넣기(힙[संदर्भ + 1], 1); continue;
            }
            if (मोल == 192) {
                int नांव = वर्ग_नांव_SMS(명짧()), संदर्भ = 빼기(2);
                if (!Word_SMS(नांव, "java/lang/String")) अपेस_मोल("unsupported checkcast");
                else if (संदर्भ != 0) ऑब्जॅक्ट_मोल(संदर्भ, 1);
                넣기(संदर्भ, 2); continue;
            }
            अपेस_मोल("unsupported bytecode");
        }
    }
    public static int चलोवप() {
        if (उपेगकर्तो.인수개수() == 1 && 자바도구.같음(उपेगकर्तो.인수(0), "-version")) {
            उपेगकर्तो.बरोवचें("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (उपेगकर्तो.인수개수() < 1) { उपेगकर्तो.बरोवचें("Usage: java CLASS [ARGS]\n"); return 2; }
        int लांबाय_मोल = 자바도구.नांव(फायल_नांव_SMS, उपेगकर्तो.인수(0));
        if (लांबाय_मोल < 1 || लांबाय_मोल > 57) { उपेगकर्तो.बरोवचें("java: invalid class name\n"); return 2; }
        फायल_नांव_SMS[लांबाय_मोल] = '.'; फायल_नांव_SMS[लांबाय_मोल + 1] = 'c'; फायल_नांव_SMS[लांबाय_मोल + 2] = 'l'; फायल_नांव_SMS[लांबाय_मोल + 3] = 'a'; फायल_नांव_SMS[लांबाय_मोल + 4] = 's'; फायल_नांव_SMS[लांबाय_मोल + 5] = 's';
        आवाठ = उपेगकर्तो.파일읽기(फायल_नांव_SMS, फायल);
        if (आवाठ < 0) { उपेगकर्तो.बरोवचें("java: cannot read class: "); 자바도구.수쓰기(आवाठ); उपेगकर्तो.बरोवचें_वर्ण_मोल(10); return 1; }
        클래스읽기(); if (चूक) return 1;
        int वर्ण_नांव = अचल_SMS(वर्ग_नांव);
        if (!चूक && 힙[वर्ण_नांव + 1] != लांबाय_मोल) अपेस_मोल("class name does not match file");
        for (int 수 = 0; 수 < लांबाय_मोल && !चूक; 수++) if (힙[वर्ण_नांव + 2 + 수] != फायल_नांव_SMS[수]) अपेस_मोल("class name does not match file");
        int प्रवेश_पॉयंट_मोल = -1;
        for (int 수 = 0; 수 < पद्दत_COUNT; 수++) if (Word_SMS(पद्दत_नांव_SMS[수], "main") && Word_SMS(पद्दत_TYPE[수], "([Ljava/lang/String;)V") && (पद्दत_ऍक्सॅस[수] & 9) == 9) प्रवेश_पॉयंट_मोल = 수;
        if (प्रवेश_पॉयंट_मोल < 0) अपेस_मोल("public static void main(String[] args) required");
        if (चूक) return 1;
        int 인수 = नेमून_दिवचें_सांठवण(3, उपेगकर्तो.인수개수() - 1);
        for (int 수 = 1; 수 < उपेगकर्तो.인수개수() && !चूक; 수++) 힙[인수 + 1 + 수] = येजमान_वर्ण(उपेगकर्तो.인수(수));
        फ्रेम_INDEX = 0; फ्रेम_पद्दत[0] = प्रवेश_पॉयंट_मोल; फ्रेम_स्थिती[0] = पद्दत_Start[प्रवेश_पॉयंट_मोल]; थळावो_मोल[0] = 인수; थळावो_TYPE[0] = 2;
        पाळो_दिवचो_आदेश(); return चूक ? 1 : 0;
    }
}
