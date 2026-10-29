// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Wepụta_ọzi 전용 mee_nnyemiwu 묶음의 ELF32 mee_ịbanihe, 인수 zìgaā_valuu, 한 번에 한 òjìàrụ ùsòrò_valuu_6712bde7 mee_nnyemiwu. */
public final class 실행관리 {
    static final int Mbido_òjìàrụ_app = 0x04000000;
    static final int òjìàrụ_mèdebe = 0x04400000;
    static final int foto_mèdebe_àdreèsì = 0x04200000;
    static final int agụment_Mbido = 0x04300000;
    static int 인수수 = 0;
    static int[] agụment_àdreèsì = new int[16];

    static boolean ntipanye(int àdreèsì, int ogologo_valuu) {
        return àdreèsì >= Mbido_òjìàrụ_app && àdreèsì < òjìàrụ_mèdebe && ogologo_valuu >= 0 && ogologo_valuu <= òjìàrụ_mèdebe - àdreèsì;
    }

    static int 수(int àdreèsì) { return 기억공간.kerìsịa_ọnụọgụ_nzùrùòkè(àdreèsì); }
    static int 짧은수(int àdreèsì) { return njìarụ_valuu.기억읽기(àdreèsì) | njìarụ_valuu.기억읽기(àdreèsì + 1) << 8; }
    static void 수쓰기(int àdreèsì, int valuu) {
        for (int indèks = 0; indèks < 4; indèks++) njìarụ_valuu.dee_memọrị(àdreèsì + indèks, valuu >>> (indèks * 8));
    }

    static int 묶음개수() {
        int àdreèsì = njìarụ_valuu.실행묶음();
        int Ụhara = njìarụ_valuu.실행묶음크기();
        if (Ụhara < 8 || 수(àdreèsì) != 0x50414b4a) return 0;
        int 개수 = 수(àdreèsì + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Ụhara - 8) / 24 ? 개수 : 0;
    }

    static void ndebà_ndepụta() {
        for (int indèks = 0; indèks < 묶음개수(); indèks++) {
            int ndebà_valuu = njìarụ_valuu.실행묶음() + 8 + indèks * 24;
            for (int mkpụrụedemede_valuu = 0; mkpụrụedemede_valuu < 16 && njìarụ_valuu.기억읽기(ndebà_valuu + mkpụrụedemede_valuu) != 0; mkpụrụedemede_valuu++)
                문자단말.문자(njìarụ_valuu.기억읽기(ndebà_valuu + mkpụrụedemede_valuu));
            문자단말.Chekwaa_ozi("\n");
        }
    }

    static int chọta_ndebà(int[] 입력, int Bido, int ogologo_valuu) {
        if (ogologo_valuu <= 0 || ogologo_valuu >= 16) return 0;
        for (int indèks = 0; indèks < 묶음개수(); indèks++) {
            int ndebà_valuu = njìarụ_valuu.실행묶음() + 8 + indèks * 24;
            boolean 같음 = njìarụ_valuu.기억읽기(ndebà_valuu + ogologo_valuu) == 0;
            for (int mkpụrụedemede_valuu = 0; mkpụrụedemede_valuu < ogologo_valuu; mkpụrụedemede_valuu++)
                if (입력[Bido + mkpụrụedemede_valuu] != njìarụ_valuu.기억읽기(ndebà_valuu + mkpụrụedemede_valuu)) 같음 = false;
            if (같음) return ndebà_valuu;
        }
        return 0;
    }

    static int mee_ịbanihe(int Faịlụ, int ogologo_valuu) {
        if (ogologo_valuu < 52 || 수(Faịlụ) != 0x464c457f || njìarụ_valuu.기억읽기(Faịlụ + 4) != 1
            || njìarụ_valuu.기억읽기(Faịlụ + 5) != 1 || njìarụ_valuu.기억읽기(Faịlụ + 6) != 1
            || 짧은수(Faịlụ + 16) != 2 || 짧은수(Faịlụ + 18) != 3 || 수(Faịlụ + 20) != 1
            || 짧은수(Faịlụ + 40) != 52 || 짧은수(Faịlụ + 42) != 32) return -8;
        int ndebà_akara_valuu = 수(Faịlụ + 24);
        int 표위치 = 수(Faịlụ + 28);
        int 개수 = 짧은수(Faịlụ + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > ogologo_valuu - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int indèks = 0; indèks < 개수; indèks++) {
            int 표 = Faịlụ + 표위치 + indèks * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Banye/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), àdreèsì = 수(표 + 8), ọbọakwụkwọ_ụha = 수(표 + 16), memọrị_ụha = 수(표 + 20);
            int hàkọma_valuu = 수(표 + 28);
            if (àdreèsì < Mbido_òjìàrụ_app || àdreèsì >= foto_mèdebe_àdreèsì || memọrị_ụha < 0 || memọrị_ụha > foto_mèdebe_àdreèsì - àdreèsì
                || ọbọakwụkwọ_ụha < 0 || ọbọakwụkwọ_ụha > memọrị_ụha || 위치 < 0 || (ọbọakwụkwọ_ụha > 0 && 위치 > ogologo_valuu - ọbọakwụkwọ_ụha)
                || (hàkọma_valuu != 0 && (hàkọma_valuu < 0 || (hàkọma_valuu & (hàkọma_valuu - 1)) != 0
                    || ((àdreèsì - 위치) & (hàkọma_valuu - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < indèks; 앞++) {
                int 이전 = Faịlụ + 표위치 + 앞 * 32;
                if (수(이전) == 1 && memọrị_ụha > 0 && 수(이전 + 20) > 0
                    && àdreèsì < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < àdreèsì + memọrị_ụha) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && ndebà_akara_valuu >= àdreèsì && ndebà_akara_valuu - àdreèsì < ọbọakwụkwọ_ụha) 실행가능 = true;
        }
        return 실행가능 ? ndebà_akara_valuu : -8;
    }

    static int mee_nnyemiwu(int[] 입력, int Bido, int ogologo_valuu) {
        while (Bido < ogologo_valuu && 입력[Bido] == ' ') Bido++;
        int 끝 = Bido;
        while (끝 < ogologo_valuu && 입력[끝] != ' ') 끝++;
        int ndebà_valuu = chọta_ndebà(입력, Bido, 끝 - Bido);
        if (ndebà_valuu == 0) return -2;
        int 위치 = 수(ndebà_valuu + 16), Ụhara = 수(ndebà_valuu + 20);
        if (위치 < 8 + 묶음개수() * 24 || Ụhara < 52 || 위치 > njìarụ_valuu.실행묶음크기() - Ụhara) return -8;
        int Faịlụ = njìarụ_valuu.실행묶음() + 위치;
        int ndebà_akara_valuu = mee_ịbanihe(Faịlụ, Ụhara);
        if (ndebà_akara_valuu < 0) return ndebà_akara_valuu;
        njìarụ_valuu.òjìàrụ_hichaa_TOC();
        int 표위치 = 수(Faịlụ + 28), 개수 = 짧은수(Faịlụ + 44);
        for (int indèks = 0; indèks < 개수; indèks++) {
            int 표 = Faịlụ + 표위치 + indèks * 32;
            if (수(표) != 1) continue;
            int 원본 = Faịlụ + 수(표 + 4), ebemwèga_valuu = 수(표 + 8), ọbọakwụkwọ_ụha = 수(표 + 16);
            for (int baịtị_valuu = 0; baịtị_valuu < ọbọakwụkwọ_ụha; baịtị_valuu++) njìarụ_valuu.dee_memọrị(ebemwèga_valuu + baịtị_valuu, njìarụ_valuu.기억읽기(원본 + baịtị_valuu));
        }
        인수수 = 0;
        int Store_valuu = agụment_Mbido;
        while (끝 < ogologo_valuu) {
            while (끝 < ogologo_valuu && 입력[끝] == ' ') 끝++;
            if (끝 == ogologo_valuu) break;
            if (인수수 == agụment_àdreèsì.length) return -22;
            Bido = 끝;
            while (끝 < ogologo_valuu && 입력[끝] != ' ') 끝++;
            agụment_àdreèsì[인수수++] = Store_valuu;
            수쓰기(Store_valuu, 끝 - Bido);
            for (int mkpụrụedemede_valuu = Bido; mkpụrụedemede_valuu < 끝; mkpụrụedemede_valuu++) 수쓰기(Store_valuu + 4 + (mkpụrụedemede_valuu - Bido) * 4, 입력[mkpụrụedemede_valuu]);
            Store_valuu += 4 + (끝 - Bido) * 4;
        }
        Netwọọkụ_ikpo.과정정리();
        파일서술자관리.Mbido_ùsòrò();
        int 결과 = njìarụ_valuu.mee_òjìàrụ_app(ndebà_akara_valuu, òjìàrụ_mèdebe - 16);
        파일서술자관리.과정정리();
        Netwọọkụ_ikpo.과정정리();
        return 결과;
    }
}
