from email.policy import default
import hashlib
from getpass import getpass
import datetime
from itertools import product
from os.path import exists as file_exists

alleProducten = []
alleKlanten = []
aanwezigeKlanten = []
datum = str(datetime.datetime.now().strftime("%d-%m-%Y"))
drankenNummer = {'1': 'Bieren (tap)', '2': 'Bieren (fles)', '3': 'Wijnen', '4': "Shot's", '5': "Coctails", '6': 'Frisdranken', '7': 'Eten'}

def checkPassword(mode="default"): 
    if mode == "default":
        print("\t\t- Voor deze functie is een passwoord vereist!\n\t\t  Vraag even hulp aan de CREW. (verlaat met 'end')\n\t\t  ", end='')
    elif mode == "defretry":
        print("\t\t\t- Er is een verkeerd passwoord ingevult!\n\n\t\t  Probeer opnieuw. (verlaat met 'end')\n\t\t  ", end='')
    elif mode == "logretry":
        print("\nEr is een verkeerd passwoord ingevult!\nProbeer opnieuw. (verlaat met 'end')")
    elif mode == "log":
        print("\nWelkom bij het telsysteem van Den Artois,\nom in te loggen heb je een wachtwoord nodig, vul dit in en druk op enter. (verlaat met 'end')")
    with open('setup.txt') as file:
        line = file.readline().rstrip()
        while line != "//Setup":
            line = file.readline().rstrip()
        line = file.readline().rstrip()
        record = line.split(':')
        while record[0] != "password":
            line = file.readline().rstrip()
            record = line.split(':')
        plaintext = getpass()
        encodedText = plaintext.encode()
        d = hashlib.sha256(encodedText)
        hash = d.digest()
        if str(hash) == str(record[1]):
            return "correct"
        elif plaintext == "end":
            return "end"
        else:
            return "fout"




#Opstarten kassa
def startUp():
    response = checkPassword("log")
    while response != "correct":
        if response == "end":
            quit()
        elif response == "fout":
            response = checkPassword("logretry")
    
    print("Passwoord correct!", end='')
    while True:
        print("\n\nWat wil je doen?")
        keuze = "0"
        while keuze not in ["p", "d", "s"]:
            keuze = input("\t- 'p' poef van klanten checken          - 'd' dagoverzichten bekijken          - 's' PoS openen\n\t- ")
            if keuze == "p":
                poef()
            elif keuze == "d":
                dagOverzichten()
            elif keuze == "s":
                PoS()
            elif keuze == "end":
                quit()
            else:
                print("\nKeuze niet herkent probeer opnieuw!")

#Funties Point of Sale
def PoS():
    PoSstartUp()
    print("\n\nKassa klaar!")
    kassa = True
    while kassa == True:
        print("\nIn dit menu kan je volgende dingen doen:\n\t- 'm' om mensen toe te voegen\t\t\t- 't' om alle tussentotalen te zien\n\t- 'p' om overzicht poef te bekijken\t\t- 's' om de manager instellingen te openen\n\t- 'i' om initialen te tonen\t\t\t- 'd' om dranknummers te tonen\n\n\t- vul de initiale van één persoon in om deze af te melden\n\t- vul alle nodige initialen achter elkaar in om een drank toe te voegen")
        keuze = input("\t\t- ")
        if keuze == 'm':
            PoSmensenToevoegen()
        elif keuze == 't':
            PoStussenTotalenBerekenen('print', aanwezigeKlanten)
        elif keuze == 'p':
            poef('aanwezige')
        elif keuze == 's':
            PoSmanager()
        elif keuze == 'i':
            if len(aanwezigeKlanten) == 0:
                print("\t\t- er zijn geen klanten aanwezig")
            else:
                teller = 0
                
                print("\t" + "AANWEZIGE INITIALEN".center(111) + "\n\t" + ("-"*111) + "\n\t", end='')
                for klant in aanwezigeKlanten:
                    teller += 1
                    record = klant.split(";")
                    print(record[0].ljust(7) + record[1].ljust(27), end='')
                    if teller < 3:
                        print("|".ljust(7), end='')
                    if teller == 3:
                        print("\n\t", end='')
                        teller = 0
                print("\n")
        elif keuze == 'd':
            PoSprintDranken()
        else:
            record = keuze.split()
            nietHerkent = []
            herkent = []
            for initialen in record:
                gevonden = False
                for klant in aanwezigeKlanten:
                    record2 = klant.split(";")
                    if gevonden == False:
                        if initialen == record2[0]:
                            gevonden = True
                            herkent.append(initialen)
                if gevonden == False:
                    nietHerkent.append(initialen)

            if len(nietHerkent) == 1:
                print("\t\t- volgende naam is niet herkent: ", end='')
                print(nietHerkent[0])
            elif len(nietHerkent) > 1:
                print("\t\t- volgende namen zijn niet herkent: ", end='')
                for gast in nietHerkent:
                    if gast != nietHerkent[0]:
                        print(", ", end='')
                    print(gast, end='')
            
            if len(herkent) > 0:
                if len(nietHerkent) > 0:
                    print("\t\t- vul de niet herkende namen sevens nog eens in")

                if len(herkent) == 1:
                    print("\t\t- nummer van drank\t- ? om nummers weer te geven\t- 'end' om persoon uit te checken")
                elif len(herkent) > 1:
                    print("\t\t- nummer van drank\t- ? om nummers weer te geven")
                
                keuze = input("\t\t\t- ")
                if keuze == "end":
                    if len(herkent) > 1:
                        print("\t\t\t\t- Je kan maar 1 persoon tegelijk uit checken!")
                    else:
                        response = checkPassword()
                        while response == "fout":
                            response = checkPassword("defretry")

                        if response == "correct":
                            print("\t\t  Passwoord correct!\n")
                            gevonden = False
                            for klant in aanwezigeKlanten:
                                if gevonden == False:
                                    record = klant.split(";")
                                    if record[0] == herkent[0]:
                                        gevonden = True
                                        while keuze not in ['ja','nee']:
                                            keuze = input("\t\t- bent u zeker dat u " + record[1] + " uit aanwezige personen wil halen: ")
                                            if keuze == 'ja':
                                                PoSeinde(PoStussenTotalenBerekenen('checkout', (record[0]+";"+record[1])))
                                            elif keuze == 'nee':
                                                print("\t\t" + record[1] + " verwijderen geanuleerd!")
                                            else:
                                                print("\t\t- gelieve enkel met ja of nee te antwoorden.")
                        elif response == "end":
                            keuze = ""
                else:
                    while keuze != "":
                        if keuze == '?':
                            PoSprintDranken()
                            keuze = input("\n\t\t- ")
                        elif keuze == '999':
                            print("\n\t\t\t- Eigen keuze (vul naam en bedrag in)")
                            keuze = "999;"
                            keuze += input("\t\t\t  naam: ")
                            keuze += ";"
                            bedrag = input("\t\t\t  bedrag: ")
                            gecontroleerd = False
                            while gecontroleerd != True:
                                try:
                                    bedrag = int(bedrag)
                                    gecontroleerd = True
                                except ValueError:
                                    try:
                                        bedrag = float(bedrag)
                                        gecontroleerd = True
                                    except ValueError:
                                        bedrag = input("\t\t\t- Gelieve enkel getallen in te vullen: ")
                            response = ""
                            if float(bedrag) < 0:
                                print()
                                response = checkPassword()
                                while response not in ["end", "correct"]:
                                    if response == "fout":
                                        response = checkPassword("defretry")

                            if (response == 'correct') | (float(bedrag) >= 0):
                                keuze += str(bedrag)
                                record = keuze.split(";")
                                file = open(datum + '.txt', mode = "a")
                                print()
                                for initialen in herkent:
                                    for klanten in aanwezigeKlanten:
                                        record2 = klanten.split(";")
                                        if record2[0] == initialen:
                                            text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";order;" + record2[0] + ";" + record2[1] + ";" + keuze
                                            file.write(text)
                                            print("\t\t- Toegevoegd aan " + record2[1] + ": " + record[1] + " van €" + record[2])
                                file.close()
                            keuze = ""
                        else:
                            gevonden = False
                            for product in alleProducten:
                                if gevonden == False:
                                    record = product.split(";")
                                    if record[0] == keuze:
                                        gevonden = True
                                        keuze = record[0] + ";" + record[1] + ";" + record[2]
                                        file = open(datum + '.txt', mode = "a")
                                        for initialen in herkent:
                                            for klanten in aanwezigeKlanten:
                                                record2 = klanten.split(";")
                                                if record2[0] == initialen:
                                                    text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";order;" + record2[0] + ";" + record2[1] + ";" + keuze
                                                    file.write(text)
                                                    print("\t\t- " + record2[1] + " heeft " + record[1] + " besteld.")
                                        file.close()
                                        keuze = ""
                            if gevonden == False:
                                print("\t\t- keuze niet herkent, probeer nog eens.")
                                keuze = input("\n\t\t- ")

def PoSstartUp():
    print("\nKassa word opgestart\nEerst moeten er nog enkele instellingen worden geconfigureerd.")
    keuze = "0"
    while keuze not in ["ja", "nee"]:
        keuze = input("\t- is het vandaag " + datum + ": ")
        if keuze == "nee":
            input("Gelieve dan de datum van de machine correct te zetten en het programma opnieuw te openen")
            quit()
        else:
            if keuze != "ja":
                print("\t\t- gelieve enkel met ja of nee te antwoorden")

    if file_exists(datum + '.txt'):
        print("\t\t- deze datum bestaat al, dag wordt heropent.")
        with open(datum + '.txt') as file:
            line = file.readline().rstrip()
            while line != "//Logboek":
                line = file.readline().rstrip()
            line = file.readline().rstrip()
            while line:
                record = line.split(";")
                if record[1] == "checkin":
                    aanwezigeKlanten.append(record[2]+";"+record[3])
                if record[1] == "checkout":
                    aanwezigeKlanten.remove(record[2]+";"+record[3])
                line = file.readline().rstrip()

    else:
        print("\t\t- deze datum bestaat nog niet, dag wordt gemaakt")
        keuze = "0"
        while keuze not in ["ja", "nee"]:
            keuze = input("\t- staat de verwaming aan: ").lower()
            if keuze == "ja":
                verwarming = True
            elif keuze == "nee":
                verwarming = False
            else:
                print("\t\t- gelieve enkel met ja of nee te antwoorden")
        file = open(datum + '.txt', mode = "w")
        file.write("datum: " + datum + "\nverwarming: " + str(verwarming) + "\n\n//Logboek")
        file.close()
        keuze = "0"
        while keuze not in ["ja", "nee"]:
            keuze = input("\t- wil je nu al mensen toevoegen: ").lower()
            if keuze == "ja":
                PoSmensenToevoegen("log")
            else:
                if keuze != "nee":
                    print("\t\t- gelieve enkel met ja of nee te antwoorden")

def PoSalleKlantenOphalen():
    klanten = []
    klantenMetInitialen = []
    with open('setup.txt') as file:
        line = file.readline().rstrip()
        while line != "//Clients":
            line = file.readline().rstrip()
        line = file.readline().rstrip()
        while line != "//End":
            klanten.append(line)
            line = file.readline().rstrip()
    for klant in klanten:
        initialen = ""
        delen = klant.split()
        for deel in delen:
            initialen = initialen + deel[0]        
        klantenMetInitialen.append(initialen.lower() + ";" + klant)

    return klantenMetInitialen

def PoSalleProductenOphalen():
    producten = []
    with open('setup.txt', encoding='utf-8') as file:
        line = file.readline().rstrip()
        while line != "//Products":
            line = file.readline().rstrip()
        line = file.readline().rstrip()
        while line != "//End":
            producten.append(line)
            line = file.readline().rstrip()

    return producten

def PoSprintDranken():
    soort = ""
    teller = 0
    for product in alleProducten:
        record = product.split(";")
        if record[0][0] != soort:
            soort = record[0][0]
            teller = 0
            print("\n\n\t" + drankenNummer[record[0][0]].upper().center(111) + "\n\t" + ('-'*111) + "\n\t", end='')
        if teller == 2:
            print("\n\t", end='')
            teller = 0
        print(record[0].ljust(5) + record[1].center(35) + "€" + record[2].ljust(14), end='')
        if teller == 0:
            print("|".ljust(11), end='')
        teller += 1
    print()

def PoStussenTotalenBerekenen(mode, personen, date=datum):
    orders = []
    tussenTotalen = []
    with open(date + '.txt') as file:
        line = file.readline().rstrip()
        while line != "//Logboek":
            line = file.readline().rstrip()
        line = file.readline().rstrip()
        while line:
            record = line.split(";")
            if record[1] == "order":
                orders.append(record[2]+";"+record[3]+";"+record[4]+";"+record[5]+";"+record[6])
            line = file.readline().rstrip() 

    orders.sort()
    if len(orders) > 0:
        naam = orders[0].split(";")
        naam = naam[0]+";"+naam[1]
        product = orders[0].split(";")
        product = product[2]+";"+product[3]+";"+product[4]
        teller = 0
        prijs = 0.00
        producten = []
        tussenTotaal = []
        for order in orders:
            record = order.split(";")
            if (record[0]+";"+record[1])  == naam:
                if (record[2]+";"+record[3]+";"+record[4]) == product:
                    teller += 1
                else:
                    producten.append(str(teller) + ";" + product)
                    teller = 1
                    product = record[2]+";"+record[3]+";"+record[4]
            else:
                producten.append(str(teller) + ";" + product)
                for product in producten:
                    deelProduct = product.split(";")
                    prijs += (int(deelProduct[0]) * float(deelProduct[3]))
                tussenTotaal.append(str(naam))
                tussenTotaal.append(producten)
                tussenTotaal.append(str(prijs))
                tussenTotalen.append(tussenTotaal)
                tussenTotaal = []
                producten = []
                naam = record[0]+";"+record[1]
                teller = 1
                prijs = 0.00
                product = record[2]+";"+record[3]+";"+record[4]
        producten.append(str(teller) + ";" + product)
        for product in producten:
            deelProduct = product.split(";")
            prijs += (int(deelProduct[0]) * float(deelProduct[3]))
        tussenTotaal.append(str(naam))
        tussenTotaal.append(producten)
        tussenTotaal.append(str(prijs))
        tussenTotalen.append(tussenTotaal)

        tussentotaalhelper = []
        if mode in ['print', 'end', 'checkout', 'view'] :
            for tussenTotaal in tussenTotalen:
                record = tussenTotaal[0].split(";")
                prijs = 0
                if record[0] + ";" + record[1] in personen:
                    tussentotaalhelper.append(tussenTotaal)
                    if mode == 'view':
                        print("\t\t\t- " + date)
                    else:
                        print("\t\t\t- " + record[1])
                    for product in tussenTotaal[1]:
                        record = product.split(";")
                        if mode == 'view':
                            if record[1] != "1000":
                                tussenPrijs = int(record[0]) * float(record[3])
                                prijs += tussenPrijs
                                print("\t\t\t\t" + record[0] + "x\t" +record[2].ljust(30) + "(€" + record[3] + ")\t\t€" + str(round(tussenPrijs,2)))
                        else:
                            tussenPrijs = int(record[0]) * float(record[3])
                            prijs += tussenPrijs
                            print("\t\t\t\t" + record[0] + "x\t" +record[2].ljust(30) + "(€" + record[3] + ")\t\t€" + str(round(tussenPrijs,2)))
                    print("\t\t\t\t\tTOTAAL:\t\t\t\t\t\t€"+ str(round(prijs, 2)))
            if mode == 'checkout':
                if tussentotaalhelper == []:
                    tussentotaalhelper = [[personen, ['0;999;Niets genuttigd;0.0'], '0.0']]
            return tussentotaalhelper
    else:
        print("\t\t- nog geen gevonden orders!")
        


    
def PoSmensenToevoegen(mode="default"):
    gasten = []
    aanwezigeGasten = []
    nietHerkent = []

    teller = 0

    print("\t" + "ALLE INITIALEN".center(111) + "\n\t" + ("-"*111) + "\n\t", end='')
    for klant in alleKlanten:
        teller += 1
        record = klant.split(";")
        print(record[0].ljust(7) + record[1].ljust(27), end='')
        if teller < 3:
            print("|".ljust(7), end='')
        if teller == 3:
            print("\n\t", end='')
            teller = 0
    print("\n")

    if mode == "default":
        if len(aanwezigeKlanten) == 1:
            print("\t\tEnkel ", end='')
            record = aanwezigeKlanten[0].split(";")
            print(record[1] + " is momenteel al aanweezig")
        elif len(aanwezigeKlanten) > 1:
            print("\t\tMomenteel zijn ", end='')
            for klant in aanwezigeKlanten:
                if klant != aanwezigeKlanten[0]:
                    print(", ", end='')
                record = klant.split(";")
                print(record[1], end='')
            print(" al aanwezig.")
        
    print("\t\t- Vul keer per keer de initialen in van de aanwezige personen (eindiggen met enter)")
    ingevuldeNaam = input("\t\t\t- ")

    while ingevuldeNaam != "":
        if ingevuldeNaam in gasten:
            if mode == "log":
                print("\t\t\t\t\t- deze naam is al ingevuld")
            else:
                print("\t\t\t\t- deze naam is al ingevuld")
        else:
            gevonden = False
            for klant in aanwezigeKlanten:
                record = klant.split(";")
                if record[0] == ingevuldeNaam:
                    gevonden = True
                    if mode == "log":
                        print("\t\t\t\t\t- deze persoon is al aanwezig")
                    else:
                        print("\t\t\t\t- deze persoon is al aanwezig")
            if gevonden == False:
                gasten.append(ingevuldeNaam)

        ingevuldeNaam = input("\t\t\t- ")

    for gast in gasten:
        gevonden = False
        for klant in alleKlanten:
            if gevonden == False:
                record = klant.split(";")
                if gast == record[0]:
                    aanwezigeGasten.append(klant)
                    aanwezigeKlanten.append(klant)
                    gevonden = True
        if gevonden == False:
            nietHerkent.append(gast)

    if mode == "log":
        if len(aanwezigeGasten) == 1:
            print("\t\t\t\t- volgende naam is toegevoegd: ", end='')
            record = aanwezigeGasten[0].split(";")
            print(record[1])
        elif len(aanwezigeGasten) > 1:
            print("\t\t\t\t- volgende namen zijn toegevoegd: ", end='')
            teller = 0
            for gast in aanwezigeGasten:
                if gast != aanwezigeGasten[0]:
                    print(", ", end='')
                if teller == 3:
                    print("\n\t\t\t\t\t\t\t\t", end='')
                    teller = 0
                record = gast.split(";")
                print(record[1], end='')
                teller += 1
        if len(nietHerkent) == 1:
            print("\n\t\t\t\t- volgende naam is niet herkent: ", end='')
            print(nietHerkent[0])
        elif len(nietHerkent) > 1:
            print("\n\t\t\t\t- volgende namen zijn niet herkent: ", end='')
            for gast in nietHerkent:
                if gast != nietHerkent[0]:
                    print(", ", end='')
                print(gast, end='')
    else:
        if len(aanwezigeGasten) == 1:
            print("\t\t- volgende naam is toegevoegd: ", end='')
            record = aanwezigeGasten[0].split(";")
            print(record[1])
        elif len(aanwezigeGasten) > 1:
            print("\t\t- volgende namen zijn toegevoegd: ", end='')
            teller = 0
            for gast in aanwezigeGasten:
                if gast != aanwezigeGasten[0]:
                    print(", ", end='')
                    if teller == 3:
                        print("\n\t\t\t\t\t\t", end='')
                        teller = 0
                record = gast.split(";")
                print(record[1], end='')
                teller += 1
        if len(nietHerkent) == 1:
            print("\n\t\t- volgende naam is niet herkent: ", end='')
            print(nietHerkent[0])
        elif len(nietHerkent) > 1:
            print("\n\t\t- volgende namen zijn niet herkent: ", end='')
            for gast in nietHerkent:
                if gast != nietHerkent[0]:
                    print(", ", end='')
                print(gast, end='')
    file = open(datum + '.txt', mode = "a")
    for gast in aanwezigeGasten: 
        record = gast.split(";")
        text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";checkin;" + record[0] + ";" + record[1]
        file.write(text)
    file.close()
    print()

def PoSmanager():
    response = checkPassword()
    while response != "end":
        if response == "fout":
            response = checkPassword("defretry")
        elif response == "correct":
            print("\nWelkom bij manager instellingen!\nIn dit menu kan je volgende dingen doen:\n\t- 'e' om avond te beëindiggen\t\t\t- 'd' om dranken toe te voegen\n\t- 'k' om klantenbestand uit te breiden\t\t- 'c' om terug naar de gewone modus te gaan")
            keuze = ""
            while keuze not in ['e', 'd', 'k', 'c']:
                keuze = input("\t\t- ")
                if keuze == 'e':
                    print("\t\t- rekening(en) van de aanwezige person(en) worden gamaakt.")
                    PoSeinde(PoStussenTotalenBerekenen('end', aanwezigeKlanten))
                    quit()
                elif keuze == 'd':
                    nogToevoegen = True
                    while nogToevoegen == True:
                        setupFile = []
                        with open('setup.txt') as file:
                            line = file.readline().rstrip()
                            while line:
                                setupFile.append(line)
                                line = file.readline().rstrip()
                        bestaandeProducten = []
                        global alleProducten
                        for product in alleProducten:
                            record = product.split(";")
                            bestaandeProducten.append(record[0])
                        teller = 0
                        print("\n\t\t- Aangerade vrije nummers per dranksoort:\n\t", end='')
                        for categorie in drankenNummer:
                            i = (int(categorie) * 100) + 1 
                            while str(i) in bestaandeProducten:
                                i += 1
                            if teller == 3:
                                teller = 0
                                print("\n\t", end='')
                            print("\t\t- " + drankenNummer[categorie].ljust(14) + "--  " + str(i), end='')
                            teller += 1
                        gekozenNum = input("\n\n\t\t- Vul de nummer in die je wilt gebruiken: ")
                        while gekozenNum in bestaandeProducten:
                            gekozenNum = input("\t\t\t- Deze nummer bestaat al probeer opnieuw: ")
                        gekozenNaam = input("\t\t- Vul de naam in die je wilt gebruiken: ")
                        gekozenPrijs = input("\t\t- Vul de prijs van een " + gekozenNaam + ": ")
                        gecontroleerd = False
                        while gecontroleerd != True:
                            try:
                                gekozenPrijs = int(gekozenPrijs)
                                gecontroleerd = True
                            except ValueError:
                                try:
                                    gekozenPrijs = float(gekozenPrijs)
                                    gecontroleerd = True
                                except ValueError:
                                    gekozenPrijs = input("\t\t\t- Gelieve enkel getallen in te vullen: ")
                        print("\n\t\t- Klopt volgende info: ")
                        print("\t\t\t- Nummer: " + gekozenNum)
                        print("\t\t\t- Naam:   " + gekozenNaam)
                        print("\t\t\t- prijs:  " + str(gekozenPrijs))
                        correct = input("\t\t\t\t- ")
                        while correct not in ['ja', 'nee']:
                            correct = input("\t\t\t\t- gelieve enkel met ja of nee te antwoorden: ")
                        if correct == 'ja':
                            geplaatst = False
                            for product in alleProducten:
                                record = product.split(";")
                                if int(gekozenNum) < int(record[0]):
                                    if geplaatst == False:
                                        geplaatst = True
                                        setupFile.insert(setupFile.index(product), gekozenNum + ";" + gekozenNaam + ";" + str(gekozenPrijs))
                                        file = open("setup.txt","r+")
                                        file.truncate(0)
                                        file.close()
                                        file = open('setup.txt', mode = "a")
                                        for line in setupFile: 
                                            file.write(line + "\n")
                                        file.close()
                                        alleProducten = PoSalleProductenOphalen()
                                        print("\t\t\t\t- Drank toevoegevoegd!")
                        elif correct == 'nee':
                            print("\t\t\t\t- Drank toevoegen geannuleerd!")
                        
                        nogToevoegen = input("\n\t\t- Wil je nog dranken toevoegen: ")
                        while nogToevoegen not in ['ja', 'nee']:
                            nogToevoegen = input("\t\t\t- gelieve enkel met ja of nee te antwoorden: ")
                        if nogToevoegen == 'nee':
                            nogToevoegen = False
                        elif nogToevoegen == 'ja':
                            nogToevoegen = True
                    


                elif keuze == 'k':
                    namenToevoegen = True
                    while namenToevoegen == True:
                        setupFile = []
                        with open('setup.txt') as file:
                            line = file.readline().rstrip()
                            while line:
                                setupFile.append(line)
                                line = file.readline().rstrip()
                        print("\t\t\t- Vul de volledige naam in van de nieuwe persoon om deze te te voegen")
                        print("\t\t\t- Vul de volledige naam in van een bestaande persoon om deze te verwijderen")
                        naam = input("\t\t\t\t- ")
                        if naam in setupFile:
                            verification = input("\t\t\t\t- Weet je zeker dat je " + naam + " uit het klantenbestand wil verwijderen: ")
                            while verification not in ['ja', 'nee']:
                                verification = input("\t\t\t\t\t- gelieve enkel met ja of nee te antwoorden")
                            if verification == "ja":
                                setupFile.remove(naam)
                                print("\t\t\t\t\t- " + naam + " is verwijderd")
                            elif verification == "nee":
                                print("\t\t\t\t\t- " + naam + " blijft behouden")
                        else:
                            verification = input("\t\t\t\t- Weet je zeker dat je " + naam + " aan het klantenbestand wil toevoegen: ")
                            while verification not in ['ja', 'nee']:
                                verification = input("\t\t\t\t\t- gelieve enkel met ja of nee te antwoorden")
                            if verification == "ja":
                                setupFile.insert(setupFile.index('//End'), naam)
                                print("\t\t\t\t\t- " + naam + " is toegevoegd")
                            elif verification == "nee":
                                print("\t\t\t\t\t- " + naam + " is niet toegevoegd")
                        
                        file = open("setup.txt","r+")
                        file.truncate(0)
                        file.close()
                        file = open('setup.txt', mode = "a")
                        for line in setupFile: 
                            file.write(line + "\n")
                        file.close()
                        global alleKlanten
                        alleKlanten = PoSalleKlantenOphalen()

                        namenToevoegen = input("\n\t\t\t- Wil je nog namen toevoegen of verwijderen: ")
                        while namenToevoegen not in ['ja', 'nee']:
                                namenToevoegen = input("\t\t\t\t- gelieve enkel met ja of nee te antwoorden: ")
                        if namenToevoegen == 'nee':
                            namenToevoegen = False
                        elif namenToevoegen == 'ja':
                            namenToevoegen = True

                    

                elif keuze == 'c':
                    print("\t\t\t- gewone modus wordt heropend")
                else:
                    print("\t\t\t- gelieve enkel een van bevenstaande keuzes te gebruiken")
            response = "end"

def PoSeinde(tussenTotalen):
    if len(tussenTotalen) != 0:
        for tussentotaal in tussenTotalen:
            poefdata = []
            poefbedrag = 0
            naam = tussentotaal[0].split(";")
            with open('poef.txt') as file:
                line = file.readline().rstrip()
                while line:
                    record = line.split(";")
                    if record[1] == naam[0]:
                        if record[3] == "pay":
                            poefdata = []
                            poefbedrag = 0
                        else:
                            poefdata.append(record[0])
                            poefbedrag += float(record[3])
                    line = file.readline().rstrip()
            if (round(float(tussentotaal[2]),2) != 0) | (round(poefbedrag,2) != 0):
                print()
                if round(float(tussentotaal[2]),2) != 0:
                    print("\t\t\t" + naam[1] + " heeft €" + str(round(float(tussentotaal[2]),2)) + " op de rekinging staan.")
                if round(poefbedrag,2) != 0:
                    print("\t\t\t" + naam[1] + " heeft €" + str(round(poefbedrag, 2)) + " op de poef staan van: ", end='')
                    for data in poefdata:
                        print(data, end='')
                        if data != poefdata[len(poefdata)-1]:
                            print(", ", end='')
                    print()
                if (float(tussentotaal[2]) != 0) & (poefbedrag != 0):
                    print()
                    print("\t\t\tDe totale rekening is dus €" + str(round(float(tussentotaal[2]) + poefbedrag, 2)))

                print("\t\t\t  wordt deze rekening direct afgerekend 'b' of op poef 'p'")
                keuze = input("\t\t\t\t- ")
                while keuze not in ('b', 'p'):
                    print("\t\t\t\t- Gelieve enkel met 'b' of 'p' te antwoorden!")
                    keuze = input("\t\t\t\t- ")
                if keuze == 'b':
                    file = open(datum + '.txt', mode = "a")
                    if float(tussentotaal[2]) > 0:
                        text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";order;" + naam[0] + ";" + naam[1] + ";1000;Afgerekend;-" + str(round(abs(float(tussentotaal[2])),2))
                    else:
                        text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";order;" + naam[0] + ";" + naam[1] + ";1000;Afgerekend;" + str(round(abs(float(tussentotaal[2])),2))
                    file.write(text)
                    file.close()
                    if poefbedrag != 0:
                        file = open('poef.txt', mode = "a")
                        text = "\n" + str(datetime.datetime.now().strftime("%d %b %Y om %H:%M")) + ";" + naam[0] + ";" + naam[1] + ";pay"
                        file.write(text)
                        file.close()
                elif keuze == 'p':
                    if round(float(tussentotaal[2]),2) != 0:
                        file = open(datum + '.txt', mode = "a")
                        if float(tussentotaal[2]) > 0:
                            text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";order;" + naam[0] + ";" + naam[1] + ";1000;Op poef;-" + str(round(abs(float(tussentotaal[2])),2))
                        else:
                            text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";order;" + naam[0] + ";" + naam[1] + ";1000;Op poef;" + str(round(abs(float(tussentotaal[2])),2))
                        file.write(text)
                        file.close()
                        file = open('poef.txt', mode = "a")
                        text = "\n" + str(datetime.datetime.now().strftime("%d %b %Y om %H:%M")) + ";" + naam[0] + ";" + naam[1] + ";" + str(round(float(tussentotaal[2]),2))
                        file.write(text)
                        file.close()
            else:
                print("\t\t\t- " + naam[1] + " heeft geen opstaande rekening meer.")
            if naam[0] + ";" + naam[1] in aanwezigeKlanten:
                aanwezigeKlanten.remove(naam[0] + ";" + naam[1])
                file = open(datum + '.txt', mode = "a")
                text = "\n" + str(datetime.datetime.now().strftime("%X")) + ";checkout;" + naam[0] + ";" + naam[1]
                file.write(text)
                file.close()
    else:
        print("\t\t\t- Er zijn geen rekingen meer")





#Funties poef bekijken
def poef(mode= "alle"):
    samenvatting = []
    if mode == "alle":
        zoekPersonen = alleKlanten
    elif mode == "aanwezige":
        zoekPersonen = aanwezigeKlanten
    for persoon in zoekPersonen:
        poefdata = []
        poefbedrag = 0
        persoon = persoon.split(";")
        with open('poef.txt') as file:
            line = file.readline().rstrip()
            while line:
                record = line.split(";")
                if record[1] == persoon[0]:
                    if record[3] == "pay":
                        poefdata = []
                        poefbedrag = 0
                    else:
                        poefdata.append(record[0])
                        poefbedrag += float(record[3])
                line = file.readline().rstrip()
        if round(poefbedrag,2) != 0:
            if mode == "alle":
                print("\n\t(" + persoon[0] + ") " + persoon[1], end='')
            elif mode == "aanwezige":
                print("\n\t\t" + persoon[1], end='')
            if len(poefdata) == 1:
                print(" heeft een openstaande rekening van:")
            else:
                print(" heeft openstaande rekeningen van:")
            for datum in poefdata:
                if mode == "alle":
                    print("\t\t- " + datum)
                elif mode == "aanwezige":
                    print("\t\t\t- " + datum)
            if mode == "alle":
                print("\t\t\t- met een totaalbedrag van €" + str(round(poefbedrag,2)))
                dates = ""
                for datum in poefdata:
                    date = datetime.datetime.strptime(datum, "%d %b %Y om %H:%M")
                    dates += date.strftime("%d-%m-%Y") + ";"
                dates = dates[:-1]
                text = persoon[0] + "$" + persoon[1] + "$" + str(round(poefbedrag,2)) + "$" + dates
                samenvatting.append(text)
            elif mode == "aanwezige":
                print("\t\t\t\t- met een totaalbedrag van €" + str(round(poefbedrag,2)))
    if len(samenvatting) > 0:
        if mode == "alle":
            keuze = input("\n\t- Wil je een van deze rekeningen wijziggen: ")
            while keuze not in ['ja', 'nee']:
                keuze = input("\t- Gelieve enkel met 'ja' of 'nee' te antwoorden: ")
            while keuze == "ja":
                keuze = input("\t\t- Vul de initialen in van de persoon: ")
                for poef in samenvatting:
                    record = poef.split("$")
                    if keuze == record[0]:
                        keuze = input("\t\t- ben je zeker dat je de rekening van " + record[1] + " hebt afgerekend (€" + record[2] + "): ")
                        while keuze not in ['ja', 'nee']:
                            keuze = input("\t\t- vul enkel 'ja' of 'nee' in: ")
                        if keuze == "ja":
                            file = open('poef.txt', mode = "a")
                            text = "\n" + str(datetime.datetime.now().strftime("%d %b %Y om %H:%M")) + ";" + record[0] + ";" + record[1] + ";pay"
                            file.write(text)
                            file.close()
                            print("\t\t\t- poef wordt op nul gezet!")
                        elif keuze == "nee":
                            print("\t\t\t- poef wordt behouden!")
                keuze = input("\n\t- Wil je nog een van deze rekeningen wijziggen: ")
                while keuze not in ['ja', 'nee']:
                    keuze = input("\t- Gelieve enkel met 'ja' of 'nee' te antwoorden: ")

            keuze = input("\t- Wil je een van deze rekeningen uitklappen: ")
            while keuze not in ['ja', 'nee']:
                keuze = input("\t- Gelieve enkel met 'ja' of 'nee' te antwoorden: ")
            while keuze == "ja":
                keuze = input("\t\t- Vul de initialen in van de persoon: ")
                for poef in samenvatting:
                    record = poef.split("$")
                    if keuze == record[0]:
                        datums = record[3].split(";")
                        for datum in datums:
                            PoStussenTotalenBerekenen('view', record[0]+";"+record[1], datum)
                keuze = input("\n\t- Wil je nog een van deze rekeningen uitklappen: ")
                while keuze not in ['ja', 'nee']:
                    keuze = input("\t- Gelieve enkel met 'ja' of 'nee' te antwoorden: ")
    else: 
        print("\n\t- Er zijn geen openstaande rekeningen")




#Functies dagoverzichten bekijken
def dagOverzichten():
    keuze = input("\n\t- Welke dag wil je bekijken (dd-mm-yyyy): ")
    while file_exists(keuze + '.txt') == False:
        print("\t\t- deze dag bestaat niet.")
        keuze = input("\t- Welke dag wil je bekijken (dd-mm-yyyy): ")

    print("\n\t\t- Aankomst en vertrekken:")
    with open(keuze + '.txt') as file:
        line = file.readline().rstrip()
        while line != "//Logboek":
            line = file.readline().rstrip()
        line = file.readline().rstrip()
        while line:
            record = line.split(";")
            if record[1] == "checkin":
                print("\t\t\t- " + record[0] + " -- " + record[3] + " komt aan.")
            if record[1] == "checkout":
                print("\t\t\t- " + record[0] + " -- " + record[3] + " vertrekt.")
            line = file.readline().rstrip()

    print("\n\t\t- Dranken per personen:")
    PoStussenTotalenBerekenen('print', alleKlanten, keuze)

    orders = []
    with open(keuze + '.txt') as file:
        line = file.readline().rstrip()
        while line != "//Logboek":
            line = file.readline().rstrip()
        line = file.readline().rstrip()
        while line:
            record = line.split(";")
            if record[1] == "order":
                orders.append(record[4]+";"+record[5]+";"+record[6])
            line = file.readline().rstrip() 
    verbruik = []
    bedragVerbruik = 0
    if len(orders) > 0:
        for product in alleProducten:
            record = product.split(";")
            teller = 0
            for order in orders:
                if order == product:
                    teller += 1
                    bedragVerbruik += float(record[2])
            if teller > 0:
                text = str(teller) + ";" + product + ";" + str(round(teller*float(record[2]),2))
                verbruik.append(text)
        
        print("\n\t\t- Producten verkocht", end='')
        for gebruikt in verbruik:
            record = gebruikt.split(";")
            print("\n\t\t\t- " + record[2].ljust(40) + "\t(" + record[1] + ")\t\t€" + record[3])
            print("\t\t\t\t" + record[0] + "x\tTOTAAL: \t\t\t\t\t€" + record[4])
        print("\n\t\t\t- TOTAAL BEDRAG:\t\t\t\t\t\t€" + str(round(bedragVerbruik,2)))

alleKlanten = PoSalleKlantenOphalen()
alleProducten = PoSalleProductenOphalen()
startUp()
