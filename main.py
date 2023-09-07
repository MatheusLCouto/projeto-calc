import re

regex = r"^((\w)(\w+)(\s[^D])(\w+))|^((\w)(\w+)(\s)(D\w)(\s\w)(\w+))"

test_str = ("ANA CLEIDE\n"
            "DEUZALINA OLIVEIRA\n"
            "JACIRA NUNES\n"
            "JUCILENE DE JESUS\n"
            "KAMILA NUNES\n"
            "LINDALVA SERRAO\n"
            "MARILDA VELOSO\n"
            "MARLENE DA SILCA\n"
            "PAULO ROBISSON")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

        if match.group(1):
            nomeComplet: str = "".join(match.group(2) + match.group(3).lower() + match.group(4) + match.group(5).lower())
            print(nomeComplet)

        if match.group(6):
            nomeComplet: str = match.group(7) + match.group(8).lower() + match.group(9) + match.group(10).lower() + match.group(11) + match.group(12).lower()
            print(nomeComplet)
        #print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=match.start(groupNum),
                                                                        #end=match.end(groupNum),
                                                                        #group=match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
