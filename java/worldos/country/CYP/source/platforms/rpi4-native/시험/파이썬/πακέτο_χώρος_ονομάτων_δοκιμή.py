import jkoros
import πακέτο
import sys

기존목록 = jkoros.read("/lib/.pip.json")
개수 = 0
try:
    while True:
        jkoros.write("/가득%d" % 개수, b"saved")
        개수 += 1
except OSError as ΣΦΑΛΜΑ:
    assert ΣΦΑΛΜΑ.args[0] == 28
assert 개수 >= 2
for Ευρετήριο in range(개수 - 2, 개수):
    jkoros.remove("/가득%d" % Ευρετήριο)
try:
    πακέτο.εγκαθιστώ_τιμή("jkoros-space==1.0", int(sys.argv[1]))
except OSError as ΣΦΑΛΜΑ:
    assert ΣΦΑΛΜΑ.args[0] == 28
else:
    raise AssertionError("διεύθυνση_περιοχή 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == 기존목록
for Ευρετήριο in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % Ευρετήριο) == 0
for Ευρετήριο in range(개수 - 2):
    assert jkoros.read("/가득%d" % Ευρετήριο) == b"saved"
    jkoros.remove("/가득%d" % Ευρετήριο)
print("πακέτο διεύθυνση_περιοχή 부족 επιστρέφω_γέφυρα επαληθεύω")
