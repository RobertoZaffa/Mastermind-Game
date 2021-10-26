import random
import time

class Mastermind_Engine:
    
    def init_db(self, colors):                  
        self.colors = colors
        db_ac = []                              #database all codes - include tutte le combinazioni di codici possibili
        db_lc = []                              #db dei left codes - sono tutti i codici eleggibili come codice segreto
        db_bc = []                              #db dei best codes - sono i migliori codici da giocare.
        for a in range(1, colors+1):
          for b in range(1, colors+1):
            for c in range(1, colors+1):
              for d in range(1, colors+1):
                t = [a, b, c, d, True, 0, 0, 0, 0, 0, 0, 0, 0, 0] #struttura del codice 0-3 codice, 4 flag left code, 5-12 num colori, 13 score best code
                t[4 + a] += 1                   #inizializza i campi che contengono il numero di volte che ogni colore è presente nel codice
                t[4 + b] += 1
                t[4 + c] += 1
                t[4 + d] += 1
                if colors == 6 and t[5]<3 and t[6]<3 and t[7]<3 and t[8]<3 and t[9]<3 and t[10]<3 and t[11]<3 and t[12]<3:
                    db_bc.append(t)             #metti solo i codici che hanno meno di tre colori ripetuti in db_bc, cioè del tipo 1234 1123 1122
                if colors == 8 and t[5]<2 and t[6]<2 and t[7]<2 and t[8]<2 and t[9]<2 and t[10]<2 and t[11]<2 and t[12]<2:
                    db_bc.append(t)             #metti solo i codici che non hanno colori ripetuti in db_bc, cioè del tipo 1234
                db_ac.append(t)                 #solo per il primo tentativo i best code vengono popolati in questo modo, poi viene usato "best_codes"
                db_lc.append(t)                 #al primo tentativo i left codes coincidono con tutti i codici possibili
        ac = len (db_ac)                        #numero totale di codici possibili
        lc = len (db_lc)                        #nurero totale iniziale dei left codes
        bc = len (db_bc)                        #numero totale iniziale dei best codes
        return db_ac, ac, db_lc, lc, db_bc, bc

    def find_keycode(self, code_a, code_b):     #confronta due codici e ritorna il codice chiave espresso in whites e blacks
        blacks_whites = 0                       #bianchi + neri
        blacks = 0                              #neri
        for i in range(5, 13):                  #prendi il minor numero di volte che un colore è presente tra i due codici
            if code_a[i] < code_b[i]:
                blacks_whites += code_a[i]
            else:
                blacks_whites += code_b[i]
        for i in range(0,4):                    #calcola il numero di neri
            if code_a[i] == code_b[i]:
                blacks += 1
        return (blacks_whites - blacks, blacks) #i bianchi sono calcolati per differenza

    def left_codes(self, db_ac, ac, code_played, keycode ):         #crea un nuovo db_lc con i codici eleggibili come codice segreto (Left Codes)
        db_lc = []
        for i in range (ac):                                        #ripete per tutte le combinazioni di codici possibili
            found_keycode = self.find_keycode(code_played,db_ac[i]) #trova il codice chiave tra il codice tentativo e tutti codici possibili
            if keycode == found_keycode and db_ac[i][4]==True:      #se il codice chiave trovato è uguale quello inserito e il campo 4 è True ...
                db_lc.append(db_ac[i])                              #... il codice è un Left code e viene aggiunto nel db_lc altrimenti ...
            else:                                                   #... il flag del campo 4 viene impostato a False
                db_ac[i][4]=False                                   #in db_ac, solo i codici con flag True sono Left code.
        lc = len(db_lc)                                             #lc è il numero totale dei Left code rimasti
        return db_ac, db_lc, lc

    def best_codes (self, lc, db_ac, db_lc):                            #Crea db_bc con i best codes e ripopola i left codes con il peso corretto
        min_of_max = 99999                                              #imposta a un valore sicuramente più alto per il confronto
        db_loop = []                                                    #contiene i codici da giocare per la simulazione
        colors = self.colors
        if (lc > 252 and colors == 6) or (lc > 976 and colors == 8):    #se i possibili codici segreti sono troppi, i codici per la simulazione non ...
            db_loop = db_lc.copy()                                      #saranno i tutti i codici possibili ma i left codes
        else:
            db_loop = db_ac.copy()
        len_loop = len (db_loop)
        for i in range(len_loop):                                       #ripeti per tutti i codici in db_loop
            key_hits = [0]*25                                           #Ogni campo è un tipo di cod.chiave. 1 bianco, 2 bianchi, 1 nero, ...
            for j in range (lc):                                        #per ogni codice di db_loop ripete per tutti i possibili codici segreti
                whites, blacks = self.find_keycode(db_loop[i], db_lc[j])#trova il codice chiave tra i codici di db_loop e quelli di db_lc
                key_hits [whites*5 + blacks] +=1                        #incrementa le ricorrenze di codici chiave uguali. *5 simula una tabella a 2 dim        
            max_hit = max(key_hits)                                     #trova il valore massimo di ricorrenze dei codici chiave
            db_loop[i][13] = max_hit                                    #assegnazione del peso al codice
            if max_hit < min_of_max:                                    
                min_of_max = max_hit                                    #assegna a min il più piccolo dei max
        db_bc = []                                                      #azzera il db_bc dei best codes
        db_lc = []                                                      #azzera il db dei left codes. Vengono ripopolati con il peso corretto
        for i in range (len_loop):                                      #ripete per tutti i codici in db_loop
            if db_loop [i][13] == min_of_max:                           #se il codice ha un peso uguale a minimo dei massimi, allora è un best code...
                db_bc.append(db_loop[i])                                #... e viene messo nel db dei best codes
            if db_loop [i][4]==True:                                    #se è un left code, viene messo in db_lc con il suo peso
                db_lc.append(db_loop[i])
        db_lc.sort(key=lambda x: x[13])                                 #ordina db_lc in base al peso in ordine crescente
        if db_lc [0][13] == min_of_max :                                #se c'è almeno un left code in db_bc, allora elimina tutti quelli iconsistenti
            db_bc_temp=[]                                               #db temporaneo per escludere i codici incosistenti
            for i in range (len(db_bc)):                                #ripeti per per tutti i codici in db_bc
                if db_bc[i][4]==True:                                   #se è un left code, tienilo.
                    db_bc_temp.append(db_bc[i])                         
            db_bc = db_bc_temp.copy()
        bc = len(db_bc)                                                 #bc è il numero totale dei best codes
        return db_lc, db_bc, bc

    def code_adapter (self, code):
        adapted_code = [0,0,0,0,True,0,0,0,0,0,0,0,0,0]                 #il codice viene trasformato nel formato dei codici nei database
        for i in range (0,4):
            adapted_code[i] = int(code[i])
            adapted_code[4 + adapted_code[i]] += 1
        return adapted_code

class Mastermind(Mastermind_Engine):
    
    def print_board (self, game_board, len_board):
        print ("")
        for i in range (len_board-1, -1, -1):
            print (game_board [i][0], " ", "X" * game_board[i][1], "0" * game_board[i][2], sep='' )
        print ("-"*80)

    def print_codes (self, lc, db_lc, bc, db_bc, elapsed_time=0):     
        print ("")
        print ("Left Codes:", lc, " " * (13 - len(str(lc))), "Best Codes:", bc)
        end_print = False
        for i in range (lc):
            try:
                print (db_lc[i][0:4], db_lc[i][13], " " * (12 - len(str(db_lc[i][13]))),db_bc[i][0:4], db_bc[i][13])
            except:
                print (db_lc[i][0:4], db_lc[i][13])
            if i == 19:
                break
        print ("Elapsed time for processing:", round (elapsed_time, 2))


def game1(colors):                                                      #il giocatore deve indovinare il codice segreto scelto dal programma
    mm = Mastermind()                                                   #mm è la variabile di istanza della classe Mastermind()
    db_ac, ac, db_lc, lc, db_bc, bc = mm.init_db(colors)                #metodo che crea i database di tutti i codici, dei left e best codes
    secret_code = db_ac[random.randrange(ac)]                           #il programma sceglie il codice segreto tra tutti i codici possibili
##    secret_code = mm.code_adapter("1534")                             #utilizzo di CS fisso per debug
    game_board = []
    elapsed_time = 0
    for row in range(1,11):                                             #ripeti fino a un massimo di 10 tentativi
        while True:
            print ("") 
            opt = input ("Enter four digit code or 1)Print left/best codes  2)Check secret code  3)End ")
            if opt == "3":
                return
            elif opt == "1":
                mm.print_codes (lc, db_lc, bc, db_bc, elapsed_time)
            elif opt == "2":
                print ("Secret Code:", secret_code[0:4])
            else:
                code_played = mm.code_adapter (opt)                     #il codice giocato, viene adattato a 13 campi
                break          
        whites, blacks = mm.find_keycode(secret_code, code_played)      #trova il codice chiave confrontando il cod tentativo con il cod segreto
        game_board.append([code_played[0:4], blacks, whites])           #memorizza la giocata nella board game
        mm.print_board (game_board, len(game_board))
        if blacks == 4:                                                 # se il codice chiave sono 4 neri allora il codice è stato indovinato
            print ("")
            print ("Secret code GUESSED")
            return
        db_ac, db_lc, lc = mm.left_codes(db_ac, ac, code_played, (whites, blacks))#genera il db dei left codes e mette il flag True in db_ac per i lc
        start_time = time.time()
        db_lc, db_bc, bc = mm.best_codes(lc, db_ac, db_lc )             #metodo che genera il database dei best codes
        elapsed_time =(time.time() - start_time)                        #calcola il tempo di elaborazione per i best codes
    print ("** The maximum number of attempts has been exceeded **")    #il numero massimo di tentativi da parte del giocatore sono 10

def game2(colors):                                                      #partita dove il programma deve indovinare il codice segreto scelto dal giocatore
    mm = Mastermind()                                  
    db_ac, ac, db_lc, lc, db_bc, bc = mm.init_db(colors)           
    game_board = []
    elapsed_time = 0
    for row in range(1,11):                                 
        code_played = db_bc[random.randrange(bc)]                       #il programma sceglie un codice da giocare tra i best codes
        print ("\n Code played", code_played [0:4])
        if lc == 1:                                                       #se il codice giocato è l'ultimo left code rimasto èanche il codice segreto
            whites = 0
            blacks = 4
        else:
            while True:
                print ("")
                opt = input ("Enter 0 and X for the keycode or  1)Print left/best codes  2)End ")
                if opt == "2":
                    return
                elif opt == "1":
                    mm.print_codes (lc, db_lc, bc, db_bc, elapsed_time)
                else:
                    whites = opt.count("0")
                    blacks = opt.count ("X")
                    blacks += opt.count ("x")
                    break             
        game_board.append([code_played[0:4], blacks, whites])
        mm.print_board (game_board, len(game_board))
        if blacks == 4:                                                 #se inserisce 4 neri il codice segreto  è indovinato
            print ("\n Secret code GUESSED")
            return                                                      #partita terminata torna al menu per una nuova partita
        db_ac, db_lc, lc = mm.left_codes(db_ac, ac, code_played, (whites, blacks))       
        if lc == 0:                                                     #se non ci sono più codici possibili uno o più codici chiave sono errati
            print ("\n At least one key code has been entered is incorrect")
            return
        start_time = time.time()
        db_lc, db_bc, bc = mm.best_codes(lc, db_ac, db_lc )             #crea il db dei best codes                                    
        elapsed_time =(time.time() - start_time)

colors = 6
while True: 
    print ("")
    print ("="*80)
    option = input ("1)Game1  2)Game2  6)6 Colors(default)  8)8 Colors  9)Help  0)End ")
    if option == "1":
        game1(colors)                     #il giocatore deve indovinare il codice segreto scelto dal programma
    elif option == "2":
        game2 (colors)                    #il programma deve indovinare il codice segreto scelto dal giocatore
    elif option == "6":
        colors = 6
        print ("\n You will play with 6 colors/digits")
    elif option == "8":
        colors = 8
        print ("\n You will play with 8 colors/digits")
    elif option == "9":
        print ("\n 1)Game 1 - You will try to guess computer secret code \
               \n 2)Game 2 - Computer will try to guess your secret code \
               \n 6)6 Colors - For both Game1 and Game2 you will use 6 colors/digits (default) \
               \n 8)8 Colors - For both Game1 and Game2 you will use 8 colors/digits ")
    if option == "0":
        break
        
               
