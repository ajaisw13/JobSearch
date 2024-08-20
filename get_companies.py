
res = []
f2 = open('new_companies.txt', 'w')
with open('companies_raw.txt') as f:
    while True:
        try:
            s = f.readline()
            if s=='\n':
                continue
            if not s:
                break
            s = s.strip('\n')
            if s[0]>='0' and s[0]<='9':
                for x in s.split(' '):
                    if x and ((x[0]>='a' and x[0]<='z') or (x[0]>='A' and x[0]<='Z')):
                        f2.write(x+'\n')
                        break 
            else:
                f2.write("check this lines"+s,+'\n')


        except:
            f2.write("Encoding issue: "+s+'\n')
