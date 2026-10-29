"""Freestanding BMP Java identifier rules from Unicode general categories.

Java start: letters, letter numbers, currency and connector punctuation.
Java part adds combining marks, decimal digits and ignorable characters.
Surrogates are rejected; the current lexer does not combine supplementary
identifier characters. This is separate from UTF-8 string/emoji support.
"""
import unicodedata
from functools import lru_cache


@lru_cache(maxsize=1)
def source():
    def start(code):return unicodedata.category(chr(code)) in ('Lu','Ll','Lt','Lm','Lo','Nl','Sc','Pc')
    def part(code):return start(code) or unicodedata.category(chr(code)) in ('Mn','Mc','Nd','Cf') or code<=8 or 14<=code<=27 or 127<=code<=159
    def ranges(predicate):
        result=[];begin=None
        for code in range(65537):
            matched=code<65536 and predicate(code)
            if matched and begin is None:begin=code
            if not matched and begin is not None:result.extend([begin,code-1]);begin=None
        return ','.join(str(value) for value in result)
    return '''/** Unicode %s, BMP Java identifier start/part. Generated table. */
public final class 문자이름규칙 {
    static int[] 첫범위 = new int[]{%s};
    static int[] 뒤범위 = new int[]{%s};
    static boolean 범위안(int 값, int[] 범위) {
        int 왼쪽=0, 오른쪽=범위.length/2;
        while (왼쪽<오른쪽) {
            int 가운데=(왼쪽+오른쪽)/2;
            if (값<범위[가운데*2]) 오른쪽=가운데;
            else if (값>범위[가운데*2+1]) 왼쪽=가운데+1;
            else return true;
        }
        return false;
    }
    static boolean 첫글자(int 값) { return 범위안(값, 첫범위); }
    static boolean 이어진글자(int 값) { return 범위안(값, 뒤범위); }
}
''' % (unicodedata.unidata_version,ranges(start),ranges(part))
