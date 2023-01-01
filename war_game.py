import random
import operator
import matplotlib.pyplot as plt

def initialisation(s , b):
    pop = dict()
    l = list()
    for i in range (1,51):
        remained = s
        for j in range (0,b-1):
            l.append(random.randint(0,remained))
            remained -= l[j]
        l.append(remained)
        pop[i]=l
        l =[]
    for obj in list(pop.keys()):
        print( obj ,pop[obj])
    return pop
def plot_fitness_per_generation(fit , plt_num):
    # plot
    plt.scatter(list(fit.keys()) , list(fit.values()), c='purple')
    plt.xlabel('colonel axis ')
    plt.ylabel('fitness axis')
    plt.grid()
    #plt.title('Generation ')
    plt.show()

def compute_fitness(pop , b , s , plot_number):
    fit = dict()
    wining= dict()
    for colonel_a in list(pop.keys()):
        for colonel_b in list(pop.keys()):
            if colonel_a < colonel_b:
                wining_count_a = 0
                wining_count_b = 0
                for each_battle in range(0,b):
                    if pop[colonel_a][each_battle] > pop[colonel_b][each_battle]:
                        fit[colonel_a] = fit.get(colonel_a , 0) + 2
                        wining_count_a += 1
                    elif pop[colonel_a][each_battle] == pop[colonel_b][each_battle]:
                        fit[colonel_a] = fit.get(colonel_a , 0) + 1
                        fit[colonel_b] = fit.get(colonel_b , 0) + 1
                    else:
                        fit[colonel_b] = fit.get(colonel_b , 0) + 2
                        wining_count_b += 1
                if wining_count_a > wining_count_b :
                    wining[colonel_a] = wining.get(colonel_a , 0) + 1
                elif wining_count_a < wining_count_b :
                    wining[colonel_b] = wining.get(colonel_b , 0) + 1
                else:
                    wining[colonel_a] = wining.get(colonel_a , 0) + 0
                    wining[colonel_b] = wining.get(colonel_b , 0) + 0

    total_fit = best_f = 0
    for obj in list(fit.keys()):
       total_fit += fit[obj]
       if fit[obj] > best_f :
           best_f = fit[obj]

    total_fit /= 50
    #print (total_fit)
    if plot_number %4 == 0:
        plot_fitness_per_generation(fit , plot_number)
    return (fit , total_fit , best_f , wining)

def change_stratgy(pop , s, b ,fit):
    #R = 0.5
    new_fit = dict()
    for colonel_a in list(pop.keys()):
        for colonel_b in list(pop.keys()):
            if colonel_a != colonel_b:
                x = 0
                l = list()
                for each_battle in range(0,b):
                    if pop[colonel_a][each_battle] > pop[colonel_b][each_battle]:
                        x += pop[colonel_a][each_battle] - pop[colonel_b][each_battle]
                        l.append(each_battle)
                B = b - len(l)
                if x //B > 0 :
                    for each_battle in range(0,b):
                        if each_battle in l:
                            pop[colonel_a][each_battle] += 0
                        else:
                            pop[colonel_a][each_battle] += (x //B)
    return (fit) 



def selection (fit):
    #tournoment size  = 5
    selected = random.randint(1,50)
    for i in range (0,4):
        j = random.randint(1,50)
        if fit[selected]< fit[j]:
            selected = j
        #print( selected , fit[selected])
    return (selected)

def second_selection_mechanism(fit):
    #linear ranking
    rank= dict()
    Prob_per_rank = dict()
    sort_fit = sorted(fit.items(),key=lambda kv: kv[1])
    for obj in range (0,50):
        rank[obj] = sort_fit[obj][0]
    # P = (2-s)/pop_size + 2rank(s-1)/pop_size(pop_size - 1)
    # pop_size = 50 and S = 1.5
    
    for obj in range(0,50):
        Prob_per_rank[obj] = (0.5/50)+ (((2*obj)*(0.5))/(50*49))
    
    pr=random.uniform(0,0.99)
    select=0
    count =0
    while select < pr :
        select += Prob_per_rank[count]
        count += 1
    if count == 50 :
        return(rank[count-1])
    else:
        return(rank[count])

def check_valid(child , b , s):
    sum_s = 0
    for i in range(0,b):
        sum_s += child[i]
    if sum_s == s:
        return (child)
    else:
        sum_s -= s
        sub = sum_s //b
        i = 0
        while(i<b and sum_s != 0):
            if child[i] >= sub:
                child[i] -= sub
            i += 1
            sum_s -= sub
    if sum_s > 0 :
        for i in range(0,b):
            if child[i] > sum_s:
                child[i] -=sum_s
                break
        
    return(child)

def mutation(child , b):
    p=random.uniform(0,0.99)
    if p < 0.15 :
        i = random.randint(0,b-1)
        j = random.randint(0,b-1)
        child[i] , child[j] = child[j] , child[i]
    return (child)

def second_mutation(child , b):
    p = random.uniform(0,0.99)
    if p < 0.2:
        i = random.randint(0,b-1)
        j = random.randint(0,b-1)
        if child[i]>0 :
            child[i] -= 1
            child[j] += 1
        elif child[j]>0:
            child[i] += 1
            child[j] -= 1
    return(child)


def crossover_func(parent_1 , parent_2 , b , s , q):
    ch1 , ch2 = parent_1 , parent_2
    point = random.randint(0,b-1)
    ch1[0:point] , ch2[0:b-point] = ch2[b-point: ] , ch1[point: ]
    ch1 = check_valid(ch1, b , s)
    ch2 = check_valid(ch2, b , s)

    if q == 1 or q == 3:
        ch1 = mutation(ch1 , b)
        ch2 = mutation(ch2 , b)
    if q == 2:
        ch1 = second_mutation(ch1 , b)
        ch2 = second_mutation(ch2 , b)
    return (ch1 , ch2)
    

#main

S = int (input('Enter the number of soldiers: '))
B = int (input('Enter the number of battles: '))
Q = int (input('press 1 : to seeing defult form of GA \n'+
                'Press 2 : to seeing the result of diffrent mutaion operator \n'+
                'Press 3 : to seeing the result of diffrent selection mechanism \n'+
                'Press 4 : to seeing the result of third experiment \n'))
population = initialisation(S,B)
avg_fit = []
best_fit_per_generation =  []
plot_number = 0
fitness , avg , best , winer_list = compute_fitness ( population , B , S ,plot_number)
avg_fit.append(avg)
best_fit_per_generation.append(best)

flag = 0
generation_number = 1
best_fit = B*2*49
new_pop = dict()

while ( generation_number < 30):
    sorted_winer = sorted(winer_list.items(),key=lambda kv: kv[1])
    final_winer = population[sorted_winer[len(sorted_winer)-1][0]]
    number_of_war_wins =sorted_winer[len(sorted_winer)-1][1]
    print ('\nwiner stratgy in generation %i is :' %(generation_number))
    print (final_winer)
    print ('Who wins %i war from 50 wars' %(number_of_war_wins))

    #10% elitism
    sorted_fit = sorted(fitness.items(),key=lambda kv: kv[1])
    elitism = dict()
    j = 49
    for i in range(1,6):
        elitism [i] = population[sorted_fit[j][0]]
        j -= 1
    
    i = 25
    j = 1
    while i > 0:
        if Q == 1 or Q==2:
            #tournmentSelection
            colonel_1 = selection(fitness)
            colonel_2 = selection(fitness)

            #cross over and mutation
            child_1 , child_2 = crossover_func(population[colonel_1], population[colonel_2],B ,S ,Q)
            new_pop[j]  , new_pop[j+1] = child_1 , child_2
            j += 2
            i -= 1
        if Q == 3:
            colonel_1 = second_selection_mechanism(fitness)
            colonel_2 = second_selection_mechanism(fitness)

            #cross over and mutation

            child_1 , child_2 = crossover_func(population[colonel_1], population[colonel_2],B ,S ,Q)
            new_pop[j]  , new_pop[j+1] = child_1 , child_2
            j += 2
            i -= 1
        if Q == 4:
             #tournmentSelection
            colonel_1 = selection(fitness)
            colonel_2 = selection(fitness)

            #cross over and mutation
            child_1 , child_2 = crossover_func(population[colonel_1], population[colonel_2],B ,S ,Q)
            new_pop[j]  , new_pop[j+1] = child_1 , child_2
            j += 2
            i -= 1
            
    plot_number +=1
    fitness , avg , best , winer_list = compute_fitness ( new_pop , B , S ,plot_number)
    avg_fit.append(avg)
    best_fit_per_generation.append(best)

    population = elitism
    for i in range (6,51):
        population[i]= new_pop[i-2]
        
    generation_number += 1

l=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
plt.plot(l,avg_fit, c= 'blue')
plt.plot(l , best_fit_per_generation , c ='red')
plt.grid()
plt.show()