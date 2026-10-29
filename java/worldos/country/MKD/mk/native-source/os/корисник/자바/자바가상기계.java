// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Датотека/스택/Референци/гранка 경계를 Изврши_наредба 중 검사한다. */
public final class 자바가상기계 {
    static int[] Датотека = new int[16384], датотека_име_СМС = new int[64];
    static int[] константа_ознака = new int[512], 상가 = new int[512], константа_SECOND_VALUE = new int[512], низа_Референци_cdb12cb8 = new int[512];
    static int[] метод_име_СМС = new int[32], метод_TYPE = new int[32], метод_пристап = new int[32];
    static int[] метод_Start = new int[32], метод_крај = new int[32], метод_Купче = new int[32], 함수지역 = new int[32];
    static int[] метод_аргумент_COUNT = new int[32], метод_аргумент_TYPE = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] локален_VALUE = new int[4096], локален_TYPE = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] врами_метод = new int[32], врами_позиционирање = new int[32], врами_Купче = new int[32];
    static int[] 힙 = new int[8192];
    static int Големина, 읽기위치, константа_COUNT, метод_COUNT, класа_име, врами_INDEX = -1, 힙끝 = 1, 반환형;
    static boolean ГРЕШКА;

    static void неуспех_VALUE(String Word_СМС) {
        if (!ГРЕШКА) { корисник.Запиши("JVM error: "); корисник.Запиши(Word_СМС); корисник.запиши_знак_VALUE(10); }
        ГРЕШКА = true;
    }
    static boolean клип(int Изврши_2, int должина_VALUE) { return Изврши_2 >= 0 && должина_VALUE >= 0 && Изврши_2 <= Големина - должина_VALUE; }
    static int бајт_VALUE() {
        if (!клип(읽기위치, 1)) { неуспех_VALUE("truncated class file"); return 0; }
        return Датотека[읽기위치++];
    }
    static int 짧은수() { return бајт_VALUE() << 8 | бајт_VALUE(); }
    static int цел_број() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int должина_VALUE) { if (!клип(읽기위치, должина_VALUE)) неуспех_VALUE("invalid attribute size"); else 읽기위치 += должина_VALUE; }
    static boolean провери_константа(int 수, int 종류) {
        if (수 <= 0 || 수 >= константа_COUNT || константа_ознака[수] != 종류) { неуспех_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Изврши_2, int должина_VALUE, String Word_СМС) {
        if (!клип(Изврши_2, должина_VALUE) || должина_VALUE != Word_СМС.length()) return false;
        for (int 수 = 0; 수 < должина_VALUE; 수++) if (Датотека[Изврши_2 + 수] != Word_СМС.charAt(수)) return false;
        return true;
    }
    static boolean Word_СМС(int константа_VALUE, String Word_СМС) { return провери_константа(константа_VALUE, 1) && 구간(상가[константа_VALUE], константа_SECOND_VALUE[константа_VALUE], Word_СМС); }
    static boolean 같은말(int 가, int 나) {
        if (!провери_константа(가, 1) || !провери_константа(나, 1) || константа_SECOND_VALUE[가] != константа_SECOND_VALUE[나]) return false;
        for (int 수 = 0; 수 < константа_SECOND_VALUE[가]; 수++) if (Датотека[상가[가] + 수] != Датотека[상가[나] + 수]) return false;
        return true;
    }
    static int класа_име_СМС(int 수) { return провери_константа(수, 7) && провери_константа(상가[수], 1) ? 상가[수] : 0; }
    static int Референци_име(int 수) { return провери_константа(수, 12) && провери_константа(상가[수], 1) ? 상가[수] : 0; }
    static int Референци_TYPE(int 수) { return провери_константа(수, 12) && провери_константа(константа_SECOND_VALUE[수], 1) ? константа_SECOND_VALUE[수] : 0; }
    static int 서술형(int 끝, boolean празно_TYPE) {
        if (읽기위치 >= 끝) { неуспех_VALUE("invalid descriptor"); return 0; }
        int VALUE = бајт_VALUE();
        if (VALUE == 'V' && празно_TYPE) return 0;
        if (VALUE == 'I' || VALUE == 'B' || VALUE == 'C' || VALUE == 'S' || VALUE == 'Z') return 1;
        if (VALUE == '[') { 서술형(끝, false); return 2; }
        if (VALUE == 'L') {
            int Изврши_2 = 읽기위치;
            while (읽기위치 < 끝 && Датотека[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Изврши_2) неуспех_VALUE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        неуспех_VALUE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int ФУНКЦИЈА_VALUE) {
        int 이전 = 읽기위치, 수 = метод_TYPE[ФУНКЦИЈА_VALUE];
        if (!провери_константа(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + константа_SECOND_VALUE[수];
        if (бајт_VALUE() != '(') неуспех_VALUE("invalid method descriptor");
        int ставка_COUNT = 0;
        while (!ГРЕШКА && 읽기위치 < 끝 && Датотека[읽기위치] != ')') {
            if (ставка_COUNT == 16) { неуспех_VALUE("too many method arguments"); break; }
            метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + ставка_COUNT++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || бајт_VALUE() != ')') неуспех_VALUE("invalid method descriptor");
        함수반환[ФУНКЦИЈА_VALUE] = 서술형(끝, true); метод_аргумент_COUNT[ФУНКЦИЈА_VALUE] = ставка_COUNT;
        if (읽기위치 != 끝) неуспех_VALUE("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int ставка_COUNT = 짧은수();
        for (int 수 = 0; 수 < ставка_COUNT && !ГРЕШКА; 수++) { провери_константа(짧은수(), 1); 건너(цел_број()); }
    }
    static int наредба_должина(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE == 50
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE == 83 || VALUE == 87 || VALUE == 89 || VALUE == 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (цел_број() != 0xcafebabe) неуспех_VALUE("not a class file");
        int 부판 = 짧은수(), верзија_VALUE = 짧은수();
        if (верзија_VALUE < 45 || верзија_VALUE > 52 || 부판 != 0) неуспех_VALUE("supported class versions: 45..52, minor 0");
        константа_COUNT = 짧은수();
        if (константа_COUNT < 1 || константа_COUNT > 512) { неуспех_VALUE("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < константа_COUNT && !ГРЕШКА; 수++) {
            int 종류 = бајт_VALUE(); константа_ознака[수] = 종류;
            if (종류 == 1) { константа_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(константа_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = цел_број();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); константа_SECOND_VALUE[수] = 짧은수(); }
            else неуспех_VALUE("unsupported constant type");
        }
        int дозвола_VALUE = 짧은수();
        if ((дозвола_VALUE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) неуспех_VALUE("unsupported class flags");
        класа_име = класа_име_СМС(짧은수());
        if (!Word_СМС(класа_име_СМС(짧은수()), "java/lang/Object")) неуспех_VALUE("inheritance unsupported");
        if (짧은수() != 0) неуспех_VALUE("interfaces unsupported");
        if (짧은수() != 0) неуспех_VALUE("fields unsupported");
        метод_COUNT = 짧은수();
        if (метод_COUNT < 1 || метод_COUNT > 32) { неуспех_VALUE("method count limit (32)"); return; }
        for (int 수 = 0; 수 < метод_COUNT && !ГРЕШКА; 수++) {
            метод_пристап[수] = 짧은수(); метод_име_СМС[수] = 짧은수(); метод_TYPE[수] = 짧은수();
            провери_константа(метод_име_СМС[수], 1); 서술읽기(수);
            if ((метод_пристап[수] & (0x100 | 0x400 | 0x20)) != 0) неуспех_VALUE("native, abstract and synchronized methods unsupported");
            if ((метод_пристап[수] & 8) == 0 && !Word_СМС(метод_име_СМС[수], "<init>")) неуспех_VALUE("instance methods unsupported");
            if (Word_СМС(метод_име_СМС[수], "<clinit>")) неуспех_VALUE("class initializers unsupported");
            for (int предна_VALUE = 0; предна_VALUE < 수; предна_VALUE++) if (같은말(метод_име_СМС[предна_VALUE], метод_име_СМС[수]) && 같은말(метод_TYPE[предна_VALUE], метод_TYPE[수])) неуспех_VALUE("duplicate method");
            int ставка_COUNT = 짧은수();
            for (int атрибут_VALUE = 0; атрибут_VALUE < ставка_COUNT && !ГРЕШКА; атрибут_VALUE++) {
                int Име = 짧은수(), должина_VALUE = цел_број(), Изврши_2 = 읽기위치;
                if (!клип(Изврши_2, должина_VALUE)) { неуспех_VALUE("truncated method attribute"); break; }
                if (Word_СМС(Име, "Code")) {
                    if (метод_Start[수] != 0) неуспех_VALUE("duplicate Code attribute");
                    метод_Купче[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_должина = цел_број();
                    if (метод_Купче[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < метод_аргумент_COUNT[수]
                        || CODE_должина < 1 || CODE_должина > 8192) неуспех_VALUE("method memory limits exceeded");
                    метод_Start[수] = 읽기위치; 건너(CODE_должина); метод_крај[수] = 읽기위치;
                    if (짧은수() != 0) неуспех_VALUE("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Изврши_2 + должина_VALUE) неуспех_VALUE("Code attribute size mismatch");
                } else 건너(должина_VALUE);
            }
            if (метод_Start[수] == 0) неуспех_VALUE("missing Code attribute");
            int отвор_внес = метод_Start[수];
            while (отвор_внес < метод_крај[수] && !ГРЕШКА) {
                int должина_VALUE = наредба_должина(Датотека[отвор_внес]);
                if (должина_VALUE == 0 || должина_VALUE > метод_крај[수] - отвор_внес) { неуспех_VALUE("unsupported or truncated bytecode"); break; }
                경계[отвор_внес] = 수 + 1; отвор_внес += должина_VALUE;
            }
            // 실행하지 않는 경로에도 잘못된 гранка 목적지를 허용하지 않는다.
            отвор_внес = метод_Start[수];
            while (отвор_внес < метод_крај[수] && !ГРЕШКА) {
                int VALUE = Датотека[отвор_внес];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                    int одредиште_VALUE = отвор_внес + (short)(Датотека[отвор_внес + 1] << 8 | Датотека[отвор_внес + 2]);
                    if (одредиште_VALUE < метод_Start[수] || одредиште_VALUE >= метод_крај[수] || 경계[одредиште_VALUE] != 수 + 1) неуспех_VALUE("invalid branch target");
                }
                отвор_внес += наредба_должина(VALUE);
            }
        }
        if (!ГРЕШКА) 속성건너();
        if (읽기위치 != Големина) неуспех_VALUE("extra class file data");
    }
    static int додели_Склад(int 종류, int должина_VALUE) {
        if (должина_VALUE < 0 || должина_VALUE > 힙.length - 힙끝 - 2) { неуспех_VALUE("object heap exhausted or negative array size"); return 0; }
        int Референци = 힙끝; 힙끝 += должина_VALUE + 2; 힙[Референци] = 종류; 힙[Референци + 1] = должина_VALUE;
        return Референци;
    }
    static boolean објект_VALUE(int Референци, int 종류) {
        if (Референци < 1 || Референци >= 힙끝 - 1 || 힙[Референци] != 종류) { неуспех_VALUE("null or invalid object reference"); return false; }
        return true;
    }
    static int константа_СМС(int INDEX) {
        if (!провери_константа(INDEX, 1)) return 0;
        if (низа_Референци_cdb12cb8[INDEX] != 0) return низа_Референци_cdb12cb8[INDEX];
        int Референци = додели_Склад(1, константа_SECOND_VALUE[INDEX]); if (ГРЕШКА) return 0;
        int 끝 = 상가[INDEX] + константа_SECOND_VALUE[INDEX], 수 = 상가[INDEX], должина_VALUE = 0;
        while (수 < 끝 && !ГРЕШКА) {
            int VALUE = Датотека[수++];
            if (VALUE == 0) неуспех_VALUE("invalid modified UTF-8");
            else if (VALUE >= 192 && VALUE <= 223 && 수 < 끝) {
                int Следно_ставка = Датотека[수++];
                if ((Следно_ставка & 192) != 128) неуспех_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 31) << 6 | Следно_ставка & 63;
                if (VALUE != 0 && VALUE < 128) неуспех_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 224 && VALUE <= 239 && 수 + 1 < 끝) {
                int 가 = Датотека[수++], 나 = Датотека[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) неуспех_VALUE("invalid modified UTF-8");
                VALUE = (VALUE & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (VALUE < 2048) неуспех_VALUE("overlong modified UTF-8");
            } else if (VALUE >= 128) неуспех_VALUE("invalid modified UTF-8");
            힙[Референци + 2 + должина_VALUE++] = VALUE;
        }
        힙[Референци + 1] = должина_VALUE; низа_Референци_cdb12cb8[INDEX] = Референци; return Референци;
    }
    static int вдоми_знак(String VALUE) {
        int Референци = додели_Склад(1, VALUE.length()); if (ГРЕШКА) return 0;
        for (int 수 = 0; 수 < VALUE.length(); 수++) 힙[Референци + 2 + 수] = VALUE.charAt(수);
        return Референци;
    }
    static void запиши_СМС(int Референци) {
        if (Референци == 0) { корисник.Запиши("null"); return; }
        if (!објект_VALUE(Референци, 1)) return;
        for (int 수 = 0; 수 < 힙[Референци + 1]; 수++) корисник.запиши_знак_VALUE(힙[Референци + 2 + 수]);
    }
    static int цифра_знак(int VALUE) {
        int Референци = додели_Склад(1, 11); if (ГРЕШКА) return 0;
        int должина_VALUE = 0;
        if (VALUE < 0) 힙[Референци + 2 + должина_VALUE++] = '-'; else VALUE = -VALUE;
        int позиционирање_INDEX = 1000000000; boolean Изврши_2 = false;
        while (позиционирање_INDEX != 0) {
            int 수 = -(VALUE / позиционирање_INDEX);
            if (수 != 0 || Изврши_2 || позиционирање_INDEX == 1) { 힙[Референци + 2 + должина_VALUE++] = '0' + 수; Изврши_2 = true; }
            VALUE %= позиционирање_INDEX; позиционирање_INDEX /= 10;
        }
        힙[Референци + 1] = должина_VALUE; return Референци;
    }
    static int 정수해독(int Референци) {
        if (!објект_VALUE(Референци, 1)) return 0;
        int должина_VALUE = 힙[Референци + 1], 수 = 0, VALUE = 0; boolean 음수 = false;
        if (должина_VALUE > 0 && (힙[Референци + 2] == '-' || 힙[Референци + 2] == '+')) { 음수 = 힙[Референци + 2] == '-'; 수++; }
        if (수 == должина_VALUE) неуспех_VALUE("NumberFormatException");
        for (; 수 < должина_VALUE && !ГРЕШКА; 수++) {
            int цифра_VALUE = 힙[Референци + 2 + 수] - '0';
            if (цифра_VALUE < 0 || цифра_VALUE > 9 || VALUE < -214748364 || VALUE == -214748364 && цифра_VALUE > (음수 ? 8 : 7)) неуспех_VALUE("NumberFormatException");
            VALUE = VALUE * 10 - цифра_VALUE;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static void 넣기(int VALUE, int TYPE_VALUE) {
        if (ГРЕШКА) return;
        if (врами_INDEX < 0 || врами_Купче[врами_INDEX] >= метод_Купче[врами_метод[врами_INDEX]]) { неуспех_VALUE("operand stack overflow"); return; }
        int отвор_внес = врами_INDEX * 128 + врами_Купче[врами_INDEX]++; 스택값[отвор_внес] = VALUE; 스택형[отвор_внес] = TYPE_VALUE;
    }
    static int 빼기(int TYPE_VALUE) {
        if (ГРЕШКА) return 0;
        if (врами_INDEX < 0 || врами_Купче[врами_INDEX] < 1) { неуспех_VALUE("operand stack underflow"); return 0; }
        int отвор_внес = врами_INDEX * 128 + --врами_Купче[врами_INDEX]; 반환형 = 스택형[отвор_внес];
        if (TYPE_VALUE != 0 && 반환형 != TYPE_VALUE) неуспех_VALUE("operand type mismatch");
        return 스택값[отвор_внес];
    }
    static void 지역읽기(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[врами_метод[врами_INDEX]] || INDEX < 0 || локален_TYPE[врами_INDEX * 128 + INDEX] != TYPE_VALUE) { неуспех_VALUE("invalid or uninitialized local"); return; }
        넣기(локален_VALUE[врами_INDEX * 128 + INDEX], TYPE_VALUE);
    }
    static void запиши_локален(int INDEX, int TYPE_VALUE) {
        if (INDEX >= 함수지역[врами_метод[врами_INDEX]] || INDEX < 0) { неуспех_VALUE("local index out of range"); return; }
        int VALUE = 빼기(TYPE_VALUE); локален_VALUE[врами_INDEX * 128 + INDEX] = VALUE; локален_TYPE[врами_INDEX * 128 + INDEX] = TYPE_VALUE;
    }
    static int 명바() {
        int Позиција = врами_позиционирање[врами_INDEX];
        if (Позиција < метод_Start[врами_метод[врами_INDEX]] || Позиција >= метод_крај[врами_метод[врами_INDEX]]) { неуспех_VALUE("instruction pointer out of range"); return 0; }
        врами_позиционирање[врами_INDEX]++; return Датотека[Позиција];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void премести_VALUE(int Позиција) {
        int ФУНКЦИЈА_VALUE = врами_метод[врами_INDEX];
        if (Позиција < метод_Start[ФУНКЦИЈА_VALUE] || Позиција >= метод_крај[ФУНКЦИЈА_VALUE] || 경계[Позиција] != ФУНКЦИЈА_VALUE + 1) неуспех_VALUE("invalid branch target");
        else врами_позиционирање[врами_INDEX] = Позиција;
    }
    static void 호출(int ФУНКЦИЈА_VALUE) {
        if (врами_INDEX == 31) { неуспех_VALUE("call stack limit (32)"); return; }
        int Следно_ставка = врами_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) локален_TYPE[Следно_ставка * 128 + 수] = 0;
        for (int 수 = метод_аргумент_COUNT[ФУНКЦИЈА_VALUE] - 1; 수 >= 0; 수--) {
            локален_VALUE[Следно_ставка * 128 + 수] = 빼기(метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수]); локален_TYPE[Следно_ставка * 128 + 수] = метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수];
        }
        врами_INDEX = Следно_ставка; врами_метод[врами_INDEX] = ФУНКЦИЈА_VALUE; врами_позиционирање[врами_INDEX] = метод_Start[ФУНКЦИЈА_VALUE]; врами_Купче[врами_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[врами_метод[врами_INDEX]]) { неуспех_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        врами_INDEX--; if (врами_INDEX >= 0 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
    }
    static int[] Stream_датотека_име = new int[64];
    static void датотека_Stream_CALL(int сопственик_VALUE, int Име, int формат_VALUE, int Команда) {
        boolean 출력 = Word_СМС(сопственик_VALUE, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Команда == 183 && Word_СМС(Име, "<init>")) {
            boolean 이어 = false;
            if (출력 && Word_СМС(формат_VALUE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_СМС(формат_VALUE, "(Ljava/lang/String;)V")) { неуспех_VALUE("unsupported file stream constructor"); return; }
            int датотека_внес_име = 빼기(2), Stream_VALUE = 빼기(2);
            if (!објект_VALUE(датотека_внес_име, 1) || !објект_VALUE(Stream_VALUE, 종류) || ГРЕШКА) return;
            if (힙[Stream_VALUE + 3] != 0) { неуспех_VALUE("file stream already initialized"); return; }
            int должина_VALUE = 힙[датотека_внес_име + 1];
            if (должина_VALUE < 1 || должина_VALUE > 63) { неуспех_VALUE("invalid file name length"); return; }
            for (int отвор_внес = 0; отвор_внес < должина_VALUE; отвор_внес++) {
                int VALUE = 힙[датотека_внес_име + 2 + отвор_внес];
                if (VALUE < 1 || VALUE > 127) { неуспех_VALUE("file stream paths currently require ASCII"); return; }
                Stream_датотека_име[отвор_внес] = VALUE;
            }
            Stream_датотека_име[должина_VALUE] = 0;
            int 서술자 = корисник.파일서술자열기(Stream_датотека_име, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { неуспех_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Команда != 182) { неуспех_VALUE("invalid file stream invocation"); return; }
        int Дејство = -1, VALUE = 0;
        if (Word_СМС(Име, "close") && Word_СМС(формат_VALUE, "()V")) Дејство = 0;
        if (!출력 && Word_СМС(Име, "read") && Word_СМС(формат_VALUE, "()I")) Дејство = 1;
        if (출력 && Word_СМС(Име, "write") && Word_СМС(формат_VALUE, "(I)V")) { Дејство = 2; VALUE = 빼기(1); }
        if (Дејство < 0) { неуспех_VALUE("unsupported file stream method"); return; }
        int Stream_VALUE = 빼기(2);
        if (!објект_VALUE(Stream_VALUE, 종류) || ГРЕШКА) return;
        if (힙[Stream_VALUE + 3] == 0) { неуспех_VALUE("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_VALUE + 2];
        if (Дејство == 0) {
            if (서술자 >= 0 && корисник.파일서술자닫기(서술자) < 0) неуспех_VALUE("IOException: close failed");
            힙[Stream_VALUE + 2] = -1; return;
        }
        if (서술자 < 0) { неуспех_VALUE("IOException: stream closed"); return; }
        if (Дејство == 1) {
            int мерка = корисник.파일한바이트읽기(서술자);
            if (мерка < -1) неуспех_VALUE("IOException: read failed"); else 넣기(мерка, 1);
        } else if (корисник.파일한바이트쓰기(서술자, VALUE) != 1) неуспех_VALUE("IOException: write failed");
    }
    static void CALL_метод(int INDEX, int Команда) {
        if (!провери_константа(INDEX, 10)) return;
        int сопственик_VALUE = класа_име_СМС(상가[INDEX]), Име = Референци_име(константа_SECOND_VALUE[INDEX]), формат_VALUE = Референци_TYPE(константа_SECOND_VALUE[INDEX]);
        if (ГРЕШКА) return;
        if (같은말(сопственик_VALUE, класа_име)) {
            if (Команда != 184) { неуспех_VALUE("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < метод_COUNT; 수++) if (같은말(Име, метод_име_СМС[수]) && 같은말(формат_VALUE, метод_TYPE[수])) {
                if ((метод_пристап[수] & 8) == 0) неуспех_VALUE("method is not static"); else 호출(수);
                return;
            }
            неуспех_VALUE("NoSuchMethodError"); return;
        }
        if (Word_СМС(сопственик_VALUE, "java/io/FileInputStream") || Word_СМС(сопственик_VALUE, "java/io/FileOutputStream")) {
            датотека_Stream_CALL(сопственик_VALUE, Име, формат_VALUE, Команда); return;
        }
        if (Команда == 184 && Word_СМС(сопственик_VALUE, "java/lang/Integer") && Word_СМС(Име, "parseInt") && Word_СМС(формат_VALUE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Команда == 182 && Word_СМС(сопственик_VALUE, "java/io/PrintStream") && (Word_СМС(Име, "println") || Word_СМС(Име, "print"))) {
            int TYPE_VALUE = 0, VALUE = 0;
            if (Word_СМС(формат_VALUE, "(I)V")) { TYPE_VALUE = 1; VALUE = 빼기(1); }
            else if (Word_СМС(формат_VALUE, "(Z)V")) { TYPE_VALUE = 2; VALUE = 빼기(1); }
            else if (Word_СМС(формат_VALUE, "(C)V")) { TYPE_VALUE = 3; VALUE = 빼기(1); }
            else if (Word_СМС(формат_VALUE, "(Ljava/lang/String;)V")) { TYPE_VALUE = 4; VALUE = 빼기(2); }
            else if (!Word_СМС(формат_VALUE, "()V") || !Word_СМС(Име, "println")) неуспех_VALUE("unsupported print descriptor");
            if (빼기(2) != -1) неуспех_VALUE("invalid PrintStream receiver");
            if (ГРЕШКА) return;
            if (TYPE_VALUE == 1) 자바도구.수쓰기(VALUE);
            if (TYPE_VALUE == 2) корисник.Запиши(VALUE == 0 ? "false" : "true");
            if (TYPE_VALUE == 3) корисник.запиши_знак_VALUE(VALUE & 65535);
            if (TYPE_VALUE == 4) запиши_СМС(VALUE);
            if (Word_СМС(Име, "println")) корисник.запиши_знак_VALUE(10);
            return;
        }
        if (Команда == 182 && Word_СМС(сопственик_VALUE, "java/lang/String")) {
            if (Word_СМС(Име, "length") && Word_СМС(формат_VALUE, "()I")) {
                int Референци = 빼기(2); if (објект_VALUE(Референци, 1)) 넣기(힙[Референци + 1], 1); return;
            }
            if (Word_СМС(Име, "charAt") && Word_СМС(формат_VALUE, "(I)C")) {
                int индекс_VALUE = 빼기(1), Референци = 빼기(2);
                if (објект_VALUE(Референци, 1)) {
                    if (индекс_VALUE < 0 || индекс_VALUE >= 힙[Референци + 1]) неуспех_VALUE("StringIndexOutOfBoundsException"); else 넣기(힙[Референци + 2 + индекс_VALUE], 1);
                }
                return;
            }
        }
        if (Word_СМС(сопственик_VALUE, "java/lang/StringBuilder")) {
            if (Команда == 183 && Word_СМС(Име, "<init>") && Word_СМС(формат_VALUE, "()V")) { објект_VALUE(빼기(2), 4); return; }
            if (Команда == 182 && Word_СМС(Име, "toString") && Word_СМС(формат_VALUE, "()Ljava/lang/String;")) {
                int Референци = 빼기(2); if (објект_VALUE(Референци, 4)) 넣기(힙[Референци + 2] == 0 ? вдоми_знак("") : 힙[Референци + 2], 2); return;
            }
            if (Команда == 182 && Word_СМС(Име, "append")) {
                int Текст = 0;
                if (Word_СМС(формат_VALUE, "(I)Ljava/lang/StringBuilder;")) Текст = цифра_знак(빼기(1));
                else if (Word_СМС(формат_VALUE, "(Z)Ljava/lang/StringBuilder;")) Текст = вдоми_знак(빼기(1) == 0 ? "false" : "true");
                else if (Word_СМС(формат_VALUE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALUE = 빼기(1); Текст = додели_Склад(1, 1); if (!ГРЕШКА) 힙[Текст + 2] = VALUE & 65535;
                }
                else if (Word_СМС(формат_VALUE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Текст = 빼기(2); if (Текст == 0) Текст = вдоми_знак("null"); }
                else { неуспех_VALUE("unsupported StringBuilder append"); return; }
                int Референци = 빼기(2); if (!објект_VALUE(Референци, 4) || !објект_VALUE(Текст, 1)) return;
                int предна_VALUE = 힙[Референци + 2], предна_VALUE_должина = предна_VALUE == 0 ? 0 : 힙[предна_VALUE + 1], Назад_VALUE_должина = 힙[Текст + 1];
                int 새글 = додели_Склад(1, предна_VALUE_должина + Назад_VALUE_должина); if (ГРЕШКА) return;
                for (int 수 = 0; 수 < предна_VALUE_должина; 수++) 힙[새글 + 2 + 수] = 힙[предна_VALUE + 2 + 수];
                for (int 수 = 0; 수 < Назад_VALUE_должина; 수++) 힙[새글 + 2 + предна_VALUE_должина + 수] = 힙[Текст + 2 + 수];
                힙[Референци + 2] = 새글; 넣기(Референци, 2); return;
            }
        }
        неуспех_VALUE("unsupported library method");
    }
    static int низа_отвор(int Референци, int индекс_VALUE, int TYPE_VALUE) {
        if (!објект_VALUE(Референци, TYPE_VALUE)) return 0;
        if (индекс_VALUE < 0 || индекс_VALUE >= 힙[Референци + 1]) { неуспех_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Референци + 2 + индекс_VALUE;
    }
    static void Изврши_наредба() {
        int 남음 = 500000;
        while (врами_INDEX >= 0 && !ГРЕШКА) {
            if (--남음 == 0) { неуспех_VALUE("instruction limit (500000)"); break; }
            int Изврши_2 = врами_позиционирање[врами_INDEX], VALUE = 명바();
            if (ГРЕШКА) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = VALUE == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= константа_COUNT) неуспех_VALUE("invalid ldc constant");
                else if (константа_ознака[수] == 3) 넣기(상가[수], 1);
                else if (константа_ознака[수] == 8) 넣기(константа_СМС(상가[수]), 2);
                else неуспех_VALUE("unsupported ldc constant");
                continue;
            }
            if (VALUE == 21 || VALUE == 25) { 지역읽기(명바(), VALUE == 21 ? 1 : 2); continue; }
            if (VALUE >= 26 && VALUE <= 29) { 지역읽기(VALUE - 26, 1); continue; }
            if (VALUE >= 42 && VALUE <= 45) { 지역읽기(VALUE - 42, 2); continue; }
            if (VALUE == 54 || VALUE == 58) { запиши_локален(명바(), VALUE == 54 ? 1 : 2); continue; }
            if (VALUE >= 59 && VALUE <= 62) { запиши_локален(VALUE - 59, 1); continue; }
            if (VALUE >= 75 && VALUE <= 78) { запиши_локален(VALUE - 75, 2); continue; }
            if (VALUE == 46 || VALUE == 50) {
                int индекс_VALUE = 빼기(1), Референци = 빼기(2), отвор_внес = низа_отвор(Референци, индекс_VALUE, VALUE == 46 ? 2 : 3);
                if (!ГРЕШКА) 넣기(힙[отвор_внес], VALUE == 46 ? 1 : 2); continue;
            }
            if (VALUE == 79 || VALUE == 83) {
                int ставка_елемент = 빼기(VALUE == 79 ? 1 : 2), индекс_VALUE = 빼기(1), Референци = 빼기(2), отвор_внес = низа_отвор(Референци, индекс_VALUE, VALUE == 79 ? 2 : 3);
                if (VALUE == 83 && ставка_елемент != 0) објект_VALUE(ставка_елемент, 1);
                if (!ГРЕШКА) 힙[отвор_внес] = ставка_елемент; continue;
            }
            if (VALUE == 87) { 빼기(0); continue; }
            if (VALUE == 89) { int 가 = 빼기(0), TYPE_VALUE = 반환형; 넣기(가, TYPE_VALUE); 넣기(가, TYPE_VALUE); continue; }
            if (VALUE == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 120
                || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), мерка = 0;
                if ((VALUE == 108 || VALUE == 112) && 나 == 0) { неуспех_VALUE("ArithmeticException: / by zero"); continue; }
                if (VALUE == 96) мерка = 가 + 나;
                if (VALUE == 100) мерка = 가 - 나;
                if (VALUE == 104) мерка = 가 * 나;
                if (VALUE == 108) мерка = 가 / 나;
                if (VALUE == 112) мерка = 가 % 나;
                if (VALUE == 120) мерка = 가 << 나;
                if (VALUE == 122) мерка = 가 >> 나;
                if (VALUE == 124) мерка = 가 >>> 나;
                if (VALUE == 126) мерка = 가 & 나;
                if (VALUE == 128) мерка = 가 | 나;
                if (VALUE == 130) мерка = 가 ^ 나;
                넣기(мерка, 1); continue;
            }
            if (VALUE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALUE == 132) {
                int локален_обем = 명바(), 증분 = (byte)명바(); 지역읽기(локален_обем, 1); 넣기(빼기(1) + 증분, 1); запиши_локален(локален_обем, 1); continue;
            }
            if (VALUE >= 145 && VALUE <= 147) {
                int 수 = 빼기(1); 넣기(VALUE == 145 ? (byte)수 : VALUE == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) {
                int одредиште_VALUE = Изврши_2 + (short)명짧(); boolean 갈까 = VALUE == 167;
                if (VALUE >= 153 && VALUE <= 158) {
                    int 수 = 빼기(1); 갈까 = VALUE == 153 ? 수 == 0 : VALUE == 154 ? 수 != 0 : VALUE == 155 ? 수 < 0 : VALUE == 156 ? 수 >= 0 : VALUE == 157 ? 수 > 0 : 수 <= 0;
                } else if (VALUE >= 159 && VALUE <= 166) {
                    int 나 = 빼기(VALUE >= 165 ? 2 : 1), 가 = 빼기(VALUE >= 165 ? 2 : 1);
                    갈까 = VALUE == 159 || VALUE == 165 ? 가 == 나 : VALUE == 160 || VALUE == 166 ? 가 != 나 : VALUE == 161 ? 가 < 나 : VALUE == 162 ? 가 >= 나 : VALUE == 163 ? 가 > 나 : 가 <= 나;
                } else if (VALUE == 198 || VALUE == 199) { int 수 = 빼기(2); 갈까 = VALUE == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) премести_VALUE(одредиште_VALUE); continue;
            }
            if (VALUE == 172 || VALUE == 176 || VALUE == 177) { 반환(VALUE == 172 ? 1 : VALUE == 176 ? 2 : 0); continue; }
            if (VALUE == 178) {
                int 수 = 명짧(); if (!провери_константа(수, 9)) continue;
                if (!Word_СМС(класа_име_СМС(상가[수]), "java/lang/System") || !Word_СМС(Референци_име(константа_SECOND_VALUE[수]), "out")
                    || !Word_СМС(Референци_TYPE(константа_SECOND_VALUE[수]), "Ljava/io/PrintStream;")) неуспех_VALUE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALUE == 182 || VALUE == 183 || VALUE == 184) { CALL_метод(명짧(), VALUE); continue; }
            if (VALUE == 187) {
                int Име = класа_име_СМС(명짧());
                if (Word_СМС(Име, "java/lang/StringBuilder")) 넣기(додели_Склад(4, 1), 2);
                else if (Word_СМС(Име, "java/io/FileInputStream") || Word_СМС(Име, "java/io/FileOutputStream")) {
                    int Референци = додели_Склад(Word_СМС(Име, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!ГРЕШКА) { 힙[Референци + 2] = -1; 넣기(Референци, 2); }
                } else неуспех_VALUE("unsupported object construction");
                continue;
            }
            if (VALUE == 188 || VALUE == 189) {
                if (VALUE == 188) { if (명바() != 10) неуспех_VALUE("only int[] newarray is supported"); }
                else if (!Word_СМС(класа_име_СМС(명짧()), "java/lang/String")) неуспех_VALUE("only String[] anewarray is supported");
                int должина_VALUE = 빼기(1); 넣기(додели_Склад(VALUE == 188 ? 2 : 3, должина_VALUE), 2); continue;
            }
            if (VALUE == 190) {
                int Референци = 빼기(2);
                if (Референци < 1 || Референци >= 힙끝 - 1 || (힙[Референци] != 2 && 힙[Референци] != 3)) неуспех_VALUE("null or invalid array");
                else 넣기(힙[Референци + 1], 1); continue;
            }
            if (VALUE == 192) {
                int Име = класа_име_СМС(명짧()), Референци = 빼기(2);
                if (!Word_СМС(Име, "java/lang/String")) неуспех_VALUE("unsupported checkcast");
                else if (Референци != 0) објект_VALUE(Референци, 1);
                넣기(Референци, 2); continue;
            }
            неуспех_VALUE("unsupported bytecode");
        }
    }
    public static int Изврши_2() {
        if (корисник.인수개수() == 1 && 자바도구.같음(корисник.Аргументи(0), "-version")) {
            корисник.Запиши("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (корисник.인수개수() < 1) { корисник.Запиши("Usage: java CLASS [ARGS]\n"); return 2; }
        int должина_VALUE = 자바도구.Име(датотека_име_СМС, корисник.Аргументи(0));
        if (должина_VALUE < 1 || должина_VALUE > 57) { корисник.Запиши("java: invalid class name\n"); return 2; }
        датотека_име_СМС[должина_VALUE] = '.'; датотека_име_СМС[должина_VALUE + 1] = 'c'; датотека_име_СМС[должина_VALUE + 2] = 'l'; датотека_име_СМС[должина_VALUE + 3] = 'a'; датотека_име_СМС[должина_VALUE + 4] = 's'; датотека_име_СМС[должина_VALUE + 5] = 's';
        Големина = корисник.파일읽기(датотека_име_СМС, Датотека);
        if (Големина < 0) { корисник.Запиши("java: cannot read class: "); 자바도구.수쓰기(Големина); корисник.запиши_знак_VALUE(10); return 1; }
        클래스읽기(); if (ГРЕШКА) return 1;
        int знак_име = константа_СМС(класа_име);
        if (!ГРЕШКА && 힙[знак_име + 1] != должина_VALUE) неуспех_VALUE("class name does not match file");
        for (int 수 = 0; 수 < должина_VALUE && !ГРЕШКА; 수++) if (힙[знак_име + 2 + 수] != датотека_име_СМС[수]) неуспех_VALUE("class name does not match file");
        int внес_поен_VALUE = -1;
        for (int 수 = 0; 수 < метод_COUNT; 수++) if (Word_СМС(метод_име_СМС[수], "main") && Word_СМС(метод_TYPE[수], "([Ljava/lang/String;)V") && (метод_пристап[수] & 9) == 9) внес_поен_VALUE = 수;
        if (внес_поен_VALUE < 0) неуспех_VALUE("public static void main(String[] args) required");
        if (ГРЕШКА) return 1;
        int Аргументи = додели_Склад(3, корисник.인수개수() - 1);
        for (int 수 = 1; 수 < корисник.인수개수() && !ГРЕШКА; 수++) 힙[Аргументи + 1 + 수] = вдоми_знак(корисник.Аргументи(수));
        врами_INDEX = 0; врами_метод[0] = внес_поен_VALUE; врами_позиционирање[0] = метод_Start[внес_поен_VALUE]; локален_VALUE[0] = Аргументи; локален_TYPE[0] = 2;
        Изврши_наредба(); return ГРЕШКА ? 1 : 0;
    }
}
