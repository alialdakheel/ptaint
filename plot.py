import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from evaluation import Evaluation
import ptaint
from util import run_neutaint

def bar_plot(df, dataset_length):
    fig, ax = plt.subplots()
    g = sns.barplot(data=df, x='Program', y='Overtaint', hue='Taint_Analysis', ax=ax)
    g.set_title(f'Overtaint on {dataset_length} inputs')
    g.set_ylabel('Overtaint rate')
    fig.savefig('overtaint.png')
    fig, ax = plt.subplots()
    g = sns.barplot(data=df, x='Program', y='Undertaint', hue='Taint_Analysis', ax=ax)
    g.set_title(f'Undertaint on {dataset_length} inputs')
    g.set_ylabel('Undertaint rate')
    fig.savefig('undertaint.png')

def box_plot(df, dataset_length):
    fig, ax = plt.subplots()
    g = sns.boxplot(data=df, x='Program', y='Time', hue='Taint_Analysis', ax=ax)
    g.set_title(f'Runtime on {dataset_length} inputs')
    g.set_ylabel('Time (s)')
    fig.savefig('runtime.png')

if __name__ == "__main__":
    program_list = [
            'FBD',
            'TBPD'
            ]
    dataset_length = 1000
    ev = Evaluation(program_list, dataset_length=dataset_length)
    ptaint_overtaint = list()
    ptaint_undertaint = list()
    neutaint_overtaint = list()
    neutaint_undertaint = list()
    for i, program in enumerate(program_list):
        print("ptaint:")
        print(f"program: {program}, ptaint_numeric_error_rate: {ev.ptaint_numeric_results[i]}")
        print('neutaint')
        print(f"program: {program}, neutaint_error_rate: {ev.neutaint_results[i]}")
        ptaint_overtaint.append(ev.ptaint_numeric_results[i][0])
        ptaint_undertaint.append(ev.ptaint_numeric_results[i][1])
        neutaint_overtaint.append(ev.neutaint_results[i][0])
        neutaint_undertaint.append(ev.neutaint_results[i][1])
    df = pd.DataFrame({
        "Taint_Analysis": ["P-Taint"] * (len(program_list)) + ["NeuTaint"] * (len(program_list)),
        "Program": program_list * 2,
        "Overtaint": list(ptaint_overtaint) + list(neutaint_overtaint),
        "Undertaint": list(ptaint_undertaint) + list(neutaint_undertaint)
        })
    bar_plot(df, dataset_length)

    print("==== runtime experiment ====")
    methods = [ptaint.ptaint_numeric, run_neutaint]
    refs = [True, False]
    time_list = list()
    for method, ref in zip(methods, refs):
        print(method.__name__)
        time_results = ev.runtime_experiment(method, need_refs=ref)
        time_list.extend(time_results)
        for i, program in enumerate(program_list):
            print(f"program: {program}, {method.__name__}: {np.mean(time_results[i])}")
    df = pd.DataFrame({
        "Taint_Analysis": ["P-Taint"] * (len(program_list)) + ["NeuTaint"] * (len(program_list)),
        "Program": program_list * 2,
        "Time": time_list
        })
    df = df.explode('Time')
    box_plot(df, dataset_length)
