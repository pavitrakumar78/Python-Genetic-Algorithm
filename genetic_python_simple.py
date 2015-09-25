#http://burakkanber.com/blog/machine-learning-genetic-algorithms-part-1-javascript/


from random import random,randint
import string
import math 

all_char = string.ascii_uppercase + string.ascii_lowercase + string.punctuation + ' '

#A class for Chromosome - the text 
class chromosome:
    global all_char
    def __init__(self,str_len,random = True,str = ""):
        self.str_len = str_len
        self.crossover = str_len/2 #default crossover is at mid of the string
        self.random = random
        self.str = str
        if self.random:
            self.str = self.randomize()
    
    def get_random_char(self):
        #Uncomment below to experiment with a wide ASCII range
        #return unichr(randint(0,127))
        #default: ASCII of just alphabets,special characters
        return all_char[randint(0,len(all_char)-1)]

    def set_crossover(self,new_crossover):
        if new_crossover < str_len - 2:
            self.crossover = new_crossover
        else:
            print "Can't set crossover: crossover exceeds string length"

    def get_str(self):
        return self.str

    def get_len(self):
        return self.str_len

    def randomize(self):
        #randomly generate a string of size str_len using the given character set
        str_gen = [self.get_random_char() for i in range(self.str_len)]
        self.str = ''.join(str_gen)
        return self.str

    def mate(self,other_chromosome):
        if self.str_len != other_chromosome.get_len():
            print "Cant mate between 2 different species!"
            return None
        #make 2 children
        #first child -  1st half of this.chromosome + 2nd half of other_chromosome
        #second child -  1st half of other_chromosome + 2nd half of this.chromosome
        remaining = self.str_len-self.crossover
        if (self.str_len % 2) !=0:
            remaining -=1
        child_A = self.str[:self.crossover] + other_chromosome.get_str()[remaining:]
        child_B = other_chromosome.get_str()[:self.crossover] + self.str[remaining:]
        return [chromosome(len(child_A),random=False,str=child_A),chromosome(len(child_B),random=False,str=child_B)]

    def mutate(self,chance,type = 2):
        if random() < chance:
            if type == 2:
                #change one character in the string randomly to that of char+1 or char-1
                direction = 0 #1 means up and -1 means down (in ASCII value)
                if random() > 0.5:
                    direction = 1
                else:
                    direction = -1
                rand_index = randint(0,self.str_len-1)
                rand_char = ord(self.str[rand_index])+direction
                #below IF construct is needed only if the ASCII range from 0-127 is used.
                #if rand_char > 127: #prevent overflow
                #   rand_char = 127
                #elif rand_char < 0:
                #   rand_char = 0
                self.str = self.str[:rand_index] + chr(rand_char) + self.str[rand_index+1:]
            elif type == 1:
                #change one random character in the string to another random character - very poor performance
                rand_index = randint(0,self.str_len-1)
                rand_char = self.get_random_char()
                self.str = self.str[:rand_index] + rand_char + self.str[rand_index+1:]          
        return self.str

class evolve:
    def __init__(self,final,start = "",population_count = 30,random_start = True,goal_cost = 0):
        self.final = chromosome(len(final),random=False,str = final)
        self.start = chromosome(len(start),random=False,str = start)
        if random_start:
            self.start = chromosome(len(final),random=True)
        self.population = []
        self.goal_cost = goal_cost
        self.curr_gen = 0
        self.population_count = population_count


        self.populate()

    def cost(self,chromo_A):
        #Function to calculate the cost between the chromo_A and final chromosome
        #cost is the sum of square of difference in ASCII of each charactes
        final_str = self.final.get_str()
        str_len = self.final.get_len()
        curr_str = chromo_A.get_str()       
        cost = 0
        for index in range(str_len):
            cost += pow(ord(final_str[index])-ord(curr_str[index]),2)
        return cost

    def populate(self):
        #fill the population list with random strings of length equal to the final string
        self.population.append(self.start)
        n = self.population_count
        while n > 1:
            self.population.append(chromosome(self.final.get_len(),random=True))
            n-=1

    def sort_by_cost(self):
        #Sort the population list by cost
        self.population = sorted(self.population,key = lambda x:self.cost(x))

    def print_str(self,population,print_len,print_all=False):
        print "-"*50
        if print_all:
            print_len = len(population)-1
        for x in population[0:print_len]:
            print x.get_str(),"     Cost:",self.cost(x)
        print "-"*50

    def start_evolving(self):
        reached_final_state = False
        #each iteration, 
        #sort the population by cost, 
        #mate the top 2 members and  put the children in back in the list by removing the bottom 2 members(highest cost)
        while not reached_final_state:
            self.sort_by_cost()
            childrenAB = self.population[0].mate(self.population[1])
            #childrenAB is a list of [childA,childB]
            self.population[len(self.population)-2:] = childrenAB

            for index in range(len(self.population)):
                #mutate it and check the cost
                self.population[index].mutate(0.35) #mutate with a % of chance
                if self.cost(self.population[index]) == self.goal_cost:
                    self.sort_by_cost()
                    self.print_str(self.population,0,True)
                    print "DONE!"
                    print "Final Generation: ",self.curr_gen
                    reached_final_state = True
                    return self.population[index]
            self.curr_gen += 1
        




e = evolve("AbCsEdGfIhJkOlPnQrStUzQ")
e.start_evolving()

