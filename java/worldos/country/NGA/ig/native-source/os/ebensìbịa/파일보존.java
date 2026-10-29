// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_valuu hàzie_valuu. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] ọbọakwụkwọ_tebùl = new int[1024];
    static int 바이트해시(int valuu, int datà) { return (valuu ^ datà) * 16777619; }
    static void hichaa_datà() {
        for (int indèks = 0; indèks < 512; indèks++) Nchekwa_njìarụ_njikọ.nkebì_datà[indèks] = 0;
    }
    static int tebùl_ọnụọgụ_nzùrùòkè(int 위치) {
        return ọbọakwụkwọ_tebùl[위치] | ọbọakwụkwọ_tebùl[위치 + 1] << 8 | ọbọakwụkwọ_tebùl[위치 + 2] << 16 | ọbọakwụkwọ_tebùl[위치 + 3] << 24;
    }
    static void dee_tebùl_ọnụọgụ_nzùrùòkè(int 위치, int valuu) {
        for (int indèks = 0; indèks < 4; indèks++) ọbọakwụkwọ_tebùl[위치 + indèks] = (valuu >>> (indèks * 8)) & 255;
    }
    static boolean cheèk_tebùl() {
        for (int Faịlụ = 0; Faịlụ < 8; Faịlụ++) {
            int ogologo_valuu = 0;
            for (int oghere_ndebà = 0; oghere_ndebà < 64; oghere_ndebà++) memọrị_sistèm_ọbọakwụkwo.Aha[oghere_ndebà] = ọbọakwụkwọ_tebùl[Faịlụ * 72 + oghere_ndebà];
            while (ogologo_valuu < 64 && memọrị_sistèm_ọbọakwụkwo.Aha[ogologo_valuu] != 0) ogologo_valuu++;
            if (ogologo_valuu == 0) continue;
            if (!memọrị_sistèm_ọbọakwụkwo.cheèk_akara_ahà(memọrị_sistèm_ọbọakwụkwo.Aha, ogologo_valuu)
                || tebùl_ọnụọgụ_nzùrùòkè(Faịlụ * 72 + 64) < 0 || tebùl_ọnụọgụ_nzùrùòkè(Faịlụ * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Faịlụ; 앞++) {
                boolean 같음 = ọbọakwụkwọ_tebùl[앞 * 72 + ogologo_valuu] == 0;
                for (int oghere_ndebà = 0; oghere_ndebà < ogologo_valuu; oghere_ndebà++) if (ọbọakwụkwọ_tebùl[앞 * 72 + oghere_ndebà] != memọrị_sistèm_ọbọakwụkwo.Aha[oghere_ndebà]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Mbido_nkebì = 1 + 보존본 * 259;
        if (Nchekwa_njìarụ_njikọ.Wepụta_ọzi(Mbido_nkebì) < 0 || Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(0) != 0x4a4b534e) return -1;
        int 세대 = Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(4), 검사합 = Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(8);
        if (세대 < 1 || Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int di_ike_ọbọakwụkwọ = 0x811c9dc5;
        for (int nkebì_valuu = 0; nkebì_valuu < 258; nkebì_valuu++) {
            if (Nchekwa_njìarụ_njikọ.Wepụta_ọzi(Mbido_nkebì + 1 + nkebì_valuu) < 0) return -1;
            for (int oghere_ndebà = 0; oghere_ndebà < 512; oghere_ndebà++) {
                int valuu = Nchekwa_njìarụ_njikọ.nkebì_datà[oghere_ndebà];
                di_ike_ọbọakwụkwọ = 바이트해시(di_ike_ọbọakwụkwọ, valuu);
                if (nkebì_valuu < 2) ọbọakwụkwọ_tebùl[nkebì_valuu * 512 + oghere_ndebà] = valuu;
            }
        }
        return di_ike_ọbọakwụkwọ == 검사합 && cheèk_tebùl() ? 세대 : -1;
    }
    static int ibu(int 보존본) {
        int Mbido_nkebì = 1 + 보존본 * 259;
        for (int nkebì_valuu = 0; nkebì_valuu < 2; nkebì_valuu++) {
            if (Nchekwa_njìarụ_njikọ.Wepụta_ọzi(Mbido_nkebì + 1 + nkebì_valuu) < 0) return -5;
            for (int oghere_ndebà = 0; oghere_ndebà < 512; oghere_ndebà++) ọbọakwụkwọ_tebùl[nkebì_valuu * 512 + oghere_ndebà] = Nchekwa_njìarụ_njikọ.nkebì_datà[oghere_ndebà];
        }
        for (int Faịlụ = 0; Faịlụ < 8; Faịlụ++) {
            for (int oghere_ndebà = 0; oghere_ndebà < 64; oghere_ndebà++) memọrị_sistèm_ọbọakwụkwo.이름들[Faịlụ * 64 + oghere_ndebà] = ọbọakwụkwọ_tebùl[Faịlụ * 72 + oghere_ndebà];
            memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ] = ọbọakwụkwọ_tebùl[Faịlụ * 72] == 0 ? 0 : tebùl_ọnụọgụ_nzùrùòkè(Faịlụ * 72 + 64);
            memọrị_sistèm_ọbọakwụkwo.허가들[Faịlụ] = tebùl_ọnụọgụ_nzùrùòkè(Faịlụ * 72 + 68) & 511;
            for (int nkebì_valuu = 0; nkebì_valuu < 32; nkebì_valuu++) {
                if (Nchekwa_njìarụ_njikọ.Wepụta_ọzi(Mbido_nkebì + 3 + Faịlụ * 32 + nkebì_valuu) < 0) return -5;
                int àdreèsì = njìarụ_valuu.ọbọakwụkwọ_memọrị() + Faịlụ * 16384 + nkebì_valuu * 512;
                for (int oghere_ndebà = 0; oghere_ndebà < 512; oghere_ndebà++) njìarụ_valuu.dee_memọrị(àdreèsì + oghere_ndebà, Nchekwa_njìarụ_njikọ.nkebì_datà[oghere_ndebà]);
            }
        }
        return 0;
    }
    static void Kwado() {
        if (Nchekwa_njìarụ_njikọ.Wepụta_ọzi(0) < 0 || Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(0) != 0x54534b4a
            || Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(4) != 0x3145524f || Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(8) != 2048
            || Nchekwa_njìarụ_njikọ.kerìsịa_ọnụọgụ_nzùrùòkè(12) != 0x3153464a) {
            문자단말.Chekwaa_ozi("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Nchekwa_njìarụ_njikọ.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Chekwaa_ozi("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (ibu(현재보존본) < 0) {
            문자단말.Chekwaa_ozi("STORE read failed; halted to preserve files\n"); njìarụ_valuu.정지();
        }
        문자단말.Chekwaa_ozi("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int hàkọọ() {
        if (!Nchekwa_njìarụ_njikọ.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, Mbido_nkebì = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 njìarụ_valuu 캐시를 비운다.
        hichaa_datà();
        if (Nchekwa_njìarụ_njikọ.Chekwaa_ozi(Mbido_nkebì) < 0 || Nchekwa_njìarụ_njikọ.밀어쓰기() < 0) return -5;
        for (int oghere_ndebà = 0; oghere_ndebà < 1024; oghere_ndebà++) ọbọakwụkwọ_tebùl[oghere_ndebà] = 0;
        for (int Faịlụ = 0; Faịlụ < 8; Faịlụ++) if (memọrị_sistèm_ọbọakwụkwo.이름들[Faịlụ * 64] != 0) {
            for (int oghere_ndebà = 0; oghere_ndebà < 64; oghere_ndebà++) ọbọakwụkwọ_tebùl[Faịlụ * 72 + oghere_ndebà] = memọrị_sistèm_ọbọakwụkwo.이름들[Faịlụ * 64 + oghere_ndebà];
            dee_tebùl_ọnụọgụ_nzùrùòkè(Faịlụ * 72 + 64, memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ]);
            dee_tebùl_ọnụọgụ_nzùrùòkè(Faịlụ * 72 + 68, memọrị_sistèm_ọbọakwụkwo.허가들[Faịlụ]);
        }
        int di_ike_ọbọakwụkwọ = 0x811c9dc5;
        for (int nkebì_valuu = 0; nkebì_valuu < 258; nkebì_valuu++) {
            for (int oghere_ndebà = 0; oghere_ndebà < 512; oghere_ndebà++) {
                int valuu = 0;
                if (nkebì_valuu < 2) valuu = ọbọakwụkwọ_tebùl[nkebì_valuu * 512 + oghere_ndebà];
                else {
                    int Faịlụ = (nkebì_valuu - 2) / 32, 위치 = (nkebì_valuu - 2) % 32 * 512 + oghere_ndebà;
                    if (ọbọakwụkwọ_tebùl[Faịlụ * 72] != 0 && 위치 < memọrị_sistèm_ọbọakwụkwo.ụha_ndepụta[Faịlụ])
                        valuu = njìarụ_valuu.기억읽기(njìarụ_valuu.ọbọakwụkwọ_memọrị() + Faịlụ * 16384 + 위치);
                }
                Nchekwa_njìarụ_njikọ.nkebì_datà[oghere_ndebà] = valuu; di_ike_ọbọakwụkwọ = 바이트해시(di_ike_ọbọakwụkwọ, valuu);
            }
            if (Nchekwa_njìarụ_njikọ.Chekwaa_ozi(Mbido_nkebì + 1 + nkebì_valuu) < 0) return -5;
        }
        if (Nchekwa_njìarụ_njikọ.밀어쓰기() < 0) return -5;
        hichaa_datà(); Nchekwa_njìarụ_njikọ.dee_ọnụọgụ_nzùrùòkè_valuu(0, 0x4a4b534e);
        Nchekwa_njìarụ_njikọ.dee_ọnụọgụ_nzùrùòkè_valuu(4, 세대번호 + 1); Nchekwa_njìarụ_njikọ.dee_ọnụọgụ_nzùrùòkè_valuu(8, di_ike_ọbọakwụkwọ);
        Nchekwa_njìarụ_njikọ.dee_ọnụọgụ_nzùrùòkè_valuu(12, (세대번호 + 1) ^ di_ike_ọbọakwụkwọ ^ 0x4a4b534e);
        if (Nchekwa_njìarụ_njikọ.Chekwaa_ozi(Mbido_nkebì) < 0 || Nchekwa_njìarụ_njikọ.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
