"""
    Compare ptaint to neutaint

    TODO:
        - Prepare ground truth for any input for each of programs
        - run both ptaint & neutaint on many inputs
        - compute errors
        - compare run time
"""
import programs
import ptaint

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

    def construct_dataset(self, inst):
        return inst.gen_inputs(self.dataset_length)


if __name__ == "__main__":
    program_list = [
            'FBD',
            'TBPD'
            ]
    dataset_length = 100
    ev = Evaluation(program_list, dataset_length=dataset_length)

