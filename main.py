from ctypes.wintypes import POINT
from random import shuffle, randint

class Genome:
    def __init__(self, gn):
        self.gene = [n for n in range(gn)]
        shuffle(self.gene)

class Individual:
    def __init__(self, gn):
        self.genome = Genome(gn)
        self.fit = 0
        self.ac_fit = 0

    def fitness(self, points):
        fit = 0
        for i in range(len(points)):
            p1 = self.genome.gene[i]
            p2 = self.genome.gene[i-1]
            fit += ((points[p1][0] - points[p2][0])**2+
            (points[p1][1] - points[p2][1])**2)**0.5

        self.fit = (1/fit)*99999
        return fit    

class Population:
    def __init__(self, ind, gn):
        self.individuals = [Individual(gn) for _ in range(ind)]
    
    def get_pop_fit(self, points):
        for ind in self.individuals:
            ind.fitness(points)

    def sort_inds(self):
        k = True
        while k:
            k = False
            for n in range(len(self.individuals)-1):     
                if self.individuals[n].fit > self.individuals[n+1].fit:
                    self.individuals[n], self.individuals[n+1] = self.individuals[n+1], self.individuals[n]
                    k = True

    def get_new_ind(self):

        
        def give_ac_fit():
            ac_fit = 0
            for ind in self.individuals:
                ac_fit += ind.fit
                ind.ac_fit = ac_fit

        def random_ac():
            return randint(0, int(self.individuals[-1].ac_fit))
        
        def select_father():
 
            selected = self.individuals[-1]
            sortn = random_ac()
            for d in range(len(self.individuals)-1):
                ind_ac1 = self.individuals[d].ac_fit
                ind_ac2 = self.individuals[d+1].ac_fit
                if ind_ac1 < sortn > ind_ac2:
                    selected = self.individuals[d]
            return selected
        
        def crossover(f1, f2):
            f1_gn = f1.genome.gene
            f2_gn = f2.genome.gene
            s1_gn = [-1 for _  in range(len(f1_gn))]

            oc = 0       
            while True:
                s1_gn[oc] = f1_gn[oc]
                nic = f1_gn.index(f2_gn[oc])
                if nic == 0:
                    break
                oc = nic

            for c in range(len(f1_gn)):
                if s1_gn[c] == -1:
                    s1_gn[c] = f2_gn[c]  
            
            new_ind =  Individual(len(f1_gn))
            new_ind.genome.gene = s1_gn
            return new_ind

        self.sort_inds()

        give_ac_fit()
        
        f1 = select_father()
        f2 = select_father()
        return crossover(f1, f2)

    def get_new_gen(self):
        pop_len = len(self.individuals)
        new_gen = Population(pop_len, len(self.individuals[0].genome.gene))
        new_inds = [self.get_new_ind() for _ in range(pop_len)]
        new_gen.individuals = new_inds       
        return new_gen

        
if __name__ == '__main__':
    np = 20
    pop_len =500
    pop = Population(pop_len, np)
    points = [(randint(1, 100), randint(1, 100)) for _ in range(np)]
    for c in range(3000):
        pop.get_pop_fit(points)

        pop.sort_inds()
        if c%10 == 0:
            print(f'GEN: {c}')
            for i in range(pop_len-5, pop_len):
                print(pop.individuals[i].fit)
            print('-'*12)


        pop = pop.get_new_gen()
    
    
        