#http://burakkanber.com/blog/machine-learning-genetic-algorithms-part-1-javascript/


#A class for chromosome - the text 
from random import random,randint
import string
from collections import deque
import math 

all_char = string.ascii_uppercase + string.ascii_lowercase + string.punctuation + ' '

class chromozome:
	global all_char
	def __init__(self,str_len,random = True,str = ""):
		self.str_len = str_len
		self.crossover = str_len/2 #default crossover is at mid of the string
		self.random = random
		self.str = str
		if self.random:
			#print "str set as random"
			self.str = self.randomize()
	
	def get_random_char(self):
		#return unichr(randint(32,126))
		return all_char[randint(0,len(all_char)-1)]

	def set_crossover(self,new_crossover):
		if new_crossover < str_len - 2:
			self.crossover = new_crossover
		else:
			print "cant set crossover: Limit exceeded"

	def get_str(self):
		return self.str

	def get_len(self):
		return self.str_len

	def randomize(self):
		#randomly generate a string of size str_len using the given character set
		str_gen = [self.get_random_char() for i in range(self.str_len)]
		#print str_gen
		self.str = ''.join(str_gen)
		#print self.str
		return self.str

	def mate(self,other_chromozome):
		if self.str_len != other_chromozome.get_len():
			print "Cant mate between 2 different species!"
			return None
		#make 2 children
		#first child -  1st half of this.chromozome + 2nd half of other_chromozome
		#second child -  2nt half of this.chromozome + 1sd half of other_chromozome
		#print self.str
		#print other_chromozome.get_str()
		remaining = self.str_len-self.crossover
		if (self.str_len % 2) !=0:
			remaining -=1
		child_A = self.str[:self.crossover] + other_chromozome.get_str()[remaining:]
		child_B = other_chromozome.get_str()[:self.crossover] + self.str[remaining:]
		#print "childa:",child_A,"childb:",child_B
		return [chromozome(len(child_A),random=False,str=child_A),chromozome(len(child_B),random=False,str=child_B)]

	def mutate(self,chance,type = 2):
		#chance is from 1 to 10
		#print "before:",self.str
#		do_mutation = False
#		if chance < 10 and chance > 0:
#			if random()*10 < chance:
#				do_mutation = True
#		elif chance == 10:
#				do_mutation = True
		if random() < chance:
			if type == 2:
				#change one character in the string randomly to that char+1 or char-1
				direction = 0 # 1 means up and -1 means down (in ascii value)
				if random() > 0.5:
					direction = 1
				else:
					direction = -1
				rand_index = randint(0,self.str_len-1)
				#print "----------------->:",self.str[rand_index]
				#print "----------------->:",ord(self.str[rand_index])
				rand_char = ord(self.str[rand_index])+direction
				if rand_char > 127:
					rand_char = 127
				elif rand_char < 0:
					rand_char = 0
				#print rand_char , "<---------------------"
				#self.str = self.str[:rand_index] + chr(rand_char) + self.str[rand_index+1:]
				temp = list(self.str)
				temp[rand_index] = chr(rand_char)
				self.str = ''.join(temp)
			elif type == 1:
				#change one character in the string randomly to another character randomly - very poor performance
				rand_index = randint(0,self.str_len-1)
				#rand_index = int(random.random() * self.str_len)
				rand_char = self.get_random_char()
				self.str = self.str[:rand_index] + rand_char + self.str[rand_index+1:]			
		#print "after: ",self.str
		#print len(self.str)
		return self.str

class evolve:

	def __init__(self,final,start = "",random_start = True,goal_cost = 0):
		self.final = chromozome(len(final),random=False,str = final)
		#print self.final.get_str() ,"IS THE FINAL"
		self.start = chromozome(len(start),random=False,str = start)
		if random_start:
			self.start = chromozome(len(final),random=True)
		self.population = []
		self.goal_cost = goal_cost
		self.curr_gen = 0
		self.populate()

	def cost(self,chromo_A):
		#calculate the cost between the chromo_A and final chromozome - sum of square of difference in ascii of each charactes
		final_str = self.final.get_str()
		str_len = self.final.get_len()
		curr_str = chromo_A.get_str()		
		cost = 0
		for index in range(str_len):
			cost += pow(ord(final_str[index])-ord(curr_str[index]),2)
		return cost

	def populate(self,n=30):
		#fill the population randomly
		self.population.append(self.start)
		while n > 1:
			self.population.append(chromozome(self.final.get_len(),random=True))
			n-=1

	def sort_by_cost(self):
		self.population = sorted(self.population,key = lambda x:self.cost(x))


	def print_str(self,population,print_len,print_all=False):
		print "-"*50
		if print_all:
			print_len = len(population)-1
		for x in population[0:print_len]:
			print x.get_str(),"len:   ",x.get_len(),"     Cost:",self.cost(x)
		print "-"*50

	def start_evolving(self):
		got_goal = False
		#each iteration, sort the population by cost and mate the top 2 members and put the children in back in the list by removing the bottom 2 members(highest cost)
		#and call this function recursively
		#print "before loop"
		#self.print_str(self.population,0,True)
		while not got_goal:
			self.sort_by_cost()
			childrenAB = self.population[0].mate(self.population[1])
			#childrenAB is a list of [childA,childB]
			self.population[len(self.population)-2:] = childrenAB

			for index in range(len(self.population)):
				#mutate it and check the cost
				self.population[index].mutate(0.35) #mutate with a % chance
				#print "after mutation:"
				#self.print_str(self.population,0,True)
				if self.cost(self.population[index]) == self.goal_cost:
					self.sort_by_cost()
					self.print_str(self.population,0,True)
					print "DONE!"
					print "generation: ",self.curr_gen
					got_goal = True
					return self.population[index]
			self.curr_gen += 1
		





#s = chromozome(5)
#b = chromozome(5)
#m = s.mate(b)

#print s.get_str()
#print b.get_str()
#print s.mutate(5) #mutate with a chance of 50%

#s.randomize()

e = evolve("AbCsEdGfIhJkOlPnQrStUzQ")
e.start_evolving()

