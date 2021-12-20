#include <iostream>
#include <string>
#include <stdlib.h>     //exit(0)
#include <cmath>        // pow
#include <time.h>       // srand (time(NULL))
#include <chrono>
#include<bits/stdc++.h>  // count
using namespace std;
using namespace std::chrono;

class Mastermind_Engine {
    public:
        int init_db(int colors, int db_ac[][14], int db_lc[][14], int db_bc[][14]){
            int i=0; int j=0;
            for (int a = 1; a < colors+1; a++) {
                for (int b = 1; b < colors+1; b++) {
                    for (int c = 1; c < colors+1; c++) {
                        for (int d = 1; d < colors+1; d++) {
                            db_ac[i][0]=a; db_ac[i][1]=b; db_ac[i][2]=c; db_ac[i][3]=d; db_ac[i][4]=1;
                            db_ac[i][5]=0; db_ac[i][6]=0; db_ac[i][7]=0; db_ac[i][8]=0; db_ac[i][9]=0;
                            db_ac[i][10]=0; db_ac[i][11]=0; db_ac[i][12]=0; db_ac[i][13]=0;
                            db_ac[i][4+a] += 1; db_ac[i][4+b] += 1;
                            db_ac[i][4+c] += 1; db_ac[i][4+d] += 1;
                            for (int k=0; k<14; ++k) {db_lc[i][k] = db_ac[i][k];}
                            if (colors==6 && db_ac[i][5]<3 && db_ac[i][6]<3 && db_ac[i][7]<3 && db_ac[i][8]<3
                                && db_ac[i][9]<3 && db_ac[i][10]<3 && db_ac[i][11]<3 && db_ac[i][12]<3){
                                 for (int k=0; k<14; ++k) {db_bc[j][k] = db_ac[i][k];}
                                 ++j;
                                }
                            if (colors==8 && db_ac[i][5]<2 && db_ac[i][6]<2 && db_ac[i][7]<2 && db_ac[i][8]<2
                                && db_ac[i][9]<2 && db_ac[i][10]<2 && db_ac[i][11]<2 && db_ac[i][12]<2){
                                 for (int k=0; k<14; ++k) {db_bc[j][k] = db_ac[i][k];}
                                 ++j;
                                }
                            ++i;
                        }
                    }
                }
            }
            return (j);     // return the number of best codes
        };

        int find_keycode(int code_a[14], int code_b[14], int key_code[2]){
            int blacks_whites = 0;
            int blacks = 0;
            for (int i=5; i<13; i++){
                if (code_a[i] < code_b[i]){
                    blacks_whites += code_a[i];}
                else {
                    blacks_whites += code_b[i];}
            }
            for (int i=0; i<4; i++){
                if (code_a[i] == code_b[i]){
                    blacks += 1;}
            }
            int whites = blacks_whites - blacks;
            key_code [0] = whites;
            key_code [1] = blacks;
            return (0);
        }

        int left_codes(int db_ac[][14], int ac, int code_played[14], int key_code[2], int db_lc[][14]){
            // save key code received as argument
            int save_key_code [2];
            save_key_code[0]=key_code[0];save_key_code[1]=key_code[1];
            // code_b assume all values of db_ac
            int code_b[14]; int j=0;
            for (int i=0; i<ac; i++){
                for (int k=0; k<14; k++){code_b[k]=db_ac[i][k];}
                    find_keycode (code_played, code_b, key_code);
                    // compare key code received as arg with found key code
                    if (save_key_code[0]==key_code[0] && save_key_code[1]==key_code[1] && db_ac[i][4]==1){
                        // append new record in db_lc
                        for (int k=0; k<14; k++){db_lc[j][k] = db_ac[i][k];}
                        j++;
                    }
                    else{
                        // flag the code as deleted
                        db_ac[i][4]=0;
                    }
                }
            int lc = j;
            return(lc);
            }

        int best_codes (int lc, int db_ac[][14], int db_lc[][14], int ac, int colors, int db_bc[][14] ){
            int min_of_max = 99999;
            for(int i=0; i<ac; i++){
                int key_hits[25]={};
                for (int j=0; j<lc; j++){
                    int key_code[2]={};
                    int code_a[14]; int code_b[14];
                    for (int k=0; k<14; k++){code_a[k]=db_ac[i][k];}
                    for (int k=0; k<14; k++){code_b[k]=db_lc[j][k];}
                    find_keycode (code_a, code_b, key_code);
                    key_hits [key_code[0]*5 + key_code[1]] +=1;
                }
                int max_hit=0;
                //max_hit = max(key_hits)
                for (int k=0; k<25; k++){if (max_hit<key_hits[k]){max_hit=key_hits[k];}}
                db_ac[i][13] = max_hit;
                if (max_hit < min_of_max){
                    min_of_max = max_hit;
                    }
            }
            //reset db_lc and db_bc
            for (int x=0 ; x < ac; x++){
                    for (int y=0 ; y < 14; y++){
                        db_lc[x][y]=0; db_bc[x][y]=0;
                    }
            }
            // feeds db_lc and db_bc
            int j=0; int z=0;
            for(int i=0; i<ac; i++){
                if (db_ac[i][13]==min_of_max){
                    for (int k=0; k<14; k++){db_bc[j][k]=db_ac[i][k];}
                    j++;
                }
                if (db_ac[i][4]==1){
                    for (int k=0; k<14; k++){db_lc[z][k]=db_ac[i][k];}
                    z++;
                }
            }
            //lc=z;
            int bc=j;
            // sort db_lc
            int temp [14] = {};
            for (int i=0; i<lc; i++){
                for (int j=lc-2; j>=i; j--){
                    if (db_lc[j][13] > db_lc[j+1][13]){
                        // swap j con j+1
                        for (int k=0; k<14; k++){temp[k]=db_lc[j][k];}
                        for (int k=0; k<14; k++){db_lc[j][k]=db_lc[j+1][k];}
                        for (int k=0; k<14; k++){db_lc[j+1][k]=temp[k];}
                    }
                }
            }
            //if in db_bc there is almost a left code, deletes every inconsistent codes
            if (db_lc[0][13] == min_of_max){
                int db_bc_temp[bc][14] = {}; int j=0;
                for (int i=0; i<bc; i++){
                    if (db_bc[i][4]==1){
                        for (int k=0; k<14; k++){db_bc_temp[j][k]=db_bc[i][k];}
                        j++;
                    }
                }
                bc = j;
                for (int x=0 ; x < bc; x++){
                    for (int y=0 ; y < 14; y++){
                        db_bc[x][y] = db_bc_temp[x][y];
                    }
                }
            }
            return(bc);
}
        void code_adapter (int code[14]){
            for (int i=0; i<4; ++i){
                code [4 + code[i]] ++;
            }
        }

        //only for debugging purpose
        void print_db (int combinations, int db[][14]){
            for (int i=0; i <combinations; i++) {
                cout <<"\n "<<i<<" "<<db[i][0]<<" "<<db[i][1]<<" "<<db[i][2]<<" "<<db[i][3]<<"  ";
                cout <<db[i][4]<<"  "<<db[i][5]<<" "<<db[i][6]<<" "<<db[i][7]<<" "<<db[i][8]<<" ";
                cout <<db[i][9]<<" "<<db[i][10]<<" "<<db[i][11]<<" "<<db[i][12]<<"  "<<db[i][13];
            }
        }

        //only for debugging purpose
        void print_code (int code[]){
            cout << "\n";
            for (int k=0; k<14; ++k) {cout << code[k] << " ";}
        }
};

class Mastermind: public Mastermind_Engine {
    public:
        void print_board (int game_board[][6], int row) {
            for (int i=row; i >0; i--){
                    cout << "\n";
                    for (int k=0; k<4; k++){
                            if (k==0){cout << "[";}
                            cout << game_board[i][k];
                            if (k<3){cout << ", ";}
                            if (k==3){cout << "] ";}
                            }
                    for (int k=0; k<game_board[i][4]; k++) {cout << "X";}
                    for (int k=0; k<game_board[i][5]; k++) {cout << "0";}
                    }
            cout << "\n----------------------------------------------------------------------------\n";
            }

        void print_codes (int lc, int db_lc[][14], int bc, int db_bc[][14], float elapsed_time=0){
            string header_space = ""; string lc_str = to_string(lc);
            for (int i=0; i<16-lc_str.size();i++){header_space.append(" ");}
            cout << "\n\nLeft Codes: " << lc << header_space << "Best Codes: "<< bc;
            string codes_space = ""; string rate_str = to_string(db_lc[0][13]);
            for (int i=0; i<19-rate_str.size();i++){codes_space.append(" ");}
            for (int i=0; i<min(lc,20); i++){
                string row_to_print;
                for (int j=0; j<4; j++) {row_to_print.append(to_string(db_lc[i][j])+" ");}
                row_to_print.append(" "+to_string(db_lc[i][13]));
                if (i<bc) {
                    row_to_print.append(codes_space);
                    for (int j=0; j<4; j++) {row_to_print.append(to_string(db_bc[i][j])+" ");}
                    row_to_print.append(" "+to_string(db_bc[i][13]));
                }
                cout << "\n" << row_to_print;
                }
                cout <<"\nElapsed time for processing: "<<elapsed_time<<" seconds";
            }
};


void game1 (int colors){
    Mastermind mm;
    int ac = pow(colors, 4); int lc = ac;     //4 is the numbers of holes in the board game
    int db_ac [ac][14], db_lc [ac][14], db_bc [ac][14];
    int bc = mm.init_db (colors, db_ac, db_lc, db_bc);
    int secret_code [14]; int rndCode = rand()%ac;
    for (int k=0; k<14; ++k) {secret_code[k] = db_ac[rndCode][k];}
    // set fix secret code for debugging purpose
    //int secret_code[14] = {1,5,3,4,0,0,0,0,0,0,0,0,0,0}; /* secret code for debugging */
    //mm.code_adapter(secret_code);
    int game_board [11][6];
    float elapsed_time = 0;
    for (int row=1; row<11; row++) {
        int code_played[14]={0}; int opt;
        do {
            cout << "\n\nEnter four digit code or 1)Print left/best codes  2)Check secret code  9)End ";
            cin >> opt;
            switch(opt) {
                case 1:
                    mm.print_codes (lc, db_lc, bc, db_bc, elapsed_time);
                    break;
                case 2:
                    cout << "Secret Code: ["<<secret_code[0]<<", "<<secret_code[1]<<", ";
                    cout << secret_code[2]<<", "<<secret_code[3]<<"]";
                    break;
                case 9:
                    return;
                default:
                    string code_str = to_string (opt);
                    code_str.append ("0000000000");
                    for (int k=0; k<14; ++k) {code_played[k]=0;code_played[k] = code_played[k] * 10 + (code_str[k] - 48);}
                    mm.code_adapter (code_played);
                    break;
            }
        }
        while (opt<3);
        int key_code [2] = {};
        mm.find_keycode(secret_code, code_played, key_code);
        int whites = key_code [0];
        int blacks = key_code [1];
        for (int k=0; k<4; ++k){game_board[row][k]=code_played[k];}
        game_board[row][4]=blacks; game_board[row][5]=whites;
        mm.print_board (game_board, row);
        if (blacks == 4){
            cout << "\n\nSecret Code GUESSED";
            return;
        }
        lc = mm.left_codes(db_ac, ac, code_played, key_code, db_lc);
        auto start = high_resolution_clock::now();
        bc = mm.best_codes(lc, db_ac, db_lc, ac, colors, db_bc);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        elapsed_time = (float)duration.count()/1000000;
    }
    cout << "** The maximum number of attempts has been exceeded **";
}

void game2 (int colors){
    Mastermind mm;
    int ac = pow(colors, 4); int lc = ac;     //4 is the numbers of holes in the board game
    int db_ac [ac][14], db_lc [ac][14], db_bc [ac][14];
    int bc = mm.init_db (colors, db_ac, db_lc, db_bc);
    int game_board [11][6];
    float elapsed_time = 0;
    int whites; int blacks; int empty_keycode;
    cout<< "\n Write down your secret code. Press enter when ready ";
    // waiting until any key is pressed
    cin.ignore(); cin.get();
    for (int row=1; row<11; row++){
        int code_played [14]; int rndCode = rand()%bc;
        for (int k=0; k<14; ++k) {code_played[k] = db_bc[rndCode][k];}
        cout << "\n Code played: ["<<code_played[0]<<", "<<code_played[1]<<", ";
        cout << code_played[2]<<", "<<code_played[3]<<"]";
        string opt;
        if (lc==1){
            whites = 0;
            blacks = 4;}
        else {
            while (true){
                cout << "\n\n Use X, 0, -, for keycode  1)Print left/best codes  2)Help  9)End ";
                cin >> opt;
                if (count(opt.begin(), opt.end(), '1')==1){
                    mm.print_codes (lc, db_lc, bc, db_bc, elapsed_time);
                }
                else if (count(opt.begin(), opt.end(), '2')==1){
                    cout<<"\n Enter one X for each right digits in the right place\
                            \n Enter one 0 for each right digits but in the wrong place \
                            \n Enter one - if all the digits are not present in your secret code \
                            \n Enter 1 to view the remaining and best codes \
                            \n Enter 2 to stop this game \
                            \n Enter 9 to view this Help ";
                    }
                else if (count(opt.begin(), opt.end(), '9')==1){
                    return;
                }
                else {
                    blacks = count(opt.begin(), opt.end(), 'X');
                    blacks += count(opt.begin(), opt.end(), 'x');
                    whites = count(opt.begin(), opt.end(), '0');
                    break;
                }
            }
        }
        //  append code played to game board
        for (int k=0; k<4; ++k){game_board[row][k]=code_played[k];}
        game_board[row][4]=blacks; game_board[row][5]=whites;
        mm.print_board (game_board, row);
        if (blacks == 4){
            cout << "\nSecret Code GUESSED";
            return;
        }
        int key_code[2];
        key_code[0] = whites;
        key_code[1] = blacks;
        lc = mm.left_codes(db_ac, ac, code_played, key_code, db_lc);
        if (lc == 0){
            cout << "\n At least one key code has been entered is incorrect";
            return;
        }
        auto start = high_resolution_clock::now();
        bc = mm.best_codes(lc, db_ac, db_lc, ac, colors, db_bc);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        elapsed_time = (float)duration.count()/1000000;
    }
}




int main() {
  /* initialize random seed: */
  srand (time(NULL));
  int colors = 6;
  cout << "\n M A S T E R   M I N D    G A M E  -  mastermind.altervista.org";
  while (true){
    cout << "\n\n================================================================================ \
             \n1)Game1  2)Game2  3)Help  6)6 Colors(default)  8)8 Colors  9)End ";
    int option;
    cin >> option;
    switch(option) {
        case 1:
            game1(colors);
            break;
        case 2:
            game2(colors);
            break;
        case 3:
            cout << "\n 1)Game1 - You will try to guess computer secret code \
                    \n 2)Game2 - Computer will try to guess your secret code \
                    \n 6)6 Colors - For both Game1 and Game2 you will use 6 colors/digits (default) \
                    \n 8)8 Colors - For both Game1 and Game2 you will use 8 colors/digits ";
            break;
        case 6:
            colors = 6;
            cout << "\n You will play with 6 colors/digits";
            break;
        case 8:
            colors = 8;
            cout << "\n You will play with 8 colors/digits";
            break;
        case 9:
            exit(0);
}
}
}
