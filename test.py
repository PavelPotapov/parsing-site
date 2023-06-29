def zapret_s(s):
    zapret = ["'", '"', ':', '?', '>', '<', '*', '|']
    for i in zapret:
        if i in s:
            s = s.replace(i,'')
    return s