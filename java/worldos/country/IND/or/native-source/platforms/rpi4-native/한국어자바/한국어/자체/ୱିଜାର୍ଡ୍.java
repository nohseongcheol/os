// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 Excel_ଟେବଲ୍_ମୂଲ୍ୟ. */
public final class ୱିଜାର୍ଡ୍ {
    private ୱିଜାର୍ଡ୍() {}
    public static void 나중에실행(실행할일 ଟାସ୍କ_କ୍ରିୟା) { ଘଟଣା_ପ୍ରତିଧାଡ଼ି.나중에실행(ଟାସ୍କ_କ୍ରିୟା); }
    public static ସୂଚକ ଟ୍ୟାଗ୍_ମୂଲ୍ୟ(String ପାଠ୍ଯ, int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, int 폭, int 높이) {
        return new ସୂଚକ(ପାଠ୍ଯ, 가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 폭, 높이);
    }
    public static ବଟନ୍ ବଟନ୍(String ପାଠ୍ଯ, int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, int 폭, int 높이, 동작받이 받이) {
        return new ବଟନ୍(ପାଠ୍ଯ, 가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 폭, 높이, 받이);
    }
    public static ପାଠ୍ୟ_କ୍ଷେତ୍ର ପାଠ୍ୟ_କ୍ଷେତ୍ର(String ପାଠ୍ଯ, int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, int 폭, int 높이) {
        return new ପାଠ୍ୟ_କ୍ଷେତ୍ର(ପାଠ୍ଯ, 가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 폭, 높이);
    }
}
