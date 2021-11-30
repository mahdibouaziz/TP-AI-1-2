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
        print("conclusion :", self.conclusion)

def lire_fait():
    # file = input("base des faits: ")
    file="BF1.txt"
    f= open(file,"r")
    line =f.readline().strip()
    base_fait = []
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

def print_base_r(base):
    for index in range (0, len(base)):
        base[index].print_regle()

def in_base(base_fait,fait):
    for i in range(0,len(base_fait)):
        if fait == base_fait[i].fait :
            return True
    return False

def verifAllPremissInTab(prem,tab):
    for j in range(0,len(prem)):
        if not(prem[j] in tab):
            return False
    return True


def chainage_avant(base_fait,base_regle,fait) : 
    tab_fait = []
    #tableau de fait
    for i in range(0,len(base_fait)):
        tab_fait.append(base_fait[i].fait)

    while not(in_base(base_fait,fait)):
        nb_fait = len(tab_fait)
        for i in range(0,len(base_regle)):

            prem =base_regle[i].premisse
            if verifAllPremissInTab(prem,tab_fait):
                base_fait.append(
                    Fait(
                        base_regle[i].conclusion[0],
                        base_regle[i].regle
                    )
                )
                tab_fait.append(base_regle[i].conclusion[0].strip())

                base_regle.remove(base_regle[i])
                break
        if nb_fait == len(tab_fait):
            break 
    if fait in tab_fait:
        print(fait+ " établi")
    else :
        print(fait + " non-établi")

def chainage_arriere(base_fait,base_regle,but,trace=list()):
    tr = []
    for b in but :
        if b in base_fait:
            tr.append('-1')
            continue
        for regle in base_regle:
            tr.append(regle.regle)
            if b in regle.conclusion:
                if verifAllPremissInTab(regle.premisse,base_fait):
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


#the main function
while True:
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
    print("1: chainage avant\n2: chainage arriere\n3: exit\n")
    x=input("Rep: ")
    if x=="1":
        #chainage avant
        chainage_avant(base_fait,base_regle,but)
        #Ecrire la trace dans un fichier texte
        f = open("traceAvant.txt","w")
        print_base_f(base_fait)
        for f1 in base_fait:
            if (f1.explication!=-1):
                tr=str(f1.explication)+"\n"
                f.write(tr)
        print("-------------------------\n")
        f.close()
    elif x=="2":
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
        else:
            print(but,"non établi")

        #Ecrire la trace dans un fichier texte
        f = open("traceArriere.txt","w")
        tr=str(tr)
        f.write(tr)
        f.close()
        print("-------------------------\n")
    elif x=="3":
        break
