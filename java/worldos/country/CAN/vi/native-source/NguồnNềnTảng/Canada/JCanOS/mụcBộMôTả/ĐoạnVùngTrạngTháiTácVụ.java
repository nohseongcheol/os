// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.mụcBộMôTả;

/** Biểu diễn TSS được quản lý, cung cấp ngăn xếp đặc quyền khi chuyển tác vụ x86. */
public final class ĐoạnVùngTrạngTháiTácVụ {
    private int khốiKhôngSốNgănXếp;
    private int địaChỉKhôngSốNgănXếp;
    private int vịTríBảngTraQuyềnVàoRa = 104;

    public void đặtGiáTrịNgănXếpCóĐặcQuyền(int giáTrịĐoạn, int địaChỉ) {
        khốiKhôngSốNgănXếp = giáTrịĐoạn;
        địaChỉKhôngSốNgănXếp = địaChỉ;
    }

    public int khốiKhôngSốNgănXếp() { return khốiKhôngSốNgănXếp; }
    public int địaChỉKhôngSốNgănXếp() { return địaChỉKhôngSốNgănXếp; }
    public int vịTríBảngTraQuyềnVàoRa() { return vịTríBảngTraQuyềnVàoRa; }
}

