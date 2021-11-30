class Fait :
    def __init__(self,fait,explication):
        self.fait = fait
        self.explication = explication

    def print_fait(self):
        print("Fait :",self.fait)
        print("Explication: ",self.explication )

class Regle:
    def __init__(self,regle,premisse,conclusion):
        self.regle = regle 
        self.premisse = premisse
        self.conclusion = conclusion

    def print_regle(self):
        print("regle:",self.regle)
        print("premisse: ",self.premisse )
        print("concclusion :", self.conclusion)

def lire_fait():
    # file = input("base des faits: ")
    file="BF1.txt"
    f= open(file,"r")
    line =f.readline().strip()
    base_fait = list()
    while line: 
        base_fait.append(
            Fait(line,-1) 
        )
        line = f.readline().strip()
        
    f.close()
    return base_fait

def lire_regle():
    # file = input("base des regles: ")
    file="BR1.txt"
    f= open(file,"r")
    line =f.readline()
    base_regle = list()
    while line : 
        aux = line
        regle = aux.strip()
        # premisse = aux[1][ 
        #     aux[1].find("si") +2 : 
        #     aux[1].find("alors")
        # ].strip().split(' et ')
        
        premisse=regle[2:].split('alors')[0].strip().split('et')

        conclusion = aux.split('alors')[1].strip().split("et")
        base_regle.append(
            Regle(
                regle,
                premisse,
                conclusion
            )
        )
        line =f.readline()
    f.close()
    return base_regle

def print_base_f(base):
    for index in range (0, len(base)):
        base[index].print_fait()
        print("----------------------")

def print_base_r(base):
    for index in range (0, len(base)):
        base[index].print_regle()
        print("----------------------")

def in_base(base_fait,fait):
    for i in range(0,len(base_fait)):
        if fait == base_fait[i].fait :
            return True
    return False

def test(prem,tab):
    for j in range(0,len(prem)):
        if not(prem[j] in tab):
            return False
    return True


def chainage_avant(base_fait,base_regle,fait) : 
    tab_fait = list()
    #creation d'un tableau de fait
    for i in range(0,len(base_fait)):
        tab_fait.append(base_fait[i].fait)

    while not(in_base(base_fait,fait)):
        nb_fait = len(tab_fait)
        for i in range(0,len(base_regle)):

            prem =base_regle[i].premisse
            if test(prem,tab_fait):
                for k in range(0,len(base_regle[i].conclusion)):
                    base_fait.append(
                        Fait(
                            base_regle[i].conclusion[k],
                            base_regle[i].regle
                        )
                    )
                    tab_fait.append(base_regle[i].conclusion[k].strip())

                base_regle.remove(base_regle[i])
                #print(tab_fait)
                break
        if nb_fait == len(tab_fait):
            break 
    if fait in tab_fait:
        print(fait+ " établi")
    else :
        print(fait + " non-établi")


def chainage_arriere(base_fait,base_regle,but,trace=list()):
    tr = list()
    for b in but :
        if b in base_fait:
            tr.append('-1')
            continue
        for regle in base_regle:
            tr.append(regle.regle)
            if b in regle.conclusion:
                if test(regle.premisse,base_fait):
                    base_fait.append(b)
                    #print(b)
                    break
                else:
                    trace = chainage_arriere(base_fait,base_regle,regle.premisse,tr)
                    if not(trace == list()):
                        base_fait.append(b)
                        tr.append(trace)
                    else:
                        tr.remove(regle.regle)
                        
            else :
                tr.remove(regle.regle)
                #break
    return tr


#initialisation
base_fait=[]
base_regle=[]
but=""


base_fait=lire_fait()
base_regle=lire_regle()
#saisie But
but=input("But: ")

# print("Base faits: ")
# print_base_f(base_fait)
# print("Base Regle: ")
# print_base_r(base_regle)

#chainage avant
chainage_avant(base_fait,base_regle,but)

# Chainage arriere
tab_fait=[]
for ft in base_fait :
    tab_fait.append(ft.fait)
trace=[]
b=[]
b.append(but)
tr=chainage_arriere(tab_fait,base_regle,b,trace)
if len(tr) != 0 :
    print(but,"établi")
    trace = tr
else:
    print(but,"non établi")


