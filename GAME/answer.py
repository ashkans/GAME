# -*- coding: utf-8 -*-

class Answer():
    def __init__(self, input_path, result_path, question_for_this_answer):
        self.question = question_for_this_answer
        self.get_input(input_path)
        self.get_results(result_path)


    def get_mark(self):
        return self.question.marker(self.input, self.results)

    def get_results(self, result_path):
        self.results = self.question.result_loader(result_path)


    def get_input(self, input_path):
        self.input = self.question.input_loader(input_path)
        