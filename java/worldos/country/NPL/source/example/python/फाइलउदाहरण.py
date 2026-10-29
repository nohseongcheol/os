from नेपाली import 출력, लेख्नुहोस्_फाइल, 파일읽기, 글부호화, 글해독
लगत = "PYTHON फाइल: Nepali (macrolanguage) 😀\n"
लेख्नुहोस्_फाइल("python.txt", 글부호화(लगत))
읽은글 = 글해독(파일읽기("python.txt"))
assert 읽은글 == लगत
출력(읽은글, 끝="")
