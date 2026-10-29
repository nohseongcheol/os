// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Датотека/스택/Референци/гранка 경계를 Изврши_наредба 중 검사한다. */
public final class 자바가상기계 {
    static int[] Датотека = new int[16 * 16384], 임시파일 = new int[16384], датотека_име_СМС = new int[512];
    static int[] константа_ознака = new int[8192], 상가 = new int[8192], константа_SECOND_VALUE = new int[8192], низа_Референци_cdb12cb8 = new int[8192];
    static int[] метод_име_СМС = new int[512], метод_TYPE = new int[512], метод_пристап = new int[512], метод_сопственик = new int[512];
    static int[] метод_Start = new int[512], метод_крај = new int[512], метод_Купче = new int[512], 함수지역 = new int[512];
    static int[] метод_аргумент_COUNT = new int[512], метод_аргумент_TYPE = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] локален_VALUE = new int[16384], локален_TYPE = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] врами_метод = new int[128], врами_позиционирање = new int[128], врами_Купче = new int[128], врами_инструкција = new int[128], иницијализирај_врами = new int[128];
    static int[] класа_Дефиниција_име = new int[16], класа_Дефиниција_големина = new int[16], 종부모 = new int[16], класа_Дефиниција_статус = new int[16], класа_отвор_COUNT = new int[16], иницијализирај_класа_Дефиниција = new int[16];
    static int[] класа_интерфејс = new int[16 * 16], класа_интерфејс_COUNT = new int[16];
    static int[] отвор_име = new int[512], отвор_TYPE = new int[512], отвор_сопственик = new int[512], отвор_Дозволи = new int[512], отвор_позиционирање = new int[512], отвор_податоци = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], низа_елемент = new int[32768], Store_цел_број = new int[256];
    static int Големина, 읽기위치, метод_COUNT, класа_име, врами_INDEX = -1, 힙끝 = 1, 반환형;
    static int класа_Дефиниција_COUNT, отвор_COUNT, 잡기수, 현재읽는종, 던진객체, 잠시수, екран_COUNT, збирка_COUNT;
    static int 현재가닥, нишка_COUNT = 1, внес_класа_Дефиниција;
    static int[] нишка_врами = new int[4], нишка_статус = new int[4], нишка_објект = new int[4], нишка_цел = new int[4], 가닥대기 = new int[4];
    static boolean ГРЕШКА, измени_Барање_на_HTTP;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], класа_нишка = new int[16];

    static void неуспех_VALUE(String Word_СМС) {
        if (ГРЕШКА) return;
        int област_CODE = 0;
        if (자바도구.같음(Word_СМС, "ArithmeticException: / by zero")) област_CODE = 4;
        if (자바도구.같음(Word_СМС, "NullPointerException") || 자바도구.같음(Word_СМС, "null or invalid array")) област_CODE = 5;
        if (자바도구.같음(Word_СМС, "ArrayIndexOutOfBoundsException")) област_CODE = 7;
        if (자바도구.같음(Word_СМС, "StringIndexOutOfBoundsException")) област_CODE = 8;
        if (자바도구.같음(Word_СМС, "NumberFormatException")) област_CODE = 10;
        if (자바도구.같음(Word_СМС, "FileNotFoundException: file open failed")) област_CODE = 12;
        if (자바도구.같음(Word_СМС, "IOException: stream closed") || 자바도구.같음(Word_СМС, "IOException: read failed") || 자바도구.같음(Word_СМС, "IOException: write failed")) област_CODE = 11;
        if (자바도구.같음(Word_СМС, "ClassCastException")) област_CODE = 14;
        if (자바도구.같음(Word_СМС, "NegativeArraySizeException")) област_CODE = 15;
        if (област_CODE != 0 && врами_INDEX >= 0) { 예외던짐(област_CODE, Word_СМС); return; }
        корисник.Запиши("JVM error: "); корисник.Запиши(Word_СМС); корисник.запиши_знак_VALUE(10); ГРЕШКА = true;
    }
    static boolean клип(int Изврши_2, int должина_VALUE) {
        if (Изврши_2 < 0 || Изврши_2 >= Датотека.length || должина_VALUE < 0) return false;
        int класа_Дефиниција = Изврши_2 / 16384;
        return Изврши_2 % 16384 <= класа_Дефиниција_големина[класа_Дефиниција] && должина_VALUE <= класа_Дефиниција_големина[класа_Дефиниција] - Изврши_2 % 16384;
    }
    static int бајт_VALUE() {
        if (!клип(읽기위치, 1)) { неуспех_VALUE("truncated class file"); return 0; }
        return Датотека[읽기위치++];
    }
    static int 짧은수() { return бајт_VALUE() << 8 | бајт_VALUE(); }
    static int цел_број() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int должина_VALUE) { if (!клип(읽기위치, должина_VALUE)) неуспех_VALUE("invalid attribute size"); else 읽기위치 += должина_VALUE; }
    static boolean провери_константа(int 수, int 종류) {
        if (수 <= 0 || 수 >= константа_ознака.length || константа_ознака[수] != 종류) { неуспех_VALUE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Изврши_2, int должина_VALUE, String Word_СМС) {
        if (!клип(Изврши_2, должина_VALUE)) return false;
        int 읽는자리 = Изврши_2, 끝 = Изврши_2 + должина_VALUE;
        for (int Loop_INDEX = 0; Loop_INDEX < Word_СМС.length(); Loop_INDEX++) {
            int кодна_точка = Word_СМС.charAt(Loop_INDEX);
            if (кодна_точка > 0 && кодна_точка < 128) { if (읽는자리 >= 끝 || Датотека[읽는자리++] != кодна_точка) return false; }
            else if (кодна_точка < 2048) {
                if (읽는자리 + 2 > 끝 || Датотека[읽는자리++] != (192 | (кодна_точка >> 6)) || Датотека[읽는자리++] != (128 | (кодна_точка & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Датотека[읽는자리++] != (224 | (кодна_точка >> 12)) || Датотека[읽는자리++] != (128 | ((кодна_точка >> 6) & 63)) || Датотека[읽는자리++] != (128 | (кодна_точка & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int VALUE = 짧은수(); return VALUE == 0 ? 0 : 현재읽는종 * 512 + VALUE; }
    static int 명상수() { return метод_сопственик[врами_метод[врами_INDEX]] * 512 + 명짧(); }
    static void 속성건너() {
        int ставка_COUNT = 짧은수();
        for (int 수 = 0; 수 < ставка_COUNT && !ГРЕШКА; 수++) { провери_константа(상번호(), 1); 건너(цел_број()); }
    }
    static int наредба_должина(int VALUE) {
        if (VALUE == 16 || VALUE == 18 || VALUE == 21 || VALUE == 25 || VALUE == 54 || VALUE == 58 || VALUE == 188) return 2;
        if (VALUE == 17 || VALUE == 19 || VALUE == 132 || VALUE >= 153 && VALUE <= 167
            || VALUE >= 178 && VALUE <= 184 || VALUE == 187 || VALUE == 189 || VALUE == 192 || VALUE == 193 || VALUE == 198 || VALUE == 199) return 3;
        if (VALUE == 185 || VALUE == 200) return 5;
        if (VALUE >= 0 && VALUE <= 8 || VALUE >= 26 && VALUE <= 29 || VALUE >= 42 && VALUE <= 46 || VALUE >= 50 && VALUE <= 53
            || VALUE >= 59 && VALUE <= 62 || VALUE >= 75 && VALUE <= 79 || VALUE >= 83 && VALUE <= 95
            || VALUE == 96 || VALUE == 100 || VALUE == 104 || VALUE == 108 || VALUE == 112 || VALUE == 116
            || VALUE == 120 || VALUE == 122 || VALUE == 124 || VALUE == 126 || VALUE == 128 || VALUE == 130
            || VALUE >= 145 && VALUE <= 147 || VALUE == 172 || VALUE == 176 || VALUE == 177 || VALUE == 190 || VALUE == 191
            || VALUE == 194 || VALUE == 195) return 1;
        return 0;
    }
    static int позиционирање_цел_број(int 읽는자리) {
        if (!клип(읽는자리, 4)) { неуспех_VALUE("truncated bytecode operand"); return 0; }
        return Датотека[읽는자리] << 24 | Датотека[읽는자리 + 1] << 16 | Датотека[읽는자리 + 2] << 8 | Датотека[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Изврши_2, int 끝) {
        int VALUE = Датотека[읽는자리], должина_VALUE = наредба_должина(VALUE);
        if (VALUE == 170 || VALUE == 171) {
            int BASE_позиционирање = 읽는자리 + 1;
            while ((BASE_позиционирање - Изврши_2) % 4 != 0) BASE_позиционирање++;
            if (끝 - BASE_позиционирање < (VALUE == 170 ? 12 : 8)) return 0;
            int внес_COUNT = VALUE == 170 ? позиционирање_цел_број(BASE_позиционирање + 8) - позиционирање_цел_број(BASE_позиционирање + 4) + 1 : позиционирање_цел_број(BASE_позиционирање + 4);
            if (внес_COUNT < 0 || внес_COUNT > 2048) return 0;
            должина_VALUE = BASE_позиционирање - 읽는자리 + (VALUE == 170 ? 12 + 4 * внес_COUNT : 8 + 8 * внес_COUNT);
        }
        if (VALUE == 196 && 읽는자리 + 1 < 끝) {
            int Word_податоци = Датотека[읽는자리 + 1]; должина_VALUE = Word_податоци == 132 ? 6 : (Word_податоци == 21 || Word_податоци == 25 || Word_податоци == 54 || Word_податоци == 58) ? 4 : 0;
        }
        return должина_VALUE > 0 && должина_VALUE <= 끝 - 읽는자리 ? должина_VALUE : 0;
    }
    static void провери_одредиште_VALUE(int одредиште_VALUE, int ФУНКЦИЈА_VALUE) {
        if (одредиште_VALUE < метод_Start[ФУНКЦИЈА_VALUE] || одредиште_VALUE >= метод_крај[ФУНКЦИЈА_VALUE] || 경계[одредиште_VALUE] != ФУНКЦИЈА_VALUE + 1) неуспех_VALUE("invalid branch target");
    }
    static void 클래스읽기(int класа_Дефиниција) {
        현재읽는종 = класа_Дефиниција; 읽기위치 = класа_Дефиниција * 16384; Големина = 읽기위치 + класа_Дефиниција_големина[класа_Дефиниција];
        if (цел_број() != 0xcafebabe) { неуспех_VALUE("not a class file"); return; }
        int 부판 = 짧은수(), верзија_VALUE = 짧은수();
        if (верзија_VALUE < 45 || верзија_VALUE > 52 || 부판 != 0) { неуспех_VALUE("supported class versions: 45..52, minor 0"); return; }
        int константа_COUNT = 짧은수(), BASE_позиционирање = класа_Дефиниција * 512;
        if (константа_COUNT < 1 || константа_COUNT > 512) { неуспех_VALUE("constant pool limit (511)"); return; }
        for (int внес_COUNT = 1; внес_COUNT < константа_COUNT && !ГРЕШКА; внес_COUNT++) {
            int 수 = BASE_позиционирање + внес_COUNT, 종류 = бајт_VALUE(); константа_ознака[수] = 종류;
            if (종류 == 1) { константа_SECOND_VALUE[수] = 짧은수(); 상가[수] = 읽기위치; 건너(константа_SECOND_VALUE[수]); }
            else if (종류 == 3) 상가[수] = цел_број();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); константа_SECOND_VALUE[수] = 상번호(); }
            else неуспех_VALUE("unsupported constant type");
        }
        int дозвола_VALUE = 짧은수();
        if ((дозвола_VALUE & (0x2000 | 0x4000)) != 0) неуспех_VALUE("annotation/enum class unsupported");
        класа_Дефиниција_име[класа_Дефиниција] = класа_име_СМС(상번호());
        종부모[класа_Дефиниција] = класа_име_СМС(상번호());
        int интерфејс_COUNT = 짧은수(); if (интерфејс_COUNT > 16) { неуспех_VALUE("interface count limit"); return; }
        класа_интерфејс_COUNT[класа_Дефиниција] = интерфејс_COUNT;
        for (int Loop_INDEX = 0; Loop_INDEX < интерфејс_COUNT; Loop_INDEX++) класа_интерфејс[класа_Дефиниција * 16 + Loop_INDEX] = класа_име_СМС(상번호());
        int поле_COUNT = 짧은수();
        if (поле_COUNT > 512 - отвор_COUNT) { неуспех_VALUE("field count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < поле_COUNT && !ГРЕШКА; Loop_INDEX++) {
            int датотека_INDEX = отвор_COUNT++; отвор_сопственик[датотека_INDEX] = класа_Дефиниција; отвор_Дозволи[датотека_INDEX] = 짧은수(); отвор_име[датотека_INDEX] = 상번호(); отвор_TYPE[датотека_INDEX] = 상번호();
            провери_константа(отвор_име[датотека_INDEX], 1); провери_константа(отвор_TYPE[датотека_INDEX], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[отвор_TYPE[датотека_INDEX]]; int област_CODE = 서술형(읽기위치 + константа_SECOND_VALUE[отвор_TYPE[датотека_INDEX]], false); 읽기위치 = 보존값;
            if ((отвор_Дозволи[датотека_INDEX] & 8) == 0) отвор_позиционирање[датотека_INDEX] = класа_отвор_COUNT[класа_Дефиниција]++;
            int атрибут_податоци = 짧은수();
            for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < атрибут_податоци && !ГРЕШКА; внатрешно_поврзување_позиционирање++) {
                int име_константа = 상번호(), 유효길이 = цел_број();
                if (Word_СМС(име_константа, "ConstantValue") && 유효길이 == 2) {
                    int податоци_VALUE = 상번호();
                    if (област_CODE == 1 && провери_константа(податоци_VALUE, 3)) отвор_податоци[датотека_INDEX] = 상가[податоци_VALUE];
                    else if (област_CODE == 2 && провери_константа(податоци_VALUE, 8)) отвор_податоци[датотека_INDEX] = константа_СМС(상가[податоци_VALUE]);
                } else 건너(유효길이);
            }
        }
        int ставка_COUNT = 짧은수();
        if (ставка_COUNT > 512 - метод_COUNT) { неуспех_VALUE("method count limit (512)"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < ставка_COUNT && !ГРЕШКА; Loop_INDEX++) {
            int 수 = метод_COUNT++; метод_сопственик[수] = класа_Дефиниција;
            метод_пристап[수] = 짧은수(); метод_име_СМС[수] = 상번호(); метод_TYPE[수] = 상번호();
            провери_константа(метод_име_СМС[수], 1); 서술읽기(수);
            if ((метод_пристап[수] & 8) == 0) {
                if (метод_аргумент_COUNT[수] == 16) { неуспех_VALUE("too many instance method arguments"); return; }
                for (int Споредба_позиционирање = метод_аргумент_COUNT[수]; Споредба_позиционирање > 0; Споредба_позиционирање--) метод_аргумент_TYPE[수 * 16 + Споредба_позиционирање] = метод_аргумент_TYPE[수 * 16 + Споредба_позиционирање - 1];
                метод_аргумент_TYPE[수 * 16] = 2; метод_аргумент_COUNT[수]++;
            }
            if ((метод_пристап[수] & 0x100) != 0) неуспех_VALUE("user native method unsupported");
            if (Word_СМС(метод_име_СМС[수], "<clinit>")) иницијализирај_класа_Дефиниција[класа_Дефиниција] = 수 + 1;
            for (int предна_VALUE = 0; предна_VALUE < 수; предна_VALUE++) if (метод_сопственик[предна_VALUE] == класа_Дефиниција && 같은말(метод_име_СМС[предна_VALUE], метод_име_СМС[수]) && 같은말(метод_TYPE[предна_VALUE], метод_TYPE[수])) неуспех_VALUE("duplicate method");
            int атрибут_COUNT = 짧은수();
            for (int атрибут_VALUE = 0; атрибут_VALUE < атрибут_COUNT && !ГРЕШКА; атрибут_VALUE++) {
                int Име = 상번호(), должина_VALUE = цел_број(), Изврши_2 = 읽기위치;
                if (!клип(Изврши_2, должина_VALUE)) { неуспех_VALUE("truncated method attribute"); break; }
                if (Word_СМС(Име, "Code")) {
                    if (метод_Start[수] != 0) неуспех_VALUE("duplicate Code attribute");
                    метод_Купче[수] = 짧은수(); 함수지역[수] = 짧은수(); int CODE_должина = цел_број();
                    if (метод_Купче[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < метод_аргумент_COUNT[수]
                        || CODE_должина < 1 || CODE_должина > 8192) неуспех_VALUE("method memory limits exceeded");
                    метод_Start[수] = 읽기위치; 건너(CODE_должина); метод_крај[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { неуспех_VALUE("exception table limit"); return; }
                    for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 잡는수; внатрешно_поврзување_позиционирање++) {
                        int грешка_Референци = 잡기수++; 잡기함수[грешка_Референци] = 수;
                        잡기시작[грешка_Референци] = метод_Start[수] + 짧은수(); 잡기끝[грешка_Референци] = метод_Start[수] + 짧은수();
                        잡기위치[грешка_Референци] = метод_Start[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[грешка_Референци] = 부호값 == 0 ? 0 : класа_име_СМС(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Изврши_2 + должина_VALUE) неуспех_VALUE("Code attribute size mismatch");
                } else 건너(должина_VALUE);
            }
            if ((метод_пристап[수] & 0x400) != 0) continue;
            if (метод_Start[수] == 0) неуспех_VALUE("missing Code attribute");
            int отвор_внес = метод_Start[수];
            while (отвор_внес < метод_крај[수] && !ГРЕШКА) {
                int должина_VALUE = 길이읽기(отвор_внес, метод_Start[수], метод_крај[수]);
                if (должина_VALUE == 0) { неуспех_VALUE("unsupported or truncated bytecode"); break; }
                경계[отвор_внес] = 수 + 1; отвор_внес += должина_VALUE;
            }
            отвор_внес = метод_Start[수];
            while (отвор_внес < метод_крај[수] && !ГРЕШКА) {
                int VALUE = Датотека[отвор_внес];
                if (VALUE >= 153 && VALUE <= 167 || VALUE == 198 || VALUE == 199) провери_одредиште_VALUE(отвор_внес + (short)(Датотека[отвор_внес + 1] << 8 | Датотека[отвор_внес + 2]), 수);
                if (VALUE == 200) провери_одредиште_VALUE(отвор_внес + позиционирање_цел_број(отвор_внес + 1), 수);
                if (VALUE == 170 || VALUE == 171) {
                    int 읽는자리 = отвор_внес + 1; while ((읽는자리 - метод_Start[수]) % 4 != 0) 읽는자리++;
                    провери_одредиште_VALUE(отвор_внес + позиционирање_цел_број(읽는자리), 수);
                    int внес_COUNT = VALUE == 170 ? позиционирање_цел_број(읽는자리 + 8) - позиционирање_цел_број(읽는자리 + 4) + 1 : позиционирање_цел_број(읽는자리 + 4);
                    읽는자리 += VALUE == 170 ? 12 : 8;
                    for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < внес_COUNT; внатрешно_поврзување_позиционирање++) провери_одредиште_VALUE(отвор_внес + позиционирање_цел_број(읽는자리 + внатрешно_поврзување_позиционирање * (VALUE == 170 ? 4 : 8) + (VALUE == 170 ? 0 : 4)), 수);
                }
                отвор_внес += 길이읽기(отвор_внес, метод_Start[수], метод_крај[수]);
            }
            for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 잡기수; внатрешно_поврзување_позиционирање++) if (잡기함수[внатрешно_поврзување_позиционирање] == 수) {
                провери_одредиште_VALUE(잡기시작[внатрешно_поврзување_позиционирање], 수); провери_одредиште_VALUE(잡기위치[внатрешно_поврзување_позиционирање], 수);
                if (잡기끝[внатрешно_поврзување_позиционирање] != метод_крај[수]) провери_одредиште_VALUE(잡기끝[внатрешно_поврзување_позиционирање], 수);
                if (잡기시작[внатрешно_поврзување_позиционирање] >= 잡기끝[внатрешно_поврзување_позиционирање]) неуспех_VALUE("invalid exception range");
            }
        }
        if (!ГРЕШКА) 속성건너();
        if (읽기위치 != Големина) неуспех_VALUE("extra class file data");
    }
    static int додели_Склад(int 종류, int должина_VALUE) { return 새기억(종류, должина_VALUE); }
    static boolean објект_VALUE(int Референци, int 종류) {
        if (!객체유효(Референци)) return false;
        if (힙[Референци] != 종류) { неуспех_VALUE("object type mismatch"); return false; }
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
        if (반환형 == 2) заштита_VALUE(스택값[отвор_внес]);
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
        if (врами_INDEX % 32 == 31) { неуспех_VALUE("call stack limit (32)"); return; }
        int Следно_ставка = врами_INDEX + 1;
        for (int 수 = 0; 수 < 128; 수++) локален_TYPE[Следно_ставка * 128 + 수] = 0;
        for (int 수 = метод_аргумент_COUNT[ФУНКЦИЈА_VALUE] - 1; 수 >= 0; 수--) {
            локален_VALUE[Следно_ставка * 128 + 수] = 빼기(метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수]); локален_TYPE[Следно_ставка * 128 + 수] = метод_аргумент_TYPE[ФУНКЦИЈА_VALUE * 16 + 수];
        }
        if (ГРЕШКА) return;
        врами_INDEX = Следно_ставка; иницијализирај_врами[врами_INDEX] = 0; врами_метод[врами_INDEX] = ФУНКЦИЈА_VALUE; врами_позиционирање[врами_INDEX] = метод_Start[ФУНКЦИЈА_VALUE]; врами_Купче[врами_INDEX] = 0;
    }
    static void 반환(int TYPE_VALUE) {
        if (TYPE_VALUE != 함수반환[врами_метод[врами_INDEX]]) { неуспех_VALUE("return type mismatch"); return; }
        int VALUE = TYPE_VALUE == 0 ? 0 : 빼기(TYPE_VALUE);
        if (иницијализирај_врами[врами_INDEX] != 0) класа_Дефиниција_статус[иницијализирај_врами[врами_INDEX] - 1] = 2;
        if (틀잠금[врами_INDEX] != 0) { 잠금풀기(틀잠금[врами_INDEX]); 틀잠금[врами_INDEX] = 0; }
        врами_INDEX--; if (врами_INDEX >= 현재가닥 * 32 && TYPE_VALUE != 0) 넣기(VALUE, TYPE_VALUE);
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
                if (VALUE < 1) { неуспех_VALUE("invalid file stream path"); return; }
                Stream_датотека_име[отвор_внес] = VALUE;
            }
            Stream_датотека_име[должина_VALUE] = 0;
            int 서술자 = корисник.파일서술자열기(Stream_датотека_име, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { неуспех_VALUE("FileNotFoundException: file open failed"); return; }
            힙[Stream_VALUE + 2] = 서술자; 힙[Stream_VALUE + 3] = 1;
            return;
        }
        if (Команда != 182) { неуспех_VALUE("invalid file stream invocation"); return; }
        if ((출력 && Word_СМС(Име, "write") || !출력 && Word_СМС(Име, "read"))
            && (Word_СМС(формат_VALUE, 출력 ? "([B)V" : "([B)I") || Word_СМС(формат_VALUE, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean клип_VALUE = Word_СМС(формат_VALUE, 출력 ? "([BII)V" : "([BII)I");
            int внес_COUNT = клип_VALUE ? 빼기(1) : 0, 시작점 = клип_VALUE ? 빼기(1) : 0, податоци_низа = 빼기(2), објект_Референци = 빼기(2);
            if (!објект_VALUE(податоци_низа, 20) || !објект_VALUE(објект_Референци, 종류)) return;
            if (!клип_VALUE) внес_COUNT = 힙[податоци_низа + 1];
            if (시작점 < 0 || внес_COUNT < 0 || 시작점 > 힙[податоци_низа + 1] - внес_COUNT) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[објект_Референци + 3] == 0 || 힙[објект_Референци + 2] < 0) { неуспех_VALUE("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < внес_COUNT && !ГРЕШКА) {
                int 반환값 = 출력 ? корисник.파일한바이트쓰기(힙[објект_Референци + 2], 힙[податоци_низа + 2 + 시작점 + 완료수]) : корисник.파일한바이트읽기(힙[објект_Референци + 2]);
                if (반환값 < 0) { неуспех_VALUE(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[податоци_низа + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(внес_COUNT != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Word_СМС(Име, "flush") && Word_СМС(формат_VALUE, "()V")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 종류) && 힙[објект_Референци + 2] < 0) неуспех_VALUE("IOException: stream closed"); return; }
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
            if (мерка < -1) неуспех_VALUE("IOException: read failed"); else 넣기(мерка == 256 ? -1 : мерка, 1);
        } else if (корисник.파일한바이트쓰기(서술자, VALUE) != 1) неуспех_VALUE("IOException: write failed");
    }
    static void CALL_метод(int INDEX, int Команда) {
        if (INDEX <= 0 || INDEX >= константа_ознака.length || (константа_ознака[INDEX] != 10 && константа_ознака[INDEX] != 11)) { неуспех_VALUE("invalid method reference"); return; }
        int сопственик_VALUE = класа_име_СМС(상가[INDEX]), Име = Референци_име(константа_SECOND_VALUE[INDEX]), формат_VALUE = Референци_TYPE(константа_SECOND_VALUE[INDEX]);
        if (ГРЕШКА) return;
        if (기본호출(сопственик_VALUE, Име, формат_VALUE, Команда)) return;
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
        int класа_Дефиниција = FIND_класа_Дефиниција(сопственик_VALUE); if (класа_Дефиниција < 0 || ГРЕШКА) return;
        int датотека_INDEX = FIND_метод(класа_Дефиниција, Име, формат_VALUE);
        if (датотека_INDEX < 0) {
            for (int кодна_точка = класа_Дефиниција, внес_COUNT = 0; кодна_точка >= 0 && внес_COUNT < 16; внес_COUNT++, кодна_точка = 부모종(кодна_точка))
                if (Word_СМС(종부모[кодна_точка], "java/lang/Thread")) { 가닥호출(Име, формат_VALUE, Команда); return; }
            неуспех_VALUE("NoSuchMethodError"); return;
        }
        if (((метод_пристап[датотека_INDEX] & 8) != 0) != (Команда == 184)) { неуспех_VALUE("method static/instance mismatch"); return; }
        if (Команда == 184) { if (!иницијализирај(метод_сопственик[датотека_INDEX], врами_инструкција[врами_INDEX])) return; }
        else {
            int 읽는자리 = врами_Купче[врами_INDEX] - метод_аргумент_COUNT[датотека_INDEX];
            if (읽는자리 < 0 || 스택형[врами_INDEX * 128 + 읽는자리] != 2) { неуспех_VALUE("invalid method receiver"); return; }
            int објект_Референци = 스택값[врами_INDEX * 128 + 읽는자리];
            if (!객체유효(објект_Референци)) return;
            if (힙[објект_Референци] < 32 || !종포함(힙[објект_Референци] - 32, сопственик_VALUE)) { неуспех_VALUE("method receiver type mismatch"); return; }
            if (Команда != 183) датотека_INDEX = FIND_метод(힙[објект_Референци] - 32, Име, формат_VALUE);
        }
        if (датотека_INDEX < 0 || (метод_пристап[датотека_INDEX] & 0x400) != 0) { неуспех_VALUE("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((метод_пристап[датотека_INDEX] & 32) != 0) {
            if (Команда == 184) { int кодна_точка = метод_сопственик[датотека_INDEX]; if (종잠금[кодна_точка] == 0) 종잠금[кодна_точка] = додели_Склад(8, 0); 잠금참조 = 종잠금[кодна_точка]; }
            else 잠금참조 = 스택값[врами_INDEX * 128 + врами_Купче[врами_INDEX] - метод_аргумент_COUNT[датотека_INDEX]];
            if (!잠금얻기(잠금참조)) { if (!ГРЕШКА) врами_позиционирање[врами_INDEX] = врами_инструкција[врами_INDEX]; return; }
        }
        호출(датотека_INDEX); if (!ГРЕШКА) 틀잠금[врами_INDEX] = 잠금참조;
    }
    static boolean 배열저장가능(int низа_Референци, int податоци_VALUE) {
        if (податоци_VALUE == 0 || низа_елемент[низа_Референци] == 0) return true;
        boolean 성공여부 = низа_елемент[низа_Референци] == -1 ? (податоци_VALUE > 0 && податоци_VALUE < 힙끝 && 힙[податоци_VALUE] == 1) : 맞는객체(податоци_VALUE, низа_елемент[низа_Референци]);
        if (!성공여부 && !ГРЕШКА) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int низа_отвор(int Референци, int индекс_VALUE, int TYPE_VALUE) {
        if (!објект_VALUE(Референци, TYPE_VALUE)) return 0;
        if (индекс_VALUE < 0 || индекс_VALUE >= 힙[Референци + 1]) { неуспех_VALUE("ArrayIndexOutOfBoundsException"); return 0; }
        return Референци + 2 + индекс_VALUE;
    }
    static void Изврши_наредба() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (ГРЕШКА) { if (던진객체 != 0) рачка_исклучок(); if (ГРЕШКА || врами_INDEX < 현재가닥 * 32) break; }
            if (врами_INDEX < 현재가닥 * 32 || измени_Барање_на_HTTP || --조각 == 0) { if (!SWITCH_нишка()) break; 조각 = 100; }
            if (врами_INDEX == 0 && класа_Дефиниција_статус[внес_класа_Дефиниција] != 2 && !иницијализирај(внес_класа_Дефиниција, врами_позиционирање[врами_INDEX])) continue;
            if (врами_INDEX == 현재가닥 * 32 && 현재가닥 != 0 && (метод_пристап[врами_метод[врами_INDEX]] & 32) != 0 && 틀잠금[врами_INDEX] == 0) {
                int објект_Референци = нишка_цел[현재가닥]; if (!잠금얻기(објект_Референци)) { if (ГРЕШКА) break; continue; } 틀잠금[врами_INDEX] = објект_Референци;
            }
            잠시수 = 0;
            if (--남음 == 0) { неуспех_VALUE("instruction limit (500000)"); break; }
            int Изврши_2 = врами_позиционирање[врами_INDEX]; врами_инструкција[врами_INDEX] = Изврши_2; int VALUE = 명바();
            if (ГРЕШКА) break;
            if (VALUE == 0) continue;
            if (VALUE == 1) { 넣기(0, 2); continue; }
            if (VALUE >= 2 && VALUE <= 8) { 넣기(VALUE - 3, 1); continue; }
            if (VALUE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALUE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALUE == 18 || VALUE == 19) {
                int 수 = метод_сопственик[врами_метод[врами_INDEX]] * 512 + (VALUE == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= константа_ознака.length) неуспех_VALUE("invalid ldc constant");
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
            if (VALUE == 46 || VALUE >= 50 && VALUE <= 53) {
                int внес_позиционирање = 빼기(1), објект_Референци = 빼기(2), област_CODE = VALUE == 46 ? 2 : VALUE == 50 ? 3 : VALUE == 51 ? 20 : VALUE == 52 ? 22 : 23;
                if (VALUE == 51 && објект_Референци > 0 && објект_Референци < 힙끝 && 힙[објект_Референци] == 21) област_CODE = 21;
                int 읽는자리 = низа_отвор(објект_Референци, внес_позиционирање, област_CODE); if (!ГРЕШКА) 넣기(힙[읽는자리], VALUE == 50 ? 2 : 1); continue;
            }
            if (VALUE == 79 || VALUE >= 83 && VALUE <= 86) {
                int внес_Референци = 빼기(VALUE == 83 ? 2 : 1), внес_позиционирање = 빼기(1), објект_Референци = 빼기(2), област_CODE = VALUE == 79 ? 2 : VALUE == 83 ? 3 : VALUE == 84 ? 20 : VALUE == 85 ? 22 : 23;
                if (VALUE == 84 && објект_Референци > 0 && објект_Референци < 힙끝 && 힙[објект_Референци] == 21) област_CODE = 21;
                int 읽는자리 = низа_отвор(објект_Референци, внес_позиционирање, област_CODE);
                if (!ГРЕШКА && област_CODE == 3 && !배열저장가능(објект_Референци, внес_Референци)) continue;
                if (!ГРЕШКА) 힙[읽는자리] = област_CODE == 20 ? (byte)внес_Референци : област_CODE == 21 ? внес_Референци & 1 : област_CODE == 22 ? (char)внес_Референци : област_CODE == 23 ? (short)внес_Референци : внес_Референци;
                continue;
            }
            if (VALUE >= 87 && VALUE <= 95) { Купче_инструкција(VALUE); continue; }
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
            if (VALUE >= 178 && VALUE <= 181) { 필드호출(명상수(), VALUE, Изврши_2); continue; }
            if (VALUE >= 182 && VALUE <= 185) {
                int 부호값 = 명상수();
                if (VALUE == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { неуспех_VALUE("invalid invokeinterface operands"); continue; } }
                CALL_метод(부호값, VALUE); continue;
            }
            if (VALUE == 187) { 새객체(класа_име_СМС(명상수()), Изврши_2); continue; }
            if (VALUE == 188 || VALUE == 189) {
                int област_CODE = 3, компонента = 0;
                if (VALUE == 188) { int 임시값 = 명바(); област_CODE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else компонента = класа_име_СМС(명상수());
                if (област_CODE == 0) { неуспех_VALUE("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), објект_Референци = додели_Склад(област_CODE, 유효길이); if (!ГРЕШКА) низа_елемент[објект_Референци] = компонента; 넣기(објект_Референци, 2); continue;
            }
            if (VALUE == 190) {
                int објект_Референци = 빼기(2);
                if (객체유효(објект_Референци)) { int Споредба_позиционирање = 힙[објект_Референци]; if (Споредба_позиционирање != 2 && Споредба_позиционирање != 3 && (Споредба_позиционирање < 20 || Споредба_позиционирање > 23)) неуспех_VALUE("not an array"); else 넣기(힙[објект_Референци + 1], 1); }
                continue;
            }
            if (VALUE == 191) {
                int објект_Референци = 빼기(2); if (객체유효(објект_Референци)) { if (힙[објект_Референци] != 9) неуспех_VALUE("athrow requires supported Throwable"); else { 던진객체 = објект_Референци; ГРЕШКА = true; } }
                continue;
            }
            if (VALUE == 192 || VALUE == 193) {
                int име_константа = класа_име_СМС(명상수()), објект_Референци = 빼기(2); boolean MATCH = 맞는객체(објект_Референци, име_константа);
                if (VALUE == 193) 넣기(објект_Референци != 0 && MATCH ? 1 : 0, 1);
                else { if (!MATCH && !ГРЕШКА) неуспех_VALUE("ClassCastException"); 넣기(објект_Референци, 2); }
                continue;
            }
            if (VALUE == 170 || VALUE == 171) {
                int 읽는자리 = Изврши_2 + 1, датотека_INDEX = врами_метод[врами_INDEX], Клуч_Референци = 빼기(1);
                while ((읽는자리 - метод_Start[датотека_INDEX]) % 4 != 0) 읽는자리++;
                int цел_адреса = позиционирање_цел_број(읽는자리);
                if (VALUE == 170) { int 낮은값 = позиционирање_цел_број(읽는자리 + 4), 높은값 = позиционирање_цел_број(읽는자리 + 8); if (Клуч_Референци >= 낮은값 && Клуч_Референци <= 높은값) цел_адреса = позиционирање_цел_број(읽는자리 + 12 + (Клуч_Референци - 낮은값) * 4); }
                else { int 총수 = позиционирање_цел_број(읽는자리 + 4); for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (позиционирање_цел_број(읽는자리 + 8 + Loop_INDEX * 8) == Клуч_Референци) цел_адреса = позиционирање_цел_број(읽는자리 + 12 + Loop_INDEX * 8); }
                премести_VALUE(Изврши_2 + цел_адреса); continue;
            }
            if (VALUE == 200) { премести_VALUE(Изврши_2 + позиционирање_цел_број(Изврши_2 + 1)); continue; }
            if (VALUE == 194 || VALUE == 195) {
                int објект_Референци = 빼기(2);
                if (VALUE == 195) 잠금풀기(објект_Референци);
                else if (!잠금얻기(објект_Референци) && !ГРЕШКА) { 넣기(објект_Референци, 2); врами_позиционирање[врами_INDEX] = Изврши_2; }
                continue;
            }
            if (VALUE == 196) {
                int наредба_CODE = 명바(), внес_позиционирање = 명짧();
                if (наредба_CODE == 21 || наредба_CODE == 25) 지역읽기(внес_позиционирање, наредба_CODE == 21 ? 1 : 2);
                else if (наредба_CODE == 54 || наредба_CODE == 58) запиши_локален(внес_позиционирање, наредба_CODE == 54 ? 1 : 2);
                else if (наредба_CODE == 132) { int DELTA_VALUE = (short)명짧(); 지역읽기(внес_позиционирање, 1); 넣기(빼기(1) + DELTA_VALUE, 1); запиши_локален(внес_позиционирање, 1); }
                else неуспех_VALUE("unsupported wide opcode");
                continue;
            }
            неуспех_VALUE("unsupported bytecode");
        }
    }
    static int FIND_класа_Дефиниција(int Име) {
        for (int Loop_INDEX = 0; Loop_INDEX < класа_Дефиниција_COUNT; Loop_INDEX++) if (класа_Дефиниција_име[Loop_INDEX] != 0 && 같은말(класа_Дефиниција_име[Loop_INDEX], Име)) return Loop_INDEX;
        return вчитај_класа_Дефиниција(константа_СМС(Име));
    }
    static int вчитај_класа_Дефиниција(int име_низа) {
        if (!објект_VALUE(име_низа, 1)) return -1;
        int должина_VALUE = 힙[име_низа + 1];
        if (должина_VALUE < 1 || должина_VALUE > 505 || класа_Дефиниција_COUNT == 16) { неуспех_VALUE("class name/count limit"); return -1; }
        for (int Loop_INDEX = 0; Loop_INDEX < должина_VALUE; Loop_INDEX++) { int кодна_точка = 힙[име_низа + 2 + Loop_INDEX]; датотека_име_СМС[Loop_INDEX] = кодна_точка == '/' ? '.' : кодна_точка; }
        датотека_име_СМС[должина_VALUE] = '.'; датотека_име_СМС[должина_VALUE + 1] = 'c'; датотека_име_СМС[должина_VALUE + 2] = 'l'; датотека_име_СМС[должина_VALUE + 3] = 'a'; датотека_име_СМС[должина_VALUE + 4] = 's'; датотека_име_СМС[должина_VALUE + 5] = 's'; датотека_име_СМС[должина_VALUE + 6] = 0;
        int Големина = корисник.파일읽기(датотека_име_СМС, 임시파일);
        if (Големина < 0) { неуспех_VALUE("ClassNotFoundException"); return -1; }
        int класа_Дефиниција = класа_Дефиниција_COUNT++; класа_Дефиниција_големина[класа_Дефиниција] = Големина;
        for (int Loop_INDEX = 0; Loop_INDEX < Големина; Loop_INDEX++) Датотека[класа_Дефиниција * 16384 + Loop_INDEX] = 임시파일[Loop_INDEX];
        클래스읽기(класа_Дефиниција); if (ГРЕШКА) return -1;
        int реален_податоци = константа_СМС(класа_Дефиниција_име[класа_Дефиниција]);
        if (!글같음(реален_податоци, име_низа, true)) { неуспех_VALUE("class name does not match file"); return -1; }
        int 부모 = 종부모[класа_Дефиниција];
        if (부모 != 0 && !Word_СМС(부모, "java/lang/Object") && !Word_СМС(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = FIND_класа_Дефиниција(부모);
            if (ГРЕШКА || 위 < 0) return -1;
            int 읽는자리 = 위, фаза_COUNT = 0;
            while (읽는자리 >= 0 && фаза_COUNT++ < 16) {
                if (읽는자리 == класа_Дефиниција) { неуспех_VALUE("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = класа_отвор_COUNT[위];
            for (int датотека_INDEX = 0; датотека_INDEX < отвор_COUNT; датотека_INDEX++) if (отвор_сопственик[датотека_INDEX] == класа_Дефиниција && (отвор_Дозволи[датотека_INDEX] & 8) == 0) отвор_позиционирање[датотека_INDEX] += 시작변위;
            класа_отвор_COUNT[класа_Дефиниција] += 시작변위;
        }
        return класа_Дефиниција;
    }
    static int 부모종(int класа_Дефиниција) {
        int Име = 종부모[класа_Дефиниција];
        for (int Loop_INDEX = 0; Loop_INDEX < класа_Дефиниција_COUNT; Loop_INDEX++) if (Име != 0 && класа_Дефиниција_име[Loop_INDEX] != 0 && 같은말(класа_Дефиниција_име[Loop_INDEX], Име)) return Loop_INDEX;
        return -1;
    }
    static int FIND_метод(int класа_Дефиниција, int Име, int формат_VALUE) {
        for (int 깊이 = 0; класа_Дефиниција >= 0 && 깊이 < 16; 깊이++, класа_Дефиниција = 부모종(класа_Дефиниција)) {
            for (int Loop_INDEX = 0; Loop_INDEX < метод_COUNT; Loop_INDEX++) if (метод_сопственик[Loop_INDEX] == класа_Дефиниција && 같은말(метод_име_СМС[Loop_INDEX], Име) && 같은말(метод_TYPE[Loop_INDEX], формат_VALUE)) return Loop_INDEX;
        }
        return -1;
    }
    static int име_метод(int класа_Дефиниција, String Име, String формат_VALUE) {
        for (int 깊이 = 0; класа_Дефиниција >= 0 && 깊이 < 16; 깊이++, класа_Дефиниција = 부모종(класа_Дефиниција))
            for (int Loop_INDEX = 0; Loop_INDEX < метод_COUNT; Loop_INDEX++) if (метод_сопственик[Loop_INDEX] == класа_Дефиниција && Word_СМС(метод_име_СМС[Loop_INDEX], Име) && Word_СМС(метод_TYPE[Loop_INDEX], формат_VALUE)) return Loop_INDEX;
        return -1;
    }
    static int 형종류(int Име) { return Датотека[상가[Име]] == 'L' || Датотека[상가[Име]] == '[' ? 2 : 1; }
    static boolean иницијализирај(int класа_Дефиниција, int наредба_Start) {
        if (класа_Дефиниција < 0 || ГРЕШКА) return false;
        if (класа_Дефиниција_статус[класа_Дефиниција] == 3) { неуспех_VALUE("NoClassDefFoundError: initialization failed"); return false; }
        if (класа_Дефиниција_статус[класа_Дефиниција] == 1 && класа_нишка[класа_Дефиниција] != 현재가닥) { врами_позиционирање[врами_INDEX] = наредба_Start; измени_Барање_на_HTTP = true; return false; }
        if (класа_Дефиниција_статус[класа_Дефиниција] != 0) return true;
        int 위 = 부모종(класа_Дефиниција);
        if (위 >= 0 && !иницијализирај(위, наредба_Start)) return false;
        класа_Дефиниција_статус[класа_Дефиниција] = 1; класа_нишка[класа_Дефиниција] = 현재가닥;
        if (иницијализирај_класа_Дефиниција[класа_Дефиниција] != 0) {
            врами_позиционирање[врами_INDEX] = наредба_Start;
            호출(иницијализирај_класа_Дефиниција[класа_Дефиниција] - 1); if (!ГРЕШКА) иницијализирај_врами[врами_INDEX] = класа_Дефиниција + 1;
            return false;
        }
        класа_Дефиниција_статус[класа_Дефиниција] = 2; return true;
    }
    static void 필드호출(int INDEX, int Команда, int Изврши_2) {
        if (!провери_константа(INDEX, 9)) return;
        int сопственик_VALUE = класа_име_СМС(상가[INDEX]), Име = Референци_име(константа_SECOND_VALUE[INDEX]), формат_VALUE = Референци_TYPE(константа_SECOND_VALUE[INDEX]);
        if (Word_СМС(сопственик_VALUE, "java/lang/System") && (Word_СМС(Име, "out") || Word_СМС(Име, "err")) && Word_СМС(формат_VALUE, "Ljava/io/PrintStream;") && Команда == 178) { 넣기(-1, 2); return; }
        int класа_Дефиниција = FIND_класа_Дефиниција(сопственик_VALUE); if (класа_Дефиниција < 0 || ГРЕШКА) return;
        int 찾음 = -1;
        for (int 읽는자리 = класа_Дефиниција, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int датотека_INDEX = 0; датотека_INDEX < отвор_COUNT; датотека_INDEX++) if (отвор_сопственик[датотека_INDEX] == 읽는자리 && 같은말(отвор_име[датотека_INDEX], Име) && 같은말(отвор_TYPE[датотека_INDEX], формат_VALUE)) 찾음 = датотека_INDEX;
        if (찾음 < 0) { неуспех_VALUE("NoSuchFieldError"); return; }
        boolean статичен_VALUE = Команда == 178 || Команда == 179;
        if (статичен_VALUE != ((отвор_Дозволи[찾음] & 8) != 0)) { неуспех_VALUE("field static/instance mismatch"); return; }
        if (статичен_VALUE && !иницијализирај(отвор_сопственик[찾음], Изврши_2)) return;
        int TYPE_VALUE = 형종류(формат_VALUE), VALUE = 0;
        if (Команда == 179 || Команда == 181) VALUE = 빼기(TYPE_VALUE);
        if (статичен_VALUE) { if (Команда == 178) 넣기(отвор_податоци[찾음], TYPE_VALUE); else if (!ГРЕШКА) отвор_податоци[찾음] = VALUE; return; }
        int објект_Референци = 빼기(2);
        if (!객체유효(објект_Референци)) return;
        if (힙[објект_Референци] < 32 || !종포함(힙[објект_Референци] - 32, сопственик_VALUE)) { неуспех_VALUE("field receiver type mismatch"); return; }
        int 보관칸 = објект_Референци + 2 + отвор_позиционирање[찾음];
        if (Команда == 180) 넣기(힙[보관칸], TYPE_VALUE);
        else if (!ГРЕШКА) { 힙[보관칸] = VALUE; 힙참조[보관칸] = TYPE_VALUE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int класа_Дефиниција, int Име) {
        for (int 중첩깊이 = 0; класа_Дефиниција >= 0 && 중첩깊이 < 16; 중첩깊이++, класа_Дефиниција = 부모종(класа_Дефиниција)) {
            if (같은말(класа_Дефиниција_име[класа_Дефиниција], Име) || (종부모[класа_Дефиниција] != 0 && 같은말(종부모[класа_Дефиниција], Име))) return true;
            for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < класа_интерфејс_COUNT[класа_Дефиниција]; внатрешно_поврзување_позиционирање++) if (같은말(класа_интерфејс[класа_Дефиниција * 16 + внатрешно_поврзување_позиционирање], Име)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int бајт_податоци, boolean ПАТЕКА) {
        if (첫값 == бајт_податоци) return true;
        if (첫값 <= 0 || бајт_податоци <= 0 || 힙[첫값] != 1 || 힙[бајт_податоци] != 1 || 힙[첫값 + 1] != 힙[бајт_податоци + 1]) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) {
            int координата_х = 힙[첫값 + 2 + Loop_INDEX], 세로좌표 = 힙[бајт_податоци + 2 + Loop_INDEX];
            if (ПАТЕКА) { if (координата_х == '.') координата_х = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (координата_х != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int објект_Референци) {
        if (објект_Референци == 0) { неуспех_VALUE("NullPointerException"); return false; }
        if (објект_Референци < 1 || објект_Референци >= 힙끝 || 힙폭[објект_Референци] < 2 || 힙[објект_Референци] == 0) { неуспех_VALUE("invalid object reference"); return false; }
        return true;
    }
    static void заштита_VALUE(int објект_Референци) {
        if (објект_Референци > 0 && објект_Референци < 힙끝 && 힙폭[објект_Референци] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = објект_Референци;
    }
    static void прикажи_VALUE(int објект_Референци) {
        if (објект_Референци > 0 && објект_Референци < 힙끝 && 힙폭[објект_Референци] >= 2 && 힙[објект_Референци] != 0 && 힙표시[објект_Референци] == 0) {
            힙표시[објект_Референци] = 1; 표시대기[екран_COUNT++] = објект_Референци;
        }
    }
    static void 수거() {
        екран_COUNT = 0; збирка_COUNT++;
        for (int провери_позиционирање_9b8e3629 = 1; провери_позиционирање_9b8e3629 < 힙끝; провери_позиционирање_9b8e3629 += 힙폭[провери_позиционирање_9b8e3629]) 힙표시[провери_позиционирање_9b8e3629] = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < низа_Референци_cdb12cb8.length; Loop_INDEX++) прикажи_VALUE(низа_Референци_cdb12cb8[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < отвор_COUNT; Loop_INDEX++) if ((отвор_Дозволи[Loop_INDEX] & 8) != 0 && 형종류(отвор_TYPE[Loop_INDEX]) == 2) прикажи_VALUE(отвор_податоци[Loop_INDEX]);
        for (int 임시값 = 0; 임시값 < нишка_COUNT; 임시값++) {
            прикажи_VALUE(нишка_објект[임시값]); прикажи_VALUE(нишка_цел[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? врами_INDEX : нишка_врами[임시값];
            for (int датотека_INDEX = 임시값 * 32; датотека_INDEX <= 꼭대기자리; датотека_INDEX++) {
                for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 함수지역[врами_метод[датотека_INDEX]]; внатрешно_поврзување_позиционирање++) if (локален_TYPE[датотека_INDEX * 128 + внатрешно_поврзување_позиционирање] == 2) прикажи_VALUE(локален_VALUE[датотека_INDEX * 128 + внатрешно_поврзување_позиционирање]);
                for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < врами_Купче[датотека_INDEX]; внатрешно_поврзување_позиционирање++) if (스택형[датотека_INDEX * 128 + внатрешно_поврзување_позиционирање] == 2) прикажи_VALUE(스택값[датотека_INDEX * 128 + внатрешно_поврзување_позиционирање]);
            }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 화면참조.length; Loop_INDEX++) прикажи_VALUE(화면참조[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < 나중수; Loop_INDEX++) прикажи_VALUE(나중실행[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < Store_цел_број.length; Loop_INDEX++) прикажи_VALUE(Store_цел_број[Loop_INDEX]);
        for (int Loop_INDEX = 0; Loop_INDEX < класа_Дефиниција_COUNT; Loop_INDEX++) прикажи_VALUE(종잠금[Loop_INDEX]);
        for (int провери_позиционирање_9b8e3629 = 1; провери_позиционирање_9b8e3629 < 힙끝; провери_позиционирање_9b8e3629 += 힙폭[провери_позиционирање_9b8e3629]) if (잠금깊이[провери_позиционирање_9b8e3629] > 0) прикажи_VALUE(провери_позиционирање_9b8e3629);
        прикажи_VALUE(던진객체);
        for (int Loop_INDEX = 0; Loop_INDEX < 잠시수; Loop_INDEX++) прикажи_VALUE(잠시참조[Loop_INDEX]);
        while (екран_COUNT > 0) {
            int објект_Референци = 표시대기[--екран_COUNT], област_CODE = 힙[објект_Референци];
            for (int Loop_INDEX = објект_Референци + 2; Loop_INDEX < објект_Референци + 힙폭[објект_Референци]; Loop_INDEX++) if (област_CODE == 3 || област_CODE == 4 || 힙참조[Loop_INDEX] != 0) прикажи_VALUE(힙[Loop_INDEX]);
        }
        for (int провери_позиционирање_9b8e3629 = 1; провери_позиционирање_9b8e3629 < 힙끝; провери_позиционирање_9b8e3629 += 힙폭[провери_позиционирање_9b8e3629]) if (힙표시[провери_позиционирање_9b8e3629] == 0) 힙[провери_позиционирање_9b8e3629] = 0;
        for (int провери_позиционирање_9b8e3629 = 1; провери_позиционирање_9b8e3629 < 힙끝; провери_позиционирање_9b8e3629 += 힙폭[провери_позиционирање_9b8e3629]) if (힙[провери_позиционирање_9b8e3629] == 0) {
            while (провери_позиционирање_9b8e3629 + 힙폭[провери_позиционирање_9b8e3629] < 힙끝 && 힙[провери_позиционирање_9b8e3629 + 힙폭[провери_позиционирање_9b8e3629]] == 0) { int Следно_позиционирање = провери_позиционирање_9b8e3629 + 힙폭[провери_позиционирање_9b8e3629]; 힙폭[провери_позиционирање_9b8e3629] += 힙폭[Следно_позиционирање]; 힙폭[Следно_позиционирање] = 0; }
            if (провери_позиционирање_9b8e3629 + 힙폭[провери_позиционирање_9b8e3629] == 힙끝) { 힙끝 = провери_позиционирање_9b8e3629; break; }
        }
    }
    static int 새기억(int 종류, int должина_VALUE) {
        if (должина_VALUE < 0) { неуспех_VALUE("NegativeArraySizeException"); return 0; }
        if (должина_VALUE > 힙.length - 3) { неуспех_VALUE("object heap exhausted"); return 0; }
        int 필요수 = должина_VALUE + 2, објект_Референци = 0;
        if (필요수 <= 힙.length - 힙끝) { објект_Референци = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { објект_Референци = 읽는자리; break; }
            if (објект_Референци != 0) {
                int 남은길이 = 힙폭[објект_Референци] - 필요수;
                if (남은길이 >= 2) { 힙폭[објект_Референци + 필요수] = 남은길이; 힙[објект_Референци + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { објект_Референци = 힙끝; 힙끝 += 필요수; }
        }
        if (објект_Референци == 0) { неуспех_VALUE("object heap exhausted"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < 필요수; Loop_INDEX++) { 힙[објект_Референци + Loop_INDEX] = 0; 힙참조[објект_Референци + Loop_INDEX] = 0; 힙폭[објект_Референци + Loop_INDEX] = 0; }
        низа_елемент[објект_Референци] = 0;
        힙폭[објект_Референци] = 필요수; 힙[објект_Референци] = 종류; 힙[објект_Референци + 1] = должина_VALUE; заштита_VALUE(објект_Референци); return објект_Референци;
    }
    static int исклучок_класа(String име_константа) {
        if (자바도구.같음(име_константа, "java/lang/Throwable")) return 1;
        if (자바도구.같음(име_константа, "java/lang/Exception")) return 2;
        if (자바도구.같음(име_константа, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(име_константа, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(име_константа, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(име_константа, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(име_константа, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(име_константа, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(име_константа, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(име_константа, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(име_константа, "java/io/IOException")) return 11;
        if (자바도구.같음(име_константа, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(име_константа, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(име_константа, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(име_константа, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int исклучок_константа(int Име) {
        for (int Loop_INDEX = 1; Loop_INDEX <= 41; Loop_INDEX++) if (Word_СМС(Име, исклучок_име(Loop_INDEX))) return Loop_INDEX;
        return 0;
    }
    static String исклучок_име(int сметка_VALUE) {
        if (сметка_VALUE == 40) return "java/lang/InterruptedException";
        if (сметка_VALUE == 41) return "Македонски/자체/대기중단예외";
        if (сметка_VALUE == 39) return "java/net/SocketException";
        if (сметка_VALUE == 20) return "Македонски/자체/исклучок";
        if (сметка_VALUE == 21) return "Македонски/자체/실행예외";
        if (сметка_VALUE == 22) return "Македонски/자체/В_И_исклучок";
        if (сметка_VALUE == 23) return "Македонски/자체/почекај_TIMEOUT_исклучок";
        if (сметка_VALUE == 24) return "Македонски/자체/адреса_LOOKUP_исклучок";
        if (сметка_VALUE == 25) return "Македонски/자체/파일없음예외";
        if (сметка_VALUE == 26) return "Македонски/자체/통신예외";
        if (сметка_VALUE == 27) return "Македонски/자체/неважечки_аргумент_исклучок";
        if (сметка_VALUE == 28) return "Македонски/자체/숫자형식예외";
        if (сметка_VALUE == 29) return "Македонски/자체/범위예외";
        if (сметка_VALUE == 30) return "Македонски/자체/배열범위예외";
        if (сметка_VALUE == 31) return "Македонски/자체/문자열범위예외";
        if (сметка_VALUE == 32) return "Македонски/자체/NULL_Референци_исклучок";
        if (сметка_VALUE == 33) return "Македонски/자체/산술예외";
        if (сметка_VALUE == 34) return "Македонски/자체/статус_исклучок";
        if (сметка_VALUE == 35) return "Македонски/자체/TYPE_емитувај_исклучок";
        if (сметка_VALUE == 36) return "Македонски/자체/음수배열크기예외";
        if (сметка_VALUE == 37) return "Македонски/자체/низа_Store_неуспех";
        if (сметка_VALUE == 38) return "Македонски/자체/нишка_статус_исклучок";
        if (сметка_VALUE == 1) return "java/lang/Throwable"; if (сметка_VALUE == 2) return "java/lang/Exception";
        if (сметка_VALUE == 3) return "java/lang/RuntimeException"; if (сметка_VALUE == 4) return "java/lang/ArithmeticException";
        if (сметка_VALUE == 5) return "java/lang/NullPointerException"; if (сметка_VALUE == 6) return "java/lang/IndexOutOfBoundsException";
        if (сметка_VALUE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (сметка_VALUE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (сметка_VALUE == 9) return "java/lang/IllegalArgumentException"; if (сметка_VALUE == 10) return "java/lang/NumberFormatException";
        if (сметка_VALUE == 11) return "java/io/IOException"; if (сметка_VALUE == 12) return "java/io/FileNotFoundException";
        if (сметка_VALUE == 17) return "java/lang/ArrayStoreException";
        if (сметка_VALUE == 18) return "java/net/UnknownHostException";
        if (сметка_VALUE == 19) return "java/net/SocketTimeoutException";
        if (сметка_VALUE == 16) return "java/lang/IllegalThreadStateException";
        if (сметка_VALUE == 13) return "java/lang/IllegalStateException"; if (сметка_VALUE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int сметка_VALUE) {
        if (сметка_VALUE == 40) return 2;
        if (сметка_VALUE == 41) return 40;
        if (сметка_VALUE == 39) return 11;
        if (сметка_VALUE == 1) return 0;
        if (сметка_VALUE == 2) return 1;
        if (сметка_VALUE == 3) return 2;
        if (сметка_VALUE == 4) return 3;
        if (сметка_VALUE == 5) return 3;
        if (сметка_VALUE == 6) return 3;
        if (сметка_VALUE == 7) return 6;
        if (сметка_VALUE == 8) return 6;
        if (сметка_VALUE == 9) return 3;
        if (сметка_VALUE == 10) return 9;
        if (сметка_VALUE == 11) return 2;
        if (сметка_VALUE == 12) return 11;
        if (сметка_VALUE == 13) return 3;
        if (сметка_VALUE == 14) return 3;
        if (сметка_VALUE == 15) return 3;
        if (сметка_VALUE == 16) return 9;
        if (сметка_VALUE == 17) return 3;
        if (сметка_VALUE == 18) return 11;
        if (сметка_VALUE == 19) return 11;
        if (сметка_VALUE == 20) return 2;
        if (сметка_VALUE == 21) return 3;
        if (сметка_VALUE == 22) return 11;
        if (сметка_VALUE == 23) return 22;
        if (сметка_VALUE == 24) return 22;
        if (сметка_VALUE == 25) return 22;
        if (сметка_VALUE == 26) return 22;
        if (сметка_VALUE == 27) return 9;
        if (сметка_VALUE == 28) return 27;
        if (сметка_VALUE == 29) return 6;
        if (сметка_VALUE == 30) return 29;
        if (сметка_VALUE == 31) return 29;
        if (сметка_VALUE == 32) return 5;
        if (сметка_VALUE == 33) return 4;
        if (сметка_VALUE == 34) return 13;
        if (сметка_VALUE == 35) return 14;
        if (сметка_VALUE == 36) return 15;
        if (сметка_VALUE == 37) return 17;
        if (сметка_VALUE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int реален_VALUE, int 요구값) {
        for (int 깊이 = 0; реален_VALUE != 0 && 깊이 < 16; 깊이++, реален_VALUE = 예외부모(реален_VALUE))
            if (реален_VALUE == 요구값) return true;
        return false;
    }
    static void 예외던짐(int сметка_VALUE, String информации_пред_употреба_Референци) {
        int објект_Референци = 새기억(9, 2); if (ГРЕШКА) return;
        힙[објект_Референци + 2] = сметка_VALUE; 힙[објект_Референци + 3] = вдоми_знак(информации_пред_употреба_Референци); 힙참조[објект_Референци + 3] = 1;
        던진객체 = објект_Референци; ГРЕШКА = true;
    }
    static boolean 맞는객체(int објект_Референци, int Име) {
        if (објект_Референци == 0) return true;
        if (!객체유효(објект_Референци)) return false;
        int област_CODE = 힙[објект_Референци];
        if (Word_СМС(Име, "java/lang/Object")) return true;
        if (област_CODE >= 32) return 종포함(област_CODE - 32, Име);
        if (област_CODE == 9) { int цел_адреса = исклучок_константа(Име); return цел_адреса != 0 && 예외포함(힙[објект_Референци + 2], цел_адреса); }
        if (област_CODE == 1) return Word_СМС(Име, "java/lang/String") || Word_СМС(Име, "java/lang/CharSequence");
        if (област_CODE == 4) return Word_СМС(Име, "java/lang/StringBuilder") || Word_СМС(Име, "java/lang/CharSequence");
        if (област_CODE == 10) return Word_СМС(Име, "java/util/ArrayList") || Word_СМС(Име, "java/util/List");
        if (област_CODE == 11) return Word_СМС(Име, "java/util/HashMap") || Word_СМС(Име, "java/util/Map");
        if (област_CODE == 12) return Word_СМС(Име, "java/lang/Integer") || Word_СМС(Име, "java/lang/Number");
        if (област_CODE >= 24 && област_CODE <= 28 && 힙[објект_Референци + 13] != 0) return 한국어화면종(Име) == област_CODE || Word_СМС(Име, "Македонски/자체/화면구성요소");
        if (област_CODE >= 24 && област_CODE <= 28) return (한국어화면종(Име) == 0 && 화면종(Име) == област_CODE) || Word_СМС(Име, "java/awt/Component") || Word_СМС(Име, "java/awt/Container") || Word_СМС(Име, "javax/swing/JComponent");
        if (област_CODE == 29) return Word_СМС(Име, 힙[објект_Референци + 3] != 0 ? "Македонски/자체/동작알림" : "java/awt/event/ActionEvent");
        if (област_CODE == 30) return Word_СМС(Име, "java/awt/FlowLayout") || Word_СМС(Име, "java/awt/LayoutManager");
        if (област_CODE == 17) return Word_СМС(Име, "java/net/Socket");
        if (област_CODE == 18) return Word_СМС(Име, "java/net/ServerSocket");
        if (област_CODE == 19) return Word_СМС(Име, 힙[објект_Референци + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (област_CODE == 14) return Word_СМС(Име, "java/net/InetAddress");
        if (област_CODE == 15) return Word_СМС(Име, "java/net/DatagramSocket");
        if (област_CODE == 16) return Word_СМС(Име, "java/net/DatagramPacket");
        if (област_CODE == 13) return Word_СМС(Име, 힙[објект_Референци + 3] != 0 ? "Македонски/자체/작업가닥" : "java/lang/Thread");
        if (област_CODE == 2) return Word_СМС(Име, "[I"); if (област_CODE == 20) return Word_СМС(Име, "[B"); if (област_CODE == 21) return Word_СМС(Име, "[Z");
        if (област_CODE == 22) return Word_СМС(Име, "[C"); if (област_CODE == 23) return Word_СМС(Име, "[S");
        if (област_CODE != 3) return false;
        if (Word_СМС(Име, "[Ljava/lang/Object;")) return true;
        int компонента = низа_елемент[објект_Референци];
        if (компонента == -1) return Word_СМС(Име, "[Ljava/lang/String;") || Word_СМС(Име, "[Ljava/lang/CharSequence;");
        if (компонента == 0) return false;
        if (배열종비교(компонента, Име)) return true;
        if ((Word_СМС(компонента, "java/lang/String") || Word_СМС(компонента, "java/lang/StringBuilder")) && Word_СМС(Име, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDEX = 0; Loop_INDEX < класа_Дефиниција_COUNT; Loop_INDEX++) if (같은말(класа_Дефиниција_име[Loop_INDEX], компонента)) {
            for (int кодна_точка = Loop_INDEX, 중첩깊이 = 0; кодна_точка >= 0 && 중첩깊이 < 16; 중첩깊이++, кодна_точка = 부모종(кодна_точка)) {
                if (배열종비교(종부모[кодна_точка], Име)) return true;
                for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < класа_интерфејс_COUNT[кодна_точка]; внатрешно_поврзување_позиционирање++) if (배열종비교(класа_интерфејс[кодна_точка * 16 + внатрешно_поврзување_позиционирање], Име)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int име_константа, int 형식참조) {
        int провери_позиционирање_9b8e3629 = 상가[형식참조], внес_COUNT = константа_SECOND_VALUE[형식참조];
        if (име_константа == 0 || внес_COUNT < 4 || Датотека[провери_позиционирање_9b8e3629] != '[' || Датотека[провери_позиционирање_9b8e3629 + 1] != 'L' || Датотека[провери_позиционирање_9b8e3629 + внес_COUNT - 1] != ';' || константа_SECOND_VALUE[име_константа] != внес_COUNT - 3) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT - 3; Loop_INDEX++) if (Датотека[상가[име_константа] + Loop_INDEX] != Датотека[провери_позиционирање_9b8e3629 + 2 + Loop_INDEX]) return false;
        return true;
    }
    static void рачка_исклучок() {
        if (던진객체 == 0) return;
        ГРЕШКА = false;
        while (врами_INDEX >= 현재가닥 * 32) {
            int датотека_INDEX = врами_метод[врами_INDEX], 읽는자리 = врами_инструкција[врами_INDEX];
            for (int Loop_INDEX = 0; Loop_INDEX < 잡기수; Loop_INDEX++) if (잡기함수[Loop_INDEX] == датотека_INDEX && 읽는자리 >= 잡기시작[Loop_INDEX] && 읽는자리 < 잡기끝[Loop_INDEX]
                && (잡기종[Loop_INDEX] == 0 || 맞는객체(던진객체, 잡기종[Loop_INDEX]))) {
                врами_позиционирање[врами_INDEX] = 잡기위치[Loop_INDEX]; врами_Купче[врами_INDEX] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (иницијализирај_врами[врами_INDEX] != 0) класа_Дефиниција_статус[иницијализирај_врами[врами_INDEX] - 1] = 3;
            if (틀잠금[врами_INDEX] != 0) { 잠금풀기(틀잠금[врами_INDEX]); 틀잠금[врами_INDEX] = 0; }
            врами_INDEX--;
        }
        корисник.Запиши("Uncaught ");
        if (힙[던진객체] == 9) { корисник.Запиши(исклучок_име(힙[던진객체 + 2])); корисник.Запиши(": "); запиши_СМС(힙[던진객체 + 3]); }
        else корисник.Запиши("user exception");
        корисник.запиши_знак_VALUE(10); 던진객체 = 0; ГРЕШКА = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void Купче_инструкција(int наредба_CODE) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (наредба_CODE == 87) return;
        if (наредба_CODE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int бајт_податоци = 빼기(0), SECOND_формат = 반환형;
        if (наредба_CODE == 88) return;
        if (наредба_CODE == 90) { 넣기(첫값, 첫형식); 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); return; }
        if (наредба_CODE == 92) { 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); return; }
        if (наредба_CODE == 95) { 넣기(첫값, 첫형식); 넣기(бајт_податоци, SECOND_формат); return; }
        int кодна_точка = 빼기(0), 셋째형식 = 반환형;
        if (наредба_CODE == 91) { 넣기(첫값, 첫형식); 넣기(кодна_точка, 셋째형식); 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); return; }
        if (наредба_CODE == 93) { 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); 넣기(кодна_точка, 셋째형식); 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(кодна_точка, 셋째형식); 넣기(бајт_податоци, SECOND_формат); 넣기(첫값, 첫형식);
    }
    static void 새객체(int име_константа, int 시작점) {
        int област_CODE = 0, 유효길이 = 0, исклучок_Референци = исклучок_константа(име_константа);
        if (Word_СМС(име_константа, "java/lang/StringBuilder")) { област_CODE = 4; 유효길이 = 1; }
        if (Word_СМС(име_константа, "java/io/FileInputStream")) { област_CODE = 5; 유효길이 = 2; }
        if (Word_СМС(име_константа, "java/io/FileOutputStream")) { област_CODE = 6; 유효길이 = 2; }
        if (исклучок_Референци != 0) { област_CODE = 9; 유효길이 = 2; }
        if (Word_СМС(име_константа, "java/util/ArrayList")) { област_CODE = 10; 유효길이 = 2; }
        if (Word_СМС(име_константа, "java/util/HashMap")) { област_CODE = 11; 유효길이 = 2; }
        if (Word_СМС(име_константа, "java/lang/Integer")) { област_CODE = 12; 유효길이 = 1; }
        if (Word_СМС(име_константа, "java/net/Socket")) { област_CODE = 17; 유효길이 = 5; }
        if (Word_СМС(име_константа, "java/net/ServerSocket")) { област_CODE = 18; 유효길이 = 5; }
        if (Word_СМС(име_константа, "java/net/DatagramSocket")) { област_CODE = 15; 유효길이 = 3; }
        if (Word_СМС(име_константа, "java/net/DatagramPacket")) { област_CODE = 16; 유효길이 = 4; }
        if (Word_СМС(име_константа, "java/lang/Thread") || Word_СМС(име_константа, "Македонски/자체/작업가닥")) { област_CODE = 13; 유효길이 = 2; }
        if (Word_СМС(име_константа, "java/lang/Object")) { област_CODE = 8; }
        if (област_CODE == 0 && 화면종(име_константа) != 0) { област_CODE = 화면종(име_константа); 유효길이 = 12; }
        if (област_CODE == 0) {
            int кодна_точка = FIND_класа_Дефиниција(име_константа); if (кодна_точка < 0 || ГРЕШКА || !иницијализирај(кодна_точка, 시작점)) return;
            област_CODE = 32 + кодна_точка; 유효길이 = класа_отвор_COUNT[кодна_точка];
        }
        int објект_Референци = додели_Склад(област_CODE, 유효길이); if (ГРЕШКА) return;
        if (област_CODE == 13 && Word_СМС(име_константа, "Македонски/자체/작업가닥")) 힙[објект_Референци + 3] = 1;
        if (област_CODE >= 24 && област_CODE <= 28 && 한국어화면종(име_константа) != 0) 힙[објект_Референци + 13] = 1;
        if (област_CODE == 5 || област_CODE == 6 || област_CODE == 15 || област_CODE == 17 || област_CODE == 18) 힙[објект_Референци + 2] = -1;
        if (област_CODE == 9) 힙[објект_Референци + 2] = исклучок_Референци;
        넣기(објект_Референци, 2);
    }
    static boolean 값같음(int 첫값, int бајт_податоци) {
        if (첫값 == бајт_податоци) return true;
        if (첫값 == 0 || бајт_податоци == 0 || 첫값 < 0 || бајт_податоци < 0 || 첫값 >= 힙끝 || бајт_податоци >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[бајт_податоци] == 1) return 글같음(첫값, бајт_податоци, false);
        return 힙[첫값] == 12 && 힙[бајт_податоци] == 12 && 힙[첫값 + 2] == 힙[бајт_податоци + 2];
    }
    static int 글조각(int објект_Референци, int Start_позиционирање, int крај_позиционирање) {
        if (!објект_VALUE(објект_Референци, 1)) return 0;
        if (Start_позиционирање < 0 || крај_позиционирање < Start_позиционирање || крај_позиционирање > 힙[објект_Референци + 1]) { неуспех_VALUE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = додели_Склад(1, крај_позиционирање - Start_позиционирање); if (ГРЕШКА) return 0;
        for (int Loop_INDEX = Start_позиционирање; Loop_INDEX < крај_позиционирање; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX - Start_позиционирање] = 힙[објект_Референци + 2 + Loop_INDEX];
        return 반환값;
    }
    static int поврзување_СМС(int 첫값, int бајт_податоци) {
        if (!објект_VALUE(첫값, 1) || !објект_VALUE(бајт_податоци, 1)) return 0;
        int внес_COUNT = 힙[첫값 + 1], метод_INDEX = 힙[бајт_податоци + 1], 반환값 = додели_Склад(1, внес_COUNT + метод_INDEX); if (ГРЕШКА) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 힙[첫값 + 2 + Loop_INDEX];
        for (int Loop_INDEX = 0; Loop_INDEX < метод_INDEX; Loop_INDEX++) 힙[반환값 + 2 + внес_COUNT + Loop_INDEX] = 힙[бајт_податоци + 2 + Loop_INDEX];
        return 반환값;
    }
    static boolean 기본호출(int сопственик, int име_константа, int 서술상수, int наредба_CODE) {
        if (Word_СМС(сопственик, "Македонски/자체/실행인수") && наредба_CODE == 184) {
            if (Word_СМС(име_константа, "ставка_COUNT") && Word_СМС(서술상수, "()I")) { 넣기(корисник.인수개수() - 1, 1); return true; }
            if (Word_СМС(име_константа, "Текст") && Word_СМС(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= корисник.인수개수() - 1) 예외던짐(29, "Изврши_наредба Аргументи 범위를 벗어났습니다");
                else 넣기(вдоми_знак(корисник.Аргументи(순번 + 1)), 2);
                return true;
            }
            неуспех_VALUE("지원하지 않는 Македонски Изврши_наредба Аргументи 호출"); return true;
        }
        if (Word_СМС(сопственик, "Македонски/자체/작업가닥")) { Процес_нишка(име_константа, 서술상수, наредба_CODE, true); return true; }
        if (한국어화면소유(сопственик)) { 한국어화면호출(сопственик, име_константа, 서술상수, наредба_CODE); return true; }
        if (화면소유(сопственик)) { 화면호출(сопственик, име_константа, 서술상수, наредба_CODE); return true; }
        if (Word_СМС(сопственик, "java/net/Socket") || Word_СМС(сопственик, "java/net/ServerSocket") || Word_СМС(сопственик, "java/io/InputStream") || Word_СМС(сопственик, "java/io/OutputStream")) { 흐름호출(сопственик, име_константа, 서술상수, наредба_CODE); return true; }
        if (Word_СМС(сопственик, "Македонски/자체/јадро_VALUE") && наредба_CODE == 184) {
            if (Word_СМС(име_константа, "화면너비") && Word_СМС(서술상수, "()I")) { 넣기(корисник.화면너비(), 1); return true; }
            if (Word_СМС(име_константа, "화면높이") && Word_СМС(서술상수, "()I")) { 넣기(корисник.화면높이(), 1); return true; }
            if (Word_СМС(име_константа, "밀리초") && Word_СМС(서술상수, "()I")) { 넣기(корисник.밀리초(), 1); return true; }
            if (Word_СМС(име_константа, "그림대기") && Word_СМС(서술상수, "()I")) { 넣기(корисник.그림대기(), 1); return true; }
            if (Word_СМС(име_константа, "사각형") && Word_СМС(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), координата_х = 빼기(1); 넣기(корисник.사각형(координата_х, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Word_СМС(сопственик, "java/net/InetAddress") || Word_СМС(сопственик, "java/net/DatagramPacket") || Word_СМС(сопственик, "java/net/DatagramSocket")) { 통신호출(сопственик, име_константа, 서술상수, наредба_CODE); return true; }
        if (Word_СМС(сопственик, "java/lang/Thread")) { 가닥호출(име_константа, 서술상수, наредба_CODE); return true; }
        if (Word_СМС(сопственик, "java/lang/Object")) {
            if (Word_СМС(име_константа, "<init>") && Word_СМС(서술상수, "()V") && наредба_CODE == 183) { 객체유효(빼기(2)); return true; }
            if (Word_СМС(име_константа, "equals") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) { int бајт_податоци = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == бајт_податоци ? 1 : 0, 1); return true; }
        }
        if (исклучок_константа(сопственик) != 0) {
            if (Word_СМС(име_константа, "<init>") && наредба_CODE == 183 && (Word_СМС(서술상수, "()V") || Word_СМС(서술상수, "(Ljava/lang/String;)V"))) {
                int промпт = Word_СМС(서술상수, "()V") ? 0 : 빼기(2), објект_Референци = 빼기(2);
                if (објект_VALUE(објект_Референци, 9)) { 힙[објект_Референци + 3] = промпт; 힙참조[објект_Референци + 3] = 1; } return true;
            }
            if ((Word_СМС(име_константа, "getMessage") || Word_СМС(име_константа, "설명")) && Word_СМС(서술상수, "()Ljava/lang/String;")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 9)) 넣기(힙[објект_Референци + 3], 2); return true; }
        }
        if (Word_СМС(сопственик, "java/lang/String")) {
            if (наредба_CODE == 182 && Word_СМС(име_константа, "getBytes") && (Word_СМС(서술상수, "()[B") || Word_СМС(서술상수, "(Ljava/lang/String;)[B"))) {
                int кодирање_име = Word_СМС(서술상수, "()[B") ? 0 : 빼기(2), објект_Референци = 빼기(2);
                if (!објект_VALUE(објект_Референци, 1)) return true;
                if (кодирање_име != 0 && !글같음(кодирање_име, вдоми_знак("UTF-8"), false) && !글같음(кодирање_име, вдоми_знак("UTF8"), false) && !글같음(кодирање_име, вдоми_знак("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int внес_COUNT = 힙[објект_Референци + 1], 반환값 = додели_Склад(20, внес_COUNT * 3), 사용수 = 0; if (ГРЕШКА) return true;
                for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < внес_COUNT; внатрешно_поврзување_позиционирање++) {
                    int кодна_точка = 힙[објект_Референци + 2 + внатрешно_поврзување_позиционирање];
                    if (кодна_точка >= 0xd800 && кодна_точка <= 0xdbff && внатрешно_поврзување_позиционирање + 1 < внес_COUNT && 힙[објект_Референци + 3 + внатрешно_поврзување_позиционирање] >= 0xdc00 && 힙[објект_Референци + 3 + внатрешно_поврзување_позиционирање] <= 0xdfff) кодна_точка = 0x10000 + ((кодна_точка - 0xd800) << 10) + 힙[објект_Референци + 2 + ++внатрешно_поврзување_позиционирање] - 0xdc00;
                    else if (кодна_точка >= 0xd800 && кодна_точка <= 0xdfff) кодна_точка = '?';
                    if (кодна_точка < 128) 힙[반환값 + 2 + 사용수++] = кодна_точка;
                    else { int бајт_COUNT = кодна_точка < 2048 ? 2 : кодна_точка < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((бајт_COUNT == 2 ? 192 : бајт_COUNT == 3 ? 224 : 240) | кодна_точка >> (6 * (бајт_COUNT - 1))); for (int Споредба_позиционирање = бајт_COUNT - 1; Споредба_позиционирање > 0; Споредба_позиционирање--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | кодна_точка >> (6 * (Споредба_позиционирање - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (наредба_CODE == 184 && Word_СМС(име_константа, "valueOf") && Word_СМС(서술상수, "(I)Ljava/lang/String;")) { 넣기(цифра_знак(빼기(1)), 2); return true; }
            if (наредба_CODE != 182) return false;
            if (Word_СМС(име_константа, "equals") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) { int бајт_податоци = 빼기(2), 첫값 = 빼기(2); if (објект_VALUE(첫값, 1)) 넣기(글같음(첫값, бајт_податоци, false) ? 1 : 0, 1); return true; }
            if (Word_СМС(име_константа, "isEmpty") && Word_СМС(서술상수, "()Z")) { int 첫값 = 빼기(2); if (објект_VALUE(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_СМС(име_константа, "substring") && (Word_СМС(서술상수, "(I)Ljava/lang/String;") || Word_СМС(서술상수, "(II)Ljava/lang/String;"))) {
                boolean SECOND_VALUE = Word_СМС(서술상수, "(II)Ljava/lang/String;"); int крај_позиционирање = SECOND_VALUE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (објект_VALUE(첫값, 1)) 넣기(글조각(첫값, 시작점, SECOND_VALUE ? крај_позиционирање : 힙[첫값 + 1]), 2); return true;
            }
            if (Word_СМС(име_константа, "concat") && Word_СМС(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int бајт_податоци = 빼기(2), 첫값 = 빼기(2); 넣기(поврзување_СМС(첫값, бајт_податоци), 2); return true; }
            if (Word_СМС(име_константа, "hashCode") && Word_СМС(서술상수, "()I")) { int 첫값 = 빼기(2), хаш_VALUE = 0; if (објект_VALUE(첫값, 1)) { for (int Loop_INDEX = 0; Loop_INDEX < 힙[첫값 + 1]; Loop_INDEX++) хаш_VALUE = хаш_VALUE * 31 + 힙[첫값 + 2 + Loop_INDEX]; 넣기(хаш_VALUE, 1); } return true; }
            if (Word_СМС(име_константа, "toString") && Word_СМС(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (објект_VALUE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_СМС(сопственик, "java/lang/Integer")) {
            if (наредба_CODE == 184 && Word_СМС(име_константа, "valueOf") && Word_СМС(서술상수, "(I)Ljava/lang/Integer;")) { int податоци_VALUE = 빼기(1), објект_Референци = податоци_VALUE >= -128 && податоци_VALUE <= 127 ? Store_цел_број[податоци_VALUE + 128] : 0; if (објект_Референци == 0) { објект_Референци = додели_Склад(12, 1); if (!ГРЕШКА) { 힙[објект_Референци + 2] = податоци_VALUE; if (податоци_VALUE >= -128 && податоци_VALUE <= 127) Store_цел_број[податоци_VALUE + 128] = објект_Референци; } } 넣기(објект_Референци, 2); return true; }
            if (наредба_CODE == 183 && Word_СМС(име_константа, "<init>") && Word_СМС(서술상수, "(I)V")) { int податоци_VALUE = 빼기(1), објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 12)) 힙[објект_Референци + 2] = податоци_VALUE; return true; }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "intValue") && Word_СМС(서술상수, "()I")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 12)) 넣기(힙[објект_Референци + 2], 1); return true; }
            if (наредба_CODE == 184 && Word_СМС(име_константа, "toString") && Word_СМС(서술상수, "(I)Ljava/lang/String;")) { 넣기(цифра_знак(빼기(1)), 2); return true; }
        }
        if (Word_СМС(сопственик, "java/lang/Math") && наредба_CODE == 184) {
            if (Word_СМС(име_константа, "abs") && Word_СМС(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_СМС(име_константа, "min") || Word_СМС(име_константа, "max")) && Word_СМС(서술상수, "(II)I")) { int бајт_податоци = 빼기(1), 첫값 = 빼기(1); 넣기(Word_СМС(име_константа, "min") ? (첫값 < бајт_податоци ? 첫값 : бајт_податоци) : (첫값 > бајт_податоци ? 첫값 : бајт_податоци), 1); return true; }
        }
        if (Word_СМС(сопственик, "java/lang/System") && наредба_CODE == 184) {
            if (Word_СМС(име_константа, "gc") && Word_СМС(서술상수, "()V")) { 수거(); return true; }
            if (Word_СМС(име_константа, "arraycopy") && Word_СМС(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int внес_COUNT = 빼기(1), одредиште_VALUE_INDEX = 빼기(1), бајт_податоци = 빼기(2), Start_позиционирање = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(бајт_податоци)) {
                    int област_CODE = 힙[첫값];
                    if (힙[бајт_податоци] != област_CODE || (област_CODE != 2 && област_CODE != 3 && (област_CODE < 20 || област_CODE > 23))) неуспех_VALUE("arraycopy type mismatch");
                    else if (внес_COUNT < 0 || Start_позиционирање < 0 || одредиште_VALUE_INDEX < 0 || Start_позиционирање > 힙[첫값 + 1] - внес_COUNT || одредиште_VALUE_INDEX > 힙[бајт_податоци + 1] - внес_COUNT) неуспех_VALUE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == бајт_податоци && одредиште_VALUE_INDEX > Start_позиционирање) { for (int Loop_INDEX = внес_COUNT - 1; Loop_INDEX >= 0; Loop_INDEX--) 힙[бајт_податоци + 2 + одредиште_VALUE_INDEX + Loop_INDEX] = 힙[첫값 + 2 + Start_позиционирање + Loop_INDEX]; }
                    else { for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT && !ГРЕШКА; Loop_INDEX++) { int податоци_VALUE = 힙[첫값 + 2 + Start_позиционирање + Loop_INDEX]; if (област_CODE != 3 || 배열저장가능(бајт_податоци, податоци_VALUE)) 힙[бајт_податоци + 2 + одредиште_VALUE_INDEX + Loop_INDEX] = податоци_VALUE; } }
                }
                return true;
            }
        }
        if (Word_СМС(сопственик, "java/util/ArrayList") || Word_СМС(сопственик, "java/util/List") || Word_СМС(сопственик, "java/util/HashMap") || Word_СМС(сопственик, "java/util/Map")) {
            모음호출(сопственик, име_константа, 서술상수, наредба_CODE); return true;
        }
        return false;
    }
    static void 모음늘리기(int објект_Референци, int 필요수) {
        int 이전값 = 힙[објект_Референци + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int Следно_позиционирање = 용량값 < 8 ? 8 : 용량값 * 2; if (Следно_позиционирање < 필요수) Следно_позиционирање = 필요수;
        int податоци_низа = додели_Склад(3, Следно_позиционирање); if (ГРЕШКА) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 용량값; Loop_INDEX++) 힙[податоци_низа + 2 + Loop_INDEX] = 힙[이전값 + 2 + Loop_INDEX];
        힙[објект_Референци + 2] = податоци_низа; 힙참조[објект_Референци + 2] = 1;
    }
    static void 모음호출(int сопственик, int име_константа, int 서술상수, int наредба_CODE) {
        boolean 대응참조 = Word_СМС(сопственик, "java/util/HashMap") || Word_СМС(сопственик, "java/util/Map"); int област_CODE = 대응참조 ? 11 : 10;
        if (Word_СМС(име_константа, "<init>") && наредба_CODE == 183 && Word_СМС(서술상수, "()V")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, област_CODE)) 모음늘리기(објект_Референци, 8); return; }
        if (наредба_CODE != 182 && наредба_CODE != 185) { неуспех_VALUE("invalid collection invocation"); return; }
        if (Word_СМС(име_константа, "size") && Word_СМС(서술상수, "()I") || Word_СМС(име_константа, "isEmpty") && Word_СМС(서술상수, "()Z")) {
            int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, област_CODE)) 넣기(Word_СМС(име_константа, "size") ? 힙[објект_Референци + 3] : 힙[објект_Референци + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_СМС(име_константа, "clear") && Word_СМС(서술상수, "()V")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, област_CODE)) { int податоци_низа = 힙[објект_Референци + 2]; for (int Loop_INDEX = 0; Loop_INDEX < 힙[податоци_низа + 1]; Loop_INDEX++) 힙[податоци_низа + 2 + Loop_INDEX] = 0; 힙[објект_Референци + 3] = 0; } return; }
        if (!대응참조 && Word_СМС(име_константа, "add") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) {
            int податоци_VALUE = 빼기(2), објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 10)) return;
            int внес_COUNT = 힙[објект_Референци + 3]; 모음늘리기(објект_Референци, внес_COUNT + 1); if (!ГРЕШКА) { 힙[힙[објект_Референци + 2] + 2 + внес_COUNT] = податоци_VALUE; 힙[објект_Референци + 3] = внес_COUNT + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_СМС(име_константа, "get") || Word_СМС(име_константа, "remove")) && Word_СМС(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Word_СМС(име_константа, "set") && Word_СМС(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Word_СМС(име_константа, "set"); int податоци_VALUE = 지정여부 ? 빼기(2) : 0, внес_позиционирање = 빼기(1), објект_Референци = 빼기(2);
            if (!објект_VALUE(објект_Референци, 10)) return;
            int внес_COUNT = 힙[објект_Референци + 3], податоци_низа = 힙[објект_Референци + 2];
            if (внес_позиционирање < 0 || внес_позиционирање >= внес_COUNT) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[податоци_низа + 2 + внес_позиционирање];
            if (지정여부) 힙[податоци_низа + 2 + внес_позиционирање] = податоци_VALUE;
            if (Word_СМС(име_константа, "remove")) { for (int Loop_INDEX = внес_позиционирање + 1; Loop_INDEX < внес_COUNT; Loop_INDEX++) 힙[податоци_низа + 1 + Loop_INDEX] = 힙[податоци_низа + 2 + Loop_INDEX]; 힙[податоци_низа + 1 + внес_COUNT] = 0; 힙[објект_Референци + 3] = внес_COUNT - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Word_СМС(име_константа, "get") || Word_СМС(име_константа, "remove")) && Word_СМС(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_СМС(име_константа, "put") && Word_СМС(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_СМС(име_константа, "containsKey") && Word_СМС(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_СМС(име_константа, "put"), отстрани = Word_СМС(име_константа, "remove");
            int податоци_VALUE = 넣기여부 ? 빼기(2) : 0, Клуч_Референци = 빼기(2), објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 11)) return;
            int внес_COUNT = 힙[објект_Референци + 3], податоци_низа = 힙[објект_Референци + 2], 찾은여부 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) if (값같음(Клуч_Референци, 힙[податоци_низа + 2 + 2 * Loop_INDEX])) { 찾은여부 = Loop_INDEX; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[податоци_низа + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(објект_Референци, (внес_COUNT + 1) * 2); податоци_низа = 힙[објект_Референци + 2]; 찾은여부 = внес_COUNT; if (!ГРЕШКА) 힙[објект_Референци + 3] = внес_COUNT + 1; }
                if (!ГРЕШКА) { 힙[податоци_низа + 2 + 2 * 찾은여부] = Клуч_Референци; 힙[податоци_низа + 3 + 2 * 찾은여부] = податоци_VALUE; }
            }
            if (отстрани && 찾은여부 >= 0) { for (int Loop_INDEX = 찾은여부 + 1; Loop_INDEX < внес_COUNT; Loop_INDEX++) { 힙[податоци_низа + 2 * Loop_INDEX] = 힙[податоци_низа + 2 + 2 * Loop_INDEX]; 힙[податоци_низа + 1 + 2 * Loop_INDEX] = 힙[податоци_низа + 3 + 2 * Loop_INDEX]; } 힙[податоци_низа + 2 * внес_COUNT] = 0; 힙[податоци_низа + 1 + 2 * внес_COUNT] = 0; 힙[објект_Референци + 3] = внес_COUNT - 1; }
            if (Word_СМС(име_константа, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        неуспех_VALUE("unsupported collection method");
    }
    static boolean 잠금얻기(int објект_Референци) {
        if (!객체유효(објект_Референци)) return false;
        if (잠금깊이[објект_Референци] != 0 && 잠금주인[објект_Референци] != 현재가닥 + 1) { измени_Барање_на_HTTP = true; return false; }
        잠금주인[објект_Референци] = 현재가닥 + 1; 잠금깊이[објект_Референци]++; return true;
    }
    static void 잠금풀기(int објект_Референци) {
        if (!객체유효(објект_Референци)) return;
        if (잠금깊이[објект_Референци] == 0 || 잠금주인[објект_Референци] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[објект_Референци] == 0) 잠금주인[објект_Референци] = 0;
    }
    static boolean SWITCH_нишка() {
        нишка_врами[현재가닥] = врами_INDEX;
        if (врами_INDEX < 현재가닥 * 32) нишка_статус[현재가닥] = 3;
        for (int Loop_INDEX = 0; Loop_INDEX < нишка_COUNT; Loop_INDEX++) if (нишка_статус[Loop_INDEX] == 2 && нишка_статус[가닥대기[Loop_INDEX]] == 3) нишка_статус[Loop_INDEX] = 1;
        for (int Loop_INDEX = 1; Loop_INDEX <= нишка_COUNT; Loop_INDEX++) {
            int Следно_позиционирање = (현재가닥 + Loop_INDEX) % нишка_COUNT;
            if (нишка_статус[Следно_позиционирање] == 1) { 현재가닥 = Следно_позиционирање; врами_INDEX = нишка_врами[Следно_позиционирање]; измени_Барање_на_HTTP = false; return true; }
        }
        for (int Loop_INDEX = 0; Loop_INDEX < нишка_COUNT; Loop_INDEX++) if (нишка_статус[Loop_INDEX] != 3) { неуспех_VALUE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int име_константа, int 서술상수, int наредба_CODE) { Процес_нишка(име_константа, 서술상수, наредба_CODE, false); }
    static void Процес_нишка(int име_константа, int 서술상수, int наредба_CODE, boolean Македонски) {
        if (наредба_CODE == 184 && Word_СМС(име_константа, Македонски ? "YIELD_задача" : "yield") && Word_СМС(서술상수, "()V")) { измени_Барање_на_HTTP = true; return; }
        if (наредба_CODE == 184 && Word_СМС(име_константа, "currentThread") && Word_СМС(서술상수, "()Ljava/lang/Thread;")) { 넣기(нишка_објект[현재가닥], 2); return; }
        if (наредба_CODE == 183 && Word_СМС(име_константа, "<init>") && (Word_СМС(서술상수, "()V") || Word_СМС(서술상수, Македонски ? "(LМакедонски/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int цел_адреса = Word_СМС(서술상수, "()V") ? 0 : 빼기(2), објект_Референци = 빼기(2);
            if (!객체유효(објект_Референци)) return;
            if (힙[објект_Референци] == 13) { 힙[објект_Референци + 2] = цел_адреса; 힙참조[објект_Референци + 2] = 1; }
            else if (цел_адреса != 0) неуспех_VALUE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (наредба_CODE == 182 && (Word_СМС(име_константа, Македонски ? "Start_задача" : "start") || Word_СМС(име_константа, Македонски ? "기다리기" : "join")) && Word_СМС(서술상수, "()V") || наредба_CODE == 182 && Word_СМС(име_константа, Македонски ? "살아있는가" : "isAlive") && Word_СМС(서술상수, "()Z")) {
            int објект_Референци = 빼기(2); if (!객체유효(објект_Референци)) return;
            int сметка_VALUE = -1; for (int Loop_INDEX = 0; Loop_INDEX < нишка_COUNT; Loop_INDEX++) if (нишка_објект[Loop_INDEX] == објект_Референци) сметка_VALUE = Loop_INDEX;
            if (Word_СМС(име_константа, Македонски ? "살아있는가" : "isAlive")) { 넣기(сметка_VALUE >= 0 && нишка_статус[сметка_VALUE] != 3 ? 1 : 0, 1); return; }
            if (Word_СМС(име_константа, Македонски ? "기다리기" : "join")) { if (сметка_VALUE >= 0 && нишка_статус[сметка_VALUE] != 3) { 가닥대기[현재가닥] = сметка_VALUE; нишка_статус[현재가닥] = 2; измени_Барање_на_HTTP = true; } return; }
            if (сметка_VALUE >= 0) { 예외던짐(Македонски ? 38 : 16, "thread already started"); return; }
            if (нишка_COUNT == 4) { неуспех_VALUE("thread limit (4 including main)"); return; }
            int цел_адреса = 힙[објект_Референци] == 13 ? 힙[објект_Референци + 2] : објект_Референци;
            int датотека_INDEX = цел_адреса > 0 && 힙[цел_адреса] >= 32 ? име_метод(힙[цел_адреса] - 32, Македонски ? "Изврши" : "run", "()V") : -1;
            if (цел_адреса != 0 && датотека_INDEX < 0) { неуспех_VALUE("Runnable.run required"); return; }
            сметка_VALUE = нишка_COUNT++; нишка_објект[сметка_VALUE] = објект_Референци; нишка_цел[сметка_VALUE] = цел_адреса;
            int врами = сметка_VALUE * 32; нишка_врами[сметка_VALUE] = датотека_INDEX < 0 ? врами - 1 : врами; нишка_статус[сметка_VALUE] = датотека_INDEX < 0 ? 3 : 1;
            if (датотека_INDEX >= 0) { врами_метод[врами] = датотека_INDEX; врами_позиционирање[врами] = метод_Start[датотека_INDEX]; локален_VALUE[врами * 128] = цел_адреса; локален_TYPE[врами * 128] = 2; }
            return;
        }
        неуспех_VALUE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], адреса_СМС = new int[16];
    static int локален_адреса() { return адреса_објект(0x7f000001); }
    static int адреса_објект(int VALUE) { int објект_Референци = додели_Склад(14, 1); if (!ГРЕШКА) 힙[објект_Референци + 2] = VALUE; return објект_Референци; }
    static int 주소해독(int објект_Референци) {
        if (објект_Референци == 0 || 글같음(објект_Референци, вдоми_знак("localhost"), false)) return 0x7f000001;
        if (!објект_VALUE(објект_Референци, 1)) return 0;
        int податоци_VALUE = 0, 총수 = 0, адреса_бајт = 0, 자릿수 = 0, внес_COUNT = 힙[објект_Референци + 1];
        for (int Loop_INDEX = 0; Loop_INDEX <= внес_COUNT; Loop_INDEX++) {
            int кодна_точка = Loop_INDEX == внес_COUNT ? '.' : 힙[објект_Референци + 2 + Loop_INDEX];
            if (кодна_точка == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } податоци_VALUE = податоци_VALUE << 8 | адреса_бајт; 총수++; адреса_бајт = 자릿수 = 0; }
            else { if (кодна_точка < '0' || кодна_точка > '9' || ++자릿수 > 3 || (адреса_бајт = адреса_бајт * 10 + кодна_точка - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return податоци_VALUE;
    }
    static int адреса_знак(int податоци_VALUE) {
        int внес_COUNT = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int адреса_бајт = податоци_VALUE >>> 이동비트 & 255;
            if (адреса_бајт >= 100) адреса_СМС[внес_COUNT++] = '0' + адреса_бајт / 100;
            if (адреса_бајт >= 10) адреса_СМС[внес_COUNT++] = '0' + адреса_бајт / 10 % 10;
            адреса_СМС[внес_COUNT++] = '0' + адреса_бајт % 10; if (이동비트 != 0) адреса_СМС[внес_COUNT++] = '.';
        }
        int објект_Референци = додели_Склад(1, внес_COUNT); if (!ГРЕШКА) for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) 힙[објект_Референци + 2 + Loop_INDEX] = адреса_СМС[Loop_INDEX]; return објект_Референци;
    }
    static void 통신호출(int сопственик, int име_константа, int 서술상수, int наредба_CODE) {
        if (Word_СМС(сопственик, "java/net/InetAddress")) {
            if (наредба_CODE == 184 && Word_СМС(име_константа, "getLoopbackAddress") && Word_СМС(서술상수, "()Ljava/net/InetAddress;")) { 넣기(локален_адреса(), 2); return; }
            if (наредба_CODE == 184 && Word_СМС(име_константа, "getByName") && Word_СМС(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int податоци_VALUE = 주소해독(빼기(2)); if (던진객체 == 0 && !ГРЕШКА) 넣기(адреса_објект(податоци_VALUE), 2); return;
            }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "getHostAddress") && Word_СМС(서술상수, "()Ljava/lang/String;")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 14)) 넣기(адреса_знак(힙[објект_Референци + 2]), 2); return; }
        }
        if (Word_СМС(сопственик, "java/net/DatagramPacket")) {
            if (наредба_CODE == 183 && Word_СМС(име_константа, "<init>") && (Word_СМС(서술상수, "([BI)V") || Word_СМС(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean одредиште_VALUE_Референци = Word_СМС(서술상수, "([BILjava/net/InetAddress;I)V"); int број_на_порта = одредиште_VALUE_Референци ? 빼기(1) : 0, адреса_Референци = одредиште_VALUE_Референци ? 빼기(2) : 0;
                int внес_COUNT = 빼기(1), податоци_низа = 빼기(2), објект_Референци = 빼기(2);
                if (!објект_VALUE(објект_Референци, 16) || !објект_VALUE(податоци_низа, 20)) return;
                if (внес_COUNT < 0 || внес_COUNT > 힙[податоци_низа + 1] || број_на_порта < 0 || број_на_порта > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (адреса_Референци != 0 && !објект_VALUE(адреса_Референци, 14)) return;
                힙[објект_Референци + 2] = податоци_низа; 힙참조[објект_Референци + 2] = 1; 힙[објект_Референци + 3] = внес_COUNT;
                힙[објект_Референци + 4] = адреса_Референци; 힙참조[објект_Референци + 4] = 1; 힙[објект_Референци + 5] = број_на_порта; return;
            }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "setLength") && Word_СМС(서술상수, "(I)V")) {
                int внес_COUNT = 빼기(1), објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 16)) return;
                if (внес_COUNT < 0 || внес_COUNT > 힙[힙[објект_Референци + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[објект_Референци + 3] = внес_COUNT; return;
            }
            if (наредба_CODE == 182 && (Word_СМС(име_константа, "getData") && Word_СМС(서술상수, "()[B") || Word_СМС(име_константа, "getLength") && Word_СМС(서술상수, "()I") || Word_СМС(име_константа, "getAddress") && Word_СМС(서술상수, "()Ljava/net/InetAddress;") || Word_СМС(име_константа, "getPort") && Word_СМС(서술상수, "()I"))) {
                int објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 16)) return;
                int внес_позиционирање = Word_СМС(име_константа, "getData") ? 2 : Word_СМС(име_константа, "getLength") ? 3 : Word_СМС(име_константа, "getAddress") ? 4 : 5;
                넣기(힙[објект_Референци + внес_позиционирање], внес_позиционирање == 2 || внес_позиционирање == 4 ? 2 : 1); return;
            }
        }
        if (Word_СМС(сопственик, "java/net/DatagramSocket")) {
            if (наредба_CODE == 183 && Word_СМС(име_константа, "<init>") && (Word_СМС(서술상수, "()V") || Word_СМС(서술상수, "(I)V"))) {
                int број_на_порта = Word_СМС(서술상수, "()V") ? 0 : 빼기(1), објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 15)) return;
                if (број_на_порта < 0 || број_на_порта > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = корисник.отвори_Мрежа(број_на_порта); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[објект_Референци + 2] = 열린파일번호; return;
            }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "setSoTimeout") && Word_СМС(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[објект_Референци + 3] = 밀리초값; return;
            }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "getLocalPort") && Word_СМС(서술상수, "()I")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 15)) 넣기(힙[објект_Референци + 2] < 0 ? -1 : корисник.Мрежа_порта(힙[објект_Референци + 2]), 1); return; }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "isClosed") && Word_СМС(서술상수, "()Z")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 15)) 넣기(힙[објект_Референци + 2] < 0 ? 1 : 0, 1); return; }
            if (наредба_CODE == 182 && Word_СМС(име_константа, "close") && Word_СМС(서술상수, "()V")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 15) && 힙[објект_Референци + 2] >= 0) { корисник.파일서술자닫기(힙[објект_Референци + 2]); 힙[објект_Референци + 2] = -1; } return; }
            if (наредба_CODE == 182 && (Word_СМС(име_константа, "send") || Word_СМС(име_константа, "receive")) && Word_СМС(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int пакет_5cd5338b = 빼기(2), објект_Референци = 빼기(2); if (!објект_VALUE(пакет_5cd5338b, 16) || !објект_VALUE(објект_Референци, 15)) return;
                int податоци_низа = 힙[пакет_5cd5338b + 2], 유효길이 = 힙[пакет_5cd5338b + 3], 열린파일번호 = 힙[објект_Референци + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_СМС(име_константа, "send")) {
                    if (!објект_VALUE(힙[пакет_5cd5338b + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < 유효길이; Loop_INDEX++) 통신임시[Loop_INDEX] = 힙[податоци_низа + 2 + Loop_INDEX];
                    if (корисник.испрати_Мрежа(열린파일번호, 힙[힙[пакет_5cd5338b + 4] + 2], 힙[пакет_5cd5338b + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int внес_COUNT = корисник.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (внес_COUNT == -11) {
                        int 현재시각 = корисник.밀리초();
                        if (힙[објект_Референци + 4] == 0) 힙[објект_Референци + 4] = 현재시각 + 1;
                        if (힙[објект_Референци + 3] > 0 && 현재시각 - (힙[објект_Референци + 4] - 1) >= 힙[објект_Референци + 3]) { 힙[објект_Референци + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(објект_Референци, 2); 넣기(пакет_5cd5338b, 2); врами_позиционирање[врами_INDEX] = врами_инструкција[врами_INDEX]; измени_Барање_на_HTTP = true; return;
                    }
                    힙[објект_Референци + 4] = 0;
                    if (внес_COUNT < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) 힙[податоци_низа + 2 + Loop_INDEX] = (byte)통신임시[Loop_INDEX];
                    힙[пакет_5cd5338b + 3] = внес_COUNT; 힙[пакет_5cd5338b + 4] = адреса_објект(통신임시[513]); 힙참조[пакет_5cd5338b + 4] = 1; 힙[пакет_5cd5338b + 5] = 통신임시[512];
                }
                return;
            }
        }
        неуспех_VALUE("unsupported java.net method");
    }
    static boolean 흐름대기(int објект_Референци) {
        int 현재시각 = корисник.밀리초();
        if (힙[објект_Референци + 5] == 0) 힙[објект_Референци + 5] = 현재시각 + 1;
        if (힙[објект_Референци + 3] > 0 && 현재시각 - (힙[објект_Референци + 5] - 1) >= 힙[објект_Референци + 3]) { 힙[објект_Референци + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        врами_позиционирање[врами_INDEX] = врами_инструкција[врами_INDEX]; измени_Барање_на_HTTP = true; return true;
    }
    static void 흐름호출(int сопственик, int име_константа, int 서술상수, int наредба_CODE) {
        boolean 수신쪽 = Word_СМС(сопственик, "java/net/ServerSocket"), Stream = Word_СМС(сопственик, "java/io/InputStream") || Word_СМС(сопственик, "java/io/OutputStream");
        if (!Stream && наредба_CODE == 183 && Word_СМС(име_константа, "<init>")) {
            boolean информатичка_технологија_празно_статус = Word_СМС(서술상수, "()V"), 이름지정여부 = Word_СМС(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_СМС(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(информатичка_технологија_празно_статус || 수신쪽 && Word_СМС(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { неуспех_VALUE("unsupported socket constructor"); return; }
            int број_на_порта = информатичка_технологија_празно_статус ? 0 : 빼기(1), адреса_Референци = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, објект_Референци = 빼기(2);
            if (!објект_VALUE(објект_Референци, 수신쪽 ? 18 : 17)) return;
            if (број_на_порта < 0 || број_на_порта > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !објект_VALUE(адреса_Референци, 14)) return;
            int Мрежа_адреса = 이름지정여부 ? 주소해독(адреса_Референци) : 주소지정여부 ? 힙[адреса_Референци + 2] : 0x7f000001;
            if (ГРЕШКА || 던진객체 != 0) return;
            int 열린파일번호 = корисник.Stream_контрола(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = информатичка_технологија_празно_статус ? 0 : 수신쪽 ? корисник.Stream_контрола(1, 열린파일번호, број_на_порта) : корисник.ПОВРЗИ_Stream(열린파일번호, Мрежа_адреса, број_на_порта);
            if (처리값 < 0) { корисник.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[објект_Референци + 2] = 열린파일번호; 힙[објект_Референци + 4] = број_на_порта; 힙[објект_Референци + 6] = информатичка_технологија_празно_статус ? 0 : 1; return;
        }
        if (!Stream && Word_СМС(име_константа, "setSoTimeout") && Word_СМС(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[објект_Референци + 3] = 밀리초값; return; }
        if (!Stream && Word_СМС(име_константа, "close") && Word_СМС(서술상수, "()V")) { int објект_Референци = 빼기(2); if (објект_VALUE(објект_Референци, 수신쪽 ? 18 : 17) && 힙[објект_Референци + 2] >= 0) { корисник.파일서술자닫기(힙[објект_Референци + 2]); 힙[објект_Референци + 2] = -1; } return; }
        if (!Stream && (Word_СМС(име_константа, "getLocalPort") || Word_СМС(име_константа, "getPort") || Word_СМС(име_константа, "isClosed") || Word_СМС(име_константа, "isConnected"))) {
            int објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 수신쪽 ? 18 : 17)) return;
            넣기(Word_СМС(име_константа, "isClosed") ? 힙[објект_Референци + 2] < 0 ? 1 : 0 : Word_СМС(име_константа, "isConnected") ? 힙[објект_Референци + 6] : Word_СМС(име_константа, "getPort") ? 힙[објект_Референци + 4] : 힙[објект_Референци + 2] < 0 ? -1 : корисник.Stream_контрола(4, 힙[објект_Референци + 2], 0), 1); return;
        }
        if (수신쪽 && Word_СМС(име_константа, "accept") && Word_СМС(서술상수, "()Ljava/net/Socket;")) {
            int објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 18)) return; int 열린파일번호 = корисник.Stream_контрола(3, 힙[објект_Референци + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(објект_Референци)) 넣기(објект_Референци, 2); return; }
            힙[објект_Референци + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = додели_Склад(17, 5); if (ГРЕШКА) { корисник.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = корисник.Stream_контрола(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Word_СМС(име_константа, "getInputStream") && Word_СМС(서술상수, "()Ljava/io/InputStream;")) || (Word_СМС(име_константа, "getOutputStream") && Word_СМС(서술상수, "()Ljava/io/OutputStream;")))) {
            int објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 17)) return; if (힙[објект_Референци + 2] < 0 || 힙[објект_Референци + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = додели_Склад(19, 4); if (ГРЕШКА) return; 힙[반환값 + 2] = објект_Референци; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Word_СМС(име_константа, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_СМС(име_константа, "read"), информатичка_технологија_запиши_операција = Word_СМС(име_константа, "write"), блокирај = Word_СМС(서술상수, "([B)I") || Word_СМС(서술상수, "([B)V"), информатичка_технологија_ПОДМАТРИЦА = Word_СМС(서술상수, "([BII)I") || Word_СМС(서술상수, "([BII)V");
            int внес_COUNT = информатичка_технологија_ПОДМАТРИЦА ? 빼기(1) : 0, 시작변위 = информатичка_технологија_ПОДМАТРИЦА ? 빼기(1) : 0, податоци_низа = блокирај || информатичка_технологија_ПОДМАТРИЦА ? 빼기(2) : 0;
            int податоци_VALUE = информатичка_технологија_запиши_операција && Word_СМС(서술상수, "(I)V") ? 빼기(1) : 0, објект_Референци = 빼기(2);
            if (!објект_VALUE(објект_Референци, 19)) return; int 부모참조 = 힙[објект_Референци + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_СМС(име_константа, "close") && Word_СМС(서술상수, "()V")) { корисник.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Word_СМС(име_константа, "flush") && Word_СМС(서술상수, "()V")) return;
            if ((!읽기여부 && !информатичка_технологија_запиши_операција) || 읽기여부 != (힙[објект_Референци + 3] == 0)) { неуспех_VALUE("unsupported stream operation"); return; }
            if (блокирај || информатичка_технологија_ПОДМАТРИЦА) { if (!објект_VALUE(податоци_низа, 20)) return; if (блокирај) внес_COUNT = 힙[податоци_низа + 1]; if (시작변위 < 0 || внес_COUNT < 0 || 시작변위 > 힙[податоци_низа + 1] - внес_COUNT) { 예외던짐(6, "stream array bounds"); return; } }
            else внес_COUNT = 1;
            if (внес_COUNT == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = информатичка_технологија_запиши_операција ? 힙[објект_Референци + 4] : 0, 처리값 = 0;
            while (완료수 < внес_COUNT) {
                처리값 = 읽기여부 ? корисник.파일한바이트읽기(열린파일번호) : корисник.파일한바이트쓰기(열린파일번호, блокирај || информатичка_технологија_ПОДМАТРИЦА ? 힙[податоци_низа + 2 + 시작변위 + 완료수] : податоци_VALUE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (блокирај || информатичка_технологија_ПОДМАТРИЦА)) 힙[податоци_низа + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(блокирај || информатичка_технологија_ПОДМАТРИЦА)) break;
            }
            if (처리값 == -11 && (информатичка_технологија_запиши_операција || 완료수 == 0)) {
                힙[објект_Референци + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(објект_Референци, 2); if (блокирај || информатичка_технологија_ПОДМАТРИЦА) 넣기(податоци_низа, 2); if (информатичка_технологија_ПОДМАТРИЦА) { 넣기(시작변위, 1); 넣기(внес_COUNT, 1); } if (информатичка_технологија_запиши_операција && !(блокирај || информатичка_технологија_ПОДМАТРИЦА)) 넣기(податоци_VALUE, 1); } return;
            }
            힙[објект_Референци + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : блокирај || информатичка_технологија_ПОДМАТРИЦА ? 완료수 : 처리값, 1); return;
        }
        неуспех_VALUE("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int име_константа) {
        if (Word_СМС(име_константа, "Македонски/자체/прозорец")) return 24;
        if (Word_СМС(име_константа, "Македонски/자체/Ознака")) return 26;
        if (Word_СМС(име_константа, "Македонски/자체/копче")) return 27;
        if (Word_СМС(име_константа, "Македонски/자체/СМС_поле")) return 28;
        if (Word_СМС(име_константа, "Македонски/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int име_константа) {
        return 한국어화면종(име_константа) != 0 || Word_СМС(име_константа, "Македонски/자체/화면구성요소") || Word_СМС(име_константа, "Македонски/자체/настан_ред_на_чекање");
    }
    static int 화면종(int име_константа) {
        int 한국어종 = 한국어화면종(име_константа); if (한국어종 != 0) return 한국어종;
        if (Word_СМС(име_константа, "javax/swing/JFrame")) return 24;
        if (Word_СМС(име_константа, "javax/swing/JPanel")) return 25;
        if (Word_СМС(име_константа, "javax/swing/JLabel")) return 26;
        if (Word_СМС(име_константа, "javax/swing/JButton")) return 27;
        if (Word_СМС(име_константа, "javax/swing/JTextField")) return 28;
        if (Word_СМС(име_константа, "java/awt/event/ActionEvent")) return 29;
        if (Word_СМС(име_константа, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int име_константа) {
        return 화면종(име_константа) != 0 || Word_СМС(име_константа, "java/awt/Component") || Word_СМС(име_константа, "java/awt/Container") || Word_СМС(име_константа, "javax/swing/JComponent") || Word_СМС(име_константа, "javax/swing/AbstractButton") || Word_СМС(име_константа, "javax/swing/text/JTextComponent") || Word_СМС(име_константа, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int објект_Референци) { if (!객체유효(објект_Референци)) return false; if (힙[објект_Референци] < 24 || 힙[објект_Референци] > 28) { неуспех_VALUE("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int објект_Референци, int СМС_Референци) {
        if (СМС_Референци != 0 && !објект_VALUE(СМС_Референци, 1)) return;
        int внес_COUNT = СМС_Референци == 0 ? 0 : 힙[СМС_Референци + 1]; if (внес_COUNT > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) 화면글임시[Loop_INDEX] = 힙[СМС_Референци + 2 + Loop_INDEX];
        if (корисник.화면글(힙[објект_Референци + 2], 화면글임시, внес_COUNT) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[објект_Референци + 3] = СМС_Референци; 힙참조[објект_Референци + 3] = 1;
    }
    static int 화면문자읽기(int објект_Референци) {
        int сметка_VALUE = 힙[објект_Референци + 2], внес_COUNT = корисник.화면연결(8, сметка_VALUE, 0, 0, 0, 0), 사용수 = 0;
        if (внес_COUNT < 0) { неуспех_VALUE("GUI text read failed"); return 0; }
        for (int Loop_INDEX = 0; Loop_INDEX < внес_COUNT; Loop_INDEX++) { int 부호값 = корисник.화면연결(9, сметка_VALUE, Loop_INDEX, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = додели_Склад(1, 사용수); if (!ГРЕШКА) for (int Loop_INDEX = 0; Loop_INDEX < 사용수; Loop_INDEX++) 힙[반환값 + 2 + Loop_INDEX] = 화면글임시[Loop_INDEX]; return 반환값;
    }
    /* Македонски 객체를 직접 만들고 јадро_VALUE 화면 기능에 연결한다. Swing објект_VALUE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int сопственик, int име_константа, int 서술상수, int наредба_CODE) {
        if (Word_СМС(сопственик, "Македонски/자체/настан_ред_на_чекање")) {
            if (наредба_CODE == 184 && Word_СМС(име_константа, "나중에실행") && Word_СМС(서술상수, "(LМакедонски/자체/실행할일;)V")) {
                int задача_Дејство = 빼기(2); if (!객체유효(задача_Дејство)) return;
                if (나중수 == 8) { неуспех_VALUE("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = задача_Дејство; return;
            }
            if (наредба_CODE == 184 && Word_СМС(име_константа, "사건처리중인가") && Word_СМС(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            неуспех_VALUE("지원하지 않는 Македонски 화면 일정 호출"); return;
        }
        if (Word_СМС(сопственик, "Македонски/자체/동작알림")) {
            int 알림 = 빼기(2); if (!објект_VALUE(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Word_СМС(име_константа, "настан_извор") && Word_СМС(서술상수, "()LМакедонски/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Word_СМС(име_константа, "наредба_СМС") && Word_СМС(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Word_СМС(име_константа, "INDEX") && Word_СМС(서술상수, "()I")) 넣기(1001, 1);
            else неуспех_VALUE("지원하지 않는 Македонски Дејство 알림 호출"); return;
        }
        if (наредба_CODE == 183 && Word_СМС(име_константа, "<init>")) {
            int 종류 = 한국어화면종(сопственик), 받이 = 0, 가로 = 0, вертикала_позиционирање = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Word_СМС(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (корисник.화면너비() - 폭) / 2; вертикала_позиционирање = (корисник.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Word_СМС(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Word_СМС(서술상수, "(Ljava/lang/String;IIIILМакедонски/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); вертикала_позиционирање = 빼기(1); 가로 = 빼기(1);
            } else { неуспех_VALUE("지원하지 않는 Македонски 화면 생성자"); return; }
            int Текст = 빼기(2), елемент_VALUE = 빼기(2); if (!화면객체(елемент_VALUE)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || вертикала_позиционирање < 0 || 폭 > корисник.화면너비() - 가로 || 높이 > корисник.화면높이() - вертикала_позиционирање) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int INDEX = корисник.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (INDEX < 1 || INDEX > 32) { неуспех_VALUE("화면 елемент_VALUE 자리가 가득 찼습니다"); return; }
            힙[елемент_VALUE + 2] = INDEX; 화면참조[INDEX - 1] = елемент_VALUE;
            힙[елемент_VALUE + 5] = 가로; 힙[елемент_VALUE + 6] = вертикала_позиционирање; 힙[елемент_VALUE + 7] = 폭; 힙[елемент_VALUE + 8] = 높이; 힙[елемент_VALUE + 10] = 2;
            힙[елемент_VALUE + 4] = 받이; 힙참조[елемент_VALUE + 4] = 1; 힙[елемент_VALUE + 12] = 1;
            корисник.화면연결(1, INDEX, 가로, вертикала_позиционирање, 폭, 높이);
            if (종류 == 24) корисник.화면연결(7, INDEX, 2, 0, 0, 0);
            화면문자설정(елемент_VALUE, Текст); return;
        }
        if (наредба_CODE != 182) { неуспех_VALUE("잘못된 Македонски 화면 호출 Команда"); return; }
        if (Word_СМС(име_константа, "запиши_СМС") && Word_СМС(서술상수, "(Ljava/lang/String;)V")) {
            int Текст = 빼기(2), елемент_VALUE = 빼기(2); if (화면객체(елемент_VALUE)) 화면문자설정(елемент_VALUE, Текст); return;
        }
        if (Word_СМС(име_константа, "글읽기") && Word_СМС(서술상수, "()Ljava/lang/String;")) {
            int елемент_VALUE = 빼기(2); if (화면객체(елемент_VALUE)) 넣기(화면문자읽기(елемент_VALUE), 2); return;
        }
        if (Word_СМС(име_константа, "동작맡기기") && Word_СМС(서술상수, "(LМакедонски/자체/동작받이;)V")) {
            int 받이 = 빼기(2), елемент_VALUE = 빼기(2);
            if (화면객체(елемент_VALUE)) { 힙[елемент_VALUE + 4] = 받이; 힙참조[елемент_VALUE + 4] = 1; 힙[елемент_VALUE + 12] = 1; } return;
        }
        if (Word_СМС(име_константа, "додавање_елемент") && Word_СМС(서술상수, "(LМакедонски/자체/화면구성요소;)V")) {
            int дете_VALUE = 빼기(2), 부모 = 빼기(2); if (!화면객체(дете_VALUE) || !화면객체(부모)) return;
            if (корисник.화면연결(2, 힙[부모 + 2], 힙[дете_VALUE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[дете_VALUE + 11] = 부모; 힙참조[дете_VALUE + 11] = 1; return;
        }
        if (Word_СМС(име_константа, "자리정하기") && Word_СМС(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), вертикала_позиционирање = 빼기(1), 가로 = 빼기(1), елемент_VALUE = 빼기(2); if (!화면객체(елемент_VALUE)) return;
            if (корисник.화면연결(1, 힙[елемент_VALUE + 2], 가로, вертикала_позиционирање, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[елемент_VALUE + 5] = 가로; 힙[елемент_VALUE + 6] = вертикала_позиционирање; 힙[елемент_VALUE + 7] = 폭; 힙[елемент_VALUE + 8] = 높이; return;
        }
        if ((Word_СМС(име_константа, "прикажи_прозорец") || Word_СМС(име_константа, "Затвори")) && Word_СМС(서술상수, "()V")) {
            boolean видливост_VALUE = Word_СМС(име_константа, "прикажи_прозорец"); int елемент_VALUE = 빼기(2); if (!화면객체(елемент_VALUE)) return;
            if (корисник.화면연결(видливост_VALUE ? 3 : 4, 힙[елемент_VALUE + 2], видливост_VALUE ? 1 : 0, 0, 0, 0) < 0) { неуспех_VALUE("화면은 интерактивен 명령에서 실행해야 합니다"); return; }
            힙[елемент_VALUE + 9] = видливост_VALUE ? 1 : 0; return;
        }
        if (Word_СМС(име_константа, "보이는가") && Word_СМС(서술상수, "()Z")) { int елемент_VALUE = 빼기(2); if (화면객체(елемент_VALUE)) 넣기(힙[елемент_VALUE + 9], 1); return; }
        неуспех_VALUE("지원하지 않는 Македонски 화면 метод_VALUE");
    }
    static void 화면호출(int сопственик, int име_константа, int 서술상수, int наредба_CODE) {
        if (Word_СМС(сопственик, "javax/swing/SwingUtilities")) {
            if (наредба_CODE == 184 && Word_СМС(име_константа, "invokeLater") && Word_СМС(서술상수, "(Ljava/lang/Runnable;)V")) { int објект_Референци = 빼기(2); if (!객체유효(објект_Референци)) return; if (나중수 == 8) { неуспех_VALUE("invokeLater queue full"); return; } 나중실행[나중수++] = објект_Референци; return; }
            if (наредба_CODE == 184 && Word_СМС(име_константа, "isEventDispatchThread") && Word_СМС(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            неуспех_VALUE("unsupported SwingUtilities method"); return;
        }
        if (Word_СМС(сопственик, "java/awt/event/ActionEvent")) {
            int објект_Референци = 빼기(2); if (!објект_VALUE(објект_Референци, 29)) return;
            if (Word_СМС(име_константа, "getSource") && Word_СМС(서술상수, "()Ljava/lang/Object;")) 넣기(힙[објект_Референци + 2], 2);
            else if (Word_СМС(име_константа, "getActionCommand") && Word_СМС(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[објект_Референци + 2]), 2);
            else if (Word_СМС(име_константа, "getID") && Word_СМС(서술상수, "()I")) 넣기(1001, 1);
            else неуспех_VALUE("unsupported ActionEvent method"); return;
        }
        if (наредба_CODE == 183 && Word_СМС(име_константа, "<init>")) {
            int COLUMNS = 0, СМС_Референци = 0;
            if (Word_СМС(서술상수, "(I)V")) COLUMNS = 빼기(1);
            else if (Word_СМС(서술상수, "(Ljava/lang/String;I)V")) { COLUMNS = 빼기(1); СМС_Референци = 빼기(2); }
            else if (Word_СМС(서술상수, "(Ljava/lang/String;)V")) СМС_Референци = 빼기(2);
            else if (Word_СМС(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_СМС(서술상수, "()V")) { неуспех_VALUE("unsupported Swing constructor"); return; }
            int објект_Референци = 빼기(2); if (!객체유효(објект_Референци)) return;
            if (힙[објект_Референци] == 30) { неуспех_VALUE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(објект_Референци) || COLUMNS < 0) return;
            int сметка_VALUE = корисник.화면연결(0, 힙[објект_Референци] - 23, 0, 0, 0, 0);
            if (сметка_VALUE < 1 || сметка_VALUE > 32) { неуспех_VALUE("GUI widget slots exhausted"); return; }
            힙[објект_Референци + 2] = сметка_VALUE; 화면참조[сметка_VALUE - 1] = објект_Референци; 힙[објект_Референци + 5] = 힙[објект_Референци] == 24 ? 130 : 16; 힙[објект_Референци + 6] = 힙[објект_Референци] == 24 ? 110 : 16;
            힙[објект_Референци + 7] = 힙[објект_Референци] == 24 ? 380 : 220; 힙[објект_Референци + 8] = 힙[објект_Референци] == 24 ? 240 : 28; 힙[објект_Референци + 10] = 1;
            화면문자설정(објект_Референци, СМС_Референци); return;
        }
        if (Word_СМС(име_константа, "setText") || Word_СМС(име_константа, "setTitle")) { int СМС_Референци = 빼기(2), објект_Референци = 빼기(2); if (화면객체(објект_Референци) && Word_СМС(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(објект_Референци, СМС_Референци); return; }
        if (Word_СМС(име_константа, "getText") || Word_СМС(име_константа, "getTitle")) { int објект_Референци = 빼기(2); if (화면객체(објект_Референци) && Word_СМС(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(објект_Референци), 2); return; }
        if (Word_СМС(име_константа, "addActionListener") && Word_СМС(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), објект_Референци = 빼기(2); if (화면객체(објект_Референци)) { 힙[објект_Референци + 4] = 수신참조; 힙참조[објект_Референци + 4] = 1; } return; }
        if (Word_СМС(име_константа, "getContentPane") && Word_СМС(서술상수, "()Ljava/awt/Container;")) { int објект_Референци = 빼기(2); if (화면객체(објект_Референци)) 넣기(објект_Референци, 2); return; }
        if (Word_СМС(име_константа, "setLayout") && Word_СМС(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Распоред_Референци = 빼기(2), објект_Референци = 빼기(2); if (화면객체(објект_Референци) && Распоред_Референци != 0) неуспех_VALUE("only absolute layout (null) is supported"); return; }
        if (Word_СМС(име_константа, "add") && (Word_СМС(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_СМС(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Распоред_услов = Word_СМС(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Распоред_услов) 빼기(2);
            int дете_Референци = 빼기(2), објект_Референци = 빼기(2); if (!화면객체(дете_Референци) || !화면객체(објект_Референци)) return;
            if (корисник.화면연결(2, 힙[објект_Референци + 2], 힙[дете_Референци + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[дете_Референци + 11] = објект_Референци; 힙참조[дете_Референци + 11] = 1; if (!Распоред_услов) 넣기(дете_Референци, 2); return;
        }
        if (Word_СМС(име_константа, "setBounds") && Word_СМС(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), координата_х = 빼기(1), објект_Референци = 빼기(2); if (!화면객체(објект_Референци)) return;
            if (корисник.화면연결(1, 힙[објект_Референци + 2], координата_х, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[објект_Референци + 5] = координата_х; 힙[објект_Референци + 6] = 세로좌표; 힙[објект_Референци + 7] = 너비; 힙[објект_Референци + 8] = 높이; return;
        }
        if (Word_СМС(име_константа, "setSize") && Word_СМС(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), објект_Референци = 빼기(2); if (!화면객체(објект_Референци)) return;
            if (корисник.화면연결(1, 힙[објект_Референци + 2], 힙[објект_Референци + 5], 힙[објект_Референци + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[објект_Референци + 7] = 너비; 힙[објект_Референци + 8] = 높이; } return;
        }
        if (Word_СМС(име_константа, "setLocationRelativeTo") && Word_СМС(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), објект_Референци = 빼기(2); if (!화면객체(објект_Референци)) return; if (상대배치 != 0) { неуспех_VALUE("only screen centering supported"); return; } 힙[објект_Референци + 5] = (корисник.화면너비() - 힙[објект_Референци + 7]) / 2; 힙[објект_Референци + 6] = (корисник.화면높이() - 힙[објект_Референци + 8]) / 2; корисник.화면연결(1, 힙[објект_Референци + 2], 힙[објект_Референци + 5], 힙[објект_Референци + 6], 힙[објект_Референци + 7], 힙[објект_Референци + 8]); return; }
        if (Word_СМС(име_константа, "setDefaultCloseOperation") && Word_СМС(서술상수, "(I)V")) { int правила = 빼기(1), објект_Референци = 빼기(2); if (화면객체(објект_Референци)) { if (правила < 0 || правила > 3) 예외던짐(9, "close policy"); else { 힙[објект_Референци + 10] = правила; корисник.화면연결(7, 힙[објект_Референци + 2], правила, 0, 0, 0); } } return; }
        if (Word_СМС(име_константа, "setVisible") && Word_СМС(서술상수, "(Z)V")) { int податоци_VALUE = 빼기(1), објект_Референци = 빼기(2); if (화면객체(објект_Референци)) { int 처리값 = корисник.화면연결(3, 힙[објект_Референци + 2], податоци_VALUE, 0, 0, 0); if (처리값 < 0) неуспех_VALUE("Swing requires a standalone interactive command"); else 힙[објект_Референци + 9] = податоци_VALUE; } return; }
        if (Word_СМС(име_константа, "dispose") && Word_СМС(서술상수, "()V")) { int објект_Референци = 빼기(2); if (화면객체(објект_Референци)) { корисник.화면연결(4, 힙[објект_Референци + 2], 0, 0, 0, 0); 힙[објект_Референци + 9] = 0; } return; }
        if (Word_СМС(име_константа, "repaint") || Word_СМС(име_константа, "validate")) { int објект_Референци = 빼기(2); if (!화면객체(објект_Референци) || !Word_СМС(서술상수, "()V")) return; корисник.화면연결(1, 힙[објект_Референци + 2], 힙[објект_Референци + 5], 힙[објект_Референци + 6], 힙[објект_Референци + 7], 힙[објект_Референци + 8]); return; }
        if (Word_СМС(име_константа, "isVisible") && Word_СМС(서술상수, "()Z")) { int објект_Референци = 빼기(2); if (화면객체(објект_Референци)) 넣기(힙[објект_Референци + 9], 1); return; }
        неуспех_VALUE("unsupported Swing method (native subset)");
    }
    static void 사건실행(int цел_адреса, int 사건번호, boolean Македонски) {
        if (цел_адреса < 1 || 힙[цел_адреса] < 32) { неуспех_VALUE("Java event listener required"); return; }
        int датотека_INDEX = име_метод(힙[цел_адреса] - 32, 사건번호 == 0 ? (Македонски ? "Изврши" : "run") : (Македонски ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (Македонски ? "(LМакедонски/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (датотека_INDEX < 0) { неуспех_VALUE("event callback missing"); return; }
        현재가닥 = 0; нишка_COUNT = 1; врами_INDEX = 0; нишка_статус[0] = 1; врами_Купче[0] = 0; 틀잠금[0] = иницијализирај_врами[0] = 0; измени_Барање_на_HTTP = false;
        for (int Loop_INDEX = 0; Loop_INDEX < 128; Loop_INDEX++) { локален_VALUE[Loop_INDEX] = локален_TYPE[Loop_INDEX] = 0; }
        врами_метод[0] = датотека_INDEX; врами_позиционирање[0] = метод_Start[датотека_INDEX]; локален_VALUE[0] = цел_адреса; локален_TYPE[0] = 2;
        if (사건번호 != 0) { локален_VALUE[1] = 사건번호; локален_TYPE[1] = 2; }
        사건중 = true; Изврши_наредба(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!ГРЕШКА) {
            if (나중수 > 0) { int цел_адреса = 나중실행[0], Македонски = 나중한국어[0]; for (int Loop_INDEX = 1; Loop_INDEX < 나중수; Loop_INDEX++) { 나중실행[Loop_INDEX - 1] = 나중실행[Loop_INDEX]; 나중한국어[Loop_INDEX - 1] = 나중한국어[Loop_INDEX]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(цел_адреса, 0, Македонски != 0); continue; }
            if (корисник.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = корисник.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { неуспех_VALUE("GUI event I/O failed"); return; }
            int сметка_VALUE = 사건번호 & 65535; if (сметка_VALUE < 1 || сметка_VALUE > 32) continue; int објект_Референци = 화면참조[сметка_VALUE - 1]; if (објект_Референци == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[објект_Референци + 10] != 0) 힙[објект_Референци + 9] = 0;
                if (힙[објект_Референци + 10] == 3) for (int Loop_INDEX = 0; Loop_INDEX < 32; Loop_INDEX++) if (화면참조[Loop_INDEX] != 0 && 힙[화면참조[Loop_INDEX]] == 24) корисник.화면연결(4, Loop_INDEX + 1, 0, 0, 0, 0);
            } else if (힙[објект_Референци + 4] != 0) {
                int информации_пред_употреба_Референци = додели_Склад(29, 2); if (ГРЕШКА) return; 힙[информации_пред_употреба_Референци + 2] = објект_Референци; 힙[информации_пред_употреба_Референци + 3] = 힙[објект_Референци + 12]; 힙참조[информации_пред_употреба_Референци + 2] = 1; 사건실행(힙[објект_Референци + 4], информации_пред_употреба_Референци, 힙[објект_Референци + 12] != 0);
            }
        }
    }
    public static int Изврши_2() {
        if (корисник.인수개수() == 1 && 자바도구.같음(корисник.Аргументи(0), "-version")) {
            корисник.Запиши("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (корисник.인수개수() < 1) { корисник.Запиши("Usage: java CLASS [ARGS]\n"); return 2; }
        внес_класа_Дефиниција = вчитај_класа_Дефиниција(вдоми_знак(корисник.Аргументи(0))); if (ГРЕШКА || внес_класа_Дефиниција < 0) return 1;
        int внес_поен_VALUE = име_метод(внес_класа_Дефиниција, "Изврши_2", "()V");
        boolean 한국어진입 = внес_поен_VALUE >= 0 && (метод_пристап[внес_поен_VALUE] & 9) == 9;
        if (!한국어진입) внес_поен_VALUE = име_метод(внес_класа_Дефиниција, "main", "([Ljava/lang/String;)V");
        if (внес_поен_VALUE < 0 || (метод_пристап[внес_поен_VALUE] & 9) != 9) неуспех_VALUE("public static void Изврши_2() or main(String[] args) required");
        if (ГРЕШКА) return 1;
        int Аргументи = додели_Склад(3, корисник.인수개수() - 1); низа_елемент[Аргументи] = -1;
        for (int 수 = 1; 수 < корисник.인수개수() && !ГРЕШКА; 수++) 힙[Аргументи + 1 + 수] = вдоми_знак(корисник.Аргументи(수));
        врами_INDEX = 0; врами_метод[0] = внес_поен_VALUE; врами_позиционирање[0] = метод_Start[внес_поен_VALUE]; локален_VALUE[0] = 한국어진입 ? 0 : Аргументи; локален_TYPE[0] = 한국어진입 ? 0 : 2;
        нишка_статус[0] = 1; нишка_објект[0] = додели_Склад(13, 2);
        Изврши_наредба(); if (!ГРЕШКА) 화면사건들(); return ГРЕШКА ? 1 : 0;
    }
}
