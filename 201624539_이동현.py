from random import randint
import copy
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

best_chromosomes = []


def make_chromosome():
    chromosome = [randint(1,5) for i in range(5)]
    return chromosome

def make_parent_generation(num):
    parent_chromosome_group = [make_chromosome() for i in range(num)]
    return parent_chromosome_group


def fitnessEvaluation(chromosome):
    point = 10
    for i in range(0,len(chromosome)-1):
        for j in range(i+1,len(chromosome)):
            if chromosome[i] == chromosome[j]:
                point -=1
            if abs(i-j) == abs(chromosome[i]-chromosome[j]):
                point -=1
    return point

def makeEvaluationList(chromosome_group,num):
    Evaluationlist = []
    for i in range(0,num):
        Evaluationlist.append(fitnessEvaluation(chromosome_group[i]))
    return Evaluationlist

    
def selectingchromosome(chromosome_group,EvaluationList,num):
    sorted_chromosome_group = []
    for i in range(0,len(EvaluationList)-1):
        for j in range(i+1,len(EvaluationList)):
            if EvaluationList[i] < EvaluationList[j]:
                temp = EvaluationList[i]
                EvaluationList[i] = EvaluationList[j]
                EvaluationList[j] = temp

                templist = copy.deepcopy(chromosome_group[i])
                chromosome_group[i] = copy.deepcopy(chromosome_group[j])
                chromosome_group[j] = copy.deepcopy(templist)
    
    for i in range(0,num):
        sorted_chromosome_group.append(chromosome_group[i])
    return sorted_chromosome_group



def cross_over(past_generation):
    original_generation = copy.deepcopy(past_generation)
    first_half_of_past_generation = []
    second_half_of_past_generation = []
    cross_over_finished_generation = []
    
    first_len = round(len(past_generation)/2)
    for i in range(0,first_len):
        first_half_of_past_generation.append(past_generation[i])
    second_len = len(past_generation) - first_len
    for i in range(0,second_len):
        second_half_of_past_generation.append(past_generation[i+first_len])
    for i in range(0,first_len):
        for j in range(3,5):
            temp = first_half_of_past_generation[i][j]
            first_half_of_past_generation[i][j] = second_half_of_past_generation[i][j]
            second_half_of_past_generation[i][j] = temp
    for i in range(0,first_len):
        cross_over_finished_generation.append(first_half_of_past_generation[i])
    for i in range(0,second_len):
        cross_over_finished_generation.append(second_half_of_past_generation[i])
    for i in range(0,len(original_generation)):
        cross_over_finished_generation.append(original_generation[i])
    return cross_over_finished_generation

def mutation(original_generation):
    while len(original_generation) < 100:
        new_generation = copy.deepcopy(original_generation)
        for i in range (0,len(new_generation)):
            new_generation[i][randint(0,4)] = randint(1,5)
        for i in range (0,len(new_generation)):
            original_generation.append(new_generation[i])
    return original_generation
        



def collect_best_chromosomes(Evaluationlist, generationlist):
    for i in range(0,len(Evaluationlist)):
        if Evaluationlist[i] == 10:
            best_chromosomes.append(generationlist[i])

    
def printpoint(Evaluationlist):
    for i in range(0,len(Evaluationlist)):
        print(Evaluationlist[i])
        
def print_group(num,chromosome_group):
    if num == 0:
        print("\nnot found\n")
    else:
        for i in range(0,num):
            for j in range(0,5):
                print(chromosome_group[i][j],end='')
            if i != 0 and i%9 == 0:
                print()
            else:
                print(',',end='')

def draw_table(twoDarray):
    fig = plt.figure(dpi=80)
    ax = fig.add_subplot(1,1,1)
    table_value = copy.deepcopy(twoDarray)
    table = ax.table(cellText=table_value, loc='center')
    table.set_fontsize(14)
    table.scale(1,5)
    ax.axis('off')
    plt.show()
    
def chromosome_to_array(chromosome):
    array = []
    for i in range(0,5):
        col = chromosome[i]
        array.append([0,0,0,0,0])
        for j in range(0,5):
            if j+1 == col:
                array[i][j] = 'Q'
    return array

def visualize_best_chromosomes(remove_dup):
    for i in range(0,len(remove_dup)):
       draw_table(chromosome_to_array(remove_dup[i]))
                   
if __name__ == "__main__":
    parentnum = int(input("Chromosome 개체 수를 입력: "))
    repeat_num = int(input("반복할 횟수를 입력: "))
    selected_num = 10
    generations = []
    generations.append(make_parent_generation(parentnum))
    Evaluation = copy.deepcopy(makeEvaluationList(generations[0],parentnum))
    selected_chromosome = copy.deepcopy(selectingchromosome(generations[0],Evaluation,selected_num))
    new_generation = copy.deepcopy(cross_over(selected_chromosome))
    mutationed_generation = copy.deepcopy(mutation(new_generation))
    generations.append(mutationed_generation)
    collect_best_chromosomes(makeEvaluationList(mutationed_generation,len(mutationed_generation)),mutationed_generation)
    for i in range(1,repeat_num):
        Evaluation = copy.deepcopy(makeEvaluationList(generations[i],parentnum))
        selected_chromosome = copy.deepcopy(selectingchromosome(generations[i],Evaluation,selected_num))
        new_generation = copy.deepcopy(cross_over(selected_chromosome))
        mutationed_generation = copy.deepcopy(mutation(new_generation))
        generations.append(mutationed_generation)
        collect_best_chromosomes(makeEvaluationList(mutationed_generation,len(mutationed_generation)),mutationed_generation)
    remove_dup = list(set(map(tuple,best_chromosomes)))
    print("\n\n")
    print("결과를 만족하는 개체들")
    print("\n\n")
    print_group(len(remove_dup),remove_dup)
    print("\n\n")
    visualize_best_chromosomes(remove_dup)
    os.system("pause")
