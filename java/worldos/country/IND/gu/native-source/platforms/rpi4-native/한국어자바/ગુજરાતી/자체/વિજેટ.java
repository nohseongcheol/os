// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** ગુજરાતી 화면 구성요소를 만드는 편의 ફંક્શંસ_મૂલ્ય. */
public final class વિજેટ {
    private વિજેટ() {}
    public static void 나중에실행(실행할일 કાર્ય_સંદેશ) { ઇવેંટ_કતાર.나중에실행(કાર્ય_સંદેશ); }
    public static લેબલ ટૅગ_મૂલ્ય(String લખાણ, int 가로, int ઊભી_સ્થિતિ, int 폭, int 높이) {
        return new લેબલ(લખાણ, 가로, ઊભી_સ્થિતિ, 폭, 높이);
    }
    public static બટન બટન(String લખાણ, int 가로, int ઊભી_સ્થિતિ, int 폭, int 높이, 동작받이 받이) {
        return new બટન(લખાણ, 가로, ઊભી_સ્થિતિ, 폭, 높이, 받이);
    }
    public static ટેક્સ્ટ_ફીલ્ડ ટેક્સ્ટ_ફીલ્ડ(String લખાણ, int 가로, int ઊભી_સ્થિતિ, int 폭, int 높이) {
        return new ટેક્સ્ટ_ફીલ્ડ(લખાણ, 가로, ઊભી_સ્થિતિ, 폭, 높이);
    }
}
