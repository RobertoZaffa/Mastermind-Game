#cython: language_level=3
import random
import time
import sys
import os

def init_db(colors):
    """
    init_db crea le seguenti liste di liste:
    db_ac: database all codes - include tutte le combinazioni di codici possibili 1296 per 6 colori e 4096 per 8 colori
    db_lc: database dei left codes - sono tutti i codici eleggibili come codice segreto. All'inizio del gioco, è identico ad db_ac
    db_bc: database dei best codes - sono i migliori codici da giocare. All'inizio sono del tipo 1234 1123 1122 con la versione 6 colori e 1234 per la versione a 8 colori

    Ogni codice è così composto: 0 stringa che rappresenta il codice mastermind (un numero per ogni colore), 1 flag left code(True se il codice è un left code), 2-9 numero di volte che un colore è presente nel codice.
    Ogni posizione è un colore. 10 score best code(inizializzato a 0), 11 valore nel range 1-25 utilizzato per determinare i best codes. Inizializzato a zero
    """                  
    db_ac = []                              
    db_lc = []                              
    db_bc = []                              
    for a in range(1, colors+1):
        for b in range(1, colors+1):
            for c in range(1, colors+1):
                for d in range(1, colors+1):
                    code = str(a) + str(b) + str(c) + str(d)
                    t = [code, True, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
                    t[1 + a] += 1                   
                    t[1 + b] += 1
                    t[1 + c] += 1
                    t[1 + d] += 1
                    db_ac.append(t)                 
                    db_lc.append(t)                 
                    if colors == 6 and t[2]<3 and t[3]<3 and t[4]<3 and t[5]<3 and t[6]<3 and t[7]<3 and t[8]<3 and t[9]<3:
                        db_bc.append(t)             
                    if colors == 8 and t[2]<2 and t[3]<2 and t[4]<2 and t[5]<2 and t[6]<2 and t[7]<2 and t[8]<2 and t[9]<2:
                        db_bc.append(t)             
    return db_ac, db_lc, db_bc

def find_keycode(code_a, code_b):     
    """
    riceve due codici ad esempio, codice segreto e codice giocato e dal confronto ritorna il codice chiave in termini di piolini bianchi e neri.
    Non viene usato un loop FOR per migliorare le prestazioni del metodo best codes.
    Viene sommato a blacks_whites il minor numero di volte che ogni colore è presente in entrambi i codici.
    trova poi il numero di neri per confronto e ricava per differenza i numeri di bianchi
    """
    blacks_whites = 0                       
    blacks = 0                              
    if code_a[2] < code_b[2]:               
        blacks_whites += code_a[2]
    else:
        blacks_whites += code_b[2]
    if code_a[3] < code_b[3]:
        blacks_whites += code_a[3]
    else:
        blacks_whites += code_b[3]
    if code_a[4] < code_b[4]:
        blacks_whites += code_a[4]
    else:
        blacks_whites += code_b[4]
    if code_a[5] < code_b[5]:
        blacks_whites += code_a[5]
    else:
        blacks_whites += code_b[5]
    if code_a[6] < code_b[6]:
        blacks_whites += code_a[6]
    else:
        blacks_whites += code_b[6]
    if code_a[7] < code_b[7]:
        blacks_whites += code_a[7]
    else:
        blacks_whites += code_b[7]
    if code_a[8] < code_b[8]:
        blacks_whites += code_a[8]
    else:
        blacks_whites += code_b[8]
    if code_a[9] < code_b[9]:
        blacks_whites += code_a[9]
    else:
        blacks_whites += code_b[9]
    if code_a[0][0] == code_b[0][0]:
        blacks += 1
    if code_a[0][1] == code_b[0][1]:
        blacks += 1
    if code_a[0][2] == code_b[0][2]:
        blacks += 1
    if code_a[0][3] == code_b[0][3]:
        blacks += 1
    return (blacks_whites - blacks, blacks) 

def left_codes(db_ac, code_played, key_code ):         
    """
    Riceve il db di tutti i codici, il codice giocato e il codice chiave.
    Crea db_lc che contiene tutti i codici segreti possibili. Mette il flag True per tutti i codici segreti possibili in db_ac.
    Confronta il codice giocato con tutti i codici di db_ac. Per tutti quelli che non erano già stati eliminati e che il codice chiave generato è uguale a quello
    della partita, vengono aggiunti a db_lc. Altrimenti non vengono aggiunti e il flag in db_ac viene settato a False 
    """
    db_lc = []                                                   
    for code_ac in db_ac:                                        
        found_keycode = find_keycode(code_played, code_ac) 
        if key_code == found_keycode and code_ac[1] == True:      
            db_lc.append(code_ac)
        else:                                                  
            code_ac[1]=False                                                                                
    return db_ac, db_lc8

def best_codes (db_ac, db_lc, colors):                                #Crea db_bc con i best codes e ripopola i left codes con il rate corretto
    """ check mastermind.altervista.org to understand how this algorithm works"""                                       
    db_loop = []                                                    #lista temporanea                                           
    """ Se i possibili codici segreti sono molti, i codici per la simulazione saranno i left codes. Evita che il loop richieda troppo tempo per l'esecuzione.
        Produce db_loop con [10] = a max_hit e [11] con num_of_zero. Fornisce anche min_of_max  """
    if (len(db_lc) > 252 and colors == 66) or (len(db_lc) > 976 and colors == 88):    
        db_loop = db_lc                                             
    else:
        db_loop = db_ac
    key_hits = [0]*25                       #Ogni campo corrisponde ha un tipo di cod.chiave(1 bianco, 2 bianchi, 1 nero, ...)
    for code_loop in db_loop:                                                                                             
        for i in range (25):
            key_hits[i] = 0                   
        for code_lc in db_lc:                                       #per ogni codice di db_loop ripete per tutti i possibili codici segreti 
            whites, blacks = find_keycode(code_loop, code_lc)  #trova il codice chiave tra i codici di db_loop e quelli di db_lc
            key_hits [whites*5 + blacks] +=1                        #incrementa le ricorrenze di codici chiave uguali. *5 simula una tabella a 2 dim
        #max_hit = max(key_hits)                                     #trova il numero massimo di ricorrenze dei codici chiave. Questo valore indica al massimo quanti cod segreti possono rimanee giocando code_loop
        code_loop[10] = max(key_hits)                               #trova il numero massimo di ricorrenze dei codici chiave. Questo valore indica al massimo quanti cod segreti possono rimanee giocando code_loop
        #num_of_zero = key_hits.count(0)                             #pochi campi a zero significa miglior distribuzione dei codici chiave e quindi maggior possiblità di lasciare un num di cod segreti inferiore
        code_loop[11] = key_hits.count(0)                            #pochi campi a zero significa miglior distribuzione dei codici chiave e quindi maggior possiblità di lasciare un num di cod segreti inferiore
    """ Usa db_loop, min_of_max e crea db_bc_1 con tutti i code_loop[10] = min_of_max,  produce min_num_of_zero e db_lc ordinato in base a min_of_max """ 
    db_loop = sorted(db_loop, key=lambda x: (x[10], x[11], -x[1]))
    db_lc = []
    db_bc = []
    for  code_loop in db_loop:
        if code_loop[1] == True:
            db_lc.append(code_loop)
        if code_loop[1] == db_loop[0][1] and code_loop[10] == db_loop[0][10] and code_loop[11] == db_loop[0][11]:
            db_bc.append(code_loop)
    return db_lc, db_bc

def code_adapter (code):
    """ il codice viene trasformato nel formato dei codici presenti nei database """
    adapted_code = [code, True,0,0,0,0,0,0,0,0,0,0]               
    for i in range (0,4):                                           #i campi dal 5 al 12 sono uno per ogni colore.                             
        adapted_code[1 + int(code[i])] += 1                         #ognuno di questi campi contiene quante volte il colore è presente nel codice
    return adapted_code

def make_matrix_from_file (colors, code):             #used by game4 and idented_played
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))
    #file = os.path.join(os.getcwd(), 'Played_Games', 'Game_' + str(colors) + '_' + code + '.txt')
    file = os.path.join(script_directory, 'Played_Games', 'Game_' + str(colors) + '_' + code + '.txt')   
    if not os.path.exists(file):
        print('\nMatrix file for', code, 'does not exist. Use Option 5 to create it')
        return
    fin = open(file)                                # esempio apre il file Played_Games\Game_6_1234.txt
    matrix = []
    delimiter = ';'
    for row in fin:                                 #esempio di row: 1234 XO__;1135 X___;6343 XOOO;4336 XXXX; ; ;  
        row = row.strip()                           #1234 O___;1556 OOO_;5161 XXXX; ; ; ; togli spazi prima  dopo è \n
        row = row.split(delimiter)                  #['1234 OO__', '2545 X___', '2612 XXXX', ' ', ' ', ' ', ''] da stringa a lista   
        matrix.append(row)
    return matrix

def make_matrix_from_file_renpy (colors, code):             #solo per renpy in alternativa a make_matrix_from_file
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))
    #file = os.path.join(os.getcwd(), 'Played_Games', 'Game_' + str(colors) + '_' + code + '.txt')
    file = os.path.join(script_directory, 'Played_Games', 'Game_' + str(colors) + '_' + code + '.txt')   
    if not os.path.exists(file):
        print('\nMatrix file for', code, 'does not exist. Use Option 5 to create it')
        return
    fin = open(file)                                # esempio apre il file Played_Games\Game_6_1234.txt
    matrix = []
    delimiter = ';'
    for row in fin:                                 #esempio di row: 1234 XO__;1135 X___;6343 XOOO;4336 XXXX; ; ;  
        row = row.strip()                           #1234 O___;1556 OOO_;5161 XXXX; ; ; ; togli spazi prima  dopo è \n
        sub_lista = []
        temp_str = ''
        for c in row:
            if c != ';':
                temp_str = temp_str + c
            else:
                sub_lista.append(temp_str)
                temp_str = ''
        #print (sub_lista)
        #row = row.split(delimiter)                  #['1234 OO__', '2545 X___', '2612 XXXX', ' ', ' ', ' ', ''] da stringa a lista   
        matrix.append(sub_lista)
    return matrix

def find_next_code (play, matrix, code_plus_key ):            
    """ usato solo da Game4. Usa matrix in memoria e cerca il prossimo codice da giocare + la chiave """
    matrix_temp = []
    for i in range(len(matrix)):                                    #looppa pr tutte le righe di matrix
        if matrix[i][play - 1] == code_plus_key:                    #cerca il codice giocato nella colonna che corrisponde al numero di giocata. Colonna 0 di matrix per il primo turno, colonna 1 per secondo turno, ... 
            matrix_temp.append(matrix[i])                           #salva in matrix_temp tute le righe ok. Esempio, prima giocata 1234 XX__ salva: ['1234 XX__', '1145 ____', '2166 O___', '3232 XXXX', ' ', ' ', '']
    matrix = matrix_temp                                            #il nuovo matrix ha solo le partite che portano al codice segreto
    if len(matrix) > 0:                                             #se len di matrix è 0, almeno un codice chiave inserito è sbagliato perchè non c'è nessun codice che può essere il codice segreto
        next_code_plus_key = matrix [0][play]                       #prende il primo codice+chiave della prossima colonna per il  prossimo turno. In questa colonna i codici+chiave sono comunque tutti uguali
        next_code = next_code_plus_key[:4]                          #estrapola il prossimo codice da giocare
        next_key = next_code_plus_key[5:]                           #estrapola il codice chiave. Serve solo a Game4 per capire se il codice è stato indovinato (codice chiave = XXXX) 
        return matrix, next_code, next_key
    else:
        return matrix, 'not_found', next_key

def print_board (game_board):                      
    """ visaulizza i codici giocati con relativo codice chiave """
    print()
    print ("-" * 14)
    for code in reversed(game_board):
        print ("|  ", end='')
        for peg in code[0]:
            print(peg, end='')
        print(" ", "X" * code[1], "O" * code[2], " " * (6 - code[1] - code[2]), "|", sep='' )
    print ("-" * 14)

def print_codes (db_lc, db_bc, elapsed_time):     
    """ visualizza i left, i best codes e il tempo di elaborazione dei best codes """
    lc = len(db_lc)
    bc = len(db_bc)
    print ("\nLeft Codes:", lc, "  \t\t", "Best Codes:", bc)
    for i in range (min(lc,20)):
        row_to_print = db_lc[i][0] + " . " + str(db_lc[i][10])
        if i < bc:
            row_to_print += "\t\t\t " + db_bc[i][0] + " . " + str(db_bc[i][10])
        print (row_to_print)                
    print ("Elapsed time for processing:", round (elapsed_time, 2), "secs")

def game1(colors):
    """ il giocatore deve indovinare il codice segreto scelto dal programma """                                                
    db_ac, db_lc, db_bc = init_db(colors)                            #crea il database di tutti i codici, dei left e best codes
    secret_code = random.choice(db_ac)                                  #il programma sceglie il codice segreto tra tutti i codici possibili
    secret_code = code_adapter("1234")                               #utilizzo di CS fisso per debugging
    game_board = []
    elapsed_time = 0                                                    # variabile usata per il calcolo del temp per elaborazione dei bc
    for row in range(1,11):                                             #ripeti fino a un massimo di 10 codici giocati
        while True:
            opt = input ("\nEnter four digit code or 1)Print left/best codes  2)Check secret code  9)End ")
            if opt == "1":
                print_codes (db_lc, db_bc, elapsed_time)
            elif opt == "2":
                print ("Secret Code:", secret_code[0])
            elif opt == "9":
                return
            else:
                code_played = code_adapter (opt)                     #il codice giocato, viene adattato a 12 campi
                break
        whites, blacks = find_keycode(secret_code, code_played)      #trova il codice chiave confrontando il cod tentativo con il cod segreto
        game_board.append([code_played[0], blacks, whites])             #memorizza la giocata nella board game
        print_board (game_board)                                     #visualizza la board game
        if blacks == 4:                                                 #se il codice chiave sono 4 neri allora il codice è stato indovinato
            print ("Secret Code GUESSED")
            return
        db_ac, db_lc = left_codes(db_ac, code_played, (whites, blacks))  #genera il db dei left codes e mette il flag True in db_ac per i lc
        start_time = time.time()
        db_lc, db_bc = best_codes(db_ac, db_lc, colors )                     #generazione del database dei best codes
        elapsed_time =(time.time() - start_time)                        #calcola il tempo di elaborazione per i best codes
    print ("** The maximum number of attempts has been exceeded **")    #il numero massimo di tentativi da parte del giocatore sono 10

def game2(colors):
    """ partita dove il programma deve indovinare il codice segreto scelto dal giocatore """
    db_ac, db_lc, db_bc = init_db(colors)                            #crea il database di tutti i codici, dei left e best codes  
    game_board = []
    elapsed_time = 0
    input ("\n Write down your secret code. Press enter when ready ")
    for row in range(1,11):                                 
        code_played = random.choice(db_bc)                          #il programma sceglie un codice da giocare tra i best codes
        game_board.append([code_played[0], 0, 0])                   #inserisce il codice giocato nella game_board. I cmapi dei bianchi e neri vengono valorizzati sucessivamente
        print_board (game_board)                                 #visualizza il codici tentativo effettuati dal programma  
        if len(db_lc) == 1:                                         #se il codice giocato è l'ultimo left code rimasto è anche il codice segreto
            whites = 0
            blacks = 4
        else:
            while True:
                opt = input ("\n Use X, 0, for keycode  1)Print left/best codes  2)Help  9)End ")        
                if opt == "1":
                    print_codes (db_lc, db_bc, elapsed_time)
                elif opt == "2":
                    print ("\n Enter one X for each right digits in the right place\
                            \n Enter one 0 for each right digits but in the wrong place \
                            \n Live blank if all the digits are not present in your secret code \
                            \n Enter 1 to view the remaining and best codes \
                            \n Enter 2 to stop this game \
                            \n Enter 9 to view this Help ")
                elif opt == "9":
                    return
                else:                                                   
                    whites = opt.count("0")                             #conta gli "0" e le "X" inserite come codice chiave e valorizza blacks e whites
                    blacks = opt.count ("X")
                    blacks += opt.count ("x")
                    break             
        game_board[-1][1] = blacks                                      #inserisce nell'ultimo record di game_board i neri
        game_board[-1][2] = whites                                      #inserisce nell'ultimo record di game_board i bianchi
        if blacks == 4:                                                 
            print_board (game_board)
            print ("\n Secret code GUESSED")
            return                                                          #partita terminata torna al menu per una nuova partita
        db_ac, db_lc = left_codes(db_ac, code_played, (whites, blacks))  #genera i left codes     
        if len(db_lc) == 0:                                                 #se non ci sono più left codes, uno o più codici chiave sono errati
            print ("\n At least one key code has been entered is incorrect")
            return
        start_time = time.time()
        db_lc, db_bc = best_codes(db_ac, db_lc, colors)                     #crea il db dei best codes                                    
        elapsed_time =(time.time() - start_time)                        #calcola il tempo di elaborazione

def game3(colors):
    """ il giocatore deve indovinare il codice segreto scelto dal programma """                                                  
    db_ac, db_lc_not_used, db_bc_not_used = init_db(colors)                            #crea il database di tutti i codici, dei left e best codes
    secret_code = random.choice(db_ac)                                  #il programma sceglie il codice segreto tra tutti i codici possibili
    matrix = None
    db_lc = [['0000', True, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    db_bc = [['0000', True, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    #secret_code = code_adapter("1122")                               #utilizzo di CS fisso per debugging
    game_board = []
    elapsed_time = 0                                                    # variabile usata per il calcolo del temp per elaborazione dei bc 
    for play in range(1,11):                                             #ripeti fino a un massimo di 10 codici giocati
        while True:
            opt = input ("\nEnter four digit code or 1)Print left/best codes  2)Check secret code  9)End ")
            if opt == "1":
                if matrix != None:
                    print_codes (db_lc, db_bc, elapsed_time)
                else:
                    print('\nTo see the Best Code, your first code must be one of the following: 2131, 1231, 2311, 2113, 1123, 1212, 1221, 1122, 1234')               
            elif opt == "2":
                print ("Secret Code:", secret_code[0])
            elif opt == "9":
                return
            else:
                code_played = code_adapter (opt)                     #il codice giocato, viene adattato a 12 campi
                break
        if play == 1:
            matrix = make_matrix_from_file (colors, code_played[0])              #crea la matrice delle partite giocate dal file in base al numero di colori usati e al primo codice giocato                 
        whites, blacks = find_keycode(secret_code, code_played)      #trova il codice chiave confrontando il cod tentativo con il cod segreto
        game_board.append([code_played[0], blacks, whites])             #memorizza la giocata nella board game
        print_board (game_board)                                     #visualizza la board game
        if blacks == 4:                                                 #se il codice chiave sono 4 neri allora il codice è stato indovinato
            print ("Secret Code GUESSED")
            return
        code_plus_key = code_played[0] + ' ' + 'X' * blacks + 'O' * whites + '_' * (4 - (blacks + whites)) #compone il codice giocato + il codice chiave inserito dal giocatore per cercare il prossimo codice da gocare
        if matrix != None:
            matrix, next_code, next_key = find_next_code (play, matrix, code_plus_key )                  #trova il prossimo codice da giocare. next_key serve solo se è uguale a XXXX
            db_bc[0] = code_adapter (next_code)
    print ("** The maximum number of attempts has been exceeded **")    #il numero massimo di tentativi da parte del giocatore sono 10

def game4(colors):
    """ partita dove il programma deve indovinare il codice segreto scelto dal giocatore usando le partite già giocate """
    game_board = []
    next_key = ''
    fake_pegs_dict = {6:['1', '2', '3', '4', '5', '6'], 8:['1', '2', '3', '4', '5', '6', '7', '8']}  #serve per simulare un codice random sia per la versione a 6 e a 8 colori                 
    fake_pegs = fake_pegs_dict[colors]                          #considera la fake pegs in base al numero di colori con cui si sta giocando
    random.shuffle(fake_pegs)                                   #mischia i pegs nella lista
    input ("\n Write down your secret code. Press enter when ready ")
    first_codes_list = ['2131', '1231', '2311', '2113', '1123', '1212', '1221', '1122', '1234', '1234', '1234']     #1234 è ripetuto per aumentare le probabilità
    is_first_play = True 
    first_code = random.choice(first_codes_list)                #per il primo tentativo il codice viene scelto nella lista first_codes_list
    matrix = make_matrix_from_file (colors, first_code)      #crea la matrice delle partite giocate dal file in base al numero di colori usati e al primo codice giocato 
    for play in range(1,11):                                    #loop per tutte le partite possibili
        if is_first_play:
            code_played = first_code
            is_first_play = False                               #dalla seconda giocata il codice sarà: next_code
        else:
            code_played = next_code
        code_played_fake = ''                                   #è il codice che viene visualizzao invece di quello vero. Fa sembrare che il programma gioca sempre codici diversi          
        for i in code_played:                                   #generazione del codice fake basato sul codice vero
            code_played_fake += fake_pegs[int(i) - 1]
        game_board.append([code_played_fake, 0, 0])             #aggiunta del codice fake
        print_board (game_board)                             #visualizza i codici fake giocati dal programma      
        if next_key == 'XXXX':
            blacks = 4
            whites = 0
        else:
            while True:                                                                                 #ripete fino a quando non viene inserito il codice chiave
                opt = input ("Use X, 0, for keycode  1)Help  9)End ")        
                if opt == "1":
                    print ("\n Enter one X for each right digits in the right place\
                            \n Enter one 0 for each right digits but in the wrong place \
                            \n Live blank if all the digits are not present in your secret code \
                            \n Enter 1 to view this Help \
                            \n Enter 9 to stop this game \
                             ")
                elif opt == "9":
                    return
                else:                                                   
                    whites = opt.count("0")                             #conta gli "0" e le "X" inserite come codice chiave e valorizza blacks e whites
                    blacks = opt.count ("X")
                    blacks += opt.count ("x")
                    break             
        game_board[-1][1] = blacks                                      #inserisce nell'ultimo record di game_board i neri
        game_board[-1][2] = whites                                      #inserisce nell'ultimo record di game_board i bianchi
        if blacks == 4:                                                 
            print_board (game_board)
            print ("Secret code GUESSED")
            return                                                      #partita terminata torna al menu per una nuova partita
        code_plus_key = code_played + ' ' + 'X' * blacks + 'O' * whites + '_' * (4 - (blacks + whites)) #compone il codice giocato + il codice chiave inserito dal giocatore per cercare il prossimo codice da gocare
        matrix, next_code, next_key = find_next_code (play, matrix, code_plus_key )                  #trova il prossimo codice da giocare. next_key serve solo se è uguale a XXXX
        if next_code == 'not_found':
            print ("\n At least one key code entered is incorrect")
            return

def game5(colors):
    """ vengono inseriti sia i codici tentativo che i codici chiave. Utile se si gioca in parallelo una partita come decodificatore """
    db_ac, db_lc, db_bc = init_db(colors)                            
    game_board = []
    elapsed_time = 0
    for row in range(1,11):                                             #ripeti fino a un massimo di 10 codici giocati
        while True:                                                     #continua fino a quando non viene inserito un codice tentativo
            opt = input ("\nEnter four digit code or 1)Print left/best codes  9)End ")
            if opt == "1":
                print_codes (db_lc, db_bc, elapsed_time)
            elif opt == "9":
                return
            else:
                code_played = code_adapter (opt)                     #il codice giocato, viene adattato a 12 campi
                break
        while True:                                                     #continua fino a quando non viene inserito un codice chiave
            opt = input ("\n Use X, 0, for keycode  1)Print left/best codes  2)Help  9)End ")        
            if opt == "1":
                print_codes (db_lc, db_bc, elapsed_time)
            elif opt == "2":
                print ("\n Enter one X for each right digits in the right place\
                        \n Enter one 0 for each right digits but in the wrong place \
                        \n Live blank if all the digits are not present in your secret code \
                        \n Enter 1 to view the remaining and best codes \
                        \n Enter 2 to stop this game \
                        \n Enter 9 to view this Help ")
            elif opt == "9":
                return
            else:                                                   
                whites = opt.count("0")                                 #conta gli "0" e le "X" inserite come codice chiave e valorizza blacks e whites
                blacks = opt.count ("X")
                blacks += opt.count ("x")
                break             
        game_board.append([code_played[0], blacks, whites])             #inserisce il codice giocato e il codice chiave nella game board
        print_board (game_board)
        if blacks == 4:                                                 
            print ("\n Secret code GUESSED")
            return                                                              #partita terminata torna al menu per una nuova partita
        db_ac, db_lc = left_codes(db_ac, code_played, (whites, blacks))       
        if len(db_lc) == 0:                                                     #se non ci sono più left codes, uno o più codici chiave sono errati
            print ("\n At least one key code has been entered is incorrect")
            return
        start_time = time.time()
        db_lc, db_bc = best_codes(db_ac, db_lc, colors)                     #crea il db dei best codes                                    
        elapsed_time =(time.time() - start_time)                        #calcola il tempo di elaborazione

def matrix_file_creation (colors, first_code_played = "1111"):
    """ Viene richiamato direttamente dal menu principale. 
    Riceve in input il primo codice da giocare e gioca tutte le partite per tutti i codici segreti possibili.
    A ogni partita il primo codice giocato rimane lo stesso ma si passa al cod segreto successivo. Dal secondo tentativo viene giocatoo il primo best code """

    """ salva in all_board[] tutte le partite giocate """
    stats = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}                         #memorizza le partite terminate con un tentativo, con 2 tentativi e così via
    all_board = []                                                      #memorizza tutte le partite
    first_code_played = input ("\nEnter first code to play for all games ")
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(os.path.join(script_directory, 'Played_Games', 'Game_' + str(colors) + '_' + first_code_played + '.txt')):
        print('\nGame_' + str(colors) + '_' + first_code_played + '.txt' + ' file already exist')
        return
    first_code_played = code_adapter(first_code_played)
    game_counter = 0                                                    #conta le partite giocate
    db_secret_code, db_lc_not_used, db_bc_not_used = init_db(colors) #crea il db di tutti i codi segreti
    print()
    for secret_code in db_secret_code:                                      #loop per tutti i codici segreti
        db_ac, db_lc, db_bc = init_db(colors)                            #crea nuovi db per ogni partita
        game_counter += 1                                                   #serve solo per essere visualizzato a video
        print("\rPlayed Games: ", game_counter, "of", len(db_ac), end="")   #stampa in numero progressivo delle partite. \r non salta su una nuov riga (Solo con pypy)
        blacks = 0                                                          # sttato a zero perchè testato prima dell'inizio delle partite
        board = [0] * max_play + [''] * max_play            # [0, 0, 0, 0, 0, 0, 0, '', '', '', '', '', '', ''] memorizza una partita. I campi settati a 0 per keycode e gli altri per i codici giocati
        code_played = first_code_played                     #all'inizio di ogni nuova partita il codice giocato è quello inserito in input
        for i in range(max_play):                           #loop per il numero massimo delle giocate che deve essere maggiore di quello della partita con più tentativi che verrà giocata
            if blacks == 4:                                 #se la partita è terminata, torna a giocare la prossima
                break
            whites, blacks = find_keycode(secret_code, code_played)          #trova il codice chiave confrontando il codice tentativo con il codice segreto
            board[i] = blacks * 10 + whites                                     #salva il codice chiave in un numero a due cifre. La cifra delle decine sono i neri e le unità i bianchi
            board[i + max_play] = code_played[0] + ' ' + 'X' * blacks + 'O' * whites + "_" * (4 - blacks - whites)  #salva il codice giocato e il codice chiave usando X per neri e O per i bianchi
            if blacks == 4:                                                     #se il codice è stato indovinato aggiungi la partita a all_board e il numero di tentativi in stats
                stats[i+1] += 1                                                   #esempio se la partita è finita con 4 tentativi, viene incrementato stats[3]                 
                all_board.append(board)                                         #es: append [10, 0, 30, 40, 0, 0, 0, '1234 X___', '2566 ____', '1113 XXX_', '1111 XXXX', '', '', ''] 
                break                                                           #torna a giocare la prossima partita
            db_ac, db_lc = left_codes(db_ac, code_played, (whites, blacks))  #genera il db dei left codes e mette il flag True in db_ac per i lc
            db_lc, db_bc = best_codes(db_ac, db_lc, colors)                         #genera il database dei best codes  
            code_played = db_bc[0]                                              #il programma sceglie come prossimo tentativo il primo codice dei best codes.
        #if game_counter == 10: break                                             #usato per debug per ridurre i tempi d elaborazione

    """ visualizza  tutte le partite """
    print("\n\n#     cod1-key1   cod2-key2   cod3;key3   cod4;key4   cod5;key5   cod6;key6   cod7;key7")
    i = 1                                                               #contatore delle partite visualizzato a video
    for board in all_board:                                             #loop per tutte le partite giocate
        print()                                                         #fa andare alla riga successiva del video
        print(str(i), ')',  ' ' * (5 - len(str(i))), end='', sep='')    #visualizza il contatore
        for play in board[max_play:]:                                   #visualizza solo la secoda parte di board evitando i codici chiave di due cifre
            print(play, '  ', end="")                                   #lascia dello spazio tra un codice e l'altro
        i += 1                                                          
    """
    Struttura all_board prima del sort 
    [11, 20, 0, 40, 0, 0, 0, '1234 XO__', '1135 XX__', '4536 ____', '1112 XXXX', '', '', '']
    [11, 21, 11, 40, 0, 0, 0, '1234 XO__', '1135 XXO_', '5136 XO__', '1113 XXXX', '', '', '']
    [20, 21, 30, 40, 0, 0, 0, '1234 XX__', '1145 XXO_', '1164 XXX_', '1114 XXXX', '', '', '']
    """
    all_board.sort()                                                    #ordina secondo i codici chiave a due cifre

    """ Salva in Game_c_nnnn.txt tutte le partite giocate (all_board)  - 'c' è colors e 'nnnn' è il primo codice giocato """ 
    if not os.path.exists('Played_Games'):          #crea la cartella Played_Games se non esiste
        os.makedirs('Played_Games')
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(script_directory, 'Played_Games', ('Game_' + str(colors) + '_' + first_code_played[0] + '.txt'))    #crea ad esempio Played_Games\Game_6_1234.cvs
    file_out = open(file, 'w', newline='')
    for board in all_board:                         #lopp per tutte le partite giocate. Esempio: [10, 0, 30, 40, 0, 0, 0, '1234 X___', '2566 ____', '1113 XXX_', '1111 XXXX', '', '', '']
        row = ''                                    #la riga che verrà scritta nel file              
        for play in board[max_play:]:               #esempio di play: 1234 X___
            row += play + ';'                       #aggiunge per ogni codice più codice chiave il ";" per creare un file txt   
        row = row[:-1]                              #toglie l'ultimo  ';' che è in più 
        file_out.write(row+"\n")                    #esempio scrive "1111 XX__;1223 XOO_;1132 XXXX; ; ; ;" su Played_Games\Game_6_1234.cvs
    file_out.close()
    print("\n\nAll played game are saved in ", 'Played_Games\\Game_' + str(colors) + '_' + str(first_code_played[0]) + '.txt')

    """ appende nel TXT delle statistiche di riepilogo che servirà per la funzione statistics  """
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))                    
    file = os.path.join(script_directory, 'Played_Games', ('Statistics' + '.txt')) #esempio: Statistics\Temp\Statistics_6_1111.txt
    file_out = open(file, 'a', newline='')          #apre in scrittura il file Statistics\Temp\Statistics_6_1111.txt
    total_attempts = 0                              #numero di tentativi di tutte le partite
    average = 0                                     #media dei tentativi che servono per vincere una partita
    for x, y in stats.items():                      #loop per tutti le coppie di chiavi e valori di stats.
        total_attempts += x * y                     #ogni valore di x rappresenta con quanti tentativi è vinta una partita ed è associata a y che sono il numero di partite
    average = total_attempts / game_counter         #calcola la media dei tentativi che servono per vincere una partita. Il totale dei tentativivi rispetto al numero di partite giocate 
    str_stats = ''                                  
    for stat in stats.values():                     #loop per tutte le tipologie di partite, quelle vinte con 1 tentativo, 2, con 3, ...
        str_stats += str(stat) + ';'                #converte la lista in stringa. Ogni valore è separato da ;
    #salva il numero di colori es: 6, il primo codice, es: 1111, la media con 3 cifre decimali, stats convertito in stringa nel file   
    file_out.write(str(colors) + ';' + first_code_played[0] + ';' + str(round(average,3)) + ';' + str_stats + '\n')  
    file_out.close()                                #chiude il file Statistics\Statistics.txt

def statistics(colors):
    print("\nColors  First           Won in  Won in  Won in  Won in  Won in  Won in  Won in \
               \nused    Code  Average   1_play  2_play  3_play  4_play  5_play  6_play  7_play")
    print("-" * 80)
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(script_directory, 'Played_Games', ('Statistics' + '.txt'))
    if not os.path.exists(file):
        print('\nStatistics.txt does not exist. Use Option 5 to create it')
        return
    fin = open(file)                                #apre il file Played_Games\Statistics.txt
    stats = {}                                      #
    delimiter = ';'                                 #il separatore che occorre rimuovere
    for row in fin:                                 #esempio di row: 6;1234;4.0;0;0;0;5;0;0;
        row = row.strip()                           #esempio: 6;2233;4.2;0;0;0;4;1;0; togli spazi prima  dopo è \n
        row = row.split(delimiter)                  #esempio: ['6', '1234', '4.0', '0', '0', '0', '5', '0', '0', ''] da stringa a lista   
        stats[str(row[0])+str(row[1])] = row        #ogni riga del file Statistics viene messa in stats
    stats_lst = []
    for row in stats.values():
        stats_lst.append(row)
    stats_lst.sort()
    for stat in stats_lst:                              #stampa usando il TAB per l'incolonnamento
        for idem in stat:
            print(str(idem), "\t", end="")              #esempio: 6 	2233 	4.2 	0 	0 	0 	4 	1 	0 
        print()            

def idented_played(colors):
    first_code_played = input ("\nEnter first code to play for all games ")
    matrix = make_matrix_from_file (colors, first_code_played)
    if matrix == None:                                                  #se per il codice dato in input non esiste il corrispondente file di tutte le partite giocate, ritorna 
        return    
    nested_codes = [[] for j in range(len(matrix[0]))]                  # [[], [], [], [], [], [], []] crea tanti elementi vuoti quanti sono i codici+chiavi nella board di matrix
    i = 0                                                         
    precedente = [''] * len(matrix[0])                                  # ['', '', '', '', '', '', ''] crea tanti elementi vuoti quanti sono i codici+chiavi nella board di matrix
    for board in matrix:                                                # esempio di board: ['1234 XXX_', '1122 XXO_', '1224 XXXX', ' ', ' ', ' ', '']
        for play_num in range(len(board)):                  
            code_plus_key = ''.join(str(x) for x in board[play_num])    #da lista a stringa del codice più la chiave esempio 1156 OO__
            if precedente[play_num] != board[play_num]:
                nested_codes[play_num].append(i)
                nested_codes[play_num].append(code_plus_key)
                precedente[play_num] = board[play_num]
        i += 1
        # nested_codes [[0, '1111 XXX_'], [0, '1123 XX__'], [0, '1114 XXX_'], [0, '1115 XXX_', 1, '1115 XXXX'], [0, '1116 XXXX'], [], []] con matrix vecchio
        # nested_codes [[0, '1234 ____'], [0, '1555 ____'], [0, '6666 XXXX'], [0, ' '], [0, ' '], [0, ' '], []] con matrix nuovo che ha in più row += empty_fields
    # Get the directory containing the current script
    script_directory = os.path.abspath(os.path.dirname(__file__))    
    file_ident = os.path.join(script_directory, 'Played_Games', ('Idented_Game_' + str(colors) + '_' + first_code_played + '.txt'))
    file_out = open(file_ident, 'w', newline='')                    #apre ad esempio il file Played_Games\Idented_Game_6_1234.txt
    for board_num in range(len(matrix)):
        row = ''
        for play_num in range(len(nested_codes)):
            if board_num in nested_codes[play_num]:
                indice = nested_codes[play_num].index(board_num)
                row = row + nested_codes[play_num][indice+1] + ' ' * 3
            else:
                row = row + ' ' * 12                                    #stampa spazi invece del codice + codice chiave
        print(row)
        file_out.write(row+"\n")
    file_out.close()
    print("\nAll idented played game are saved in ", 'Played_Games\\Idented_Game_' + str(colors) + '_' + first_code_played + '.txt')
      
def menu():    
    colors = 6
    while True: 
        print("\n\n\n MASTER MIND GAME -  mastermind.altervista.org - You are playng with *", colors, "* numbers (press 'C' to change) \
                   \n =======================================================================================================\
                   \n 1) Game1 - You will try to guess computer secret code (Best Codes Algorithm) \
                   \n 2) Game2 - Computer will try to guess your secret code (Best Codes Algorithm)\
                   \n 3) Game3 - You will try to guess computer secret code (Already Played Games Algorithm)\
                   \n 4) Game4 - Computer will try to guess your secret code (Already Played Games Algorithm)  \
                   \n 5) Game5 - Two human players. One as Codemaker and one as Codebreaker (Best Codes Algorithm) \
                   \n 6) Build, print an save all games played based on given first Code\
                   \n 7) Print statistics based on all played games \
                   \n 8) Print all played games with ident format \
                   \n 9) End ")
        option = input("                   => ")
        if option == "1":                       #il giocatore deve indovinare il codice segreto scelto dal programma
            game1(colors)                       
        elif option == "2":                     #il programma deve indovinare il codice segreto scelto dal giocatore
            game2(colors)                       
        elif option == "3":                     #il giocatore deve indovinare il codice segreto scelto dal programma. Può visualizzare il best code prodotto da mm.find_next_code 
            game3(colors)                       
        elif option == "4":                     #il programma indovina il codice segreto del giocatore usando i file delle partite già giocate
            game4(colors)                       
        elif option == "5":                     #chiede in input il primo codice da giocare e gioca tutte le partite quanti sono i codici segreti (1296 / 4096)
            game5(colors)
        elif option == "6":                     #Dato il primo codice giocato, crea il file con tutte le partite giocate per tutti i possibili codici segreti
            matrix_file_creation(colors)    
        elif option == "7":                     #visualizza a video le statistiche e partite giocate con l'opzione 5
            statistics(colors)                  
        elif option == "8":                     #visualizza con identazione le partite giocate con l'opzione 5. Chiede il primo codice
            idented_played(colors)      
        elif option.upper() == "C":             #swich da 6 a 8 o viceversa del numero di colori usati per tutte le funzioni del programma.                          
            if colors == 6:                     
                colors = 8
            else:
                colors = 6
        elif option == "9":
            break   


if __name__ == '__main__':
    max_play = 7                #con 8 colori e con primo codice giocato 1111, "best code" indovina con al massimo 7 tentativi. Non serve un numero maggiore
    menu()



            
               
