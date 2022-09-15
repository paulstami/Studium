import random
import math
spaces = [] #list with empty pieces of memory; elements save information about: [start_indx, size]
fill = []   #list for filled pieces of memory; elements save information about: [start_indx, size, time left in memory]


def setup(n,size,min_size,max_size,min_durat, max_durat):
    #starting function:
    #args:
    #n: number of data blocks to be allocated
    #size: size of memory
    #min_size: minimum size of the data blocks
    #max_size: maximun size of the data blocks
    #min_durat: minumum amount of time of data blocks to stay in memory for 
    #max_durat: maximum amount of time of data blocks to stay in memory for
    #one time cicle is equivalent to the allocation of a new data block

    
    #variables to keep track of statistics:
    #how many times each algorithm couldn't fit a continuous piece of data
    global search_count_ff
    global search_count_nf
    global search_count_bf

    #variables for nextfit:
    global last_indx    #keeps track of pos in memory(fill) array
    global last_pos     #keeps track of pos in spaces array
    search_count_ff = 0
    search_count_nf = 0
    search_count_bf = 0
    last_indx = 0
    last_pos = 0

    #maximum number of empty spaces during each algorithm
    max_space_ff = 0
    max_space_nf = 0
    max_space_bf = 0

    #maximum number of very small empty spaces during each algorithm
    max_frag_ff = 0
    max_frag_nf = 0
    max_frag_bf = 0
    
    seednb = random.randint(0,100000) # seed guaranteeing the same envionment for each algorithm

#######nextfit#######   
    random.seed(seednb)
    
    #initializing with empty memory
    spaces.append([0,size])
    
    for i in range(0,n):
        show_mem(size)
        cleanmem(size)
        
        temp = 0
        for j in range(0,len(spaces)):
            if(spaces[j][1] < min_size):
                temp = temp +1
        if(len(spaces) > max_space_nf):
            max_space_nf = len(spaces)
        if(temp>max_frag_nf):
            max_frag_nf = temp
            
        duration = random.randint(min_durat,max_durat)
        amount = random.randint(min_size,max_size)
        pos = nextfit(amount)
        if(pos == -1):
            break
        insertmem( pos, duration, amount)

#######firstfit#######     
    random.seed(seednb)
    
    spaces.clear()
    fill.clear()
    spaces.append([0,size])
    
    for i in range(0,n):
        #show_mem(size)
        cleanmem(size)
        
        temp = 0
        for j in range(0,len(spaces)):
            if(spaces[j][1] < min_size):
                temp = temp +1
        
        if(len(spaces) > max_space_ff):
            max_space_ff = len(spaces)
            
        if(temp>max_frag_ff):
            max_frag_ff = temp
         
        duration = random.randint(min_durat,max_durat)
        amount = random.randint(min_size,max_size)
        pos = firstfit(amount)
        if(pos == -1):
            break
        insertmem( pos, duration, amount)
        

        
#######bestfit#######  
    random.seed(seednb)
    
    spaces.clear()
    fill.clear()
    spaces.append([0,size])
    
    for i in range(0,n):      
        cleanmem(size)
        
        temp = 0
        for j in range(0,len(spaces)):
            if(spaces[j][1] < min_size):
                temp = temp +1
        
        if(len(spaces) > max_space_bf):
            max_space_bf = len(spaces)
            
        if(temp>max_frag_bf):
            max_frag_bf = temp
         
        duration = random.randint(min_durat,max_durat)
        amount = random.randint(min_size,max_size)
        pos = bestfit(amount)
        if(pos == -1):
            break
        insertmem( pos, duration, amount)
    
    print()
    print("First-Fit total times blocked:",search_count_ff)
    print("First-Fit average:",search_count_ff/n)
    print("First-Fit maximum small fragmentaion:",max_frag_ff)
    print("First-Fit maximum fragmentaion:",max_space_ff)
    print()
    print("Next-Fit total times blocked:",search_count_nf)
    print("Next-Fit average:",search_count_nf/n)
    print("Next-Fit maximum small fragmentaion:",max_frag_nf)
    print("Next-Fit maximum fragmentaion:",max_space_nf)
    print()
    print("Best-Fit total times blocked:",search_count_bf)
    print("Best-Fit average:",search_count_bf/n)
    print("Best-Fit maximum small fragmentaion:",max_frag_bf)
    print("Best-Fit maximum fragmentaion:",max_space_bf)
    
def firstfit(amount):
    #looking for first big enough space beginning at the index 0 of memory
    global search_count_ff
    i = 0
    while spaces[i][1]< amount:
        i = i+1
        search_count_ff = search_count_ff +1
        if(i == len(spaces)):
            print("ff:No space left for size: ", amount)
            return -1
    pos = spaces[i][0]
    spaces[i][0] = spaces[i][0] + amount
    spaces[i][1] = spaces[i][1] - amount
    if(spaces[i][1] == 0):
        spaces.pop(i)
    return pos

def nextfit(amount):
    #looking for first big enough space beginning after the last allocated block of memory
    global search_count_nf
    global last_pos
    global last_indx
    i = last_indx
    count = 0
    while spaces[i][1]< amount:
        i = i+1
        count = count +1
        if(count == len(spaces)):
            print("nf:No space left for size: ", amount)
            return -1
        search_count_nf = search_count_nf +1
        if(i == len(spaces)):
            i = 0
           
    last_indx = i        
    pos = spaces[i][0]
    
    spaces[i][0] = spaces[i][0] + amount
    spaces[i][1] = spaces[i][1] - amount
    
    last_pos = spaces[i][0]
    
    if(spaces[i][1] == 0):
        spaces.pop(i)
        last_indx = last_indx % len(spaces)
    return pos    
        

def bestfit(amount):
    #looks at every empty space and selects the one with the size closest to the block of data
    global search_count_bf
    best_space = 0
    avail = False
    for i in range(0,len(spaces)):
        if(spaces[i][1] >= amount):
            if(spaces[i][1] < spaces[best_space][1] or avail == False):
                best_space = i
            avail= True
            if(spaces[i][1] == amount):
                best_space = i
                break
        search_count_bf = search_count_bf +1
        
    if(not avail):
        print("bf:No space left for size: ", amount)
        return -1
    pos = spaces[best_space][0]
    spaces[best_space][0] = spaces[best_space][0] + amount
    spaces[best_space][1] = spaces[best_space][1] - amount
    if(spaces[best_space][1] == 0):
        spaces.pop(best_space)
    return pos    

def insertmem( pos, duration, amount):
    #creating new filled(allocated) block of memory
    i = 0
    if(len(fill)>0):
        while fill[i][0]< pos:
            i = i+1
            if(i == len(fill)):
                break
    fill.insert(i, [pos,duration,amount])
    return

def insertspace( pos, amount):
    global last_pos
    global last_indx
    i = 0
    while spaces[i][0]< pos:
        i = i+1
        if(i == len(spaces)):
            break
    spaces.insert(i, [pos,amount])
    if(pos<last_pos):
        last_indx = last_indx +1

def addleftspace( pos, amount):
    i = 0
    while spaces[i][0]< pos:
        i = i+1
        if(i == len(spaces)):
            break
    spaces[i][0] = spaces[i][0] - amount
    spaces[i][1] = spaces[i][1] + amount

def addrightspace( pos, amount):
    i = 0
    while spaces[i][0]< pos:
        i = i+1
        if(i == len(spaces)):
            break
    i = i -1    
    spaces[i][1] = spaces[i][1] + amount
    
def combinespace(pos, amount):
    global last_pos
    global last_indx
    i = 0
    while spaces[i][0]< pos:
        i = i+1
        
    spaces[i-1][1] = spaces[i-1][1] + amount + spaces[i][1]
    spaces.pop(i)
    if(pos<last_pos):
        last_indx = last_indx - 1

def cleanmem(size):
    #reintegrating filled spaces with no time left into empty spaces
    i= 0
    while i < len(fill):
        pos = fill[i][0]
        posl = 0
        posr = size - fill[i][2]
        fill[i][1] = fill[i][1] - 1
        if(fill[i][1]== 0):
            
            if(i>0):
                posl = fill[i-1][0]+fill[i-1][2]
            if (i<len(fill)-1):
                posr = fill[i+1][0] - fill[i][2]
                
            if(posl == pos and posr == pos):
                insertspace( pos, fill[i][2])
            elif(posl == pos):
                addleftspace( pos, fill[i][2])
            elif(posr == pos):
                addrightspace( pos, fill[i][2])
            else:
                combinespace( pos, fill[i][2])
            fill.pop(i)
            i = i -1
        i = i +1
            
def show_mem(size):
    #visualizing current memory layout: "0" means filled and "-" stands for empty
    outstr = ""
    n = len(spaces)
    m = len(fill)
    show_list = []
    i,j,k = 0,0,0
    
    while(k<n and j < m):
        if(spaces[k][0]<=fill[j][0]):
            show_list.append(spaces[k])
            k = k +1
            i = i +1
        else:
            show_list.append(fill[j])
            j = j +1
            i = i +1
    if(k>n-1):
        show_list[i:n+m]=fill[j:m]
    else:
        show_list[i:n+m]=spaces[k:n]
    for i in range(0,n+m):
        if(len(show_list[i])==2):
            outstr = outstr + (math.ceil(((show_list[i][1]*100)/size)) * "-")
        else:
            outstr = outstr + (math.ceil(((show_list[i][2]*100)/size)) * "O")
            
    print(outstr)
    for i in range(0,n+m-1):
        if(len(show_list[i])==2):
            if(show_list[i][0]+show_list[i][1] != show_list[i+1][0]):
                print("error bei ",i)
        else:
            if(show_list[i][0]+show_list[i][2] != show_list[i+1][0]):
                print("error bei ",i)
        
            
