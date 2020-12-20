""" Compare ptaint to neutaint
"""
import numpy as np
import programs
import ptaint
from util import run_neutaint
from timeit import default_timer as timer

class Evaluation():
    """
    Takes a list of programs to evaluate on
    """
    def __init__(self, program_list, dataset_length=1000):
        self.program_names = program_list
        self.dataset_length = dataset_length

        self.program_insts = [
                getattr(programs, p)() for p in self.program_names
                ]
        self.input_datasets = [
                self.construct_dataset(inst) for inst in self.program_insts
                ]
        self.ground_truths = [
                p.gen_truths(self.input_datasets[i]) for
                i, p in enumerate(self.program_insts)
                ]
        self.refs = [p.gen_ref() for p in self.program_insts]

        self.ptaint_results = self.evaluate_taint('ptaint')
        self.neutaint_results = self.evaluate_taint('neutaint')

    def construct_dataset(self, inst):
        return inst.gen_inputs(self.dataset_length)

    def compute_errors(self, results, truth):
        res = np.array(results)
        tru = np.array(truth)
        diff = tru - res
        undertaint = np.mean(diff > 0.0)
        overtaint = np.mean(diff < 0.0)
        return overtaint, undertaint

    def evaluate_one(self, method, i, p, ref, tol, time=False):
        results = list()
        time_results = list()
        for inpt in self.input_datasets[i]:
            if ref != None:
                taint_args=[inpt, p, ref]
            else:
                taint_args=[inpt, p]

            start_t = timer()
            inf = method(*taint_args)
            end_t = timer()
            result = [
                    1.0 - np.isclose(v, np.zeros_like(v), atol=tol).astype(np.float)
                    for v in inf
                    ]
            results.append(result)
            if time:
                time_results.append(end_t - start_t)
        if time:
            return time_results
        else:
            return results

    def evaluate_taint(self, method='ptaint'):
        self.results_list = list()
        for i, (p, ref) in enumerate(zip(self.program_insts, self.refs)):
            # print('Program ... ', p.name)
            if method == 'ptaint':
                if p.typ == 'numeric':
                    method_f = ptaint.ptaint_numeric
                elif p.typ == 'string':
                    method_f = ptaint.ptaint_string
                else:
                    raise Exception("Unknown program type")
                p_ref = ref
                tolerance=1e-14
            elif method == 'neutaint':
                method_f = run_neutaint
                p_ref = None
                tolerance=1e-5
            else:
                raise Exception("Unknown taint analysis")
            results = self.evaluate_one(method_f, i, p, p_ref, tolerance)
            # print("results_length: ", len(results[0]))
            self.results_list.append(results)

        eval_result = [
                self.compute_errors(r, t) for
                r, t in zip(self.results_list, self.ground_truths)
                    ]
        return eval_result

    def runtime_experiment(self, method, need_refs=True):
        results_list = list()
        for i, (p, ref) in enumerate(zip(self.program_insts, self.refs)):
            if method == 'ptaint':
                if p.typ == 'numeric':
                    method_f = ptaint.ptaint_numeric
                elif p.typ == 'string':
                    method_f = ptaint.ptaint_string
                else:
                    raise Exception("Unknown program type")
                p_ref = ref
                tolerance=1e-14
            elif method == 'neutaint':
                method_f = run_neutaint
                p_ref = None
                tolerance=1e-5
            else:
                raise Exception("Unknown taint analysis")
            results = self.evaluate_one(method_f, i, p, p_ref, tolerance, time=True)
            results_list.append(results)
        return results_list


if __name__ == "__main__":
    program_list = [
            'FBD',
            'TBPD',
            'JC'
            ]
    dataset_length = 1000
    ev = Evaluation(program_list, dataset_length=dataset_length)

    for i, program in enumerate(program_list):
        print("ptaint:")
        print(f"program: {program}, ptaint_error_rate: {ev.ptaint_results[i]}")
    for i, program in enumerate(program_list):
        print('neutaint')
        print(f"program: {program}, neutaint_error_rate: {ev.neutaint_results[i]}")

    print("==== runtime experiment ====")
    methods = ['ptaint', 'neutaint']
    refs = [True, False]
    for method, ref in zip(methods, refs):
        time_results = ev.runtime_experiment(method, need_refs=ref)
        for i, program in enumerate(program_list):
            print(f"program: {program}, {method}: {np.mean(time_results[i])}")


