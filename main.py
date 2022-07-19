from ctypes.wintypes import POINT
from random import shuffle, randint, random

def euc_dis(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

class Individual:
    def __init__(self, genome_length):
        self.geno_len = genome_length
        self.genome = [n for n in range(genome_length)]
        shuffle(self.genome)
        self.fit = 0

    def get_fit(self, points):
        fit = 0 
        for i in range(len(points)):
            p1 = self.genome[i]
            p2 = self.genome[i-1]
            fit += euc_dis(points[p1], points[p2])
        self.fit = 1/fit*100000
        return fit    

class Population:
    def __init__(self, n_ind, genome_length):
        self.n_ind = n_ind
        self.individuals = [Individual(genome_length) for _ in range(n_ind)]
        self.mean_fit = 0

    def fit_pop(self, pts):
        # get mean fit of population
        for ind in self.individuals:
            self.mean_fit += ind.get_fit(pts)
        self.mean_fit /= self.n_ind


        # sorting the population by fitness
        changed = True
        while changed:
            changed = False
            for c in range(1, self.n_ind):
                if self.individuals[c].fit > self.individuals[c-1].fit:
                    self.individuals[c], self.individuals[c-1] = self.individuals[c-1], self.individuals[c]
                    changed = True

    def new_population(self, elite_num=50):
        def crossover(fathers):
            son = Individual(fathers[0].geno_len)
            cut_num = randint(0, fathers[0].geno_len)

            new_genome00 = fathers[0].genome[0:cut_num]
            new_genome01 = fathers[0].genome[cut_num:fathers[0].geno_len]
            new_genome11 = fathers[1].genome[cut_num:fathers[0].geno_len]

            repeated_index = []
            for c in range(len(new_genome11)):
                if new_genome11[c] in new_genome00:
                    repeated_index.append(c)

            non_repeated = []
            for c in range(len(new_genome01)):
                if new_genome01[c] not in new_genome11:
                    non_repeated.append(new_genome01[c])
                        
            for c in range(len(repeated_index)):
                new_genome11[repeated_index[c]] = non_repeated[c]

            son_genome = new_genome00 + new_genome11
            son.genome = son_genome

            return son

        def mutation(ind, mut_tax=0.005):
            mut = random()
            if mut <= mut_tax:
                s_genes = randint(0, ind.geno_len-1) 
                ind.genome[s_genes], ind.genome[s_genes-1] = ind.genome[s_genes-1], ind.genome[s_genes]
        
        def choose_father():
            ag_fit = 0
            ag_fit_list = []
            for ind in self.individuals:
                ag_fit += ind.fit
                ag_fit_list.append(ag_fit)
            self.mean_fit = ag_fit/self.n_ind
            
            chosen_num = randint(0, int(ag_fit))
            for c in range(self.n_ind-1):
                if ag_fit_list[c] < chosen_num < ag_fit_list[c+1]:
                    return self.individuals[c]
            return self.individuals[0]

        new_inds = [] +self.individuals[:elite_num]
        for _ in range(self.n_ind-elite_num):
            father01, father02 = choose_father(), choose_father()
            son = crossover([father01, father02])
            mutation(son)
            new_inds.append(son)

        self.individuals = new_inds

        
if __name__ == '__main__':
    for c in range(10):
        cut_num = 5
        new_genome0 = [n for n in range(10)]
        shuffle(new_genome0)
        new_genome1 = [n for n in range(10)]
        shuffle(new_genome0)

        new_genome00 = new_genome0[0:cut_num]
        new_genome01 = new_genome0[cut_num:10]
        new_genome11 = new_genome1[cut_num:10]

        repeated_index = []
        for c in range(len(new_genome11)):
            if new_genome11[c] in new_genome00:
                repeated_index.append(c)

        non_repeated = []
        for c in range(len(new_genome01)):
            if new_genome01[c] not in new_genome11:
                non_repeated.append(new_genome01[c])
                    
        for c in range(len(repeated_index)):
            new_genome11[repeated_index[c]] = non_repeated[c]

        son_genome = new_genome00 + new_genome11

        print(cut_num)
        print(new_genome0)
        print(son_genome)
        print(new_genome1)
        