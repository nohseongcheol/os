// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
/** ትግርኛ 화면 구성요소를 만드는 편의 ተግባር_ዋጋ. */
public final class መዘካከሪ_መትሓዚ {
    private መዘካከሪ_መትሓዚ() {}
    public static void 나중에실행(실행할일 ዕማም_ስጉምቲ) { ፍጻመ_ሪጋ.나중에실행(ዕማም_ስጉምቲ); }
    public static ገላጺ መፈለጥታ_ዋጋ(String ጽሑፍ, int 가로, int 세로, int 폭, int 높이) {
        return new ገላጺ(ጽሑፍ, 가로, 세로, 폭, 높이);
    }
    public static መጠወቒ መጠወቒ(String ጽሑፍ, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        return new መጠወቒ(ጽሑፍ, 가로, 세로, 폭, 높이, 받이);
    }
    public static ጽሑፍ_ሜዳ ጽሑፍ_ሜዳ(String ጽሑፍ, int 가로, int 세로, int 폭, int 높이) {
        return new ጽሑፍ_ሜዳ(ጽሑፍ, 가로, 세로, 폭, 높이);
    }
}
