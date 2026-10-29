// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 ᎢᎩᏓ 작업 ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ 할당/반환. 일반 물리 ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ 관리자는 아니다. */
public final class 기억공간 {
    static int[] ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ = new int[8192];
    static int[] 사용 = new int[8];

    static int 정수읽기(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        return ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.기억읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) | (ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.기억읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ + 1) << 8)
            | (ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.기억읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ + 2) << 16) | (ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.기억읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.부팅정보();
        if (ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (정수읽기(msinfo32_exe) & 1) == 0) return -1;
        return 정수읽기(msinfo32_exe + 8);
    }

    static int 할당() {
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 사용.length; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            if (사용[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] == 0) {
                사용[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * 1024 + 칸] = 0;
                return ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ;
            }
        }
        return -1;
    }

    static boolean 반환(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 0 || ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ >= 사용.length || 사용[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] == 0) return false;
        사용[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 사용.length; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) 개수 += 사용[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ];
        return 개수;
    }
}
